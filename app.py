import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

DB_NAME = "corporate_expenses.db"

# --- Direct SQLite Database Initialization ---
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                payment_method TEXT DEFAULT 'Corporate Card',
                date TEXT NOT NULL,
                receipt_ref TEXT UNIQUE,
                notes TEXT,
                status TEXT DEFAULT 'Pending',
                comments TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets(
                username TEXT NOT NULL,
                category TEXT NOT NULL,
                monthly_limit REAL NOT NULL,
                PRIMARY KEY (username, category)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                username TEXT PRIMARY KEY,
                role TEXT DEFAULT 'Employee'
            )
        """)
        conn.commit()

init_db()

def get_user_role(username: str) -> str:
    with get_connection() as conn:
        row = conn.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
        if row:
            return row["role"]
        role = "Admin" if "admin" in username.lower() else "Employee"
        conn.execute("INSERT OR IGNORE INTO users(username, role) VALUES (?, ?)", (username, role))
        conn.commit()
        return role

def add_expense(username, title, amount, category, payment_method, date_str, receipt_ref, notes):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO expenses(username, title, amount, category, payment_method, date, receipt_ref, notes, status, comments) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending', '')
        """, (username, title, amount, category, payment_method, date_str, receipt_ref, notes))
        conn.commit()
        return cursor.lastrowid

def get_expenses(username, role):
    with get_connection() as conn:
        if role == "Admin":
            return [dict(row) for row in conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()]
        else:
            return [dict(row) for row in conn.execute("SELECT * FROM expenses WHERE username = ? ORDER BY date DESC", (username,)).fetchall()]

def update_expense_status_with_comments(expense_id, status, comments):
    with get_connection() as conn:
        cursor = conn.execute("UPDATE expenses SET status = ?, comments = ? WHERE id = ?", (status, comments, expense_id))
        conn.commit()
        return cursor.rowcount > 0

def modify_expense(expense_id, title, amount, category, payment_method, date_str, receipt_ref, notes, comments):
    with get_connection() as conn:
        cursor = conn.execute("""
            UPDATE expenses 
            SET title = ?, amount = ?, category = ?, payment_method = ?, date = ?, receipt_ref = ?, notes = ?, comments = ?
            WHERE id = ?
        """, (title, amount, category, payment_method, date_str, receipt_ref, notes, comments, expense_id))
        conn.commit()
        return cursor.rowcount > 0

def set_budget(username, category, limit):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO budgets(username, category, monthly_limit) VALUES (?, ?, ?)
            ON CONFLICT(username, category) DO UPDATE SET monthly_limit = ?
        """, (username, category, limit, limit))
        conn.commit()

def get_budgets(username):
    with get_connection() as conn:
        return {row["category"]: row["monthly_limit"] for row in conn.execute("SELECT * FROM budgets WHERE username = ? OR username = 'global'", (username,)).fetchall()}

# --- Streamlit UI Configuration ---
st.set_page_config(
    page_title="Enterprise Expense Hub", 
    page_icon="🏢", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {background-color: #f8fafc;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1, h2, h3 {color: #1e293b; font-family: 'Helvetica Neue', sans-serif;}
    .stMetric {
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("https://img.icons8.com/clouds/200/company.png", width=100)
st.sidebar.title("Corporate Portal")
st.sidebar.markdown("---")

username = st.sidebar.text_input("👤 Corporate ID / Email", value="employee@company.com")
user_role = get_user_role(username)

if user_role == "Admin":
    admin_password = st.sidebar.text_input("🔑 Admin Access Password", type="password")
    if admin_password != "CorporateAdmin2026!":
        st.sidebar.warning("🔒 Enter correct password for Admin rights.")
        user_role = "Employee"

st.sidebar.markdown(f"**Active Role:** `{user_role}`")
st.sidebar.markdown("---")

if not username:
    st.warning("⚠️ Please input your Corporate ID in the sidebar to proceed.")
    st.stop()

def generate_pdf_report(df, user):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor("#1e293b"), spaceAfter=10)
    
    elements.append(Paragraph("Official Corporate Expense Audit Report", title_style))
    elements.append(Paragraph(f"<b>Generated For:</b> {user} | <b>Date:</b> {date.today().strftime('%Y-%m-%d')}", styles['Normal']))
    elements.append(Spacer(1, 15))
    
    table_data = [["ID", "Date", "User", "Title", "Category", "Status", "Comments", "Amount (₹)"]]
    for _, row in df.iterrows():
        table_data.append([str(row['id']), str(row['date'])[:10], str(row.get('username', user)), str(row['title']), str(row['category']), str(row.get('status', 'Pending')), str(row.get('comments', '')), f"₹{row['amount']:,.2f}"])
        
    t = Table(table_data, colWidths=[25, 65, 85, 100, 85, 55, 95, 60])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8fafc")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1"))
    ]))
    
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return buffer

st.title("🏢 Enterprise Expense & Financial Hub")
st.markdown("Seamless multi-tenant expense tracking, departmental budgeting, and executive audit oversight.")
st.markdown("")

expenses = get_expenses(username, user_role)
budgets = get_budgets(username)

# Calculate comparison analytics
spend_map = {}
for exp in expenses:
    cat = exp["category"]
    spend_map[cat] = spend_map.get(cat, 0.0) + exp["amount"]
    
comp_data = []
all_categories = set(list(spend_map.keys()) + list(budgets.keys()))
for cat in all_categories:
    comp_data.append({
        "category": cat,
        "actual_spend": spend_map.get(cat, 0.0),
        "budget_limit": budgets.get(cat, 0.0)
    })

df = pd.DataFrame(expenses) if expenses else pd.DataFrame()
if not df.empty:
    df['date'] = pd.to_datetime(df['date'])

if user_role == "Admin":
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Dashboard", "📝 Submit Claim", "📋 Audit & Management", "⚙️ Budget Policies"])
else:
    tab1, tab2, tab3 = st.tabs(["📊 My Dashboard", "📝 Submit Claim", "📋 My Records"])

with tab1:
    st.subheader("Financial Performance & Analytics")
    if not df.empty:
        total_spend = df['amount'].sum()
        total_claims = len(df)
        avg_claim = df['amount'].mean()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Managed Spend" if user_role == "Admin" else "Total My Spend", f"₹ {total_spend:,.2f}")
        c2.metric("Total Claims Logged", total_claims)
        c3.metric("Average Claim Value", f"₹ {avg_claim:,.2f}")
        
        st.markdown("---")
        
        if user_role == "Admin" and comp_data:
            st.markdown("#### 📊 Domain Budget vs. Actual Spend Comparison")
            comp_df = pd.DataFrame(comp_data)
            comp_melted = comp_df.melt(id_vars="category", value_vars=["actual_spend", "budget_limit"], 
                                       var_name="Metric", value_name="Amount")
            comp_melted['Metric'] = comp_melted['Metric'].map({"actual_spend": "Actual Spend", "budget_limit": "Allocated Budget"})
            
            fig_bar = px.bar(comp_melted, x="category", y="Amount", color="Metric", barmode="group",
                             color_discrete_map={"Actual Spend": "#ef4444", "Allocated Budget": "#3b82f6"})
            fig_bar.update_layout(margin=dict(t=20, b=20, l=20, r=20), xaxis_title="Cost Center / Domain", yaxis_title="Amount (₹)")
            st.plotly_chart(fig_bar, width='stretch')
            st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Spend Distribution by Cost Center")
            cat_df = df.groupby('category')['amount'].sum().reset_index()
            fig_pie = px.pie(cat_df, values='amount', names='category', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_pie, width='stretch')
            
        with col2:
            st.markdown("#### Cash Outflow Trend")
            trend_df = df.groupby('date')['amount'].sum().reset_index()
            fig_line = px.line(trend_df, x='date', y='amount', markers=True, line_shape="spline", color_discrete_sequence=["#2563eb"])
            fig_line.update_layout(margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_line, width='stretch')

        if user_role == "Admin" and budgets:
            st.markdown("---")
            st.markdown("#### 🚨 Departmental Budget Compliance")
            current_month_df = df[df['date'].dt.month == pd.Timestamp.today().month]
            spent_by_cat = current_month_df.groupby('category')['amount'].sum().to_dict()
            
            for cat, limit in budgets.items():
                spent = spent_by_cat.get(cat, 0)
                pct = min(int((spent / limit) * 100), 100) if limit > 0 else 0
                st.text(f"{cat}: ₹{spent:,.2f} / ₹{limit:,.2f} ({pct}% utilized)")
                st.progress(pct / 100)
                if spent > limit:
                    st.error(f"🚨 Budget breach detected in {cat}!")
    else:
        st.info("No analytics data available yet. Submit your first expense claim!")

with tab2:
    st.subheader("Submit New Business Expense Claim")
    with st.form("corporate_expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Expense Description / Vendor Name")
            amount = st.number_input("Amount (₹)", min_value=1.0, format="%.2f")
            category = st.selectbox("Cost Center Category", ["Travel & Conveyance", "Client Entertainment", "Software & Cloud", "Office Supplies", "Training & Upskilling", "Miscellaneous"])
        with col2:
            payment_method = st.selectbox("Payment Channel", ["Corporate Card", "Direct Reimbursement", "Company Petty Cash", "Vendor Invoice"])
            expense_date = st.date_input("Transaction Date", value=date.today())
            receipt_ref = st.text_input("Unique Receipt / Invoice Ref ID", placeholder="INV-2026-XXXX")
            notes = st.text_area("Business Purpose / Justification")
            
        submitted = st.form_submit_button("Submit Claim for Approval", type="primary")
        if submitted:
            if not receipt_ref:
                st.error("Receipt reference ID is mandatory to prevent duplicate claims.")
            else:
                try:
                    add_expense(username, title, float(amount), category, payment_method, expense_date.isoformat(), receipt_ref, notes)
                    st.success("Expense claim filed successfully!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Duplicate Error: Receipt reference '{receipt_ref}' already exists in the system!")

with tab3:
    if user_role == "Admin":
        st.subheader("Corporate Audit Records & Review Console")
    else:
        st.subheader("My Submitted Records")

    if not df.empty:
        cols_to_show = ['id', 'date', 'username', 'title', 'category', 'payment_method', 'status', 'comments', 'receipt_ref', 'amount'] if user_role == "Admin" else ['id', 'date', 'title', 'category', 'payment_method', 'status', 'comments', 'receipt_ref', 'amount']
        st.dataframe(df[cols_to_show], width='stretch')
        
        ex_col1, ex_col2 = st.columns(2)
        with ex_col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export CSV Audit Report", data=csv, file_name=f"audit_report_{username}.csv", mime="text/csv")
        with ex_col2:
            pdf_buffer = generate_pdf_report(df, username)
            st.download_button("📄 Download Official PDF Statement", data=pdf_buffer, file_name=f"expense_statement_{username}.pdf", mime="application/pdf")
        
        if user_role == "Admin":
            st.markdown("---")
            st.markdown("#### 🛠️ Administrative Action & Review Panel")
            
            selected_id = st.selectbox("Select Expense ID to Review / Edit", df['id'].tolist())
            target_row = df[df['id'] == selected_id].iloc[0]
            
            with st.form(f"admin_action_form_{selected_id}"):
                st.markdown(f"**Selected Claim ID:** `{selected_id}` | **Submitted By:** `{target_row.get('username')}` | **Current Status:** `{target_row.get('status')}`")
                
                action_type = st.selectbox("Action Type", ["Approve", "Reject", "Modify Details"])
                admin_comment = st.text_input("Reviewer Comment / Justification", value=str(target_row.get('comments', '')))
                
                if action_type == "Modify Details":
                    st.markdown("##### Edit Claim Parameters")
                    mod_title = st.text_input("Title / Merchant", value=target_row['title'])
                    mod_amount = st.number_input("Amount (₹)", value=float(target_row['amount']))
                    mod_cat = st.text_input("Category", value=target_row['category'])
                    mod_pay = st.text_input("Payment Method", value=target_row['payment_method'])
                    mod_date = st.text_input("Date (YYYY-MM-DD)", value=str(target_row['date'])[:10])
                    mod_ref = st.text_input("Receipt Ref", value=target_row.get('receipt_ref', 'N/A'))
                    mod_notes = st.text_area("Notes", value=target_row.get('notes', ''))
                
                if st.form_submit_button("Execute Admin Action", type="primary"):
                    if action_type == "Approve":
                        update_expense_status_with_comments(selected_id, "Approved", admin_comment)
                        st.success(f"Expense #{selected_id} Approved successfully!")
                        st.rerun()
                    elif action_type == "Reject":
                        update_expense_status_with_comments(selected_id, "Rejected", admin_comment)
                        st.warning(f"Expense #{selected_id} Rejected.")
                        st.rerun()
                    elif action_type == "Modify Details":
                        try:
                            modify_expense(selected_id, mod_title, mod_amount, mod_cat, mod_pay, mod_date, mod_ref, mod_notes, admin_comment)
                            st.success(f"Expense #{selected_id} updated successfully!")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("Modification failed: Receipt reference already exists.")
    else:
        st.info("No records found in the system.")

if user_role == "Admin":
    with tab4:
        st.subheader("Departmental Budget Allocation Policies")
        target_user = st.text_input("Target Employee ID or 'global'", value="global")
        cat = st.selectbox("Select Cost Center Policy", ["Travel & Conveyance", "Client Entertainment", "Software & Cloud", "Office Supplies", "Training & Upskilling", "Miscellaneous"], key="budget_cat")
        limit = st.number_input("Monthly Allocation Limit (₹)", min_value=5000.0, step=1000.0, key="budget_limit")
        if st.button("Save Budget Policy", type="primary"):
            set_budget(target_user, cat, limit)
            st.success(f"Budget policy updated for {target_user} / {cat}!")
            st.rerun()
import sqlite3

DB_NAME = "corporate_expenses.db"

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

def get_user_role(username: str) -> str:
    with get_connection() as conn:
        row = conn.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
        if row:
            return row["role"]
        role = "Admin" if "admin" in username.lower() else "Employee"
        conn.execute("INSERT OR IGNORE INTO users(username, role) VALUES (?, ?)", (username, role))
        conn.commit()
        return role

def add_expense(username: str, title: str, amount: float, category: str, payment_method: str, date: str, receipt_ref: str, notes: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO expenses(username, title, amount, category, payment_method, date, receipt_ref, notes, status, comments) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending', '')
        """, (username, title, amount, category, payment_method, date, receipt_ref, notes))
        return cursor.lastrowid

def get_expenses(username: str, role: str):
    with get_connection() as conn:
        if role == "Admin":
            return [dict(row) for row in conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()]
        else:
            return [dict(row) for row in conn.execute("SELECT * FROM expenses WHERE username = ? ORDER BY date DESC", (username,)).fetchall()]

def update_expense_status_with_comments(expense_id: int, status: str, comments: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("UPDATE expenses SET status = ?, comments = ? WHERE id = ?", (status, comments, expense_id))
        conn.commit()
        return cursor.rowcount > 0

def modify_expense(expense_id: int, title: str, amount: float, category: str, payment_method: str, date: str, receipt_ref: str, notes: str, comments: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("""
            UPDATE expenses 
            SET title = ?, amount = ?, category = ?, payment_method = ?, date = ?, receipt_ref = ?, notes = ?, comments = ?
            WHERE id = ?
        """, (title, amount, category, payment_method, date, receipt_ref, notes, comments, expense_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_expense(expense_id: int, username: str, role: str) -> bool:
    with get_connection() as conn:
        if role == "Admin":
            cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        else:
            cursor = conn.execute("DELETE FROM expenses WHERE id = ? AND username = ? AND status = 'Pending'", (expense_id, username))
        conn.commit()
        return cursor.rowcount > 0

def set_budget(username: str, category: str, limit: float):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO budgets(username, category, monthly_limit) VALUES (?, ?, ?)
            ON CONFLICT(username, category) DO UPDATE SET monthly_limit = ?
        """, (username, category, limit, limit))
        conn.commit()

def get_budgets(username: str):
    with get_connection() as conn:
        return {row["category"]: row["monthly_limit"] for row in conn.execute("SELECT * FROM budgets WHERE username = ? OR username = 'global'", (username,)).fetchall()}
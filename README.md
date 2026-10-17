# 🏢 Enterprise Financial & Expense Control Center

A production-grade, multi-tenant expense management and corporate auditing platform built with **FastAPI**, **Streamlit**, **SQLite**, and **ReportLab**. Designed for modern businesses to streamline expense logging, enforce strict budgetary guardrails, prevent duplicate receipt fraud, and generate executive-level reports.

---

## 🚀 Key Features

* **🔐 Multi-Tenant Role-Based Access Control (RBAC):**
  * **Employees:** Submit expense claims, track real-time approval lifecycles (`Pending`, `Approved`, `Rejected`), and view personal spend dashboards.
  * **Administrators:** Secure password-protected access (`CorporateAdmin2026!`) to oversee global company claims, review/approve/reject submissions with comments, and manage departmental policies.
* **🛡️ Fraud Prevention & Data Integrity:**
  * Strict database constraints enforce unique receipt/invoice reference numbers (`receipt_ref`) to completely eliminate duplicate claims.
* **📊 Departmental Budgeting & Analytics:**
  * Real-time comparative analytics (Admin-only) displaying **Allocated Budget vs. Actual Spend** across various corporate cost centers.
  * Interactive Plotly charts visualizing cash-outflow trends and departmental spend distribution.
* **📄 Professional Audit & Reporting:**
  * Generate formal, publication-ready **PDF audit statements** using ReportLab.
  * Export structured CSV audit reports for accounting handoffs.

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python), Pydantic
* **Frontend:** Streamlit, Plotly Express
* **Database:** SQLite (Relational integrity with unique constraints)
* **Reporting:** ReportLab (PDF generation engine)

---

## ⚙️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/ShashwatMisra008/Enterprise-Expense-Tracker.git](https://github.com/ShashwatMisra008/Enterprise-Expense-Tracker.git)
cd Enterprise-Expense-Tracker

# 🏢 Enterprise Financial & Expense Control Center

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enterprise-expense-tracker-shashwatmisra.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/ShashwatMisra008/Enterprise-Expense-Tracker)
[![Python Version](https://img.shields.io/badge/Python-3.14%2B-blue?logo=python)](https://www.python.org/)

A production-grade, multi-tenant expense management and corporate auditing platform built with FastAPI, Streamlit, SQLite, and ReportLab. Designed to help modern enterprises streamline expense submission, enforce strict budgetary guardrails, prevent duplicate receipt fraud, and generate executive-level reports.

🔗 **Live App URL:** [https://enterprise-expense-tracker-shashwatmisra.streamlit.app/](https://enterprise-expense-tracker-shashwatmisra.streamlit.app/)

---

## 🚀 Key Features

* **🔐 Multi-Tenant Role-Based Access Control (RBAC):**
  * **Employees:** Submit expense claims, track real-time approval lifecycles (`Pending`, `Approved`, `Rejected`), and view personal spend analytics.
  * **Administrators:** Secure password-protected access (`CorporateAdmin2026!`) to oversee global company claims, review/approve/reject submissions with comments, and manage departmental policies.
* **🛡️ Fraud Prevention & Data Integrity:**
  * Strict database constraints enforce unique receipt/invoice reference numbers (`receipt_ref`) to eliminate duplicate claims.
* **📊 Departmental Budgeting & Analytics:**
  * Real-time comparative analytics (Admin-only) displaying **Allocated Budget vs. Actual Spend** across various corporate cost centres.
  * Interactive Plotly charts visualising cash-outflow trends and departmental spend distribution.
* **📄 Professional Audit & Reporting:**
  * Generate formal, publication-ready **PDF audit statements** using ReportLab.
  * Export structured **CSV audit reports** for accounting handoffs.

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python), Pydantic
* **Frontend:** Streamlit, Plotly Express
* **Database:** SQLite (Relational integrity with unique constraints)
* **Reporting:** ReportLab (PDF generation engine)

---

## 🔑 Access Credentials (For Testing)

* **Employee Portal:** Use any corporate ID/email (e.g., `employee@company.com`)
* **Admin Portal:** Log in with an admin-recognised ID and use the password: 
  > `CorporateAdmin2026!`

---

## 📂 Project Structure

```text
Enterprise-Expense-Tracker/
│
├── app.py             # Streamlit SaaS user interface & database engine
├── main.py            # FastAPI REST API & endpoints
├── database.py        # SQLite database operations & schema init
├── models.py          # Pydantic data validation models
├── requirements.txt   # Cloud deployment dependencies configuration
└── README.md          # Project documentation

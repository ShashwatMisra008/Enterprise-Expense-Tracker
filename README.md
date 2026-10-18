# 🏢 Enterprise Financial & Expense Control Center

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enterprise-expense-tracker-shashwatmisra.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)

A production-grade, multi-tenant expense management and corporate auditing platform built with **FastAPI**, **Streamlit**, **SQLite**, and **ReportLab**. Designed to help modern enterprises streamline expense submission, enforce strict budgetary guardrails, prevent duplicate receipt fraud, and generate executive-level reports.

🔗 **Live App URL:** [Launch Enterprise Expense Control Center](https://enterprise-expense-tracker-shashwatmisra.streamlit.app/)

---

## 🚀 Key Features

* 🔐 **Multi-Tenant Role-Based Access Control (RBAC):**
  * 🧑‍💻 **Employees:** Submit expense claims, track real-time approval lifecycles (*Pending*, *Approved*, *Rejected*), and view personal spend analytics.
  * 🛡️ **Administrators:** Secure password-protected access (`CorporateAdmin2026!`) to oversee global company claims, review/approve/reject submissions with audit comments, and manage departmental policies.
* 🛡️ **Fraud Prevention & Data Integrity:**
  * Strict database-level constraints and Pydantic validation enforce unique receipt/invoice reference numbers (`receipt_ref`) to eliminate duplicate claims at the point of entry.
* 📊 **Departmental Budgeting & Analytics:**
  * Real-time comparative analytics (Admin-only) displaying **Allocated Budget vs. Actual Spend** across corporate cost centres.
  * Interactive **Plotly** charts visualising cash-outflow trends and departmental spend distribution.
* 📄 **Professional Audit & Reporting:**
  * Generate formal, publication-ready **PDF audit statements** using **ReportLab**.
  * Export structured **CSV audit reports** for seamless accounting handoffs.

---

## 🛠️ Languages & Tech Stack

* **Core Languages:** Python, SQL
* **Backend & API:** FastAPI, Pydantic (Data Validation & Schema Enforcement), Uvicorn
* **Frontend & BI Visuals:** Streamlit, Plotly Express, Pandas
* **Database & Reporting:** SQLite3 (Relational Storage & Unique Constraints), ReportLab (Automated PDF Generation)

---

## 🔑 Access Credentials (For Testing)

| Portal Role | Login ID / Email | Password |
| :--- | :--- | :--- |
| **🧑‍💻 Employee Portal** | Any corporate email (e.g., `employee@company.com`) | *No password required* |
| **🛡️ Admin Portal** | Any admin-recognised ID (e.g., `admin@company.com`) | `CorporateAdmin2026!` |

---

## 📂 Project Structure

```text
Enterprise-Expense-Tracker/
│
├── app.py             # 🎈 Streamlit SaaS user interface & database engine
├── main.py            # ⚡ FastAPI REST API & endpoints
├── database.py        # 🗄️ SQLite database operations & schema init
├── models.py          # 🛡️ Pydantic data validation models
├── requirements.txt   # 📦 Cloud deployment dependencies configuration
└── README.md          # 📄 Project documentation

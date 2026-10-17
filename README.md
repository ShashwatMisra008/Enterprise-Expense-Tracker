# 🏢 Enterprise Financial & Expense Control Center

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enterprise-expense-tracker-shashwatmisra.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/ShashwatMisra008/Enterprise-Expense-Tracker)
[![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/Language-SQL-4479A1?logo=postgresql&logoColor=white)]()
[![HTML5/CSS3](https://img.shields.io/badge/Styling-HTML5%20%26%20CSS3-1572B6?logo=css3&logoColor=white)]()
[![Markdown](https://img.shields.io/badge/Docs-Markdown-000000?logo=markdown&logoColor=white)]()

A production-grade, multi-tenant expense management and corporate auditing platform built with FastAPI, Streamlit, SQLite, and ReportLab. Designed to help modern enterprises streamline expense submission, enforce strict budgetary guardrails, prevent duplicate receipt fraud, and generate executive-level reports.

🔗 **Live App URL:** [https://enterprise-expense-tracker-shashwatmisra.streamlit.app/](https://enterprise-expense-tracker-shashwatmisra.streamlit.app/)

---

## 🚀 Key Features

- **🔐 Multi-Tenant Role-Based Access Control (RBAC):**
  - 🧑‍💻 **Employees:** Submit expense claims, track real-time approval lifecycles (`Pending`, `Approved`, `Rejected`), and view personal spend analytics.
  - 🛡️ **Administrators:** Secure password-protected access (`CorporateAdmin2026!`) to oversee global company claims, review/approve/reject submissions with comments, and manage departmental policies.
- **🛡️ Fraud Prevention & Data Integrity:**
  - Strict database constraints enforce unique receipt/invoice reference numbers (`receipt_ref`) to eliminate duplicate claims.
- **📊 Departmental Budgeting & Analytics:**
  - Real-time comparative analytics (Admin-only) displaying **Allocated Budget vs. Actual Spend** across various corporate cost centres.
  - Interactive Plotly charts visualising cash-outflow trends and departmental spend distribution.
- **📄 Professional Audit & Reporting:**
  - Generate formal, publication-ready **PDF audit statements** using ReportLab.
  - Export structured **CSV audit reports** for accounting handoffs.

---

## 🛠️ Languages & Tech Stack

* **Core Languages:** ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-003B57?style=for-the-badge&logo=sqlite&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![Markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)
* **Backend & API:** ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white) ![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
* **Frontend & BI Visuals:** ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly_Express-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
* **Database & Reporting:** ![SQLite](https://img.shields.io/badge/SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white) ![ReportLab](https://img.shields.io/badge/ReportLab_PDF-CC0000?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)
---

## 🔑 Access Credentials (For Testing)

- **Employee Portal:** Use any corporate ID/email (e.g., `employee@company.com`)
- **Admin Portal:** Log in with an admin-recognised ID and use the password: 
  > `CorporateAdmin2026!`

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

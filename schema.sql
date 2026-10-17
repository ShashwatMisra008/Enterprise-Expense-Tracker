-- Enterprise Expense Hub Database Schema

CREATE TABLE IF NOT EXISTS expenses (
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
);

CREATE TABLE IF NOT EXISTS budgets (
    username TEXT NOT NULL,
    category TEXT NOT NULL,
    monthly_limit REAL NOT NULL,
    PRIMARY KEY (username, category)
);

CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    role TEXT DEFAULT 'Employee'
);

-- Analytical Queries for Cost Center Aggregations
SELECT category, SUM(amount) AS total_spend, COUNT(id) AS claim_count
FROM expenses
WHERE status = 'Approved'
GROUP BY category
ORDER BY total_spend DESC;
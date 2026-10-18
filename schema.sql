-- ============================================================================
-- ENTERPRISE FINANCIAL & EXPENSE CONTROL CENTER - DATABASE ARCHITECTURE
-- Engine: SQLite3 / ANSI SQL Compliant
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- 1. CORE TABLES & RELATIONAL SCHEMA
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(150) PRIMARY KEY,
    role VARCHAR(50) NOT NULL DEFAULT 'Employee' CHECK(role IN ('Employee', 'Admin', 'Auditor')),
    department VARCHAR(100) DEFAULT 'General Operations',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(150) NOT NULL,
    title VARCHAR(255) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL CHECK(amount > 0),
    category VARCHAR(100) NOT NULL,
    payment_method VARCHAR(100) DEFAULT 'Corporate Card',
    date DATE NOT NULL,
    receipt_ref VARCHAR(100) UNIQUE NOT NULL,
    notes TEXT,
    status VARCHAR(50) DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Rejected')),
    comments TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS budgets (
    username VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    monthly_limit DECIMAL(12, 2) NOT NULL CHECK(monthly_limit > 0),
    fiscal_year INTEGER DEFAULT 2026,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username, category)
);

-- ----------------------------------------------------------------------------
-- 2. PERFORMANCE INDEXES FOR ANALYTICS & AUDITING
-- ----------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_expenses_username ON expenses(username);
CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category);
CREATE INDEX IF NOT EXISTS idx_expenses_status ON expenses(status);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_receipt ON expenses(receipt_ref);

-- ----------------------------------------------------------------------------
-- 3. EXECUTIVE ANALYTICAL VIEWS (BI & REPORTING)
-- ----------------------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_departmental_spend_summary AS
SELECT 
    e.category AS cost_center,
    COUNT(e.id) AS total_claims_submitted,
    SUM(CASE WHEN e.status = 'Approved' THEN e.amount ELSE 0 END) AS approved_spend,
    SUM(CASE WHEN e.status = 'Pending' THEN e.amount ELSE 0 END) AS pending_exposure,
    SUM(CASE WHEN e.status = 'Rejected' THEN e.amount ELSE 0 END) AS rejected_amount,
    ROUND(AVG(e.amount), 2) AS average_claim_ticket
FROM expenses e
GROUP BY e.category
ORDER BY approved_spend DESC;

CREATE VIEW IF NOT EXISTS vw_budget_vs_actual_compliance AS
SELECT 
    b.category AS cost_center,
    b.monthly_limit AS allocated_budget,
    COALESCE(SUM(e.amount), 0) AS actual_utilized_spend,
    (b.monthly_limit - COALESCE(SUM(e.amount), 0)) AS remaining_variance,
    ROUND((COALESCE(SUM(e.amount), 0) / b.monthly_limit) * 100, 2) AS utilization_percentage
FROM budgets b
LEFT JOIN expenses e 
    ON b.category = e.category 
    AND e.status != 'Rejected'
WHERE b.username = 'global'
GROUP BY b.category, b.monthly_limit;

-- ----------------------------------------------------------------------------
-- 4. DEFAULT SEED POLICIES FOR GLOBAL COST CENTERS
-- ----------------------------------------------------------------------------

INSERT OR IGNORE INTO budgets (username, category, monthly_limit) VALUES
('global', 'Travel & Conveyance', 75000.00),
('global', 'Client Entertainment', 50000.00),
('global', 'Software & Cloud', 120000.00),
('global', 'Office Supplies', 30000.00),
('global', 'Training & Upskilling', 60000.00),
('global', 'Miscellaneous', 25000.00);
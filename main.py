from fastapi import FastAPI, HTTPException
from sqlite3 import IntegrityError
from typing import List
from models import ExpenseCreate, ExpenseUpdate, StatusUpdateWithComments, BudgetCreate
import database

app = FastAPI(title="Corporate Expense Intelligence API", version="8.0")

@app.on_event("startup")
def startup_event():
    database.init_db()

@app.get("/")
def read_root():
    return {"message": "Enterprise Corporate Hub API is online."}

@app.get("/role/{username}")
def get_role(username: str):
    return {"role": database.get_user_role(username)}

@app.post("/expenses/", response_model=dict)
def create_expense(expense: ExpenseCreate):
    try:
        expense_id = database.add_expense(
            username=expense.username,
            title=expense.title,
            amount=expense.amount,
            category=expense.category,
            payment_method=expense.payment_method,
            date=str(expense.date),
            receipt_ref=expense.receipt_ref,
            notes=expense.notes
        )
        return {"id": expense_id, "message": "Expense logged successfully"}
    except IntegrityError:
        raise HTTPException(
            status_code=400, 
            detail=f"Duplicate Error: Receipt reference '{expense.receipt_ref}' already exists in the system!"
        )

@app.get("/expenses/{username}")
def read_expenses(username: str):
    role = database.get_user_role(username)
    return database.get_expenses(username, role)

@app.patch("/expenses/{expense_id}/review")
def review_expense(expense_id: int, payload: StatusUpdateWithComments):
    success = database.update_expense_status_with_comments(expense_id, payload.status, payload.comments)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": f"Expense marked as {payload.status}"}

@app.put("/expenses/{expense_id}")
def edit_expense(expense_id: int, payload: ExpenseUpdate):
    try:
        success = database.modify_expense(
            expense_id, payload.title, payload.amount, payload.category, 
            payload.payment_method, payload.date, payload.receipt_ref, payload.notes, payload.comments
        )
        if not success:
            raise HTTPException(status_code=404, detail="Expense not found")
        return {"message": "Expense modified successfully"}
    except IntegrityError:
        raise HTTPException(
            status_code=400, 
            detail=f"Duplicate Error: Receipt reference '{payload.receipt_ref}' is already assigned to another expense!"
        )

@app.delete("/expenses/{expense_id}/{username}")
def remove_expense(expense_id: int, username: str):
    role = database.get_user_role(username)
    success = database.delete_expense(expense_id, username, role)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found or unauthorized")
    return {"message": "Expense removed successfully"}

@app.post("/budgets/")
def set_budget(budget: BudgetCreate):
    database.set_budget(budget.username, budget.category, budget.monthly_limit)
    return {"message": "Budget policy configured"}

@app.get("/budgets/{username}")
def get_budgets(username: str):
    return database.get_budgets(username)

@app.get("/analytics/budget-comparison/{username}")
def get_budget_comparison(username: str):
    role = database.get_user_role(username)
    expenses = database.get_expenses(username, role)
    budgets = database.get_budgets(username)
    
    # Calculate spend per category
    spend_map = {}
    for exp in expenses:
        cat = exp["category"]
        spend_map[cat] = spend_map.get(cat, 0.0) + exp["amount"]
        
    comparison_data = []
    all_categories = set(list(spend_map.keys()) + list(budgets.keys()))
    
    for cat in all_categories:
        comparison_data.append({
            "category": cat,
            "actual_spend": spend_map.get(cat, 0.0),
            "budget_limit": budgets.get(cat, 0.0)
        })
    return comparison_data
import datetime
from pydantic import BaseModel, Field
from typing import Optional

class ExpenseCreate(BaseModel):
    username: str
    title: str = Field(min_length=1, max_length=150)
    amount: float = Field(gt=0)
    category: str = "Operations"
    payment_method: str = "Corporate Card"
    date: datetime.date = Field(default_factory=datetime.date.today)
    receipt_ref: Optional[str] = "N/A"
    notes: Optional[str] = ""

class ExpenseUpdate(BaseModel):
    title: str
    amount: float
    category: str
    payment_method: str
    date: str
    receipt_ref: Optional[str]
    notes: Optional[str]
    comments: Optional[str]

class StatusUpdateWithComments(BaseModel):
    status: str
    comments: str

class BudgetCreate(BaseModel):
    username: str
    category: str
    monthly_limit: float = Field(..., gt=0)
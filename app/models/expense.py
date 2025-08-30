from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ExpenseIn(BaseModel):
    amount: float
    description: str
    date: date
    category: Optional[str] = None

class ExpenseOut(ExpenseIn):
    id: str = Field(..., alias="_id")

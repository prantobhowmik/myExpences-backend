
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExpenseIn(BaseModel):
    amount: float
    description: str
    date: datetime  # now supports date and time
    category: Optional[str] = None

class ExpenseOut(ExpenseIn):
    id: str = Field(..., alias="_id")

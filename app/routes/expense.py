from fastapi import APIRouter, HTTPException
from app.models.expense import ExpenseIn, ExpenseOut
from app.db.mongo import db
from bson import ObjectId
from typing import List, Optional
from datetime import date

router = APIRouter()

@router.post("/expenses", response_model=ExpenseOut)
async def add_expense(expense: ExpenseIn):
    doc = expense.dict()
    result = await db.expenses.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc

@router.get("/expenses", response_model=List[ExpenseOut])
async def list_expenses(month: Optional[int] = None, year: Optional[int] = None):
    query = {}
    if month and year:
        query["date"] = {"$gte": date(year, month, 1), "$lt": date(year, month + 1 if month < 12 else 1, year if month < 12 else year + 1, 1)}
    cursor = db.expenses.find(query)
    expenses = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        expenses.append(doc)
    return expenses

@router.get("/expenses/{expense_id}", response_model=ExpenseOut)
async def get_expense(expense_id: str):
    doc = await db.expenses.find_one({"_id": ObjectId(expense_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Expense not found")
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/summary/{year}/{month}")
async def monthly_summary(year: int, month: int):
    start = date(year, month, 1)
    end_month = month + 1 if month < 12 else 1
    end_year = year if month < 12 else year + 1
    end = date(end_year, end_month, 1)
    cursor = db.expenses.find({"date": {"$gte": start, "$lt": end}})
    total = 0.0
    count = 0
    async for doc in cursor:
        total += doc["amount"]
        count += 1
    return {"year": year, "month": month, "total": total, "count": count}

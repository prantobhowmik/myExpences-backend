
from fastapi import APIRouter, HTTPException, Depends
from app.utils.jwt_auth import verify_jwt_token
from app.models.expense import ExpenseIn, ExpenseOut
from app.db.mongo import db
from bson import ObjectId
from typing import List, Optional
from datetime import date

router = APIRouter()



# Add expense and return the expense plus updated monthly summary
@router.post("/expenses")
async def add_expense(expense: ExpenseIn, user=Depends(verify_jwt_token)):
    doc = expense.dict()
    # Convert date to ISO string for MongoDB
    if isinstance(doc["date"], date):
        doc["date"] = doc["date"].isoformat()
    result = await db.expenses.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    # Calculate updated summary for the month
    exp_date = expense.date
    start = date(exp_date.year, exp_date.month, 1)
    end_month = exp_date.month + 1 if exp_date.month < 12 else 1
    end_year = exp_date.year if exp_date.month < 12 else exp_date.year + 1
    end = date(end_year, end_month, 1)
    cursor = db.expenses.find({"date": {"$gte": start.isoformat(), "$lt": end.isoformat()}})
    total = 0.0
    count = 0
    async for e in cursor:
        total += e["amount"]
        count += 1
    return {"expense": doc, "summary": {"year": exp_date.year, "month": exp_date.month, "total": total, "count": count}}


# Edit expense
@router.put("/expenses/{expense_id}", response_model=ExpenseOut)
async def edit_expense(expense_id: str, expense: ExpenseIn, user=Depends(verify_jwt_token)):
    update_doc = expense.dict()
    if isinstance(update_doc["date"], date):
        update_doc["date"] = update_doc["date"].isoformat()
    result = await db.expenses.update_one({"_id": ObjectId(expense_id)}, {"$set": update_doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    updated = await db.expenses.find_one({"_id": ObjectId(expense_id)})
    updated["_id"] = str(updated["_id"])
    return updated

# Delete expense
@router.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: str, user=Depends(verify_jwt_token)):
    result = await db.expenses.delete_one({"_id": ObjectId(expense_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"msg": "Expense deleted"}


# List expenses (optionally filter by month/year)
@router.get("/expenses", response_model=List[ExpenseOut])
async def list_expenses(month: Optional[int] = None, year: Optional[int] = None, user=Depends(verify_jwt_token)):
    query = {}
    if month and year:
        start = date(year, month, 1)
        end_month = month + 1 if month < 12 else 1
        end_year = year if month < 12 else year + 1
        end = date(end_year, end_month, 1)
        query["date"] = {"$gte": start.isoformat(), "$lt": end.isoformat()}
    cursor = db.expenses.find(query)
    expenses = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        expenses.append(doc)
    return expenses

@router.get("/expenses/{expense_id}", response_model=ExpenseOut)
async def get_expense(expense_id: str, user=Depends(verify_jwt_token)):
    doc = await db.expenses.find_one({"_id": ObjectId(expense_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Expense not found")
    doc["_id"] = str(doc["_id"])
    return doc


# Get latest summary (current month)
@router.get("/summary/latest")
async def latest_summary(user=Depends(verify_jwt_token)):
    today = date.today()
    start = date(today.year, today.month, 1)
    end_month = today.month + 1 if today.month < 12 else 1
    end_year = today.year if today.month < 12 else today.year + 1
    end = date(end_year, end_month, 1)
    cursor = db.expenses.find({"date": {"$gte": start, "$lt": end}})
    total = 0.0
    count = 0
    async for doc in cursor:
        total += doc["amount"]
        count += 1
    return {"year": today.year, "month": today.month, "total": total, "count": count}

# Get summary for any month
@router.get("/summary/{year}/{month}")
async def monthly_summary(year: int, month: int, user=Depends(verify_jwt_token)):
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

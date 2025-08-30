

from fastapi import FastAPI
from app.routes.expense import router as expense_router

app = FastAPI(title="myExpences")
app.include_router(expense_router)

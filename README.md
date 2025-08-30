# myExpences FastAPI App

## Features
- Add a new expense
- List expenses (optionally filter by month/year)
- View details of a specific expense
- Monthly summary (total and count)

## How to Run

1. Activate your virtual environment:
   ```zsh
   source .venv/bin/activate
   ```
2. Start the FastAPI server:
   ```zsh
   uvicorn main:app --reload
   ```
3. Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs.

## Example Expense Object
```
{
  "id": "<uuid>",
  "amount": 100.0,
  "description": "Groceries",
  "date": "2025-08-30",
  "category": "Food"
}
```

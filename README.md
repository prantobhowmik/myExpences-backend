# myExpences FastAPI App

## Features
- Add a new expense
- List expenses (optionally filter by month/year)
- View details of a specific expense
- Monthly summary (total and count)

## Project Structure

- `main.py`: FastAPI entry point
- `app/models/`: Pydantic models
- `app/routes/`: API routes
- `app/db/`: MongoDB connection
- `app/utils/`: Utility functions

## How to Run Locally

1. Activate your virtual environment:
   ```zsh
   source .venv/bin/activate
   ```
2. Start the FastAPI server:
   ```zsh
   uvicorn main:app --reload
   ```
3. Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs.

## How to Run with Docker Compose

1. Make sure Docker is installed and running.
2. Start the app and MongoDB:
   ```zsh
   docker compose up --build
   ```
3. Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

## Example Expense Object
```json
{
  "amount": 100.0,
  "description": "Groceries",
  "date": "2025-08-30",
  "category": "Food"
}
```




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.expense import router as expense_router

tags_metadata = [
	{
		"name": "Auth",
		"description": "Authentication endpoints for login and token generation."
	},
	{
		"name": "Expenses",
		"description": "Operations for adding, listing, and viewing expenses."
	},
	{
		"name": "Summary",
		"description": "Endpoints for monthly and latest expense calculations."
	}
]

app = FastAPI(
	title="myExpences",
	description="Track your monthly expenses and get automatic calculations.",
	version="1.0.0",
	openapi_tags=tags_metadata,
	docs_url="/docs",
	redoc_url="/redoc"
)

# Allow CORS for frontend integration
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


# Welcoming message endpoint
@app.get("/", tags=["Welcome"])
def welcome():
	return {"message": "Welcome to myExpences API! Track your monthly expenses easily."}



# Import and register auth router
from app.routes.auth import router as auth_router
from app.routes.google_auth import router as google_auth_router
app.include_router(auth_router, tags=["Auth"])
app.include_router(google_auth_router, tags=["Auth"])
app.include_router(expense_router, tags=["Expenses", "Summary"])

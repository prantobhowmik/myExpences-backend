




import logging
from fastapi import FastAPI, Request
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


# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("myExpences")

app = FastAPI(
	title="myExpences",
	description="Track your monthly expenses and get automatic calculations.",
	version="1.0.0",
	openapi_tags=tags_metadata,
	docs_url="/docs",
	redoc_url="/redoc"
)

# Allow CORS for frontend integration

# allow your vite dev & any prod origin (add later)
origins = [
	"http://localhost:3000",
	"http://127.0.0.1:3000",
	# add your deployed web app origin here when you deploy the frontend
	"https://my-expences-frontend-otepnjnbs-pranto-bhowmiks-projects.vercel.app",
	"https://my-expences-frontend-git-main-pranto-bhowmiks-projects.vercel.app",
]



app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,       # allow all specified origins
	allow_credentials=True,
	allow_methods=["*"],         # allow all HTTP methods
	allow_headers=["*"],         # allow all headers
)




# (Session and session timeout middleware removed; use JWT only)



# Welcoming message endpoint
@app.get("/", tags=["Welcome"])
async def welcome(request: Request):
	logger.info(f"{request.method} {request.url.path} from {request.client.host}")
	return {"message": "Welcome to myExpences API! Track your monthly expenses easily."}



# Import and register auth router
from app.routes.auth import router as auth_router
from app.routes.google_auth import router as google_auth_router
app.include_router(auth_router, tags=["Auth"])
app.include_router(google_auth_router, tags=["Auth"])
app.include_router(expense_router, tags=["Expenses", "Summary"])

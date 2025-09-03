

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt
from app.db.mongo import db

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserIn(BaseModel):
	full_name: str
	username: str
	email: EmailStr
	mobile: str
	age: int
	password: str

class UserLogin(BaseModel):
	identifier: str  # username, email, or mobile
	password: str

class Token(BaseModel):
	access_token: str
	token_type: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
	to_encode = data.copy()
	expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

@router.post("/signup")
async def signup(user: UserIn):
	# Check for existing user by username, email, or mobile
	existing = await db.users.find_one({"$or": [
		{"username": user.username},
		{"email": user.email},
		{"mobile": user.mobile}
	]})
	if existing:
		raise HTTPException(status_code=400, detail="User already registered with username, email, or mobile")
	hashed_password = pwd_context.hash(user.password)
	user_doc = user.dict()
	user_doc["hashed_password"] = hashed_password
	del user_doc["password"]
	await db.users.insert_one(user_doc)
	return {"msg": "User created successfully"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
	# Find user by username, email, or mobile
	db_user = await db.users.find_one({"$or": [
		{"username": user.identifier},
		{"email": user.identifier},
		{"mobile": user.identifier}
	]})
	if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
	access_token = create_access_token(data={"sub": db_user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
	return {"access_token": access_token, "token_type": "bearer"}


from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {}

class UserIn(BaseModel):
	username: str
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
def signup(user: UserIn):
	if user.username in fake_users_db:
		raise HTTPException(status_code=400, detail="Username already registered")
	hashed_password = pwd_context.hash(user.password)
	fake_users_db[user.username] = {"username": user.username, "hashed_password": hashed_password}
	return {"msg": "User created successfully"}

@router.post("/login", response_model=Token)
def login(user: UserIn):
	db_user = fake_users_db.get(user.username)
	if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
	access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
	return {"access_token": access_token, "token_type": "bearer"}

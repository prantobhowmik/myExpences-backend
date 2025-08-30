from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

http_bearer = HTTPBearer()
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Contains user info
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired JWT token",
        )

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from typing import Optional

SECRET_KEY = "ggew324109gadbfk1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("password123")
    }
}

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_user(username: str):
    user = fake_users_db.get(username)
    if user:
        return UserInDB(username=user["username"], hashed_password=user["hashed_password"])

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_tokens(username: str):
    access = create_token({"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh = create_token({"sub": username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    return {"access_token": access, "refresh_token": refresh}

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return User(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
async def get_optional_user(request: Request) -> Optional[User]:
    auth: str = request.headers.get("Authorization")
    if auth:
        scheme, token = get_authorization_scheme_param(auth)
        if scheme.lower() != "bearer":
            return None
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                return None
            return User(username=username)
        except JWTError:
            return None
    return None
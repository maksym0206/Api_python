from fastapi import APIRouter, HTTPException, Form
from .auth import authenticate_user, create_tokens, Token

auth_router = APIRouter()

@auth_router.post("/token", response_model=Token)
def login(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return create_tokens(username)

@auth_router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str = Form(...)):
    from jose import JWTError, jwt
    from .auth import SECRET_KEY, ALGORITHM
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return create_tokens(username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
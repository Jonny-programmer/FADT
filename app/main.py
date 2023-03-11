import time
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import *
from app.db import database
from .db.crud import get_user_by_username
from .db.schemas import User, TokenData, Token
from .dependencies import get_token_header, oauth2_scheme, verify_password, get_db_session
from .internal import admin
from .routers import items, users

# Можно вместо этого absolute import: from app.routers import items, users
# app = FastAPI(dependencies=[Depends(oauth2_scheme)])
app = FastAPI()

# database.global_init(SQLALCHEMY_DATABASE_URI)

origins = [
    "http://localhost.domain_name.com",
    "https://localhost.com",
    "http://localhost",
    "https://localhost"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)
# You can add the same router multiple times with different prefixes This might be useful, for example, when you want
# to expose API under different prefixes, e.g.: /api/v1 and /api/latest
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

fake_users_db = {
    "jonny": {
        "username": "jonny",
        "full_name": "John E.",
        "email": "real_boss@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": True,
    }
}


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str, db: Session = Depends(get_db_session)):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # Очень важно, чтобы заголовки возвращались именно такие, как здесь
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/get_users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/get_users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_name": "Computer", "owner": current_user.username}]


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    return {'message': 'Hello from the fastapi application!!'}

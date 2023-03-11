from fastapi import Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.config import SECRET_KEY
from app.db import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_token_header(x_token: str = Header(default=None)):
    if x_token != SECRET_KEY:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_db_session():
    db_session = database.create_session()
    try:
        yield db_session
    finally:
        db_session.close()

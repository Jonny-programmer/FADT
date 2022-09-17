from fastapi import Header, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import SECRET_KEY
from app.db import database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_token_header(x_token: str = Header(default=None)):
    if x_token != SECRET_KEY:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token.lower() != "jessika":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


async def get_db():
    db_session = database.create_session()
    try:
        yield db_session
    finally:
        db_session.close()
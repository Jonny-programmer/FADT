from fastapi import Header, HTTPException

# noinspection PyArgumentList
from app.db.database import SessionLocal


async def get_token_header(x_token: str = Header(default=None)):
    if x_token != "super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token.lower() != "jessika":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
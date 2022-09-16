from fastapi import Depends, FastAPI

from .dependencies import get_token_header, get_db
from .internal import admin
from .routers import items, users
# Можно вместо этого absolute import: from app.routers import items, users
from app.db import crud, models, schemas
from app.db import database


database.global_init("app/db/data/FADT_database.db")


app = FastAPI(dependencies=[Depends(get_token_header)])

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


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
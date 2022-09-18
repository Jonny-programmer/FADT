from flask import Flask
from asgiref.wsgi import WsgiToAsgi
from flask.logging import default_handler
from fastapi import Depends, FastAPI
# Можно вместо этого absolute import: from app.routers import items, users
from flask import render_template

from app.db import database
from .dependencies import get_token_header
from .internal import admin
from .routers import items, users
from app.config import *

app = Flask(__name__)
app.logger.removeHandler(default_handler)

api = FastAPI(dependencies=[Depends(get_token_header)])

database.global_init(SQLALCHEMY_DATABASE_URI)

api.include_router(users.router)
api.include_router(items.router)
# You can add the same router multiple times with different prefixes This might be useful, for example, when you want
# to expose API under different prefixes, e.g.: /api/v1 and /api/latest
api.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


wsgi = WsgiToAsgi(app)


@api.get("/")
async def root():
    return {'message': 'Hello from the fastapi application!!'}


@app.route("/")
def root():
    return render_template('index.html')

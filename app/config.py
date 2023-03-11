# App configuration file
import os

# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:password@localhost:5433/tgym_server"
SQLALCHEMY_DATABASE_URI = "sqlite:///app/pspsh.db?check_same_thread=False"
# Если будешь менять адрес БД, не забудь поменять его же в alembic.ini, чтобы работали миграции
PROJECT_ROOT = str(os.getcwd()).rsplit("/", maxsplit=1)[0]

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = '913d9d6a530b3853a4aabee7d1538aa67f36df16bf42828199c5b1cdaad60bb5'
CSRF_ENABLED = True
STATIC_FOLDER = 'static'
TEMPLATE_FOLDER = 'templates'
# EXPLAIN_TEMPLATE_LOADING = True

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# DEBUG = True

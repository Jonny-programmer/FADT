# App configuration file
import os

# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:password@localhost:5433/tgym_server"
SQLALCHEMY_DATABASE_URI = "sqlite:///app/pspsh.db?check_same_thread=False"
# Если будешь менять адрес БД, не забудь поменять его же в alembic.ini, чтобы работали миграции
PROJECT_ROOT = str(os.getcwd()).rsplit("/", maxsplit=1)[0]

SECRET_KEY = '820b4ad02742e6630b554a48de7d2d9f'
CSRF_ENABLED = True
STATIC_FOLDER = 'static'
TEMPLATE_FOLDER = 'templates'
# EXPLAIN_TEMPLATE_LOADING = True

# DEBUG = True

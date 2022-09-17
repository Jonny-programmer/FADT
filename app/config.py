# App configuration file
import os
from datetime import timedelta

SQLALCHEMY_DATABASE_URI = "sqlite:///app/db/data/FADT_app.db"

PROJECT_ROOT = str(os.getcwd()).rsplit("/", maxsplit=1)[0]

SECRET_KEY = '820b4ad02742e6630b554a48de7d2d9f'
CSRF_ENABLED = True
STATIC_FOLDER = 'static'
TEMPLATE_FOLDER = 'templates'
# EXPLAIN_TEMPLATE_LOADING = True

# DEBUG = True

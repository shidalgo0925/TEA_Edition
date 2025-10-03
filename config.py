# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Archivo de credenciales de OAuth2 (descargado de Google Cloud Console)
# Pon el JSON aquí o cambia la ruta absoluta si lo tienes en otro lado
CLIENT_SECRETS_FILE = os.environ.get(
    "CLIENT_SECRETS_FILE",
    os.path.join(BASE_DIR, "client_secret.json"),
)

# Dónde guardar el token de usuario
TOKEN_FILE = os.environ.get(
    "TOKEN_FILE",
    os.path.join(BASE_DIR, ".secrets", "token.json"),
)

# Redirect URI registrado en Google (debe coincidir 1:1)
OAUTH_REDIRECT_URI = os.environ.get(
    "OAUTH_REDIRECT_URI",
    "https://focus.easytech.services/oauth2callback"
)

# Scopes mínimos para leer eventos
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly"
]

# Zona horaria local
LOCAL_TZ = os.environ.get("LOCAL_TZ", "America/Panama")

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://onepercent_user:STRONG_PASS@localhost:5432/onepercent_db"
)
SQLALCHEMY_ECHO = os.environ.get("SQL_ECHO", "0") == "1"

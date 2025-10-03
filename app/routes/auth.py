# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from flask import Blueprint, redirect, request, session, url_for, flash, jsonify, current_app
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import config  # CLIENT_SECRETS_FILE, TOKEN_FILE, OAUTH_REDIRECT_URI, GOOGLE_SCOPES

auth_bp = Blueprint("auth", __name__)

# ---------------------------
# Helpers de token
# ---------------------------
def _ensure_token_dir():
    Path(config.TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)

def _save_credentials(creds: Credentials):
    _ensure_token_dir()
    Path(config.TOKEN_FILE).write_text(creds.to_json(), encoding="utf-8")

def _load_credentials():
    if os.path.exists(config.TOKEN_FILE):
        with open(config.TOKEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Credentials.from_authorized_user_info(data, config.GOOGLE_SCOPES)
    return None

def get_credentials():
    creds = _load_credentials()
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_credentials(creds)
        except Exception:
            return None
    return creds

def _auth_response_url():
    """Corrige scheme detrás de proxy si hace falta."""
    url = request.url
    xf = request.headers.get("X-Forwarded-Proto", "")
    if xf and xf.split(",")[0].strip().lower() == "https" and url.startswith("http://"):
        url = "https://" + url.split("://", 1)[1]
    return url

# ---------------------------
# Rutas
# ---------------------------
@auth_bp.route("/google/connect")
def google_connect():
    if not current_app.secret_key:
        return "SECRET_KEY no configurada en Flask.", 500

    flow = Flow.from_client_secrets_file(
        client_secrets_file=config.CLIENT_SECRETS_FILE,
        scopes=config.GOOGLE_SCOPES,
        redirect_uri=config.OAUTH_REDIRECT_URI,
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    session["oauth_state"] = state
    return redirect(authorization_url)

@auth_bp.route("/oauth2callback")
def oauth2callback():
    state_from_google = request.args.get("state")
    state_expected = session.get("oauth_state")
    if not state_from_google or state_from_google != state_expected:
        return "Estado OAuth inválido. Reintenta desde /google/connect.", 400

    flow = Flow.from_client_secrets_file(
        client_secrets_file=config.CLIENT_SECRETS_FILE,
        scopes=config.GOOGLE_SCOPES,
        redirect_uri=config.OAUTH_REDIRECT_URI,
    )
    flow.fetch_token(authorization_response=_auth_response_url())
    creds = flow.credentials
    _save_credentials(creds)

    flash("Cuenta de Google conectada correctamente.", "success")
    return redirect(url_for("dashboard.dashboard"))

@auth_bp.route("/google/disconnect")
def google_disconnect():
    if os.path.exists(config.TOKEN_FILE):
        os.remove(config.TOKEN_FILE)
    session.clear()
    flash("Desconectado de Google Calendar.", "warning")
    return redirect(url_for("dashboard.dashboard"))

from pathlib import Path
from flask import current_app, redirect, request, session, jsonify
from google_auth_oauthlib.flow import Flow
import config  # CLIENT_SECRETS_FILE, TOKEN_FILE, OAUTH_REDIRECT_URI, GOOGLE_SCOPES

def _ensure_token_dir():
    Path(config.TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)

def _save_credentials(creds):
    _ensure_token_dir()
    Path(config.TOKEN_FILE).write_text(creds.to_json(), encoding="utf-8")

from . import auth_bp  # después de definir auth_bp

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
        access_type="offline", include_granted_scopes="true", prompt="consent"
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
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    _save_credentials(creds)

    return jsonify({
        "status": "OK",
        "refresh_token_present": bool(getattr(creds, "refresh_token", None)),
        "scopes": list(creds.scopes or []),
        "token_file": str(config.TOKEN_FILE),
    }), 200

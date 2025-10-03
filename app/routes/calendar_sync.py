from flask import Blueprint, render_template, redirect, url_for, flash
from .auth import get_credentials
from app.utils.google_calendar import get_today_events
from datetime import datetime

cal_bp = Blueprint("cal", __name__)

@cal_bp.route("/sync/today")
def sync_today():
    creds = get_credentials()
    if not creds:
        flash("Conecta tu Google primero.", "warning")
        return redirect(url_for("auth.google_connect"))

    events = get_today_events(creds)
    # Podrías guardar en DB; de momento lo mostramos directo
    flash(f"Eventos de hoy sincronizados: {len(events)}", "success")
    return redirect(url_for("dashboard.dashboard"))

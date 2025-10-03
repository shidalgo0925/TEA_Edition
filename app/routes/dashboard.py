# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from datetime import datetime, timedelta, date
import os

from config import TOKEN_FILE
from app.utils.google_calendar import get_events_range
from app.routes.auth import get_credentials
from app.extensions import get_db
from app.models.plan_day import PlanDay

dashboard_bp = Blueprint("dashboard", __name__)
misc_bp = Blueprint("misc", __name__)

@dashboard_bp.route("/")
def dashboard():
    hoy_date = datetime.now().date()
    manana_date = hoy_date + timedelta(days=1)

    stats = {
        "meta_dic": 5000,
        "prospeccion_min": 30,
        "hoy": hoy_date.strftime("%Y-%m-%d"),
    }

    events_by_day = {hoy_date.isoformat(): [], manana_date.isoformat(): []}
    google_connected = os.path.exists(TOKEN_FILE)

    if google_connected:
        creds = get_credentials()
        if creds:
            try:
                events_by_day.update(get_events_range(creds, days=2))
            except Exception:
                pass
        else:
            google_connected = False

    # Fallback si no hay eventos reales
    if not any(events_by_day.values()):
        events_by_day[hoy_date.isoformat()] = [
            {"hora": "07:30 - 08:30", "actividad": "Proyecto Odoo (Import Center)", "categoria": "Easytech", "done": False},
            {"hora": "08:30 - 09:00", "actividad": "Curso Big Data (capsula diaria)", "categoria": "Personal", "done": False},
            {"hora": "09:00 - 09:30", "actividad": "Prospeccion Mariachi", "categoria": "Mariachi", "done": False},
        ]

    # Aplana y ordena
    def parse_hora_val(h: str) -> str:
        if not h:
            return "23:59"
        h_l = h.lower()
        if h_l.startswith("todo el día"):
            return "00:00"
        if len(h) >= 5 and h[2] == ":":
            return h[:5]
        return "23:59"

    events_flat = []
    for day, evs in events_by_day.items():
        for e in evs:
            events_flat.append({
                "fecha": day,
                "hora": e.get("hora", ""),
                "actividad": e.get("actividad", ""),
                "categoria": e.get("categoria", ""),
                "done": e.get("done", False),
                "_sort_hora": parse_hora_val(e.get("hora", "")),
            })

    events_flat.sort(key=lambda x: (x["fecha"], x["_sort_hora"]))
    for e in events_flat:
        e.pop("_sort_hora", None)

    stats["total_eventos"] = len(events_flat)
    stats["completados"] = sum(1 for e in events_flat if e.get("done"))

    # -------------------
    # NUEVO BLOQUE PLAN
    db = get_db()

    plan = db.query(PlanDay).filter(
        PlanDay.user_id == 1,
        PlanDay.fecha == date.today()
    ).first()

    plan_date = date.today()
    is_today = True

    if not plan:
        plan = db.query(PlanDay).filter(
            PlanDay.user_id == 1,
            PlanDay.fecha >= date.today()
        ).order_by(PlanDay.fecha.asc()).first()
        if plan:
            plan_date = plan.fecha
            is_today = (plan.fecha == date.today())

    plan_items = plan.items if plan else []
    # -------------------

    return render_template(
        "dashboard.html",
        events_flat=events_flat,
        stats=stats,
        google_connected=google_connected,
        plan_items_today=plan_items,
        plan_date=plan_date,
        plan_is_today=is_today
    )

@misc_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@misc_bp.route("/terms")
def terms():
    return render_template("terms.html")

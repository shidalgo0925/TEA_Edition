# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from datetime import date
from ..services.ai_planner import AIPlanner
from ..extensions import get_db
from ..models.goals import Goal
from ..models.plan_day import PlanDay, PlanItem

api_ai_bp = Blueprint("api_ai", __name__, url_prefix="/api/ai/plan")
planner = AIPlanner()

@api_ai_bp.post("/suggest")
def suggest():
    data = request.get_json(force=True, silent=True) or {}
    goals_raw = data.get("metas_crudas", "")
    horizonte = data.get("horizonte", "90d")
    restricciones = data.get("restricciones", {})
    agenda = data.get("agenda", [])
    draft = planner.suggest(goals_raw, horizonte, restricciones, agenda)
    return jsonify({"ok": True, "draft": draft})

@api_ai_bp.post("/refine")
def refine():
    data = request.get_json(force=True, silent=True) or {}
    draft = data.get("draft", {})
    feedback = data.get("feedback", "")
    refined = planner.refine(draft, feedback)
    return jsonify({"ok": True, "draft": refined})

@api_ai_bp.post("/move_to_today")
def move_to_today():
    data = request.get_json(force=True, silent=True) or {}
    user_id = int(data.get("user_id", 1))
    from_fecha = data.get("from_fecha")
    if not from_fecha:
        return jsonify({"ok": False, "error": "from_fecha requerido"}), 400

    db = get_db()
    try:
        src = db.query(PlanDay).filter(
            PlanDay.user_id == user_id,
            PlanDay.fecha == date.fromisoformat(from_fecha)
        ).first()
        if not src:
            return jsonify({"ok": False, "error": "Plan origen no existe"}), 404

        # upsert de hoy
        today = date.today()
        dst = db.query(PlanDay).filter(
            PlanDay.user_id == user_id,
            PlanDay.fecha == today
        ).first()
        if not dst:
            dst = PlanDay(user_id=user_id, fecha=today)
            db.add(dst)
            db.flush()

        # limpiar y copiar items
        db.query(PlanItem).filter(PlanItem.plan_id == dst.id).delete()
        for it in src.items:
            db.add(PlanItem(
                plan_id=dst.id,
                titulo=it.titulo,
                categoria=it.categoria,
                prioridad=it.prioridad,
                dur_min=it.dur_min,
                from_calendar=it.from_calendar,
            ))
        db.commit()
        return jsonify({"ok": True, "moved_from": from_fecha, "to": today.isoformat()})
    except Exception as e:
        db.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500
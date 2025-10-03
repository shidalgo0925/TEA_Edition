# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

ai_wizard_bp = Blueprint("ai_wizard", __name__, url_prefix="/wizard")

@ai_wizard_bp.get("/ai-plan")
def ai_plan():
    return render_template("wizard_ai_plan.html")

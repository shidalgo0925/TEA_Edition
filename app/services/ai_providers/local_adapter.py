# -*- coding: utf-8 -*-
from datetime import date, timedelta

class LocalAdapter:
    """
    Adaptador local 'fake' sin dependencias externas.
    Genera borradores coherentes para probar el flujo end-to-end.
    """

    AREAS = ["Personal", "Económico", "Familiar", "Físico"]

    def normalize_goals(self, goals_raw: str):
        # Parse básico: divide por líneas y asigna áreas por heurística
        lines = [s.strip("-• ").strip() for s in goals_raw.splitlines() if s.strip()]
        metas = []
        for i, line in enumerate(lines[:5], start=1):
            area = self._infer_area(line)
            metas.append({
                "area": area,
                "titulo": line,
                "kpi": "Progreso semanal (%)",
                "fecha_objetivo": (date.today() + timedelta(days=90)).isoformat(),
            })
        if not metas:
            metas = [{
                "area": "Económico",
                "titulo": "Reducir deudas en 10%",
                "kpi": "Saldo total de deuda",
                "fecha_objetivo": (date.today() + timedelta(days=90)).isoformat(),
            }]
        return metas

    def breakdown_weekly(self, metas_smart: list):
        rocas = []
        for m in metas_smart[:3]:
            rocas.append({"semana": 1, "titulo": f"Iniciar: {m['titulo']}"})
        return rocas

    def microactions_daily(self, metas_smart: list, agenda: list, tz: str):
        # Demo: 3 microacciones para mañana
        d = (date.today() + timedelta(days=1)).isoformat()
        base = []
        if metas_smart:
            base.append({"titulo": f"Primer paso: {metas_smart[0]['titulo']}", "categoria":"Personal","prioridad":1,"dur_min":25})
        base.append({"titulo": "Bloque foco 25min", "categoria":"Easytech","prioridad":2,"dur_min":25})
        base.append({"titulo": "Caminata 20min", "categoria":"Físico","prioridad":2,"dur_min":20})
        return { d: base }

    def refine_draft(self, draft: dict, feedback: str):
        # Agrega nota de refinamiento
        draft = dict(draft or {})
        draft["nota_refinado"] = (feedback or "")[:200]
        return draft

    def _infer_area(self, text: str) -> str:
        t = text.lower()
        if "deuda" in t or "ingreso" in t or "pago" in t:
            return "Económico"
        if "famil" in t or "hijo" in t or "pareja" in t:
            return "Familiar"
        if any(word in t for word in ["salud", "peso", "correr", "caminata"]):
            return "Físico"
        return "Personal"

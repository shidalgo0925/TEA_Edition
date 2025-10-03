# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
try:
    from zoneinfo import ZoneInfo  # py3.9+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # py3.8

from .ai_providers.provider_factory import get_provider

LOCAL_TZ = os.environ.get("LOCAL_TZ", "America/Panama")

class AIPlanner:
    def __init__(self):
        self.provider = get_provider()

    def suggest(self, goals_raw: str, horizonte: str, restricciones: dict, agenda: list):
        """
        Retorna un 'draft' con:
          - metas_smart: [{area, titulo, kpi, fecha_objetivo}]
          - rocas_semanales: [{semana, titulo}]
          - microacciones: {YYYY-MM-DD: [ {titulo, categoria, prioridad, dur_min} ]}
        """
        metas_smart = self.provider.normalize_goals(goals_raw)
        rocas = self.provider.breakdown_weekly(metas_smart)
        micro = self.provider.microactions_daily(metas_smart, agenda, LOCAL_TZ)
        return {
            "metas_smart": metas_smart,
            "rocas_semanales": rocas,
            "microacciones": micro,
            "horizonte": horizonte,
            "restricciones": restricciones,
        }

    def refine(self, draft: dict, feedback: str):
        return self.provider.refine_draft(draft, feedback)

    def default_fecha_inicial(self) -> str:
        """Mañana según zona horaria local (America/Panama por defecto)."""
        tz = ZoneInfo(LOCAL_TZ)
        now_local = datetime.now(tz)
        return (now_local + timedelta(days=1)).date().isoformat()

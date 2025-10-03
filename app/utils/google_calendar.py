# -*- coding: utf-8 -*-
"""
Google Calendar utils — obtener eventos por rango (hoy, hoy+mañana), con categorización.
Compatible con Python 3.8 (usa backport de zoneinfo).
"""
from datetime import datetime, time, timedelta
from typing import List, Dict, Any

# ZoneInfo: estándar en 3.9+, backport en 3.8
try:
    from zoneinfo import ZoneInfo  # py39+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # py38

from googleapiclient.discovery import build

# Zona horaria desde config; usa America/Panama por defecto
try:
    from config import LOCAL_TZ  # e.g., "America/Panama"
except Exception:
    LOCAL_TZ = "America/Panama"

# Palabras clave por categoría
KEYWORDS: Dict[str, List[str]] = {
    "Mariachi": ["mariachi", "ensayo", "evento", "misa", "sepelio", "funeral"],
    "Easytech": ["odoo", "import center", "flutter", "firebase", "backend", "flask", "app", "comuniapp"],
    "Personal": ["desayuno", "almuerzo", "cena", "descanso", "lectura", "diario", "familia", "ejercicio"],
}

def categorize(title: str, description: str = "") -> str:
    text = f"{title} {description}".lower()
    for cat, words in KEYWORDS.items():
        if any(w in text for w in words):
            return cat
    return "Personal"

def _parse_dt_local(dt_str: str, tz: ZoneInfo) -> datetime:
    """
    Convierte un ISO (con o sin 'Z') a datetime en zona local.
    Asume que 'date' de Google (YYYY-MM-DD) representa all-day -> 00:00 local.
    """
    if len(dt_str) == 10 and dt_str.count("-") == 2:
        # Caso all-day (solo fecha)
        y, m, d = map(int, dt_str.split("-"))
        return datetime(y, m, d, 0, 0, 0, tzinfo=tz)
    # dateTime con offset o 'Z'
    if dt_str.endswith("Z"):
        dt_str = dt_str.replace("Z", "+00:00")
    dt = datetime.fromisoformat(dt_str)
    # Si viene naive (raro), asumimos local
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(tz)

def get_events_range(
    creds,
    days: int = 3,                       # <-- default ahora 3
    calendar_id: str = "primary",
    max_results: int = 250,
    start_date: "date|None" = None,      # <-- NUEVO parámetro
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Lee eventos desde start_date 00:00 hasta (start_date + days-1) 23:59:59 del calendario indicado.
    Retorna: {"YYYY-MM-DD": [ {hora, actividad, categoria, done}, ... ], ...}
    """
    service = build("calendar", "v3", credentials=creds)
    tz = ZoneInfo(LOCAL_TZ)

    # Si no te pasan start_date, usa hoy (zona local)
    if start_date is None:
        start_date = datetime.now(tz).date()

    start_of_range = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0, tzinfo=tz)
    end_date = start_date + timedelta(days=days - 1)
    end_of_range = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59, tzinfo=tz)

    resp = service.events().list(
        calendarId=calendar_id,
        timeMin=start_of_range.isoformat(),
        timeMax=end_of_range.isoformat(),
        singleEvents=True,
        orderBy="startTime",
        maxResults=max_results,
    ).execute()

    by_day: Dict[str, List[Dict[str, Any]]] = {}
    for ev in resp.get("items", []):
        title = ev.get("summary", "(Sin título)")
        desc = ev.get("description", "") or ""

        s_info = ev.get("start", {}) or {}
        e_info = ev.get("end", {}) or {}

        s_raw = s_info.get("dateTime") or s_info.get("date")
        e_raw = e_info.get("dateTime") or e_info.get("date")
        if not s_raw:
            continue

        dt_start = _parse_dt_local(s_raw, tz)
        all_day = ("date" in s_info) or ("date" in e_info)

        if all_day:
            hora_str = "Todo el día"
        else:
            dt_end = _parse_dt_local(e_raw or s_raw, tz)
            hora_str = f"{dt_start.strftime('%H:%M')} - {dt_end.strftime('%H:%M')}"

        day_key = dt_start.date().isoformat()
        by_day.setdefault(day_key, []).append({
            "hora": hora_str,
            "actividad": title,
            "categoria": categorize(title, desc),
            "done": False,
            "_sort": dt_start.strftime("%H:%M") if not all_day else "00:00",
        })

    for k in by_day:
        by_day[k].sort(key=lambda x: x.get("_sort", "00:00"))
        for item in by_day[k]:
            item.pop("_sort", None)

    return by_day

def get_today_events(creds, max_results: int = 50) -> List[Dict[str, Any]]:
    """
    Compatibilidad con tu firma anterior: eventos SOLO de hoy.
    """
    today_dict = get_events_range(creds, days=1, max_results=max_results)
    # Devuelve lista “plana” (tu formato previo)
    today_key = datetime.now(ZoneInfo(LOCAL_TZ)).date().isoformat()
    return today_dict.get(today_key, [])

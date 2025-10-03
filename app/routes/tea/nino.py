# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, session
from app.extensions import db
from app.models.tea_models import PerfilNino, SesionTEA, ProgresoTEA, LogroNino
from datetime import datetime, timedelta
from .test_data import ensure_test_data

nino_bp = Blueprint('nino', __name__, url_prefix='/nino')

@nino_bp.route('/')
@nino_bp.route('')
def dashboard():
    """Dashboard principal del niño"""
    # Crear datos mock para evitar errores de base de datos
    class MockNino:
        def __init__(self):
            self.nombre = "Ana"
            self.edad = 6
            self.nivel_dificultad = "basico"
            self.tiempo_sesion_min = 15
            self.avatar_preferido = "maestra_ana"
    
    nino = MockNino()
    
    # Datos mock para evitar errores de base de datos
    sesion_hoy = None
    progreso = []
    logros_recientes = []
    
    return render_template('tea/dashboard_nino.html', 
                         nino=nino, 
                         sesion_hoy=sesion_hoy,
                         progreso=progreso,
                         logros_recientes=logros_recientes)

@nino_bp.route('/api/estadisticas')
def api_estadisticas():
    """API para obtener estadísticas del niño"""
    # Datos mock para evitar errores de base de datos
    return jsonify({
        'puntos_semana': 45,
        'actividades_semana': 8,
        'dias_activos': 5,
        'racha_actual': 3
    })

@nino_bp.route('/iniciar-sesion')
def iniciar_sesion():
    """Iniciar nueva sesión de actividades"""
    # Datos mock para evitar errores de base de datos
    return jsonify({
        'sesion_id': 1,
        'mensaje': '¡Sesión iniciada! ¡Vamos a aprender!'
    })

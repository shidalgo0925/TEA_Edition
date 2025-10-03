# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify

# Crear blueprint simple
simple_bp = Blueprint('simple', __name__, url_prefix='/simple')

@simple_bp.route('/')
def index():
    """Página principal simple"""
    return render_template('tea/simple_index.html')

@simple_bp.route('/nino')
def nino():
    """Dashboard del niño - versión simple"""
    return render_template('tea/simple_nino.html')

@simple_bp.route('/padres')
def padres():
    """Dashboard de padres - versión simple"""
    return render_template('tea/simple_padres.html')

@simple_bp.route('/actividades')
def actividades():
    """Lista de actividades - versión simple"""
    return render_template('tea/simple_actividades.html')

@simple_bp.route('/actividad/<int:actividad_id>')
def actividad_detalle(actividad_id):
    """Actividad específica - versión simple"""
    return render_template('tea/simple_actividad.html', actividad_id=actividad_id)

@simple_bp.route('/api/estadisticas')
def api_estadisticas():
    """API simple para estadísticas"""
    return jsonify({
        'puntos_semana': 45,
        'actividades_semana': 8,
        'dias_activos': 5,
        'racha_actual': 3
    })






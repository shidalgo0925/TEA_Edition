# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, session
from app.extensions import db
from app.models.tea_models import (
    PerfilNino, SesionTEA, ProgresoTEA, ActividadTEA, 
    SesionActividad, LogroNino, RecompensaTEA
)
from datetime import datetime, timedelta
import json

padres_bp = Blueprint('padres', __name__, url_prefix='/padres')

@padres_bp.route('/')
@padres_bp.route('')
def dashboard():
    """Dashboard principal para padres/educadores"""
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
    sesiones_semana = []
    sesiones_mes = []
    progreso_habilidades = []
    actividades_stats = []
    logros_recientes = []
    
    return render_template('tea/dashboard_padres.html',
                         nino=nino,
                         sesiones_semana=sesiones_semana,
                         sesiones_mes=sesiones_mes,
                         progreso_habilidades=progreso_habilidades,
                         actividades_stats=actividades_stats,
                         logros_recientes=logros_recientes)

@padres_bp.route('/api/progreso-semanal')
def api_progreso_semanal():
    """API para gráfico de progreso semanal"""
    nino = PerfilNino.query.first()
    if not nino:
        return jsonify({'error': 'No hay perfil de niño'}), 404
    
    # Últimos 7 días
    datos_semana = []
    for i in range(7):
        fecha = datetime.now().date() - timedelta(days=i)
        sesion = SesionTEA.query.filter(
            db.func.date(SesionTEA.fecha) == fecha,
            SesionTEA.nino_id == nino.id
        ).first()
        
        datos_semana.append({
            'fecha': fecha.strftime('%Y-%m-%d'),
            'dia': fecha.strftime('%A'),
            'actividades': sesion.actividades_completadas if sesion else 0,
            'puntos': sesion.puntos_ganados if sesion else 0,
            'duracion': sesion.duracion_minutos if sesion else 0
        })
    
    return jsonify(datos_semana[::-1])  # Ordenar cronológicamente

@padres_bp.route('/api/estadisticas-habilidades')
def api_estadisticas_habilidades():
    """API para estadísticas por habilidades"""
    nino = PerfilNino.query.first()
    if not nino:
        return jsonify({'error': 'No hay perfil de niño'}), 404
    
    habilidades = ProgresoTEA.query.filter_by(nino_id=nino.id).all()
    
    datos_habilidades = []
    for habilidad in habilidades:
        # Calcular progreso porcentual (ejemplo: 0-100%)
        progreso_porcentual = min((habilidad.puntos_totales / 100) * 100, 100)
        
        datos_habilidades.append({
            'habilidad': habilidad.habilidad,
            'nivel': habilidad.nivel_actual,
            'puntos': habilidad.puntos_totales,
            'sesiones': habilidad.sesiones_completadas,
            'racha': habilidad.racha_dias,
            'progreso_porcentual': round(progreso_porcentual, 1)
        })
    
    return jsonify(datos_habilidades)

@padres_bp.route('/configuracion')
def configuracion():
    """Página de configuración del niño"""
    nino = PerfilNino.query.first()
    if not nino:
        return render_template('tea/error.html', 
                             mensaje="No hay perfil de niño configurado")
    
    # Obtener todas las actividades disponibles
    actividades = ActividadTEA.query.filter_by(activa=True).all()
    
    return render_template('tea/configuracion_padres.html',
                         nino=nino,
                         actividades=actividades)

@padres_bp.route('/api/actualizar-configuracion', methods=['POST'])
def api_actualizar_configuracion():
    """API para actualizar configuración del niño"""
    data = request.get_json()
    
    nino = PerfilNino.query.first()
    if not nino:
        return jsonify({'error': 'No hay perfil de niño'}), 404
    
    # Actualizar configuración
    if 'nivel_dificultad' in data:
        nino.nivel_dificultad = data['nivel_dificultad']
    if 'tiempo_sesion_min' in data:
        nino.tiempo_sesion_min = data['tiempo_sesion_min']
    if 'avatar_preferido' in data:
        nino.avatar_preferido = data['avatar_preferido']
    
    db.session.commit()
    
    return jsonify({'mensaje': 'Configuración actualizada exitosamente'})

@padres_bp.route('/reportes')
def reportes():
    """Página de reportes detallados"""
    nino = PerfilNino.query.first()
    if not nino:
        return render_template('tea/error.html', 
                             mensaje="No hay perfil de niño configurado")
    
    # Obtener datos para reportes
    sesiones_totales = SesionTEA.query.filter_by(nino_id=nino.id).all()
    progreso_total = ProgresoTEA.query.filter_by(nino_id=nino.id).all()
    
    return render_template('tea/reportes_padres.html',
                         nino=nino,
                         sesiones_totales=sesiones_totales,
                         progreso_total=progreso_total)

@padres_bp.route('/api/exportar-reporte')
def api_exportar_reporte():
    """API para exportar reporte en formato JSON"""
    nino = PerfilNino.query.first()
    if not nino:
        return jsonify({'error': 'No hay perfil de niño'}), 404
    
    # Generar reporte completo
    reporte = {
        'nino': {
            'nombre': nino.nombre,
            'edad': nino.edad,
            'nivel_dificultad': nino.nivel_dificultad
        },
        'sesiones': [],
        'progreso': [],
        'logros': [],
        'fecha_generacion': datetime.now().isoformat()
    }
    
    # Datos de sesiones
    sesiones = SesionTEA.query.filter_by(nino_id=nino.id).all()
    for sesion in sesiones:
        reporte['sesiones'].append({
            'fecha': sesion.fecha.isoformat(),
            'duracion_minutos': sesion.duracion_minutos,
            'actividades_completadas': sesion.actividades_completadas,
            'puntos_ganados': sesion.puntos_ganados,
            'estado': sesion.estado
        })
    
    # Datos de progreso
    progreso = ProgresoTEA.query.filter_by(nino_id=nino.id).all()
    for prog in progreso:
        reporte['progreso'].append({
            'habilidad': prog.habilidad,
            'nivel_actual': prog.nivel_actual,
            'puntos_totales': prog.puntos_totales,
            'sesiones_completadas': prog.sesiones_completadas,
            'racha_dias': prog.racha_dias
        })
    
    # Datos de logros
    logros = LogroNino.query.filter_by(nino_id=nino.id).all()
    for logro in logros:
        reporte['logros'].append({
            'recompensa': logro.recompensa.nombre,
            'fecha_obtenido': logro.fecha_obtenido.isoformat()
        })
    
    return jsonify(reporte)

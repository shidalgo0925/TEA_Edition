# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, session
from app.extensions import db
from app.models.tea_models import (
    PerfilNino, ActividadTEA, SesionTEA, SesionActividad, 
    ProgresoTEA, LogroNino, RecompensaTEA
)
from datetime import datetime
from .test_data import ensure_test_data

actividades_bp = Blueprint('actividades', __name__, url_prefix='/actividades')

@actividades_bp.route('/')
@actividades_bp.route('')
def lista_actividades():
    """Lista de actividades disponibles"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividades = ActividadTEA.query.filter_by(activa=True).all()
    
    return render_template('tea/actividades_lista.html',
                         nino=nino,
                         actividades=actividades)

@actividades_bp.route('/<int:actividad_id>')
def realizar_actividad(actividad_id):
    """Realizar una actividad específica"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividad = ActividadTEA.query.get_or_404(actividad_id)
    
    # Obtener o crear sesión de hoy
    hoy = datetime.now().date()
    sesion = SesionTEA.query.filter(
        db.func.date(SesionTEA.fecha) == hoy,
        SesionTEA.nino_id == nino.id
    ).first()
    
    if not sesion:
        sesion = SesionTEA(
            nino_id=nino.id,
            estado='iniciada'
        )
        db.session.add(sesion)
        db.session.commit()
    
    return render_template('tea/actividad_detalle.html',
                         nino=nino,
                         actividad=actividad,
                         sesion=sesion)

@actividades_bp.route('/api/completar/<int:actividad_id>', methods=['POST'])
def api_completar_actividad(actividad_id):
    """API para completar una actividad"""
    try:
        data = request.get_json()
        nino = PerfilNino.query.first()
        actividad = ActividadTEA.query.get_or_404(actividad_id)
        
        # Obtener o crear sesión de hoy
        hoy = datetime.now().date()
        sesion = SesionTEA.query.filter(
            db.func.date(SesionTEA.fecha) == hoy,
            SesionTEA.nino_id == nino.id
        ).first()
        
        if not sesion:
            sesion = SesionTEA(
                nino_id=nino.id,
                estado='iniciada'
            )
            db.session.add(sesion)
            db.session.commit()
        
        # Crear o actualizar sesión-actividad
        sesion_actividad = SesionActividad.query.filter_by(
            sesion_id=sesion.id,
            actividad_id=actividad_id
        ).first()
        
        if not sesion_actividad:
            sesion_actividad = SesionActividad(
                sesion_id=sesion.id,
                actividad_id=actividad_id,
                orden=1,
                intentos=1,
                tiempo_dedicado=data.get('tiempo_dedicado', 0),
                puntos_obtenidos=actividad.puntos_recompensa,
                fecha_completada=datetime.now()
            )
            db.session.add(sesion_actividad)
        else:
            sesion_actividad.intentos += 1
            sesion_actividad.completada = True
            sesion_actividad.puntos_obtenidos = actividad.puntos_recompensa
            sesion_actividad.fecha_completada = datetime.now()
        
        # Actualizar sesión
        sesion.actividades_completadas += 1
        sesion.puntos_ganados += actividad.puntos_recompensa
        sesion.duracion_minutos += data.get('tiempo_dedicado', 0) // 60
        
        # Actualizar progreso
        progreso = ProgresoTEA.query.filter_by(
            nino_id=nino.id,
            habilidad=actividad.categoria
        ).first()
        
        if progreso:
            progreso.puntos_totales += actividad.puntos_recompensa
            progreso.sesiones_completadas += 1
            progreso.racha_dias = 1  # Simplificado para demo
        else:
            progreso = ProgresoTEA(
                nino_id=nino.id,
                habilidad=actividad.categoria,
                nivel_actual=nino.nivel_dificultad,
                puntos_totales=actividad.puntos_recompensa,
                sesiones_completadas=1,
                racha_dias=1
            )
            db.session.add(progreso)
        
        db.session.commit()
        
        # Verificar si desbloquea recompensa
        recompensas_desbloqueadas = []
        recompensas = RecompensaTEA.query.filter(
            RecompensaTEA.puntos_requeridos <= progreso.puntos_totales
        ).all()
        
        for recompensa in recompensas:
            # Verificar si ya la tiene
            logro_existente = LogroNino.query.filter_by(
                nino_id=nino.id,
                recompensa_id=recompensa.id
            ).first()
            
            if not logro_existente:
                logro = LogroNino(
                    nino_id=nino.id,
                    recompensa_id=recompensa.id,
                    sesion_id=sesion.id
                )
                db.session.add(logro)
                recompensas_desbloqueadas.append(recompensa)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'puntos_ganados': actividad.puntos_recompensa,
            'recompensas_desbloqueadas': [
                {
                    'nombre': r.nombre,
                    'icono': r.icono_url,
                    'descripcion': r.descripcion
                } for r in recompensas_desbloqueadas
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@actividades_bp.route('/lenguaje')
def actividades_lenguaje():
    """Actividades de lenguaje"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividades = ActividadTEA.query.filter_by(
        categoria='lenguaje',
        activa=True
    ).all()
    
    return render_template('tea/actividades_categoria.html',
                         nino=nino,
                         actividades=actividades,
                         categoria='Lenguaje',
                         icono='🗣️')

@actividades_bp.route('/numeros')
def actividades_numeros():
    """Actividades de números"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividades = ActividadTEA.query.filter_by(
        categoria='numeros',
        activa=True
    ).all()
    
    return render_template('tea/actividades_categoria.html',
                         nino=nino,
                         actividades=actividades,
                         categoria='Números',
                         icono='🔢')

@actividades_bp.route('/colores')
def actividades_colores():
    """Actividades de colores"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividades = ActividadTEA.query.filter_by(
        categoria='colores',
        activa=True
    ).all()
    
    return render_template('tea/actividades_categoria.html',
                         nino=nino,
                         actividades=actividades,
                         categoria='Colores',
                         icono='🎨')

@actividades_bp.route('/animales')
def actividades_animales():
    """Actividades de animales"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividades = ActividadTEA.query.filter_by(
        categoria='animales',
        activa=True
    ).all()
    
    return render_template('tea/actividades_categoria.html',
                         nino=nino,
                         actividades=actividades,
                         categoria='Animales',
                         icono='🐶')






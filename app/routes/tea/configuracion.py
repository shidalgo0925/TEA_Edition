# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from app.models.tea_models import ConfiguracionUsuario, PerfilNino, UsuarioNino
from app import db
from functools import wraps

configuracion_bp = Blueprint('configuracion', __name__, url_prefix='/configuracion')

def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'user_type' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'info')
            return redirect(url_for('tea.auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def padres_only(f):
    """Decorador para permitir solo acceso a padres"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'user_type' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'info')
            return redirect(url_for('tea.auth.login'))
        
        if session.get('user_type') != 'padre':
            flash('Solo los padres pueden acceder a la configuración.', 'error')
            return redirect(url_for('tea.index'))
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_nino_id():
    """Obtener el ID del niño actual"""
    if session.get('user_type') == 'nino':
        return session.get('user_id')
    elif session.get('user_type') == 'padre':
        # Si es padre, obtener el primer niño asociado
        usuario_padre = session.get('user_id')
        nino = UsuarioNino.query.filter_by(activo=True).first()
        return nino.id if nino else None
    return None

@configuracion_bp.route('/')
@padres_only
def configuracion_principal():
    """Página principal de configuración unificada"""
    nino_id = get_current_nino_id()
    if not nino_id:
        flash('No se pudo encontrar el perfil del niño.', 'error')
        return redirect(url_for('tea.index'))
    
    # Obtener o crear configuración
    config = ConfiguracionUsuario.query.filter_by(nino_id=nino_id, activa=True).first()
    if not config:
        config = ConfiguracionUsuario(nino_id=nino_id)
        db.session.add(config)
        db.session.commit()
    
    return render_template('tea/configuracion_unificada.html', config=config)

# Rutas de configuración específicas eliminadas - ahora todo está unificado

@configuracion_bp.route('/api/guardar', methods=['POST'])
@login_required
def api_guardar_configuracion():
    """API para guardar configuración"""
    try:
        nino_id = get_current_nino_id()
        if not nino_id:
            return jsonify({'error': 'No se pudo encontrar el perfil del niño'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        # Obtener o crear configuración
        config = ConfiguracionUsuario.query.filter_by(nino_id=nino_id, activa=True).first()
        if not config:
            config = ConfiguracionUsuario(nino_id=nino_id)
            db.session.add(config)
        
        # Actualizar configuración según el tipo
        tipo = data.get('tipo')
        
        if tipo == 'colores':
            config.color_primario = data.get('color_primario', config.color_primario)
            config.color_secundario = data.get('color_secundario', config.color_secundario)
            config.color_fondo = data.get('color_fondo', config.color_fondo)
            config.color_texto = data.get('color_texto', config.color_texto)
            config.color_accento = data.get('color_accento', config.color_acento)
            
        elif tipo == 'interfaz':
            config.tamaño_fuente = data.get('tamaño_fuente', config.tamaño_fuente)
            config.modo_alto_contraste = data.get('modo_alto_contraste', config.modo_alto_contraste)
            config.animaciones_habilitadas = data.get('animaciones_habilitadas', config.animaciones_habilitadas)
            config.sonidos_habilitados = data.get('sonidos_habilitados', config.sonidos_habilitados)
            
        elif tipo == 'dificultad':
            config.nivel_dificultad_global = data.get('nivel_dificultad_global', config.nivel_dificultad_global)
            config.tiempo_por_actividad = data.get('tiempo_por_actividad', config.tiempo_por_actividad)
            config.pausas_automaticas = data.get('pausas_automaticas', config.pausas_automaticas)
            config.tiempo_pausa = data.get('tiempo_pausa', config.tiempo_pausa)
            
        elif tipo == 'avatar':
            config.avatar_preferido = data.get('avatar_preferido', config.avatar_preferido)
            config.velocidad_voz = data.get('velocidad_voz', config.velocidad_voz)
            config.tono_voz = data.get('tono_voz', config.tono_voz)
            config.volumen_voz = data.get('volumen_voz', config.volumen_voz)
            
        elif tipo == 'gamificacion':
            config.mostrar_puntos = data.get('mostrar_puntos', config.mostrar_puntos)
            config.mostrar_medallas = data.get('mostrar_medallas', config.mostrar_medallas)
            config.notificaciones_logros = data.get('notificaciones_logros', config.notificaciones_logros)
            config.musica_fondo = data.get('musica_fondo', config.musica_fondo)
            
        elif tipo == 'accesibilidad':
            config.navegacion_teclado = data.get('navegacion_teclado', config.navegacion_teclado)
            config.lectores_pantalla = data.get('lectores_pantalla', config.lectores_pantalla)
            config.zoom_habilitado = data.get('zoom_habilitado', config.zoom_habilitado)
            config.modo_dalto_nico = data.get('modo_dalto_nico', config.modo_dalto_nico)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Configuración guardada exitosamente',
            'config': config.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al guardar configuración: {str(e)}'}), 500

@configuracion_bp.route('/api/cargar')
@login_required
def api_cargar_configuracion():
    """API para cargar configuración"""
    try:
        nino_id = get_current_nino_id()
        if not nino_id:
            return jsonify({'error': 'No se pudo encontrar el perfil del niño'}), 400
        
        config = ConfiguracionUsuario.query.filter_by(nino_id=nino_id, activa=True).first()
        if not config:
            # Crear configuración por defecto
            config = ConfiguracionUsuario(nino_id=nino_id)
            db.session.add(config)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'config': config.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al cargar configuración: {str(e)}'}), 500

@configuracion_bp.route('/api/guardar-unificada', methods=['POST'])
@padres_only
def api_guardar_configuracion_unificada():
    """API para guardar configuración unificada"""
    try:
        nino_id = get_current_nino_id()
        if not nino_id:
            return jsonify({'error': 'No se pudo encontrar el perfil del niño'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        # Obtener o crear configuración
        config = ConfiguracionUsuario.query.filter_by(nino_id=nino_id, activa=True).first()
        if not config:
            config = ConfiguracionUsuario(nino_id=nino_id)
            db.session.add(config)
        
        # Actualizar configuración unificada
        if 'colores' in data:
            config.color_primario = data['colores'].get('color_primario', config.color_primario)
            config.color_secundario = data['colores'].get('color_secundario', config.color_secundario)
            config.modo_alto_contraste = data['colores'].get('modo_alto_contraste', config.modo_alto_contraste)
            
        if 'dificultad' in data:
            config.nivel_dificultad_global = data['dificultad'].get('nivel_dificultad_global', config.nivel_dificultad_global)
            config.tiempo_por_actividad = data['dificultad'].get('tiempo_por_actividad', config.tiempo_por_actividad)
            config.pausas_automaticas = data['dificultad'].get('pausas_automaticas', config.pausas_automaticas)
            config.tiempo_pausa = data['dificultad'].get('tiempo_pausa', config.tiempo_pausa)
            
        if 'voz' in data:
            config.velocidad_voz = data['voz'].get('velocidad', config.velocidad_voz)
            config.tono_voz = data['voz'].get('tono', config.tono_voz)
            config.volumen_voz = data['voz'].get('volumen', config.volumen_voz)
            
        if 'avatar' in data:
            config.avatar_preferido = data['avatar'].get('avatar_preferido', config.avatar_preferido)
            config.mostrar_puntos = data['avatar'].get('mostrar_puntos', config.mostrar_puntos)
            config.mostrar_medallas = data['avatar'].get('mostrar_medallas', config.mostrar_medallas)
            config.notificaciones_logros = data['avatar'].get('notificaciones_logros', config.notificaciones_logros)
            
        if 'accesibilidad' in data:
            config.navegacion_teclado = data['accesibilidad'].get('navegacion_teclado', config.navegacion_teclado)
            config.lectores_pantalla = data['accesibilidad'].get('lectores_pantalla', config.lectores_pantalla)
            config.zoom_habilitado = data['accesibilidad'].get('zoom_habilitado', config.zoom_habilitado)
            config.modo_dalto_nico = data['accesibilidad'].get('modo_daltonico', config.modo_dalto_nico)
            
        if 'interfaz' in data:
            config.tamaño_fuente = data['interfaz'].get('tamaño_fuente', config.tamaño_fuente)
            config.animaciones_habilitadas = data['interfaz'].get('animaciones_habilitadas', config.animaciones_habilitadas)
            config.sonidos_habilitados = data['interfaz'].get('sonidos_habilitados', config.sonidos_habilitados)
            config.musica_fondo = data['interfaz'].get('musica_fondo', config.musica_fondo)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Configuración unificada guardada exitosamente',
            'config': config.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al guardar configuración: {str(e)}'}), 500

@configuracion_bp.route('/api/reset', methods=['POST'])
@padres_only
def api_reset_configuracion():
    """API para resetear configuración a valores por defecto"""
    try:
        nino_id = get_current_nino_id()
        if not nino_id:
            return jsonify({'error': 'No se pudo encontrar el perfil del niño'}), 400
        
        # Eliminar configuración actual
        config = ConfiguracionUsuario.query.filter_by(nino_id=nino_id, activa=True).first()
        if config:
            config.activa = False
            db.session.commit()
        
        # Crear nueva configuración con valores por defecto
        nueva_config = ConfiguracionUsuario(nino_id=nino_id)
        db.session.add(nueva_config)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Configuración reseteada a valores por defecto',
            'config': nueva_config.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al resetear configuración: {str(e)}'}), 500





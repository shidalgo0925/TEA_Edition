# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from app.services.avatar_system import (
    obtener_frase_avatar, 
    obtener_mensaje_diario, 
    obtener_recomendacion_actividad
)

avatar_bp = Blueprint('avatar', __name__, url_prefix='/avatar')

@avatar_bp.route('/frase', methods=['POST'])
def obtener_frase():
    """Obtiene una frase contextual del avatar"""
    try:
        data = request.get_json()
        contexto = data.get('contexto', 'saludo')
        nino_id = data.get('nino_id')
        
        frase = obtener_frase_avatar(contexto, nino_id)
        
        return jsonify({
            'success': True,
            'frase': frase,
            'contexto': contexto
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'frase': '¡Hola! ¿Cómo estás?'
        })

@avatar_bp.route('/mensaje-diario', methods=['POST'])
def obtener_mensaje_diario_api():
    """Obtiene el mensaje diario personalizado del avatar"""
    try:
        data = request.get_json()
        nino_id = data.get('nino_id')
        
        if not nino_id:
            return jsonify({
                'success': False,
                'error': 'ID del niño requerido',
                'mensaje': '¡Hola! ¿Listo para aprender algo nuevo hoy?'
            })
        
        mensaje = obtener_mensaje_diario(nino_id)
        
        return jsonify({
            'success': True,
            'mensaje': mensaje
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'mensaje': '¡Hola! ¿Listo para aprender algo nuevo hoy?'
        })

@avatar_bp.route('/recomendacion', methods=['POST'])
def obtener_recomendacion():
    """Obtiene una recomendación de actividad del avatar"""
    try:
        data = request.get_json()
        nino_id = data.get('nino_id')
        
        if not nino_id:
            return jsonify({
                'success': False,
                'error': 'ID del niño requerido',
                'frase': '¡Vamos a aprender algo nuevo!',
                'categoria': 'lenguaje',
                'porcentaje': 0
            })
        
        recomendacion = obtener_recomendacion_actividad(nino_id)
        
        return jsonify({
            'success': True,
            'frase': recomendacion['frase'],
            'categoria': recomendacion['categoria'],
            'porcentaje': recomendacion['porcentaje']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'frase': '¡Vamos a aprender algo nuevo!',
            'categoria': 'lenguaje',
            'porcentaje': 0
        })

@avatar_bp.route('/estado-emocional', methods=['POST'])
def obtener_estado_emocional():
    """Obtiene el estado emocional del avatar"""
    try:
        from app.services.avatar_system import AvatarSystem
        
        data = request.get_json()
        nino_id = data.get('nino_id')
        
        if not nino_id:
            return jsonify({
                'success': False,
                'error': 'ID del niño requerido',
                'estado': 'motivador',
                'animacion': {
                    'emoji': '💪',
                    'color': '#E74C3C',
                    'animacion': 'glow'
                }
            })
        
        estado = AvatarSystem.obtener_estado_emocional(nino_id)
        animacion = AvatarSystem.generar_animacion_avatar(estado)
        
        return jsonify({
            'success': True,
            'estado': estado,
            'animacion': animacion
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'estado': 'motivador',
            'animacion': {
                'emoji': '💪',
                'color': '#E74C3C',
                'animacion': 'glow'
            }
        })





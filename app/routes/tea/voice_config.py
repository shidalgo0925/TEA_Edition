# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify

voice_config_bp = Blueprint('voice_config', __name__, url_prefix='/voice-config')

@voice_config_bp.route('/')
def voice_config_page():
    """Página de configuración de voz y accesibilidad"""
    return render_template('tea/configuracion_accesibilidad.html')

@voice_config_bp.route('/api/voices')
def api_get_voices():
    """API para obtener voces disponibles"""
    # Datos mock de voces disponibles
    voices = [
        {
            'name': 'Microsoft Maria Desktop - Spanish (Spain)',
            'lang': 'es-ES',
            'gender': 'female',
            'isCurrent': True
        },
        {
            'name': 'Microsoft Helena Desktop - Spanish (Spain)',
            'lang': 'es-ES', 
            'gender': 'female',
            'isCurrent': False
        },
        {
            'name': 'Microsoft Pablo Desktop - Spanish (Spain)',
            'lang': 'es-ES',
            'gender': 'male',
            'isCurrent': False
        },
        {
            'name': 'Google español',
            'lang': 'es-ES',
            'gender': 'female',
            'isCurrent': False
        },
        {
            'name': 'Samantha',
            'lang': 'en-US',
            'gender': 'female',
            'isCurrent': False
        }
    ]
    
    return jsonify(voices)

@voice_config_bp.route('/api/config', methods=['GET', 'POST'])
def api_voice_config():
    """API para obtener/guardar configuración de voz"""
    if request.method == 'GET':
        # Configuración por defecto
        config = {
            'gender': 'female',
            'language': 'es',
            'speed': 0.9,
            'pitch': 1.1,
            'volume': 0.8
        }
        return jsonify(config)
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Validar datos
        config = {
            'gender': data.get('gender', 'female'),
            'language': data.get('language', 'es'),
            'speed': max(0.1, min(2.0, float(data.get('speed', 0.9)))),
            'pitch': max(0.0, min(2.0, float(data.get('pitch', 1.1)))),
            'volume': max(0.0, min(1.0, float(data.get('volume', 0.8))))
        }
        
        # Aquí se guardaría en la base de datos
        # Por ahora solo retornamos confirmación
        
        return jsonify({
            'success': True,
            'message': 'Configuración de voz guardada exitosamente',
            'config': config
        })

@voice_config_bp.route('/api/test-voice', methods=['POST'])
def api_test_voice():
    """API para probar la voz con la configuración actual"""
    data = request.get_json()
    text = data.get('text', 'Hola, esta es una prueba de voz.')
    
    # Retornar confirmación (el audio se maneja en el frontend)
    return jsonify({
        'success': True,
        'message': 'Prueba de voz iniciada',
        'text': text
    })




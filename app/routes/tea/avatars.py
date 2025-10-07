# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from app.models.tea_models import Avatar, AvatarUsuario, UsuarioNino, UsuarioPadre
from app.extensions import db
import json

avatars_bp = Blueprint('avatars', __name__, url_prefix='/avatars')

@avatars_bp.route('/')
def avatares_lista():
    """Página principal de selección de avatares"""
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a los avatares', 'error')
        return redirect(url_for('tea.auth.login'))
    
    # Obtener avatares disponibles
    avatares = Avatar.query.filter_by(activo=True).all()
    
    # Obtener avatar actual del usuario
    avatar_actual = None
    if session.get('user_type') == 'nino':
        avatar_actual = AvatarUsuario.query.filter_by(
            usuario_id=session['user_id'],
            tipo_usuario='nino',
            activo=True
        ).first()
    else:
        avatar_actual = AvatarUsuario.query.filter_by(
            usuario_id=session['user_id'],
            tipo_usuario='padre',
            activo=True
        ).first()
    
    return render_template('tea/avatars/lista_avatars.html', 
                         avatares=avatares, 
                         avatar_actual=avatar_actual)

@avatars_bp.route('/seleccionar/<int:avatar_id>', methods=['POST'])
def seleccionar_avatar(avatar_id):
    """Seleccionar un avatar para el usuario"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'})
    
    # Verificar que el avatar existe
    avatar = Avatar.query.get_or_404(avatar_id)
    if not avatar.activo:
        return jsonify({'success': False, 'message': 'Avatar no disponible'})
    
    try:
        # Desactivar avatar anterior
        AvatarUsuario.query.filter_by(
            usuario_id=session['user_id'],
            tipo_usuario=session['user_type'],
            activo=True
        ).update({'activo': False})
        
        # Crear nueva configuración de avatar
        avatar_usuario = AvatarUsuario(
            usuario_id=session['user_id'],
            tipo_usuario=session['user_type'],
            avatar_id=avatar_id,
            color_preferido=avatar.get_personalidad().get('color_principal', '#E74C3C')
        )
        
        db.session.add(avatar_usuario)
        db.session.commit()
        
        # Actualizar sesión
        session['avatar_id'] = avatar_id
        session['avatar_nombre'] = avatar.nombre
        
        return jsonify({
            'success': True, 
            'message': f'¡Avatar {avatar.nombre} seleccionado exitosamente!',
            'avatar': {
                'id': avatar.id,
                'nombre': avatar.nombre,
                'tipo': avatar.tipo,
                'imagen_url': avatar.imagen_url
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al seleccionar avatar: {str(e)}'})

@avatars_bp.route('/personalizar/<int:avatar_id>')
def personalizar_avatar(avatar_id):
    """Página de personalización de avatar"""
    if 'user_id' not in session:
        flash('Debes iniciar sesión para personalizar avatares', 'error')
        return redirect(url_for('tea.auth.login'))
    
    avatar = Avatar.query.get_or_404(avatar_id)
    
    # Obtener configuración actual del usuario
    avatar_usuario = AvatarUsuario.query.filter_by(
        usuario_id=session['user_id'],
        tipo_usuario=session['user_type'],
        avatar_id=avatar_id,
        activo=True
    ).first()
    
    return render_template('tea/avatars/personalizar_avatar.html', 
                         avatar=avatar, 
                         avatar_usuario=avatar_usuario)

@avatars_bp.route('/guardar-personalizacion/<int:avatar_id>', methods=['POST'])
def guardar_personalizacion(avatar_id):
    """Guardar personalización del avatar"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'})
    
    try:
        data = request.get_json()
        
        # Obtener o crear configuración de avatar
        avatar_usuario = AvatarUsuario.query.filter_by(
            usuario_id=session['user_id'],
            tipo_usuario=session['user_type'],
            avatar_id=avatar_id,
            activo=True
        ).first()
        
        if not avatar_usuario:
            avatar_usuario = AvatarUsuario(
                usuario_id=session['user_id'],
                tipo_usuario=session['user_type'],
                avatar_id=avatar_id
            )
            db.session.add(avatar_usuario)
        
        # Actualizar configuración
        avatar_usuario.color_preferido = data.get('color_preferido', '#E74C3C')
        avatar_usuario.velocidad_voz = float(data.get('velocidad_voz', 0.9))
        avatar_usuario.tono_voz = float(data.get('tono_voz', 1.1))
        avatar_usuario.volumen_voz = float(data.get('volumen_voz', 0.8))
        
        # Guardar frases personalizadas
        if 'frases_personalizadas' in data:
            avatar_usuario.set_frases_personalizadas(data['frases_personalizadas'])
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Personalización guardada exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al guardar: {str(e)}'})

@avatars_bp.route('/hablar/<int:avatar_id>', methods=['POST'])
def hablar_avatar(avatar_id):
    """Hacer que el avatar hable"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'})
    
    try:
        data = request.get_json()
        texto = data.get('texto', '')
        
        if not texto:
            return jsonify({'success': False, 'message': 'No se proporcionó texto'})
        
        # Obtener configuración del avatar
        avatar_usuario = AvatarUsuario.query.filter_by(
            usuario_id=session['user_id'],
            tipo_usuario=session['user_type'],
            avatar_id=avatar_id,
            activo=True
        ).first()
        
        if not avatar_usuario:
            return jsonify({'success': False, 'message': 'Avatar no configurado'})
        
        # Configuración de voz
        config_voz = {
            'velocidad': avatar_usuario.velocidad_voz,
            'tono': avatar_usuario.tono_voz,
            'volumen': avatar_usuario.volumen_voz,
            'voz': avatar_usuario.avatar.audio_voice
        }
        
        return jsonify({
            'success': True,
            'texto': texto,
            'config_voz': config_voz,
            'avatar_nombre': avatar_usuario.avatar.nombre
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al procesar voz: {str(e)}'})

@avatars_bp.route('/frase-motivacional/<int:avatar_id>')
def frase_motivacional(avatar_id):
    """Obtener una frase motivacional del avatar"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'})
    
    try:
        avatar = Avatar.query.get_or_404(avatar_id)
        frases = avatar.get_frases()
        
        if not frases:
            return jsonify({'success': False, 'message': 'No hay frases disponibles'})
        
        import random
        frase = random.choice(frases)
        
        return jsonify({
            'success': True,
            'frase': frase,
            'avatar_nombre': avatar.nombre
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al obtener frase: {str(e)}'})

@avatars_bp.route('/avatar-actual')
def avatar_actual():
    """Obtener el avatar actual del usuario"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'No autorizado'})
    
    try:
        avatar_usuario = AvatarUsuario.query.filter_by(
            usuario_id=session['user_id'],
            tipo_usuario=session['user_type'],
            activo=True
        ).first()
        
        if not avatar_usuario:
            return jsonify({'success': False, 'message': 'No hay avatar seleccionado'})
        
        avatar = avatar_usuario.avatar
        
        return jsonify({
            'success': True,
            'avatar': {
                'id': avatar.id,
                'nombre': avatar.nombre,
                'tipo': avatar.tipo,
                'imagen_url': avatar.imagen_url,
                'personalidad': avatar.get_personalidad(),
                'frases': avatar.get_frases(),
                'configuracion': {
                    'color_preferido': avatar_usuario.color_preferido,
                    'velocidad_voz': avatar_usuario.velocidad_voz,
                    'tono_voz': avatar_usuario.tono_voz,
                    'volumen_voz': avatar_usuario.volumen_voz
                }
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al obtener avatar: {str(e)}'})

# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
from app.models.tea_models import UsuarioPadre, UsuarioNino, PerfilNino, SesionUsuario
from app import db
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'user_type' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'info')
            return redirect(url_for('tea.auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Obtener el usuario actual desde la sesión"""
    if 'user_id' not in session or 'user_type' not in session:
        return None
    
    user_id = session['user_id']
    user_type = session['user_type']
    
    if user_type == 'padre':
        return UsuarioPadre.query.get(user_id)
    elif user_type == 'nino':
        return UsuarioNino.query.get(user_id)
    return None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login para padres y niños"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        tipo_usuario = request.form.get('tipo_usuario', 'padre')
        
        if tipo_usuario == 'padre':
            user = UsuarioPadre.query.filter_by(email=email, activo=True).first()
        else:
            user = UsuarioNino.query.filter_by(nombre_usuario=email, activo=True).first()
        
        if user and user.check_password(password):
            # Actualizar último acceso
            user.ultimo_acceso = datetime.utcnow()
            db.session.commit()
            
            # Crear sesión
            sesion = SesionUsuario(
                usuario_id=user.id,
                tipo_usuario=tipo_usuario,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(sesion)
            db.session.commit()
            
            # Guardar ID de sesión
            session['sesion_id'] = sesion.id
            
            # Guardar en sesión
            session['user_id'] = user.id
            session['user_type'] = tipo_usuario
            session['user_name'] = user.nombre if hasattr(user, 'nombre') else user.nombre_usuario
            
            # Redirigir según tipo de usuario
            if tipo_usuario == 'padre':
                return redirect(url_for('tea.padres.dashboard'))
            else:
                return redirect(url_for('tea.nino.dashboard'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
    
    return render_template('tea/auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos usuarios padres"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        telefono = request.form.get('telefono')
        relacion_nino = request.form.get('relacion_nino', 'padre')
        
        # Validaciones
        if not all([nombre, email, password, confirm_password]):
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('tea/auth/register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('tea/auth/register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('tea/auth/register.html')
        
        # Verificar si el email ya existe
        if UsuarioPadre.query.filter_by(email=email).first():
            flash('Este email ya está registrado.', 'error')
            return render_template('tea/auth/register.html')
        
        # Crear nuevo usuario
        nuevo_usuario = UsuarioPadre(
            nombre=nombre,
            email=email,
            telefono=telefono,
            relacion_nino=relacion_nino
        )
        nuevo_usuario.set_password(password)
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('tea.auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la cuenta. Inténtalo de nuevo.', 'error')
    
    return render_template('tea/auth/register.html')

@auth_bp.route('/register-child', methods=['GET', 'POST'])
@login_required
def register_child():
    """Registro de perfil de niño (solo para padres autenticados)"""
    current_user = get_current_user()
    if not current_user or session.get('user_type') != 'padre':
        flash('Solo los padres pueden registrar niños.', 'error')
        return redirect(url_for('tea.index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        edad = request.form.get('edad')
        nivel_dificultad = request.form.get('nivel_dificultad', 'basico')
        tiempo_sesion = request.form.get('tiempo_sesion', 15)
        avatar_preferido = request.form.get('avatar_preferido', 'maestra_ana')
        nombre_usuario = request.form.get('nombre_usuario')
        password_nino = request.form.get('password_nino')
        
        # Validaciones
        if not all([nombre, edad, nombre_usuario, password_nino]):
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('tea/auth/register_child.html')
        
        if len(password_nino) < 4:
            flash('La contraseña del niño debe tener al menos 4 caracteres.', 'error')
            return render_template('tea/auth/register_child.html')
        
        # Verificar si el nombre de usuario ya existe
        if UsuarioNino.query.filter_by(nombre_usuario=nombre_usuario).first():
            flash('Este nombre de usuario ya está en uso.', 'error')
            return render_template('tea/auth/register_child.html')
        
        try:
            # Crear perfil del niño
            perfil_nino = PerfilNino(
                nombre=nombre,
                edad=int(edad),
                nivel_dificultad=nivel_dificultad,
                tiempo_sesion_min=int(tiempo_sesion),
                avatar_preferido=avatar_preferido,
                padre_id=current_user.id
            )
            db.session.add(perfil_nino)
            db.session.flush()  # Para obtener el ID
            
            # Crear usuario del niño
            usuario_nino = UsuarioNino(
                nombre_usuario=nombre_usuario,
                perfil_nino_id=perfil_nino.id
            )
            usuario_nino.set_password(password_nino)
            db.session.add(usuario_nino)
            
            db.session.commit()
            flash(f'¡Perfil de {nombre} creado exitosamente!', 'success')
            return redirect(url_for('tea.padres.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el perfil del niño. Inténtalo de nuevo.', 'error')
    
    return render_template('tea/auth/register_child.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Cerrar sesión"""
    try:
        # Marcar sesión como inactiva
        if 'sesion_id' in session:
            sesion = SesionUsuario.query.get(session['sesion_id'])
            if sesion:
                sesion.fin_sesion = datetime.utcnow()
                sesion.activa = False
                db.session.commit()
        
        session.clear()
        
        # Si es una petición AJAX, devolver JSON
        if request.method == 'POST':
            return jsonify({
                'success': True,
                'message': 'Sesión cerrada exitosamente',
                'redirect': url_for('tea.index')
            })
        
        # Si es GET, redirigir normalmente
        flash('Has cerrado sesión exitosamente.', 'info')
        return redirect(url_for('tea.index'))
        
    except Exception as e:
        if request.method == 'POST':
            return jsonify({'error': str(e)}), 500
        flash('Error al cerrar sesión.', 'error')
        return redirect(url_for('tea.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """Perfil del usuario actual"""
    current_user = get_current_user()
    if session.get('user_type') == 'padre':
        return render_template('tea/auth/profile_padre.html', usuario=current_user)
    else:
        return render_template('tea/auth/profile_nino.html', usuario=current_user)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Cambiar contraseña"""
    current_user = get_current_user()
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('La contraseña actual es incorrecta.', 'error')
            return render_template('tea/auth/change_password.html')
        
        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden.', 'error')
            return render_template('tea/auth/change_password.html')
        
        if len(new_password) < 6:
            flash('La nueva contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('tea/auth/change_password.html')
        
        current_user.set_password(new_password)
        db.session.commit()
        flash('Contraseña actualizada exitosamente.', 'success')
        return redirect(url_for('tea.auth.profile'))
    
    return render_template('tea/auth/change_password.html')

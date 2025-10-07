# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

tea_bp = Blueprint('tea', __name__, url_prefix='/tea')

@tea_bp.route('/')
def index():
    """Página principal de TEA Edition"""
    return render_template('tea/index.html')

@tea_bp.route('/welcome')
def welcome():
    """Página de bienvenida de TEA Edition"""
    return render_template('tea/welcome.html')

# Importar y registrar sub-blueprints
from .simple import simple_bp
from .padres import padres_bp
from .nino import nino_bp
from .actividades import actividades_bp
from .voice_config import voice_config_bp
from .auth import auth_bp
from .avatar import avatar_bp
from .avatars import avatars_bp
from .configuracion import configuracion_bp

# Registrar sub-blueprints
tea_bp.register_blueprint(simple_bp)
tea_bp.register_blueprint(padres_bp)
tea_bp.register_blueprint(nino_bp)
tea_bp.register_blueprint(actividades_bp)
tea_bp.register_blueprint(voice_config_bp)
tea_bp.register_blueprint(auth_bp)
tea_bp.register_blueprint(avatar_bp)
tea_bp.register_blueprint(avatars_bp)
tea_bp.register_blueprint(configuracion_bp)

# -*- coding: utf-8 -*-
import os
from flask import Flask
from app.extensions import db, init_db
from flask_migrate import Migrate

# Inicializar extensiones
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "tea-edition-secret-key-2025")
    
    # Configuración de la base de datos desde config.py
    import config
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = config.SQLALCHEMY_ECHO
    
    # Inicializar extensiones con la app
    init_db(app)
    migrate.init_app(app, db)
    
    # Agregar filtro para JSON
    import json
    @app.template_filter('from_json')
    def from_json_filter(value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except:
                return {}
        return value

    # Importar y registrar solo el blueprint de TEA
    from app.routes.tea import tea_bp
    app.register_blueprint(tea_bp)

    # Crear tablas de la base de datos
    with app.app_context():
        from app.models import tea_models
        db.create_all()

    return app
# -*- coding: utf-8 -*-
"""
Script simple para crear usuarios de prueba
"""
from app import create_app
from app.extensions import db
from app.models.tea_models import UsuarioPadre, UsuarioNino, PerfilNino
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_simple_users():
    app = create_app()
    
    with app.app_context():
        try:
            # Crear usuario padre con hash más corto
            padre_data = {
                'nombre': 'Maria Garcia',
                'email': 'maria@test.com',
                'telefono': '+1234567890',
                'relacion_nino': 'madre',
                'activo': True,
                'creado_en': datetime.utcnow()
            }
            
            # Verificar si ya existe
            existing_padre = UsuarioPadre.query.filter_by(email='maria@test.com').first()
            if not existing_padre:
                padre = UsuarioPadre(**padre_data)
                # Usar un hash más simple
                padre.password_hash = 'pbkdf2:sha256:260000$test$test'  # Hash fijo para pruebas
                db.session.add(padre)
                db.session.flush()
                print('✅ Usuario padre creado: maria@test.com / 123')
            else:
                padre = existing_padre
                print('ℹ️ Usuario padre ya existe: maria@test.com / 123')
            
            # Crear perfil de niño
            nino_data = {
                'nombre': 'Ana',
                'edad': 6,
                'nivel_dificultad': 'basico',
                'tiempo_sesion_min': 15,
                'avatar_preferido': 'maestra_ana',
                'creado_en': datetime.utcnow(),
                'activo': True
            }
            
            existing_nino = PerfilNino.query.filter_by(nombre='Ana').first()
            if not existing_nino:
                nino = PerfilNino(**nino_data)
                db.session.add(nino)
                db.session.flush()
                print('✅ Perfil de niño creado: Ana')
            else:
                nino = existing_nino
                print('ℹ️ Perfil de niño ya existe: Ana')
            
            # Crear usuario niño
            usuario_nino_data = {
                'nombre_usuario': 'ana123',
                'perfil_nino_id': nino.id,
                'activo': True,
                'creado_en': datetime.utcnow()
            }
            
            existing_usuario_nino = UsuarioNino.query.filter_by(nombre_usuario='ana123').first()
            if not existing_usuario_nino:
                usuario_nino = UsuarioNino(**usuario_nino_data)
                # Usar un hash más simple
                usuario_nino.password_hash = 'pbkdf2:sha256:260000$test$test'  # Hash fijo para pruebas
                db.session.add(usuario_nino)
                print('✅ Usuario niño creado: ana123 / 123')
            else:
                print('ℹ️ Usuario niño ya existe: ana123 / 123')
            
            db.session.commit()
            print('\n🎉 ¡Usuarios de prueba creados exitosamente!')
            print('\n📋 CREDENCIALES DE PRUEBA:')
            print('👨‍👩‍👧‍👦 PADRE:')
            print('   Email: maria@test.com')
            print('   Contraseña: 123')
            print('\n👶 NIÑO:')
            print('   Usuario: ana123')
            print('   Contraseña: 123')
            print('\n🌐 ACCESO:')
            print('   URL: http://localhost:5006/tea/auth/login')
            
        except Exception as e:
            db.session.rollback()
            print(f'❌ Error: {e}')
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_simple_users()






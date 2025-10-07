# -*- coding: utf-8 -*-
"""
Script para crear usuarios de prueba para TEA Edition
"""
from app import create_app
from app.extensions import db
from app.models.tea_models import (
    UsuarioPadre, UsuarioNino, PerfilNino, 
    ActividadTEA, RecompensaTEA, ProgresoTEA
)
import json

def create_test_users():
    app = create_app()
    
    with app.app_context():
        try:
            # Crear usuario padre de prueba
            padre = UsuarioPadre(
                nombre="María García",
                email="maria@test.com",
                telefono="+1234567890",
                relacion_nino="madre"
            )
            padre.set_password("123")
            
            # Verificar si ya existe
            if not UsuarioPadre.query.filter_by(email="maria@test.com").first():
                db.session.add(padre)
                db.session.flush()  # Para obtener el ID
                print("✅ Usuario padre creado: maria@test.com / 123")
            else:
                padre = UsuarioPadre.query.filter_by(email="maria@test.com").first()
                print("ℹ️ Usuario padre ya existe: maria@test.com / 123")
            
            # Crear perfil de niño
            nino = PerfilNino(
                nombre="Ana",
                edad=6,
                nivel_dificultad="basico",
                tiempo_sesion_min=15,
                avatar_preferido="maestra_ana"
            )
            
            # Verificar si ya existe
            if not PerfilNino.query.filter_by(nombre="Ana").first():
                db.session.add(nino)
                db.session.flush()  # Para obtener el ID
                print("✅ Perfil de niño creado: Ana")
            else:
                nino = PerfilNino.query.filter_by(nombre="Ana").first()
                print("ℹ️ Perfil de niño ya existe: Ana")
            
            # Crear usuario niño
            usuario_nino = UsuarioNino(
                nombre_usuario="ana123",
                perfil_nino_id=nino.id
            )
            usuario_nino.set_password("123")
            
            # Verificar si ya existe
            if not UsuarioNino.query.filter_by(nombre_usuario="ana123").first():
                db.session.add(usuario_nino)
                print("✅ Usuario niño creado: ana123 / 123")
            else:
                print("ℹ️ Usuario niño ya existe: ana123 / 123")
            
            # Crear actividades básicas si no existen
            actividades_data = [
                {
                    "titulo": "Repetir Palabras",
                    "descripcion": "Imita las palabras que dice la maestra",
                    "tipo": "imitacion",
                    "nivel_dificultad": "basico",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "palabras": ["mamá", "papá", "agua", "casa", "perro"],
                        "instrucciones": "Repite la palabra que escuches"
                    }),
                    "puntos_recompensa": 10,
                    "tiempo_estimado": 5
                },
                {
                    "titulo": "Contar del 1 al 5",
                    "descripcion": "Aprende a contar números básicos",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "basico",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": [1, 2, 3, 4, 5],
                        "instrucciones": "Cuenta los objetos que veas"
                    }),
                    "puntos_recompensa": 15,
                    "tiempo_estimado": 7
                },
                {
                    "titulo": "Colores Básicos",
                    "descripcion": "Reconoce los colores principales",
                    "tipo": "asociacion",
                    "nivel_dificultad": "basico",
                    "categoria": "colores",
                    "contenido": json.dumps({
                        "colores": ["rojo", "azul", "amarillo", "verde"],
                        "instrucciones": "Señala el color que te pida"
                    }),
                    "puntos_recompensa": 12,
                    "tiempo_estimado": 6
                },
                {
                    "titulo": "Sonidos de Animales",
                    "descripcion": "Asocia animales con sus sonidos",
                    "tipo": "asociacion",
                    "nivel_dificultad": "basico",
                    "categoria": "animales",
                    "contenido": json.dumps({
                        "animales": [
                            {"nombre": "perro", "sonido": "guau guau"},
                            {"nombre": "gato", "sonido": "miau"},
                            {"nombre": "vaca", "sonido": "muu"},
                            {"nombre": "pollo", "sonido": "pío pío"}
                        ],
                        "instrucciones": "Escucha el sonido y di qué animal es"
                    }),
                    "puntos_recompensa": 15,
                    "tiempo_estimado": 8
                }
            ]
            
            for act_data in actividades_data:
                if not ActividadTEA.query.filter_by(titulo=act_data["titulo"]).first():
                    actividad = ActividadTEA(**act_data)
                    db.session.add(actividad)
                    print(f"✅ Actividad creada: {act_data['titulo']}")
                else:
                    print(f"ℹ️ Actividad ya existe: {act_data['titulo']}")
            
            # Crear recompensas básicas
            recompensas_data = [
                {
                    "nombre": "Primera Estrella",
                    "descripcion": "¡Completaste tu primera actividad!",
                    "tipo": "estrella",
                    "icono_url": "⭐",
                    "puntos_requeridos": 10,
                    "categoria": "diario"
                },
                {
                    "nombre": "Super Aprendiz",
                    "descripcion": "Completaste 5 actividades en un día",
                    "tipo": "badge",
                    "icono_url": "🏆",
                    "puntos_requeridos": 50,
                    "categoria": "diario"
                },
                {
                    "nombre": "Racha de 7 Días",
                    "descripcion": "¡Aprendiste 7 días seguidos!",
                    "tipo": "badge",
                    "icono_url": "🔥",
                    "puntos_requeridos": 200,
                    "categoria": "semanal"
                },
                {
                    "nombre": "Maestro de Colores",
                    "descripcion": "Dominaste todos los colores",
                    "tipo": "sticker",
                    "icono_url": "🎨",
                    "puntos_requeridos": 100,
                    "categoria": "especial"
                }
            ]
            
            for rec_data in recompensas_data:
                if not RecompensaTEA.query.filter_by(nombre=rec_data["nombre"]).first():
                    recompensa = RecompensaTEA(**rec_data)
                    db.session.add(recompensa)
                    print(f"✅ Recompensa creada: {rec_data['nombre']}")
                else:
                    print(f"ℹ️ Recompensa ya existe: {rec_data['nombre']}")
            
            # Crear progreso inicial
            if not ProgresoTEA.query.filter_by(nino_id=nino.id).first():
                progreso = ProgresoTEA(
                    nino_id=nino.id,
                    habilidad="lenguaje",
                    nivel_actual="basico",
                    puntos_totales=0,
                    sesiones_completadas=0,
                    racha_dias=0
                )
                db.session.add(progreso)
                print("✅ Progreso inicial creado")
            else:
                print("ℹ️ Progreso inicial ya existe")
            
            db.session.commit()
            print("\n🎉 ¡Usuarios de prueba creados exitosamente!")
            print("\n📋 CREDENCIALES DE PRUEBA:")
            print("👨‍👩‍👧‍👦 PADRE:")
            print("   Email: maria@test.com")
            print("   Contraseña: 123")
            print("\n👶 NIÑO:")
            print("   Usuario: ana123")
            print("   Contraseña: 123")
            print("\n🌐 ACCESO:")
            print("   URL: http://localhost:5006/tea/auth/login")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al crear usuarios: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_test_users()

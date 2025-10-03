# -*- coding: utf-8 -*-
"""
Script simplificado para crear datos de prueba
"""
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.insert(0, '/home/easytechservices25/tea_edition')

from app import create_app
from app.extensions import db
from app.models.tea_models import PerfilNino, ActividadTEA, RecompensaTEA, ProgresoTEA
import json

def create_test_data():
    app = create_app()
    
    with app.app_context():
        try:
            # Crear perfil de niño
            nino = PerfilNino(
                nombre="Ana",
                edad=6,
                nivel_dificultad="basico",
                tiempo_sesion_min=15,
                avatar_preferido="maestra_ana"
            )
            db.session.add(nino)
            db.session.commit()
            print("✅ Perfil de niño creado")
            
            # Crear actividad básica
            actividad = ActividadTEA(
                titulo="Repetir Palabras",
                descripcion="Imita las palabras que dice la maestra",
                tipo="imitacion",
                nivel_dificultad="basico",
                categoria="lenguaje",
                contenido=json.dumps({
                    "palabras": ["mamá", "papá", "agua", "casa"],
                    "instrucciones": "Repite la palabra que escuches"
                }),
                puntos_recompensa=10,
                tiempo_estimado=5
            )
            db.session.add(actividad)
            
            # Crear recompensa
            recompensa = RecompensaTEA(
                nombre="Primera Estrella",
                descripcion="¡Completaste tu primera actividad!",
                tipo="estrella",
                icono_url="⭐",
                puntos_requeridos=10,
                categoria="diario"
            )
            db.session.add(recompensa)
            
            # Crear progreso
            progreso = ProgresoTEA(
                nino_id=nino.id,
                habilidad="lenguaje",
                nivel_actual="basico",
                puntos_totales=0,
                sesiones_completadas=0,
                racha_dias=0
            )
            db.session.add(progreso)
            
            db.session.commit()
            print("✅ Datos de prueba creados exitosamente!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == "__main__":
    create_test_data()






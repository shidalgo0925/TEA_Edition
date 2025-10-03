# -*- coding: utf-8 -*-
"""
Script para crear datos de prueba para TEA Edition
"""
from app import create_app
from app.extensions import db
from app.models.tea_models import (
    PerfilNino, ActividadTEA, RecompensaTEA, 
    ProgresoTEA, SesionTEA
)
import json

def create_sample_data():
    app = create_app()
    
    with app.app_context():
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
        
        # Crear actividades básicas
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
            actividad = ActividadTEA(**act_data)
            db.session.add(actividad)
        
        # Crear recompensas
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
            recompensa = RecompensaTEA(**rec_data)
            db.session.add(recompensa)
        
        # Crear progreso inicial
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
        print(f"👶 Niño: {nino.nombre}")
        print(f"🎯 Actividades: {len(actividades_data)}")
        print(f"🏆 Recompensas: {len(recompensas_data)}")

if __name__ == "__main__":
    create_sample_data()






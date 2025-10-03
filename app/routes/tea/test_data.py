# -*- coding: utf-8 -*-
"""
Crear datos de prueba directamente en las rutas
"""
from app.extensions import db
from app.models.tea_models import PerfilNino, ActividadTEA, RecompensaTEA, ProgresoTEA
import json

def ensure_test_data():
    """Asegurar que existan datos de prueba"""
    try:
        # Verificar si ya existe un perfil
        nino = PerfilNino.query.first()
        if not nino:
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
        
        # Verificar si ya existe una actividad
        actividad = ActividadTEA.query.first()
        if not actividad:
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
            db.session.commit()
            print("✅ Actividad creada")
        
        # Verificar si ya existe una recompensa
        recompensa = RecompensaTEA.query.first()
        if not recompensa:
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
            db.session.commit()
            print("✅ Recompensa creada")
        
        # Verificar si ya existe progreso
        progreso = ProgresoTEA.query.first()
        if not progreso:
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
            print("✅ Progreso creado")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos: {e}")
        db.session.rollback()
        return False






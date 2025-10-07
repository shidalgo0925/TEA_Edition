#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar datos de progreso de prueba en TEA Edition
Permite ver el sistema de progreso visual funcionando
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.tea_models import (
    PerfilNino, ActividadTEA, SesionTEA, SesionActividad, 
    ProgresoUsuario, MedallaUsuario
)
from app.services.user_progress import UserProgressSystem
from datetime import datetime, timedelta
import random

def create_progress_data():
    """Crea datos de progreso de prueba"""
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener o crear el perfil del niño
            nino = PerfilNino.query.first()
            if not nino:
                nino = PerfilNino(
                    nombre="Ana",
                    edad=6,
                    nivel_dificultad="basico",
                    tiempo_sesion_min=15,
                    avatar_preferido="maestra_ana"
                )
                db.session.add(nino)
                db.session.commit()
                print(f"✅ Creado perfil del niño: {nino.nombre}")
            else:
                print(f"✅ Usando perfil existente: {nino.nombre}")
            
            # Obtener actividades existentes
            actividades = ActividadTEA.query.all()
            if not actividades:
                print("❌ No hay actividades disponibles. Ejecuta primero el script de datos de prueba.")
                return
            
            print(f"✅ Encontradas {len(actividades)} actividades")
            
            # Crear sesiones de los últimos 5 días
            sesiones_creadas = []
            for i in range(5):
                fecha = datetime.utcnow() - timedelta(days=i)
                
                # Crear sesión
                sesion = SesionTEA(
                    nino_id=nino.id,
                    fecha=fecha,
                    duracion_minutos=random.randint(10, 25),
                    actividades_completadas=0,
                    puntos_ganados=0,
                    estado='completada'
                )
                db.session.add(sesion)
                db.session.flush()  # Para obtener el ID
                
                # Completar algunas actividades en cada sesión
                actividades_sesion = random.sample(actividades, random.randint(2, 5))
                puntos_sesion = 0
                
                for j, actividad in enumerate(actividades_sesion):
                    puntos_actividad = random.randint(5, 15)
                    
                    sesion_actividad = SesionActividad(
                        sesion_id=sesion.id,
                        actividad_id=actividad.id,
                        orden=j + 1,
                        completada=True,
                        intentos=random.randint(1, 3),
                        tiempo_dedicado=random.randint(30, 120),
                        puntos_obtenidos=puntos_actividad,
                        feedback="¡Muy bien!",
                        fecha_completada=fecha
                    )
                    db.session.add(sesion_actividad)
                    puntos_sesion += puntos_actividad
                    
                    # Actualizar progreso usando el sistema
                    UserProgressSystem.actualizar_progreso_actividad(
                        nino.id, actividad.id, puntos_actividad
                    )
                
                # Actualizar sesión
                sesion.actividades_completadas = len(actividades_sesion)
                sesion.puntos_ganados = puntos_sesion
                sesiones_creadas.append(sesion)
                
                print(f"✅ Creada sesión del {fecha.strftime('%Y-%m-%d')} con {len(actividades_sesion)} actividades")
            
            db.session.commit()
            
            # Mostrar estadísticas finales
            print("\n📊 ESTADÍSTICAS GENERADAS:")
            estadisticas = UserProgressSystem.obtener_estadisticas_dashboard(nino.id)
            
            print(f"   Puntos totales: {estadisticas['puntos_totales']}")
            print(f"   Actividades completadas: {estadisticas['actividades_completadas']}")
            print(f"   Días consecutivos: {estadisticas['dias_consecutivos']}")
            print(f"   Nivel general: {estadisticas['nivel_general']}")
            print(f"   Medallas obtenidas: {estadisticas['medallas_obtenidas']}")
            
            print("\n📈 PROGRESO POR CATEGORÍA:")
            for categoria, progreso in estadisticas['progreso_por_categoria'].items():
                print(f"   {categoria.capitalize()}: {progreso['actividades_completadas']}/{progreso['actividades_totales']} "
                      f"({progreso['porcentaje_completado']:.1f}%) - {progreso['nivel_actual']}")
            
            print(f"\n🎉 ¡Datos de progreso generados exitosamente!")
            print(f"   Visita: http://localhost:5006/tea/nino/ para ver el progreso visual")
            
        except Exception as e:
            print(f"❌ Error generando datos: {e}")
            db.session.rollback()

def clear_progress_data():
    """Limpia los datos de progreso existentes"""
    app = create_app()
    
    with app.app_context():
        try:
            # Limpiar datos de progreso
            SesionActividad.query.delete()
            SesionTEA.query.delete()
            ProgresoUsuario.query.delete()
            MedallaUsuario.query.delete()
            
            # Resetear perfil del niño
            nino = PerfilNino.query.first()
            if nino:
                nino.puntos_totales_acumulados = 0
                nino.actividades_completadas_total = 0
                nino.dias_consecutivos = 0
                nino.fecha_ultima_actividad = None
            
            db.session.commit()
            print("✅ Datos de progreso limpiados")
            
        except Exception as e:
            print(f"❌ Error limpiando datos: {e}")
            db.session.rollback()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_progress_data()
    else:
        create_progress_data()





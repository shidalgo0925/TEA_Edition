#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar la base de datos con el sistema de progreso real del usuario
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.tea_models import PerfilNino, ProgresoUsuario, MedallaUsuario
from sqlalchemy import text

def update_database():
    """Actualiza la base de datos con las nuevas tablas de progreso"""
    app = create_app()
    
    with app.app_context():
        try:
            # Crear tabla progreso_usuario
            print("Creando tabla progreso_usuario...")
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS progreso_usuario (
                    id SERIAL PRIMARY KEY,
                    nino_id INTEGER NOT NULL REFERENCES perfil_nino(id),
                    categoria VARCHAR(50) NOT NULL,
                    nivel_actual VARCHAR(20) DEFAULT 'inicial',
                    actividades_completadas INTEGER DEFAULT 0,
                    actividades_totales INTEGER DEFAULT 0,
                    puntos_categoria INTEGER DEFAULT 0,
                    ultima_actividad_id INTEGER REFERENCES actividades_tea(id),
                    fecha_ultima_actividad TIMESTAMP,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Crear tabla medalla_usuario
            print("Creando tabla medalla_usuario...")
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS medalla_usuario (
                    id SERIAL PRIMARY KEY,
                    nino_id INTEGER NOT NULL REFERENCES perfil_nino(id),
                    tipo_medalla VARCHAR(50) NOT NULL,
                    categoria VARCHAR(50),
                    titulo VARCHAR(100) NOT NULL,
                    descripcion TEXT,
                    icono VARCHAR(100) DEFAULT '🏆',
                    puntos_requeridos INTEGER DEFAULT 0,
                    fecha_obtenida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    visible BOOLEAN DEFAULT TRUE
                )
            """))
            
            # Crear índices para mejor rendimiento
            print("Creando índices...")
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_progreso_usuario_nino_categoria 
                ON progreso_usuario(nino_id, categoria)
            """))
            
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_medalla_usuario_nino 
                ON medalla_usuario(nino_id)
            """))
            
            db.session.commit()
            print("✅ Base de datos actualizada correctamente")
            
            # Inicializar progreso para usuarios existentes
            print("Inicializando progreso para usuarios existentes...")
            ninos = PerfilNino.query.filter_by(activo=True).all()
            
            for nino in ninos:
                categorias = ['lenguaje', 'numeros', 'colores', 'animales']
                for categoria in categorias:
                    # Verificar si ya existe progreso para esta categoría
                    progreso_existente = ProgresoUsuario.query.filter_by(
                        nino_id=nino.id,
                        categoria=categoria
                    ).first()
                    
                    if not progreso_existente:
                        # Crear progreso inicial
                        actividades_totales = {
                            'lenguaje': 11,
                            'numeros': 11,
                            'colores': 3,
                            'animales': 3
                        }.get(categoria, 0)
                        
                        progreso = ProgresoUsuario(
                            nino_id=nino.id,
                            categoria=categoria,
                            nivel_actual='inicial',
                            actividades_totales=actividades_totales
                        )
                        db.session.add(progreso)
            
            db.session.commit()
            print(f"✅ Progreso inicializado para {len(ninos)} niños")
            
            # Mostrar estadísticas
            result = db.session.execute(text("SELECT COUNT(*) FROM progreso_usuario"))
            total_progresos = result.fetchone()[0]
            
            result = db.session.execute(text("SELECT COUNT(*) FROM medalla_usuario"))
            total_medallas = result.fetchone()[0]
            
            print(f"📊 Estadísticas:")
            print(f"   • Total de registros de progreso: {total_progresos}")
            print(f"   • Total de medallas: {total_medallas}")
            
        except Exception as e:
            print(f"❌ Error al actualizar la base de datos: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Actualizando sistema de progreso real del usuario...")
    success = update_database()
    
    if success:
        print("\n🎉 ¡Actualización completada!")
        print("\n📋 Nuevas funcionalidades disponibles:")
        print("   • Progreso real por categoría")
        print("   • Sistema de medallas e insignias")
        print("   • Barras de progreso visuales")
        print("   • Estadísticas detalladas")
        print("   • Tracking de actividades completadas")
    else:
        print("\n❌ Error en la actualización")
        sys.exit(1)






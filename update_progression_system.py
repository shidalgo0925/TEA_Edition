#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar la base de datos con el sistema de progresión permanente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.tea_models import PerfilNino
from sqlalchemy import text

def update_database():
    """Actualiza la base de datos con los nuevos campos de progresión"""
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si las columnas ya existen
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'perfil_nino' 
                AND column_name IN ('nivel_inicial_configurado', 'nivel_progresion_actual', 'nivel_maximo_alcanzado')
            """))
            
            existing_columns = [row[0] for row in result.fetchall()]
            
            # Agregar columnas que no existen
            if 'nivel_inicial_configurado' not in existing_columns:
                print("Agregando columna nivel_inicial_configurado...")
                db.session.execute(text("""
                    ALTER TABLE perfil_nino 
                    ADD COLUMN nivel_inicial_configurado VARCHAR(20) DEFAULT 'inicial'
                """))
            
            if 'nivel_progresion_actual' not in existing_columns:
                print("Agregando columna nivel_progresion_actual...")
                db.session.execute(text("""
                    ALTER TABLE perfil_nino 
                    ADD COLUMN nivel_progresion_actual VARCHAR(20) DEFAULT 'inicial'
                """))
            
            if 'nivel_maximo_alcanzado' not in existing_columns:
                print("Agregando columna nivel_maximo_alcanzado...")
                db.session.execute(text("""
                    ALTER TABLE perfil_nino 
                    ADD COLUMN nivel_maximo_alcanzado VARCHAR(20) DEFAULT 'inicial'
                """))
            
            if 'puntos_totales_acumulados' not in existing_columns:
                print("Agregando columna puntos_totales_acumulados...")
                db.session.execute(text("""
                    ALTER TABLE perfil_nino 
                    ADD COLUMN puntos_totales_acumulados INTEGER DEFAULT 0
                """))
            
            if 'actividades_completadas_total' not in existing_columns:
                print("Agregando columna actividades_completadas_total...")
                db.session.execute(text("""
                    ALTER TABLE perfil_nino 
                    ADD COLUMN actividades_completadas_total INTEGER DEFAULT 0
                """))
            
            if 'dias_consecutivos' not in existing_columns:
                print("Agregando columna dias_consecutivos...")
                db.session.execute(text("""
                    ALTER TABLE perfil_nino 
                    ADD COLUMN dias_consecutivos INTEGER DEFAULT 0
                """))
            
            if 'fecha_ultima_actividad' not in existing_columns:
                print("Agregando columna fecha_ultima_actividad...")
                db.session.execute(text("""
                    ALTER TABLE perfil_nino 
                    ADD COLUMN fecha_ultima_actividad TIMESTAMP
                """))
            
            # Actualizar registros existentes
            print("Actualizando registros existentes...")
            db.session.execute(text("""
                UPDATE perfil_nino 
                SET 
                    nivel_inicial_configurado = 'inicial',
                    nivel_progresion_actual = 'inicial',
                    nivel_maximo_alcanzado = 'inicial',
                    puntos_totales_acumulados = 0,
                    actividades_completadas_total = 0,
                    dias_consecutivos = 0
                WHERE nivel_inicial_configurado IS NULL
            """))
            
            db.session.commit()
            print("✅ Base de datos actualizada correctamente")
            
            # Mostrar estadísticas
            result = db.session.execute(text("SELECT COUNT(*) FROM perfil_nino"))
            total_ninos = result.fetchone()[0]
            print(f"📊 Total de niños en la base de datos: {total_ninos}")
            
        except Exception as e:
            print(f"❌ Error al actualizar la base de datos: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Actualizando sistema de progresión permanente...")
    success = update_database()
    
    if success:
        print("\n🎉 ¡Actualización completada!")
        print("\n📋 Nuevas funcionalidades disponibles:")
        print("   • Sistema de progresión permanente (nunca retrocede)")
        print("   • Configuración de nivel inicial para educadores")
        print("   • Estadísticas de progresión detalladas")
        print("   • Ranking de niveles")
        print("   • Panel de configuración de progresión")
    else:
        print("\n❌ Error en la actualización")
        sys.exit(1)






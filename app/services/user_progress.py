# -*- coding: utf-8 -*-
"""
Sistema de Progreso Real del Usuario - TEA Edition
Maneja el progreso detallado por categoría y sistema de medallas
"""

from datetime import datetime
from sqlalchemy import and_, desc
from app.extensions import db
from app.models.tea_models import (
    PerfilNino, ActividadTEA, ProgresoUsuario, MedallaUsuario
)

class UserProgressSystem:
    """Sistema de progreso real del usuario"""
    
    # Configuración de actividades por categoría
    ACTIVIDADES_POR_CATEGORIA = {
        'lenguaje': 11,    # 11 actividades de lenguaje
        'numeros': 11,     # 11 actividades de números
        'colores': 3,      # 3 actividades de colores
        'animales': 3      # 3 actividades de animales
    }
    
    # Tipos de medallas disponibles
    TIPOS_MEDALLAS = {
        'primera_actividad': {
            'titulo': 'Primer Paso',
            'descripcion': '¡Completaste tu primera actividad!',
            'icono': '🌟',
            'puntos_requeridos': 1
        },
        'categoria_iniciada': {
            'titulo': 'Explorador',
            'descripcion': '¡Empezaste una nueva categoría!',
            'icono': '🗺️',
            'puntos_requeridos': 1
        },
        'categoria_completa': {
            'titulo': 'Maestro',
            'descripcion': '¡Completaste toda una categoría!',
            'icono': '👑',
            'puntos_requeridos': 0  # Se otorga al completar
        },
        'dias_consecutivos_3': {
            'titulo': 'Constante',
            'descripcion': '¡3 días seguidos aprendiendo!',
            'icono': '🔥',
            'puntos_requeridos': 0
        },
        'dias_consecutivos_7': {
            'titulo': 'Dedicado',
            'descripcion': '¡7 días seguidos aprendiendo!',
            'icono': '💎',
            'puntos_requeridos': 0
        },
        'puntos_100': {
            'titulo': 'Acumulador',
            'descripcion': '¡Acumulaste 100 puntos!',
            'icono': '💯',
            'puntos_requeridos': 100
        },
        'puntos_500': {
            'titulo': 'Experto',
            'descripcion': '¡Acumulaste 500 puntos!',
            'icono': '🏆',
            'puntos_requeridos': 500
        }
    }
    
    @classmethod
    def inicializar_progreso_categoria(cls, nino_id, categoria):
        """Inicializa el progreso para una categoría específica"""
        progreso = ProgresoUsuario.query.filter_by(
            nino_id=nino_id,
            categoria=categoria
        ).first()
        
        if not progreso:
            progreso = ProgresoUsuario(
                nino_id=nino_id,
                categoria=categoria,
                nivel_actual='inicial',
                actividades_totales=cls.ACTIVIDADES_POR_CATEGORIA.get(categoria, 0)
            )
            db.session.add(progreso)
            db.session.commit()
        
        return progreso
    
    @classmethod
    def actualizar_progreso_actividad(cls, nino_id, actividad_id, puntos_obtenidos):
        """Actualiza el progreso después de completar una actividad"""
        actividad = ActividadTEA.query.get(actividad_id)
        if not actividad:
            return False
        
        categoria = actividad.categoria
        
        # Inicializar progreso si no existe
        progreso = cls.inicializar_progreso_categoria(nino_id, categoria)
        
        # Actualizar estadísticas
        progreso.actividades_completadas += 1
        progreso.puntos_categoria += puntos_obtenidos
        progreso.ultima_actividad_id = actividad_id
        progreso.fecha_ultima_actividad = datetime.utcnow()
        progreso.fecha_actualizacion = datetime.utcnow()
        
        # Actualizar nivel de progresión
        cls._actualizar_nivel_progresion(progreso)
        
        # Verificar medallas
        cls._verificar_medallas(nino_id, categoria, progreso)
        
        db.session.commit()
        return True
    
    @classmethod
    def _actualizar_nivel_progresion(cls, progreso):
        """Actualiza el nivel de progresión basado en actividades completadas"""
        porcentaje = (progreso.actividades_completadas / progreso.actividades_totales) * 100
        
        if porcentaje >= 100:
            progreso.nivel_actual = 'completo'
        elif porcentaje >= 80:
            progreso.nivel_actual = 'avanzado'
        elif porcentaje >= 60:
            progreso.nivel_actual = 'intermedio'
        elif porcentaje >= 30:
            progreso.nivel_actual = 'basico'
        else:
            progreso.nivel_actual = 'inicial'
    
    @classmethod
    def _verificar_medallas(cls, nino_id, categoria, progreso):
        """Verifica y otorga medallas según el progreso"""
        # Medalla por primera actividad
        if progreso.actividades_completadas == 1:
            cls._otorgar_medalla(nino_id, 'primera_actividad', categoria)
        
        # Medalla por iniciar categoría
        if progreso.actividades_completadas == 1:
            cls._otorgar_medalla(nino_id, 'categoria_iniciada', categoria)
        
        # Medalla por completar categoría
        if progreso.actividades_completadas >= progreso.actividades_totales:
            cls._otorgar_medalla(nino_id, 'categoria_completa', categoria)
        
        # Medallas por puntos acumulados
        puntos_totales = cls._obtener_puntos_totales(nino_id)
        if puntos_totales >= 100 and not cls._tiene_medalla(nino_id, 'puntos_100'):
            cls._otorgar_medalla(nino_id, 'puntos_100')
        elif puntos_totales >= 500 and not cls._tiene_medalla(nino_id, 'puntos_500'):
            cls._otorgar_medalla(nino_id, 'puntos_500')
    
    @classmethod
    def _otorgar_medalla(cls, nino_id, tipo_medalla, categoria=None):
        """Otorga una medalla al usuario"""
        if cls._tiene_medalla(nino_id, tipo_medalla, categoria):
            return  # Ya tiene esta medalla
        
        config_medalla = cls.TIPOS_MEDALLAS.get(tipo_medalla)
        if not config_medalla:
            return
        
        medalla = MedallaUsuario(
            nino_id=nino_id,
            tipo_medalla=tipo_medalla,
            categoria=categoria,
            titulo=config_medalla['titulo'],
            descripcion=config_medalla['descripcion'],
            icono=config_medalla['icono'],
            puntos_requeridos=config_medalla['puntos_requeridos']
        )
        
        db.session.add(medalla)
        db.session.commit()
    
    @classmethod
    def _tiene_medalla(cls, nino_id, tipo_medalla, categoria=None):
        """Verifica si el usuario ya tiene una medalla específica"""
        query = MedallaUsuario.query.filter_by(
            nino_id=nino_id,
            tipo_medalla=tipo_medalla
        )
        
        if categoria:
            query = query.filter_by(categoria=categoria)
        
        return query.first() is not None
    
    @classmethod
    def _obtener_puntos_totales(cls, nino_id):
        """Obtiene los puntos totales del usuario"""
        progresos = ProgresoUsuario.query.filter_by(nino_id=nino_id).all()
        return sum(prog.puntos_categoria for prog in progresos)
    
    @classmethod
    def obtener_progreso_categoria(cls, nino_id, categoria):
        """Obtiene el progreso detallado de una categoría"""
        progreso = ProgresoUsuario.query.filter_by(
            nino_id=nino_id,
            categoria=categoria
        ).first()
        
        if not progreso:
            progreso = cls.inicializar_progreso_categoria(nino_id, categoria)
        
        return {
            'categoria': categoria,
            'nivel_actual': progreso.nivel_actual,
            'actividades_completadas': progreso.actividades_completadas,
            'actividades_totales': progreso.actividades_totales,
            'puntos_categoria': progreso.puntos_categoria,
            'porcentaje_completado': round((progreso.actividades_completadas / progreso.actividades_totales) * 100, 1),
            'fecha_ultima_actividad': progreso.fecha_ultima_actividad
        }
    
    @classmethod
    def obtener_progreso_completo(cls, nino_id):
        """Obtiene el progreso completo del usuario"""
        categorias = ['lenguaje', 'numeros', 'colores', 'animales']
        progreso_completo = {}
        
        for categoria in categorias:
            progreso_completo[categoria] = cls.obtener_progreso_categoria(nino_id, categoria)
        
        # Estadísticas generales
        progreso_completo['estadisticas_generales'] = {
            'puntos_totales': cls._obtener_puntos_totales(nino_id),
            'actividades_totales_completadas': sum(
                prog['actividades_completadas'] for prog in progreso_completo.values()
                if isinstance(prog, dict) and 'actividades_completadas' in prog
            ),
            'categorias_completadas': sum(
                1 for prog in progreso_completo.values()
                if isinstance(prog, dict) and prog.get('porcentaje_completado', 0) >= 100
            ),
            'nivel_general': cls._calcular_nivel_general(progreso_completo)
        }
        
        return progreso_completo
    
    @classmethod
    def _calcular_nivel_general(cls, progreso_completo):
        """Calcula el nivel general del usuario"""
        porcentajes = [
            prog.get('porcentaje_completado', 0) for prog in progreso_completo.values()
            if isinstance(prog, dict) and 'porcentaje_completado' in prog
        ]
        
        if not porcentajes:
            return 'inicial'
        
        promedio = sum(porcentajes) / len(porcentajes)
        
        if promedio >= 90:
            return 'experto'
        elif promedio >= 70:
            return 'avanzado'
        elif promedio >= 50:
            return 'intermedio'
        elif promedio >= 20:
            return 'basico'
        else:
            return 'inicial'
    
    @classmethod
    def obtener_medallas_usuario(cls, nino_id):
        """Obtiene todas las medallas del usuario"""
        medallas = MedallaUsuario.query.filter_by(
            nino_id=nino_id,
            visible=True
        ).order_by(desc(MedallaUsuario.fecha_obtenida)).all()
        
        return [{
            'id': medalla.id,
            'tipo': medalla.tipo_medalla,
            'titulo': medalla.titulo,
            'descripcion': medalla.descripcion,
            'icono': medalla.icono,
            'categoria': medalla.categoria,
            'fecha_obtenida': medalla.fecha_obtenida.isoformat()
        } for medalla in medallas]
    
    @classmethod
    def obtener_estadisticas_dashboard(cls, nino_id):
        """Obtiene estadísticas para el dashboard del niño"""
        progreso_completo = cls.obtener_progreso_completo(nino_id)
        medallas = cls.obtener_medallas_usuario(nino_id)
        
        # Calcular días consecutivos (simplificado)
        dias_consecutivos = cls._calcular_dias_consecutivos(nino_id)
        
        return {
            'puntos_totales': progreso_completo['estadisticas_generales']['puntos_totales'],
            'actividades_completadas': progreso_completo['estadisticas_generales']['actividades_totales_completadas'],
            'categorias_completadas': progreso_completo['estadisticas_generales']['categorias_completadas'],
            'nivel_general': progreso_completo['estadisticas_generales']['nivel_general'],
            'dias_consecutivos': dias_consecutivos,
            'medallas_obtenidas': len(medallas),
            'progreso_por_categoria': {
                cat: prog for cat, prog in progreso_completo.items()
                if isinstance(prog, dict) and 'categoria' in prog
            }
        }
    
    @classmethod
    def _calcular_dias_consecutivos(cls, nino_id):
        """Calcula los días consecutivos de actividad"""
        try:
            from datetime import datetime, timedelta
            from app.models.tea_models import SesionTEA
            
            # Obtener las últimas sesiones del niño
            sesiones = SesionTEA.query.filter_by(
                nino_id=nino_id,
                estado='completada'
            ).order_by(desc(SesionTEA.fecha)).all()
            
            if not sesiones:
                return 0
            
            # Calcular días consecutivos
            dias_consecutivos = 0
            fecha_actual = datetime.utcnow().date()
            
            for sesion in sesiones:
                fecha_sesion = sesion.fecha.date()
                diferencia_dias = (fecha_actual - fecha_sesion).days
                
                if diferencia_dias == dias_consecutivos:
                    dias_consecutivos += 1
                    fecha_actual = fecha_sesion
                elif diferencia_dias == dias_consecutivos + 1:
                    dias_consecutivos += 1
                    fecha_actual = fecha_sesion
                else:
                    break
            
            # Actualizar el perfil del niño
            nino = PerfilNino.query.get(nino_id)
            if nino:
                nino.dias_consecutivos = dias_consecutivos
                nino.fecha_ultima_actividad = datetime.utcnow()
                db.session.commit()
            
            return dias_consecutivos
        except Exception as e:
            return 0

# Funciones de utilidad para las rutas
def actualizar_progreso_actividad(nino_id, actividad_id, puntos_obtenidos):
    """Actualiza el progreso después de completar una actividad"""
    return UserProgressSystem.actualizar_progreso_actividad(nino_id, actividad_id, puntos_obtenidos)

def obtener_progreso_completo(nino_id):
    """Obtiene el progreso completo del usuario"""
    return UserProgressSystem.obtener_progreso_completo(nino_id)

def obtener_estadisticas_dashboard(nino_id):
    """Obtiene estadísticas para el dashboard"""
    return UserProgressSystem.obtener_estadisticas_dashboard(nino_id)

def obtener_medallas_usuario(nino_id):
    """Obtiene las medallas del usuario"""
    return UserProgressSystem.obtener_medallas_usuario(nino_id)


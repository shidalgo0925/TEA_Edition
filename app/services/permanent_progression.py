# -*- coding: utf-8 -*-
"""
Sistema de Progresión Permanente para TEA Edition
Como un videojuego, nunca retrocede, siempre avanza
"""

from datetime import datetime, timedelta
from sqlalchemy import and_, desc
from app.extensions import db
from app.models.tea_models import (
    PerfilNino, ActividadTEA, SesionTEA, SesionActividad, 
    ProgresoTEA, RecompensaTEA, LogroNino
)

class PermanentProgressionSystem:
    """Sistema de progresión permanente - nunca retrocede"""
    
    # Niveles de progresión ordenados
    NIVELES_PROGRESION = [
        'inicial',
        'basico_1', 'basico_2', 'basico_3',
        'intermedio_1', 'intermedio_2', 'intermedio_3',
        'avanzado_1', 'avanzado_2', 'avanzado_3',
        'experto'
    ]
    
    # Criterios para avanzar de nivel
    CRITERIOS_AVANCE = {
        'inicial': {'puntos_min': 0, 'actividades_min': 0, 'exito_min': 0},
        'basico_1': {'puntos_min': 50, 'actividades_min': 5, 'exito_min': 60},
        'basico_2': {'puntos_min': 100, 'actividades_min': 10, 'exito_min': 65},
        'basico_3': {'puntos_min': 150, 'actividades_min': 15, 'exito_min': 70},
        'intermedio_1': {'puntos_min': 250, 'actividades_min': 25, 'exito_min': 75},
        'intermedio_2': {'puntos_min': 350, 'actividades_min': 35, 'exito_min': 80},
        'intermedio_3': {'puntos_min': 450, 'actividades_min': 45, 'exito_min': 85},
        'avanzado_1': {'puntos_min': 600, 'actividades_min': 60, 'exito_min': 90},
        'avanzado_2': {'puntos_min': 750, 'actividades_min': 75, 'exito_min': 92},
        'avanzado_3': {'puntos_min': 900, 'actividades_min': 90, 'exito_min': 95},
        'experto': {'puntos_min': 1200, 'actividades_min': 120, 'exito_min': 98}
    }
    
    @classmethod
    def obtener_nivel_siguiente(cls, nivel_actual):
        """Obtiene el siguiente nivel en la progresión"""
        try:
            indice_actual = cls.NIVELES_PROGRESION.index(nivel_actual)
            if indice_actual < len(cls.NIVELES_PROGRESION) - 1:
                return cls.NIVELES_PROGRESION[indice_actual + 1]
            return None  # Ya está en el nivel máximo
        except ValueError:
            return 'inicial'  # Nivel no válido, empezar desde el inicio
    
    @classmethod
    def obtener_nivel_anterior(cls, nivel_actual):
        """Obtiene el nivel anterior (solo para referencia, no se usa para retroceder)"""
        try:
            indice_actual = cls.NIVELES_PROGRESION.index(nivel_actual)
            if indice_actual > 0:
                return cls.NIVELES_PROGRESION[indice_actual - 1]
            return None
        except ValueError:
            return None
    
    @classmethod
    def configurar_nivel_inicial(cls, nino_id, nivel_inicial):
        """Configura el nivel inicial del niño (solo para educadores)"""
        if nivel_inicial not in cls.NIVELES_PROGRESION:
            raise ValueError(f"Nivel {nivel_inicial} no válido")
        
        perfil = PerfilNino.query.get(nino_id)
        if not perfil:
            raise ValueError("Perfil de niño no encontrado")
        
        # Solo se puede configurar si no ha empezado a jugar
        if perfil.actividades_completadas_total == 0:
            perfil.nivel_inicial_configurado = nivel_inicial
            perfil.nivel_progresion_actual = nivel_inicial
            perfil.nivel_maximo_alcanzado = nivel_inicial
            db.session.commit()
            return True
        else:
            raise ValueError("No se puede cambiar el nivel inicial después de empezar a jugar")
    
    @classmethod
    def evaluar_progreso_actividad(cls, nino_id, actividad_id, puntos_obtenidos, exito):
        """Evalúa el progreso después de completar una actividad"""
        perfil = PerfilNino.query.get(nino_id)
        if not perfil:
            return False
        
        # Actualizar estadísticas permanentes
        perfil.puntos_totales_acumulados += puntos_obtenidos
        perfil.actividades_completadas_total += 1
        perfil.fecha_ultima_actividad = datetime.utcnow()
        
        # Actualizar días consecutivos
        cls._actualizar_dias_consecutivos(perfil)
        
        # Evaluar si puede avanzar de nivel
        nuevo_nivel = cls._evaluar_avance_nivel(perfil)
        if nuevo_nivel and nuevo_nivel != perfil.nivel_progresion_actual:
            perfil.nivel_progresion_actual = nuevo_nivel
            perfil.nivel_maximo_alcanzado = nuevo_nivel
            
            # Crear logro de nivel desbloqueado
            cls._crear_logro_nivel(perfil, nuevo_nivel)
        
        db.session.commit()
        return True
    
    @classmethod
    def _actualizar_dias_consecutivos(cls, perfil):
        """Actualiza los días consecutivos de uso"""
        hoy = datetime.utcnow().date()
        
        if perfil.fecha_ultima_actividad:
            ultima_fecha = perfil.fecha_ultima_actividad.date()
            diferencia = (hoy - ultima_fecha).days
            
            if diferencia == 1:  # Día consecutivo
                perfil.dias_consecutivos += 1
            elif diferencia > 1:  # Se rompió la racha
                perfil.dias_consecutivos = 1
            # Si diferencia == 0, es el mismo día, no cambiar
        else:
            perfil.dias_consecutivos = 1
    
    @classmethod
    def _evaluar_avance_nivel(cls, perfil):
        """Evalúa si el niño puede avanzar al siguiente nivel"""
        nivel_actual = perfil.nivel_progresion_actual
        siguiente_nivel = cls.obtener_nivel_siguiente(nivel_actual)
        
        if not siguiente_nivel:
            return None  # Ya está en el nivel máximo
        
        criterios = cls.CRITERIOS_AVANCE[siguiente_nivel]
        
        # Verificar criterios
        if (perfil.puntos_totales_acumulados >= criterios['puntos_min'] and
            perfil.actividades_completadas_total >= criterios['actividades_min']):
            
            # Calcular tasa de éxito promedio
            tasa_exito = cls._calcular_tasa_exito(perfil.id)
            if tasa_exito >= criterios['exito_min']:
                return siguiente_nivel
        
        return None
    
    @classmethod
    def _calcular_tasa_exito(cls, nino_id):
        """Calcula la tasa de éxito promedio del niño"""
        # Obtener todas las actividades completadas
        actividades_completadas = db.session.query(SesionActividad).join(
            SesionTEA, SesionActividad.sesion_id == SesionTEA.id
        ).filter(
            SesionTEA.nino_id == nino_id,
            SesionActividad.completada == True
        ).all()
        
        if not actividades_completadas:
            return 0
        
        # Calcular tasa de éxito basada en puntos obtenidos vs puntos máximos
        total_actividades = len(actividades_completadas)
        actividades_exitosas = 0
        
        for sa in actividades_completadas:
            actividad = ActividadTEA.query.get(sa.actividad_id)
            if actividad:
                # Considerar exitosa si obtuvo al menos el 70% de los puntos máximos
                puntos_maximos = actividad.puntos_recompensa
                if sa.puntos_obtenidos >= (puntos_maximos * 0.7):
                    actividades_exitosas += 1
        
        return (actividades_exitosas / total_actividades) * 100
    
    @classmethod
    def _crear_logro_nivel(cls, perfil, nuevo_nivel):
        """Crea un logro cuando se desbloquea un nuevo nivel"""
        # Buscar o crear recompensa para el nivel
        recompensa = RecompensaTEA.query.filter_by(
            nombre=f"Nivel {nuevo_nivel.replace('_', ' ').title()}",
            tipo="badge"
        ).first()
        
        if not recompensa:
            recompensa = RecompensaTEA(
                nombre=f"Nivel {nuevo_nivel.replace('_', ' ').title()}",
                descripcion=f"¡Has alcanzado el nivel {nuevo_nivel.replace('_', ' ').title()}!",
                tipo="badge",
                puntos_requeridos=0,
                categoria="progresion"
            )
            db.session.add(recompensa)
            db.session.flush()
        
        # Crear logro para el niño
        logro = LogroNino(
            nino_id=perfil.id,
            recompensa_id=recompensa.id,
            fecha_obtenido=datetime.utcnow()
        )
        db.session.add(logro)
    
    @classmethod
    def obtener_actividades_disponibles(cls, nino_id):
        """Obtiene las actividades disponibles para el nivel actual del niño"""
        perfil = PerfilNino.query.get(nino_id)
        if not perfil:
            return []
        
        nivel_actual = perfil.nivel_progresion_actual
        
        # Obtener actividades del nivel actual y anteriores (para reforzar)
        actividades = ActividadTEA.query.filter(
            ActividadTEA.nivel_dificultad == nivel_actual,
            ActividadTEA.activa == True
        ).all()
        
        return actividades
    
    @classmethod
    def obtener_estadisticas_progresion(cls, nino_id):
        """Obtiene estadísticas detalladas de progresión"""
        perfil = PerfilNino.query.get(nino_id)
        if not perfil:
            return None
        
        # Calcular progreso hacia el siguiente nivel
        siguiente_nivel = cls.obtener_nivel_siguiente(perfil.nivel_progresion_actual)
        progreso_siguiente = 0
        
        if siguiente_nivel:
            criterios = cls.CRITERIOS_AVANCE[siguiente_nivel]
            progreso_puntos = min(100, (perfil.puntos_totales_acumulados / criterios['puntos_min']) * 100)
            progreso_actividades = min(100, (perfil.actividades_completadas_total / criterios['actividades_min']) * 100)
            progreso_siguiente = (progreso_puntos + progreso_actividades) / 2
        
        return {
            'nivel_actual': perfil.nivel_progresion_actual,
            'nivel_maximo': perfil.nivel_maximo_alcanzado,
            'puntos_totales': perfil.puntos_totales_acumulados,
            'actividades_completadas': perfil.actividades_completadas_total,
            'dias_consecutivos': perfil.dias_consecutivos,
            'siguiente_nivel': siguiente_nivel,
            'progreso_siguiente': round(progreso_siguiente, 1),
            'tasa_exito': round(cls._calcular_tasa_exito(nino_id), 1),
            'fecha_ultima_actividad': perfil.fecha_ultima_actividad
        }
    
    @classmethod
    def obtener_ranking_niveles(cls):
        """Obtiene ranking de niños por nivel alcanzado"""
        perfiles = PerfilNino.query.filter(
            PerfilNino.activo == True,
            PerfilNino.actividades_completadas_total > 0
        ).order_by(
            desc(PerfilNino.nivel_maximo_alcanzado),
            desc(PerfilNino.puntos_totales_acumulados)
        ).limit(10).all()
        
        ranking = []
        for perfil in perfiles:
            ranking.append({
                'nombre': perfil.nombre,
                'nivel': perfil.nivel_maximo_alcanzado,
                'puntos': perfil.puntos_totales_acumulados,
                'actividades': perfil.actividades_completadas_total
            })
        
        return ranking

# Funciones de utilidad para las rutas
def configurar_nivel_inicial_nino(nino_id, nivel_inicial):
    """Configura el nivel inicial de un niño"""
    return PermanentProgressionSystem.configurar_nivel_inicial(nino_id, nivel_inicial)

def evaluar_progreso_actividad(nino_id, actividad_id, puntos_obtenidos, exito):
    """Evalúa el progreso después de una actividad"""
    return PermanentProgressionSystem.evaluar_progreso_actividad(
        nino_id, actividad_id, puntos_obtenidos, exito
    )

def obtener_actividades_disponibles_nino(nino_id):
    """Obtiene actividades disponibles para un niño"""
    return PermanentProgressionSystem.obtener_actividades_disponibles(nino_id)

def obtener_estadisticas_progresion_nino(nino_id):
    """Obtiene estadísticas de progresión de un niño"""
    return PermanentProgressionSystem.obtener_estadisticas_progresion(nino_id)

def obtener_ranking_niveles():
    """Obtiene ranking de niveles"""
    return PermanentProgressionSystem.obtener_ranking_niveles()






# -*- coding: utf-8 -*-
"""
Sistema de Aprendizaje Adaptativo para TEA Edition
Analiza el progreso del niño y recomienda actividades apropiadas
"""
from app.extensions import db
from app.models.tea_models import (
    PerfilNino, ActividadTEA, SesionActividad, ProgresoTEA, SesionTEA
)
from datetime import datetime, timedelta
import json
import math

class AdaptiveLearningSystem:
    """Sistema de aprendizaje adaptativo que ajusta la dificultad según el progreso"""
    
    def __init__(self, nino_id):
        self.nino_id = nino_id
        self.nino = PerfilNino.query.get(nino_id)
    
    def analizar_rendimiento_actividad(self, actividad_id, ultimos_dias=7):
        """Analiza el rendimiento del niño en una actividad específica"""
        fecha_limite = datetime.now() - timedelta(days=ultimos_dias)
        
        # Obtener intentos recientes de esta actividad
        intentos = SesionActividad.query.join(SesionTEA).filter(
            SesionActividad.actividad_id == actividad_id,
            SesionActividad.sesion.has(nino_id=self.nino_id),
            SesionTEA.fecha >= fecha_limite
        ).all()
        
        if not intentos:
            return {
                'rendimiento': 0.5,  # Neutral si no hay datos
                'intentos_totales': 0,
                'tiempo_promedio': 0,
                'tasa_exito': 0.5
            }
        
        # Calcular métricas
        intentos_totales = len(intentos)
        intentos_exitosos = sum(1 for i in intentos if i.completada)
        tiempo_promedio = sum(i.tiempo_dedicado for i in intentos) / intentos_totales
        tasa_exito = intentos_exitosos / intentos_totales
        
        # Calcular rendimiento general (0-1, donde 1 es excelente)
        rendimiento = tasa_exito * 0.7 + (1 - min(tiempo_promedio / 300, 1)) * 0.3
        
        return {
            'rendimiento': rendimiento,
            'intentos_totales': intentos_totales,
            'tiempo_promedio': tiempo_promedio,
            'tasa_exito': tasa_exito
        }
    
    def analizar_progreso_habilidad(self, categoria, ultimos_dias=14):
        """Analiza el progreso general en una habilidad específica"""
        fecha_limite = datetime.now() - timedelta(days=ultimos_dias)
        
        # Obtener progreso de la habilidad
        progreso = ProgresoTEA.query.filter_by(
            nino_id=self.nino_id,
            habilidad=categoria
        ).first()
        
        if not progreso:
            return {
                'nivel_actual': 'basico',
                'puntos_totales': 0,
                'tendencia': 'estable',
                'confianza': 0.3
            }
        
        # Obtener actividades recientes de esta categoría
        actividades_recientes = SesionActividad.query.join(SesionTEA).join(ActividadTEA).filter(
            SesionActividad.sesion.has(nino_id=self.nino_id),
            ActividadTEA.categoria == categoria,
            SesionTEA.fecha >= fecha_limite
        ).all()
        
        # Calcular tendencia
        if len(actividades_recientes) >= 3:
            rendimientos = []
            for actividad in actividades_recientes:
                rendimiento = self.analizar_rendimiento_actividad(actividad.actividad_id, ultimos_dias)
                rendimientos.append(rendimiento['rendimiento'])
            
            # Calcular tendencia
            if len(rendimientos) >= 2:
                tendencia = 'mejorando' if rendimientos[-1] > rendimientos[0] else 'estable'
                if rendimientos[-1] < rendimientos[0] * 0.8:
                    tendencia = 'dificultad'
            else:
                tendencia = 'estable'
        else:
            tendencia = 'estable'
        
        # Calcular nivel de confianza
        confianza = min(progreso.puntos_totales / 100, 1.0)
        
        return {
            'nivel_actual': progreso.nivel_actual,
            'puntos_totales': progreso.puntos_totales,
            'tendencia': tendencia,
            'confianza': confianza
        }
    
    def calcular_dificultad_optima(self, categoria):
        """Calcula la dificultad óptima para una categoría basada en el progreso"""
        progreso = self.analizar_progreso_habilidad(categoria)
        
        # Mapear niveles de dificultad
        niveles = {'basico': 1, 'intermedio': 2, 'avanzado': 3}
        
        # Ajustar dificultad basada en tendencia y confianza
        nivel_base = niveles.get(progreso['nivel_actual'], 1)
        
        if progreso['tendencia'] == 'mejorando' and progreso['confianza'] > 0.7:
            # Si está mejorando y tiene confianza, puede subir de nivel
            nivel_optimo = min(nivel_base + 1, 3)
        elif progreso['tendencia'] == 'dificultad' or progreso['confianza'] < 0.4:
            # Si tiene dificultades, bajar de nivel
            nivel_optimo = max(nivel_base - 1, 1)
        else:
            # Mantener nivel actual
            nivel_optimo = nivel_base
        
        return nivel_optimo
    
    def recomendar_actividades(self, limite=5, incluir_refuerzo=True):
        """Recomienda actividades basadas en el análisis adaptativo"""
        recomendaciones = []
        
        # Obtener todas las categorías disponibles
        categorias = db.session.query(ActividadTEA.categoria).distinct().all()
        categorias = [cat[0] for cat in categorias]
        
        for categoria in categorias:
            # Analizar progreso en esta categoría
            progreso = self.analizar_progreso_habilidad(categoria)
            dificultad_optima = self.calcular_dificultad_optima(categoria)
            
            # Obtener actividades de la dificultad óptima
            actividades = ActividadTEA.query.filter_by(
                categoria=categoria,
                activa=True
            ).all()
            
            # Filtrar por dificultad óptima
            actividades_optimas = []
            for actividad in actividades:
                nivel_actividad = {'basico': 1, 'intermedio': 2, 'avanzado': 3}.get(
                    actividad.nivel_dificultad, 1
                )
                if nivel_actividad == dificultad_optima:
                    actividades_optimas.append(actividad)
            
            # Si no hay actividades de la dificultad óptima, usar las más cercanas
            if not actividades_optimas:
                actividades_optimas = actividades
            
            # Analizar rendimiento de cada actividad
            for actividad in actividades_optimas:
                rendimiento = self.analizar_rendimiento_actividad(actividad.id)
                
                # Calcular score de recomendación
                score = self._calcular_score_recomendacion(
                    actividad, progreso, rendimiento, incluir_refuerzo
                )
                
                recomendaciones.append({
                    'actividad': actividad,
                    'score': score,
                    'categoria': categoria,
                    'dificultad_optima': dificultad_optima,
                    'rendimiento_actual': rendimiento['rendimiento'],
                    'progreso_categoria': progreso
                })
        
        # Ordenar por score y retornar las mejores
        recomendaciones.sort(key=lambda x: x['score'], reverse=True)
        return recomendaciones[:limite]
    
    def _calcular_score_recomendacion(self, actividad, progreso, rendimiento, incluir_refuerzo):
        """Calcula un score para la recomendación de una actividad"""
        score = 0
        
        # Factor 1: Diversidad (evitar repetir la misma actividad muy seguido)
        ultima_vez = self._obtener_ultima_vez_actividad(actividad.id)
        if ultima_vez:
            dias_desde_ultima = (datetime.now() - ultima_vez).days
            score += min(dias_desde_ultima / 3, 1) * 0.3  # Bonus por diversidad
        else:
            score += 0.3  # Bonus por actividad nueva
        
        # Factor 2: Balance de dificultad
        nivel_actividad = {'basico': 1, 'intermedio': 2, 'avanzado': 3}.get(
            actividad.nivel_dificultad, 1
        )
        nivel_optimo = self.calcular_dificultad_optima(actividad.categoria)
        diferencia_dificultad = abs(nivel_actividad - nivel_optimo)
        score += (1 - diferencia_dificultad / 2) * 0.4
        
        # Factor 3: Rendimiento reciente
        if rendimiento['intentos_totales'] > 0:
            if rendimiento['rendimiento'] > 0.8:
                # Si va muy bien, puede intentar algo más difícil
                score += 0.2
            elif rendimiento['rendimiento'] < 0.4:
                # Si va mal, necesita refuerzo
                if incluir_refuerzo:
                    score += 0.3
            else:
                # Rendimiento medio, mantener nivel
                score += 0.1
        
        # Factor 4: Progreso general de la categoría
        if progreso['tendencia'] == 'mejorando':
            score += 0.1
        elif progreso['tendencia'] == 'dificultad':
            score += 0.2  # Priorizar actividades de refuerzo
        
        return score
    
    def _obtener_ultima_vez_actividad(self, actividad_id):
        """Obtiene la última vez que el niño hizo esta actividad"""
        ultima_sesion = SesionActividad.query.join(SesionTEA).filter(
            SesionActividad.actividad_id == actividad_id,
            SesionActividad.sesion.has(nino_id=self.nino_id)
        ).order_by(SesionActividad.fecha_completada.desc()).first()
        
        return ultima_sesion.fecha_completada if ultima_sesion else None
    
    def generar_plan_sesion(self, duracion_objetivo=15):
        """Genera un plan de sesión adaptativo basado en el tiempo objetivo"""
        recomendaciones = self.recomendar_actividades(limite=10, incluir_refuerzo=True)
        
        plan = []
        tiempo_total = 0
        
        for rec in recomendaciones:
            actividad = rec['actividad']
            tiempo_estimado = actividad.tiempo_estimado
            
            if tiempo_total + tiempo_estimado <= duracion_objetivo:
                plan.append({
                    'actividad': actividad,
                    'orden': len(plan) + 1,
                    'tiempo_estimado': tiempo_estimado,
                    'motivo': self._generar_motivo_recomendacion(rec)
                })
                tiempo_total += tiempo_estimado
            else:
                break
        
        return {
            'plan': plan,
            'tiempo_total_estimado': tiempo_total,
            'actividades_incluidas': len(plan),
            'fecha_generacion': datetime.now()
        }
    
    def _generar_motivo_recomendacion(self, recomendacion):
        """Genera un motivo explicativo para la recomendación"""
        rendimiento = recomendacion['rendimiento_actual']
        progreso = recomendacion['progreso_categoria']
        
        if rendimiento > 0.8:
            return "¡Vas muy bien! Es hora de un nuevo desafío"
        elif rendimiento < 0.4:
            return "Vamos a practicar más para mejorar"
        elif progreso['tendencia'] == 'mejorando':
            return "Sigues mejorando, ¡continúa así!"
        else:
            return "Actividad perfecta para tu nivel actual"

def obtener_actividades_adaptativas(nino_id, limite=5):
    """Función helper para obtener actividades adaptativas"""
    sistema = AdaptiveLearningSystem(nino_id)
    return sistema.recomendar_actividades(limite=limite)

def generar_plan_sesion_adaptativo(nino_id, duracion=15):
    """Función helper para generar plan de sesión adaptativo"""
    sistema = AdaptiveLearningSystem(nino_id)
    return sistema.generar_plan_sesion(duracion)

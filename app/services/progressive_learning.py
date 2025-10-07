# -*- coding: utf-8 -*-
"""
Sistema de Aprendizaje Progresivo para TEA Edition
Implementa progresión incremental de dificultad basada en el rendimiento
"""
from app.extensions import db
from app.models.tea_models import (
    PerfilNino, ActividadTEA, SesionActividad, ProgresoTEA, SesionTEA
)
from datetime import datetime, timedelta
import json
import math

class ProgressiveLearningSystem:
    """Sistema de aprendizaje progresivo que incrementa la dificultad gradualmente"""
    
    def __init__(self, nino_id):
        self.nino_id = nino_id
        self.nino = PerfilNino.query.get(nino_id)
        
        # Definir niveles de dificultad progresivos
        self.niveles_dificultad = {
            'inicial': 0,      # Primeras actividades
            'basico_1': 1,     # Básico nivel 1
            'basico_2': 2,     # Básico nivel 2
            'basico_3': 3,     # Básico nivel 3
            'intermedio_1': 4, # Intermedio nivel 1
            'intermedio_2': 5, # Intermedio nivel 2
            'intermedio_3': 6, # Intermedio nivel 3
            'avanzado_1': 7,   # Avanzado nivel 1
            'avanzado_2': 8,   # Avanzado nivel 2
            'avanzado_3': 9,   # Avanzado nivel 3
            'experto': 10      # Nivel experto
        }
        
        # Criterios para avanzar de nivel
        self.criterios_progresion = {
            'puntos_minimos': 50,      # Puntos mínimos para avanzar
            'tasa_exito_minima': 0.8,  # 80% de éxito mínimo
            'intentos_minimos': 5,     # Mínimo 5 intentos
            'tiempo_maximo': 300       # Máximo 5 minutos por actividad
        }
    
    def evaluar_progreso_actividad(self, actividad_id, ultimos_dias=7):
        """Evalúa el progreso en una actividad específica para determinar si puede avanzar"""
        fecha_limite = datetime.now() - timedelta(days=ultimos_dias)
        
        # Obtener intentos recientes
        intentos = SesionActividad.query.join(SesionTEA).filter(
            SesionActividad.actividad_id == actividad_id,
            SesionActividad.sesion.has(nino_id=self.nino_id),
            SesionTEA.fecha >= fecha_limite
        ).all()
        
        if not intentos:
            return {
                'puede_avanzar': False,
                'razon': 'No hay suficientes intentos recientes',
                'puntos_totales': 0,
                'tasa_exito': 0,
                'tiempo_promedio': 0,
                'intentos_totales': 0
            }
        
        # Calcular métricas
        intentos_totales = len(intentos)
        intentos_exitosos = sum(1 for i in intentos if i.completada)
        puntos_totales = sum(i.puntos_obtenidos for i in intentos if i.puntos_obtenidos)
        tiempo_promedio = sum(i.tiempo_dedicado for i in intentos) / intentos_totales
        tasa_exito = intentos_exitosos / intentos_totales
        
        # Evaluar si puede avanzar
        puede_avanzar = (
            puntos_totales >= self.criterios_progresion['puntos_minimos'] and
            tasa_exito >= self.criterios_progresion['tasa_exito_minima'] and
            intentos_totales >= self.criterios_progresion['intentos_minimos'] and
            tiempo_promedio <= self.criterios_progresion['tiempo_maximo']
        )
        
        razon = "Cumple todos los criterios para avanzar" if puede_avanzar else "No cumple los criterios de progresión"
        
        return {
            'puede_avanzar': puede_avanzar,
            'razon': razon,
            'puntos_totales': puntos_totales,
            'tasa_exito': tasa_exito,
            'tiempo_promedio': tiempo_promedio,
            'intentos_totales': intentos_totales
        }
    
    def determinar_siguiente_nivel(self, categoria):
        """Determina el siguiente nivel de dificultad para una categoría"""
        progreso = ProgresoTEA.query.filter_by(
            nino_id=self.nino_id,
            habilidad=categoria
        ).first()
        
        if not progreso:
            return 'inicial'
        
        nivel_actual = progreso.nivel_actual
        
        # Obtener actividades del nivel actual para evaluar progreso
        actividades_actuales = ActividadTEA.query.filter_by(
            categoria=categoria,
            nivel_dificultad=nivel_actual,
            activa=True
        ).all()
        
        if not actividades_actuales:
            return nivel_actual
        
        # Evaluar progreso en actividades del nivel actual
        actividades_completadas = 0
        actividades_que_pueden_avanzar = 0
        
        for actividad in actividades_actuales:
            evaluacion = self.evaluar_progreso_actividad(actividad.id)
            if evaluacion['intentos_totales'] > 0:
                actividades_completadas += 1
                if evaluacion['puede_avanzar']:
                    actividades_que_pueden_avanzar += 1
        
        # Si no hay actividades completadas, mantener nivel actual
        if actividades_completadas == 0:
            return nivel_actual
        
        # Si más del 70% de las actividades pueden avanzar, subir nivel
        porcentaje_avance = actividades_que_pueden_avanzar / actividades_completadas
        if porcentaje_avance >= 0.7:
            return self._obtener_siguiente_nivel(nivel_actual)
        
        return nivel_actual
    
    def _obtener_siguiente_nivel(self, nivel_actual):
        """Obtiene el siguiente nivel en la progresión"""
        nivel_num = self.niveles_dificultad.get(nivel_actual, 0)
        siguiente_num = min(nivel_num + 1, 10)  # Máximo nivel experto
        
        # Encontrar el nombre del nivel
        for nombre, num in self.niveles_dificultad.items():
            if num == siguiente_num:
                return nombre
        
        return nivel_actual
    
    def obtener_actividades_progresivas(self, categoria, limite=5):
        """Obtiene actividades que siguen la progresión natural del niño"""
        nivel_objetivo = self.determinar_siguiente_nivel(categoria)
        
        # Obtener actividades del nivel objetivo
        actividades = ActividadTEA.query.filter_by(
            categoria=categoria,
            nivel_dificultad=nivel_objetivo,
            activa=True
        ).all()
        
        # Si no hay actividades del nivel objetivo, obtener del nivel actual
        if not actividades:
            progreso = ProgresoTEA.query.filter_by(
                nino_id=self.nino_id,
                habilidad=categoria
            ).first()
            
            nivel_actual = progreso.nivel_actual if progreso else 'inicial'
            actividades = ActividadTEA.query.filter_by(
                categoria=categoria,
                nivel_dificultad=nivel_actual,
                activa=True
            ).all()
        
        # Evaluar cada actividad y calcular score de progresión
        actividades_con_score = []
        for actividad in actividades:
            evaluacion = self.evaluar_progreso_actividad(actividad.id)
            
            # Calcular score basado en progresión
            score = self._calcular_score_progresion(actividad, evaluacion, nivel_objetivo)
            
            actividades_con_score.append({
                'actividad': actividad,
                'score': score,
                'nivel_objetivo': nivel_objetivo,
                'evaluacion': evaluacion,
                'motivo_progresion': self._generar_motivo_progresion(actividad, evaluacion, nivel_objetivo)
            })
        
        # Ordenar por score y retornar las mejores
        actividades_con_score.sort(key=lambda x: x['score'], reverse=True)
        return actividades_con_score[:limite]
    
    def _calcular_score_progresion(self, actividad, evaluacion, nivel_objetivo):
        """Calcula un score para la progresión de una actividad"""
        score = 0
        
        # Factor 1: Progresión natural (40%)
        nivel_actividad = self.niveles_dificultad.get(actividad.nivel_dificultad, 0)
        nivel_objetivo_num = self.niveles_dificultad.get(nivel_objetivo, 0)
        
        if nivel_actividad == nivel_objetivo_num:
            score += 0.4  # Actividad del nivel objetivo
        elif nivel_actividad < nivel_objetivo_num:
            score += 0.2  # Actividad de nivel inferior (refuerzo)
        else:
            score += 0.1  # Actividad de nivel superior (desafío)
        
        # Factor 2: Rendimiento reciente (30%)
        if evaluacion['intentos_totales'] > 0:
            if evaluacion['puede_avanzar']:
                score += 0.3  # Listo para avanzar
            elif evaluacion['tasa_exito'] > 0.6:
                score += 0.2  # Buen rendimiento
            elif evaluacion['tasa_exito'] > 0.4:
                score += 0.1  # Rendimiento medio
            else:
                score += 0.05  # Necesita más práctica
        
        # Factor 3: Diversidad temporal (20%)
        ultima_vez = self._obtener_ultima_vez_actividad(actividad.id)
        if ultima_vez:
            dias_desde_ultima = (datetime.now() - ultima_vez).days
            score += min(dias_desde_ultima / 3, 1) * 0.2
        else:
            score += 0.2  # Actividad nueva
        
        # Factor 4: Complejidad apropiada (10%)
        if evaluacion['tiempo_promedio'] > 0:
            if evaluacion['tiempo_promedio'] <= 180:  # 3 minutos o menos
                score += 0.1  # Tiempo apropiado
            elif evaluacion['tiempo_promedio'] <= 300:  # 5 minutos o menos
                score += 0.05  # Tiempo aceptable
        
        return score
    
    def _generar_motivo_progresion(self, actividad, evaluacion, nivel_objetivo):
        """Genera un motivo explicativo para la progresión"""
        if evaluacion['puede_avanzar']:
            return f"¡Excelente! Estás listo para el nivel {nivel_objetivo}"
        elif evaluacion['tasa_exito'] > 0.7:
            return f"Vas muy bien, continúa practicando para avanzar"
        elif evaluacion['tasa_exito'] > 0.5:
            return f"Buen progreso, un poco más de práctica y podrás avanzar"
        elif evaluacion['intentos_totales'] == 0:
            return f"Nueva actividad del nivel {nivel_objetivo}"
        else:
            return f"Practica más para dominar este nivel"
    
    def _obtener_ultima_vez_actividad(self, actividad_id):
        """Obtiene la última vez que el niño hizo esta actividad"""
        ultima_sesion = SesionActividad.query.join(SesionTEA).filter(
            SesionActividad.actividad_id == actividad_id,
            SesionActividad.sesion.has(nino_id=self.nino_id)
        ).order_by(SesionActividad.fecha_completada.desc()).first()
        
        return ultima_sesion.fecha_completada if ultima_sesion else None
    
    def generar_plan_progresivo(self, duracion_objetivo=15):
        """Genera un plan de sesión con progresión incremental"""
        categorias = db.session.query(ActividadTEA.categoria).distinct().all()
        categorias = [cat[0] for cat in categorias]
        
        plan = []
        tiempo_total = 0
        
        # Obtener actividades progresivas de cada categoría
        for categoria in categorias:
            actividades_progresivas = self.obtener_actividades_progresivas(categoria, limite=2)
            
            for act_prog in actividades_progresivas:
                actividad = act_prog['actividad']
                tiempo_estimado = actividad.tiempo_estimado
                
                if tiempo_total + tiempo_estimado <= duracion_objetivo:
                    plan.append({
                        'actividad': actividad,
                        'orden': len(plan) + 1,
                        'tiempo_estimado': tiempo_estimado,
                        'nivel_objetivo': act_prog['nivel_objetivo'],
                        'motivo_progresion': act_prog['motivo_progresion'],
                        'score_progresion': act_prog['score']
                    })
                    tiempo_total += tiempo_estimado
                else:
                    break
            
            if tiempo_total >= duracion_objetivo:
                break
        
        return {
            'plan': plan,
            'tiempo_total_estimado': tiempo_total,
            'actividades_incluidas': len(plan),
            'fecha_generacion': datetime.now(),
            'tipo': 'progresivo'
        }
    
    def actualizar_nivel_progresion(self, categoria):
        """Actualiza el nivel de progresión para una categoría específica"""
        nuevo_nivel = self.determinar_siguiente_nivel(categoria)
        
        progreso = ProgresoTEA.query.filter_by(
            nino_id=self.nino_id,
            habilidad=categoria
        ).first()
        
        if progreso:
            if progreso.nivel_actual != nuevo_nivel:
                progreso.nivel_actual = nuevo_nivel
                progreso.ultima_actualizacion = datetime.now()
                db.session.commit()
                return True
        
        return False

def obtener_actividades_progresivas(nino_id, limite=5):
    """Función helper para obtener actividades progresivas"""
    sistema = ProgressiveLearningSystem(nino_id)
    categorias = db.session.query(ActividadTEA.categoria).distinct().all()
    categorias = [cat[0] for cat in categorias]
    
    todas_actividades = []
    for categoria in categorias:
        actividades = sistema.obtener_actividades_progresivas(categoria, limite=2)
        todas_actividades.extend(actividades)
    
    # Ordenar por score y retornar las mejores
    todas_actividades.sort(key=lambda x: x['score'], reverse=True)
    return todas_actividades[:limite]

def generar_plan_progresivo(nino_id, duracion=15):
    """Función helper para generar plan progresivo"""
    sistema = ProgressiveLearningSystem(nino_id)
    return sistema.generar_plan_progresivo(duracion)






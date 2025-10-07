# -*- coding: utf-8 -*-
"""
Sistema de Avatar IA Guía - TEA Edition
Maneja las interacciones del avatar virtual con el niño
"""

from datetime import datetime
from app.extensions import db
from app.models.tea_models import PerfilNino
from app.services.user_progress import UserProgressSystem

class AvatarSystem:
    """Sistema de Avatar IA para guiar al niño"""
    
    # Frases contextuales del avatar
    FRASES_CONTEXTUALES = {
        'saludo': [
            "¡Hola! Soy tu maestra virtual. ¿Cómo estás hoy?",
            "¡Buenos días! ¿Listo para aprender algo nuevo?",
            "¡Hola! Me da mucho gusto verte de nuevo.",
            "¡Hola! ¿Qué tal si aprendemos juntos hoy?"
        ],
        'motivacion': [
            "¡Eres muy inteligente! Sigue así.",
            "¡Excelente trabajo! Estoy muy orgullosa de ti.",
            "¡Qué bien lo estás haciendo! Continúa así.",
            "¡Eres un campeón! No te rindas nunca."
        ],
        'progreso': [
            "¡Mira cuánto has progresado! ¡Eres increíble!",
            "¡Wow! Has completado muchas actividades. ¡Sigue así!",
            "¡Estás mejorando cada día! Me encanta ver tu progreso.",
            "¡Qué orgullosa estoy de ti! Has aprendido mucho."
        ],
        'categoria_lenguaje': [
            "¡Vamos a practicar palabras! ¿Te gusta hablar?",
            "Hoy vamos a aprender nuevas palabras. ¿Listo?",
            "¡Las palabras son mágicas! Vamos a descubrirlas juntas.",
            "¿Sabías que cada palabra tiene su sonido especial?"
        ],
        'categoria_numeros': [
            "¡Los números son muy divertidos! ¿Quieres contar conmigo?",
            "¡Vamos a jugar con números! ¿Te gusta contar?",
            "Los números nos ayudan a entender el mundo. ¡Aprendamos juntos!",
            "¡Contar es como un juego! ¿Empezamos?"
        ],
        'categoria_colores': [
            "¡Los colores son hermosos! ¿Cuál es tu favorito?",
            "¡Vamos a pintar el mundo de colores! ¿Te gusta?",
            "Cada color tiene su magia especial. ¡Descubrámosla!",
            "¡Los colores nos hacen felices! ¿Jugamos con ellos?"
        ],
        'categoria_animales': [
            "¡Los animales son nuestros amigos! ¿Quieres conocerlos?",
            "¡Vamos a visitar el zoológico virtual! ¿Te gusta?",
            "Cada animal tiene su sonido especial. ¡Escuchemos!",
            "¡Los animales son muy divertidos! ¿Jugamos con ellos?"
        ],
        'descanso': [
            "Es importante descansar. ¿Te sientes cansado?",
            "Tomemos un descanso. ¿Quieres relajarte un poco?",
            "A veces necesitamos parar y respirar. ¿Te ayudo?",
            "¡Descansar también es parte de aprender! ¿Qué te parece?"
        ],
        'felicitacion': [
            "¡Bravo! ¡Lo hiciste perfectamente!",
            "¡Eres increíble! ¡Qué bien lo hiciste!",
            "¡Wow! ¡Eres muy inteligente!",
            "¡Excelente! ¡Estoy muy orgullosa de ti!"
        ],
        'animacion': [
            "¡Vamos a hacer una actividad divertida!",
            "¡Esto va a ser muy emocionante!",
            "¡Prepárate para algo genial!",
            "¡Vamos a jugar y aprender al mismo tiempo!"
        ]
    }
    
    # Frases según el nivel de progreso
    FRASES_PROGRESO = {
        'inicial': [
            "¡Todo comienza con el primer paso! ¡Vamos!",
            "¡Cada experto fue alguna vez un principiante!",
            "¡El aprendizaje es una aventura! ¿Empezamos?",
            "¡Tu viaje de aprendizaje comienza ahora!"
        ],
        'basico': [
            "¡Ya estás aprendiendo! ¡Sigue así!",
            "¡Vas por buen camino! ¡Continúa!",
            "¡Estás mejorando! ¡No te detengas!",
            "¡Cada día aprendes más! ¡Eres genial!"
        ],
        'intermedio': [
            "¡Estás avanzando muy bien! ¡Eres inteligente!",
            "¡Qué rápido aprendes! ¡Me impresionas!",
            "¡Ya eres un experto en muchas cosas!",
            "¡Tu progreso es increíble! ¡Sigue así!"
        ],
        'avanzado': [
            "¡Eres un verdadero maestro! ¡Qué orgullosa estoy!",
            "¡Tu conocimiento es impresionante!",
            "¡Eres un ejemplo para otros niños!",
            "¡Tu dedicación es admirable! ¡Eres increíble!"
        ],
        'experto': [
            "¡Eres un genio! ¡Tu conocimiento es asombroso!",
            "¡Eres un verdadero experto! ¡Qué talento!",
            "¡Tu nivel de aprendizaje es extraordinario!",
            "¡Eres una inspiración! ¡Qué orgullosa estoy de ti!"
        ]
    }
    
    @classmethod
    def obtener_frase_contextual(cls, contexto, nino_id=None):
        """Obtiene una frase contextual del avatar"""
        import random
        
        frases = cls.FRASES_CONTEXTUALES.get(contexto, ["¡Hola! ¿Cómo estás?"])
        
        # Si tenemos información del niño, personalizar la frase
        if nino_id:
            try:
                nino = PerfilNino.query.get(nino_id)
                if nino:
                    # Agregar el nombre del niño a algunas frases
                    if contexto == 'saludo':
                        frases = [f"¡Hola {nino.nombre}! ¿Cómo estás hoy?"] + frases
                    elif contexto == 'motivacion':
                        frases = [f"¡{nino.nombre}, eres muy inteligente!"] + frases
            except:
                pass
        
        return random.choice(frases)
    
    @classmethod
    def obtener_frase_progreso(cls, nino_id):
        """Obtiene una frase basada en el progreso del niño"""
        try:
            estadisticas = UserProgressSystem.obtener_estadisticas_dashboard(nino_id)
            nivel = estadisticas.get('nivel_general', 'inicial')
            
            frases = cls.FRASES_PROGRESO.get(nivel, cls.FRASES_PROGRESO['inicial'])
            import random
            return random.choice(frases)
        except:
            return "¡Vamos a aprender juntos!"
    
    @classmethod
    def obtener_recomendacion_actividad(cls, nino_id):
        """Obtiene una recomendación de actividad basada en el progreso"""
        try:
            estadisticas = UserProgressSystem.obtener_estadisticas_dashboard(nino_id)
            progreso_categorias = estadisticas.get('progreso_por_categoria', {})
            
            # Encontrar la categoría con menor progreso
            categoria_recomendada = None
            menor_progreso = 100
            
            for categoria, progreso in progreso_categorias.items():
                porcentaje = progreso.get('porcentaje_completado', 0)
                if porcentaje < menor_progreso:
                    menor_progreso = porcentaje
                    categoria_recomendada = categoria
            
            if categoria_recomendada:
                frases = cls.FRASES_CONTEXTUALES.get(f'categoria_{categoria_recomendada}', 
                                                   ["¡Vamos a aprender algo nuevo!"])
                import random
                return {
                    'frase': random.choice(frases),
                    'categoria': categoria_recomendada,
                    'porcentaje': menor_progreso
                }
            
            return {
                'frase': "¡Vamos a aprender algo nuevo!",
                'categoria': 'lenguaje',
                'porcentaje': 0
            }
        except:
            return {
                'frase': "¡Vamos a aprender algo nuevo!",
                'categoria': 'lenguaje',
                'porcentaje': 0
            }
    
    @classmethod
    def generar_mensaje_diario(cls, nino_id):
        """Genera un mensaje diario personalizado para el niño"""
        try:
            nino = PerfilNino.query.get(nino_id)
            estadisticas = UserProgressSystem.obtener_estadisticas_dashboard(nino_id)
            
            # Mensaje basado en el progreso
            nivel = estadisticas.get('nivel_general', 'inicial')
            dias_consecutivos = estadisticas.get('dias_consecutivos', 0)
            actividades_completadas = estadisticas.get('actividades_completadas', 0)
            
            mensaje = f"¡Hola {nino.nombre}! "
            
            if dias_consecutivos > 0:
                mensaje += f"¡Qué bien que hayas venido {dias_consecutivos} días seguidos! "
            
            if actividades_completadas > 0:
                mensaje += f"Ya has completado {actividades_completadas} actividades. "
            
            # Agregar frase de progreso
            mensaje += cls.obtener_frase_progreso(nino_id)
            
            return mensaje
        except:
            return "¡Hola! ¿Listo para aprender algo nuevo hoy?"
    
    @classmethod
    def obtener_estado_emocional(cls, nino_id):
        """Determina el estado emocional del avatar basado en el progreso del niño"""
        try:
            estadisticas = UserProgressSystem.obtener_estadisticas_dashboard(nino_id)
            nivel = estadisticas.get('nivel_general', 'inicial')
            dias_consecutivos = estadisticas.get('dias_consecutivos', 0)
            
            if nivel in ['avanzado', 'experto'] and dias_consecutivos >= 3:
                return 'muy_feliz'
            elif nivel in ['intermedio', 'avanzado']:
                return 'feliz'
            elif nivel == 'basico':
                return 'animado'
            else:
                return 'motivador'
        except:
            return 'motivador'
    
    @classmethod
    def generar_animacion_avatar(cls, estado_emocional):
        """Genera la animación del avatar según su estado emocional"""
        animaciones = {
            'muy_feliz': {
                'emoji': '🎉',
                'color': '#FFD700',
                'animacion': 'bounce'
            },
            'feliz': {
                'emoji': '😊',
                'color': '#2ECC71',
                'animacion': 'pulse'
            },
            'animado': {
                'emoji': '🌟',
                'color': '#3498DB',
                'animacion': 'wiggle'
            },
            'motivador': {
                'emoji': '💪',
                'color': '#E74C3C',
                'animacion': 'glow'
            }
        }
        
        return animaciones.get(estado_emocional, animaciones['motivador'])

# Funciones de utilidad para las rutas
def obtener_frase_avatar(contexto, nino_id=None):
    """Obtiene una frase del avatar para un contexto específico"""
    return AvatarSystem.obtener_frase_contextual(contexto, nino_id)

def obtener_mensaje_diario(nino_id):
    """Obtiene el mensaje diario personalizado del avatar"""
    return AvatarSystem.generar_mensaje_diario(nino_id)

def obtener_recomendacion_actividad(nino_id):
    """Obtiene una recomendación de actividad del avatar"""
    return AvatarSystem.obtener_recomendacion_actividad(nino_id)





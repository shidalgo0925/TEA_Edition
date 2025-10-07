# -*- coding: utf-8 -*-
"""
Script para crear actividades adaptativas con diferentes niveles de dificultad
"""
from app import create_app
from app.extensions import db
from app.models.tea_models import ActividadTEA
import json

def create_adaptive_activities():
    app = create_app()
    
    with app.app_context():
        try:
            # Actividades de Lenguaje - Diferentes niveles
            actividades_lenguaje = [
                # Nivel Básico
                {
                    "titulo": "Repetir Palabras Simples",
                    "descripcion": "Imita las palabras básicas que dice la maestra",
                    "tipo": "imitacion",
                    "nivel_dificultad": "basico",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "palabras": ["mamá", "papá", "agua", "casa", "perro"],
                        "instrucciones": "Repite la palabra que escuches",
                        "tiempo_por_palabra": 3
                    }),
                    "puntos_recompensa": 10,
                    "tiempo_estimado": 5
                },
                {
                    "titulo": "Sonidos de Animales Básicos",
                    "descripcion": "Aprende los sonidos de animales familiares",
                    "tipo": "imitacion",
                    "nivel_dificultad": "basico",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "animales": [
                            {"nombre": "perro", "sonido": "guau guau"},
                            {"nombre": "gato", "sonido": "miau"},
                            {"nombre": "vaca", "sonido": "muu"}
                        ],
                        "instrucciones": "Repite el sonido del animal"
                    }),
                    "puntos_recompensa": 12,
                    "tiempo_estimado": 6
                },
                
                # Nivel Intermedio
                {
                    "titulo": "Frases Cortas",
                    "descripcion": "Construye frases de 2-3 palabras",
                    "tipo": "construccion",
                    "nivel_dificultad": "intermedio",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "frases": [
                            "mamá come",
                            "papá juega",
                            "agua fría",
                            "casa grande"
                        ],
                        "instrucciones": "Arma la frase con las palabras que veas"
                    }),
                    "puntos_recompensa": 15,
                    "tiempo_estimado": 8
                },
                {
                    "titulo": "Preguntas y Respuestas",
                    "descripcion": "Responde preguntas simples",
                    "tipo": "comprension",
                    "nivel_dificultad": "intermedio",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "preguntas": [
                            {"pregunta": "¿Cómo te llamas?", "respuesta": "Ana"},
                            {"pregunta": "¿Qué color es el sol?", "respuesta": "amarillo"},
                            {"pregunta": "¿Cuántos ojos tienes?", "respuesta": "dos"}
                        ],
                        "instrucciones": "Responde la pregunta que escuches"
                    }),
                    "puntos_recompensa": 18,
                    "tiempo_estimado": 10
                },
                
                # Nivel Avanzado
                {
                    "titulo": "Historias Cortas",
                    "descripcion": "Cuenta una historia con 3-4 oraciones",
                    "tipo": "narrativa",
                    "nivel_dificultad": "avanzado",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "historias": [
                            "El perro corre en el parque",
                            "La niña come una manzana roja",
                            "El gato duerme en la cama"
                        ],
                        "instrucciones": "Cuenta la historia que veas en las imágenes"
                    }),
                    "puntos_recompensa": 25,
                    "tiempo_estimado": 12
                }
            ]
            
            # Actividades de Números - Diferentes niveles
            actividades_numeros = [
                # Nivel Básico
                {
                    "titulo": "Contar del 1 al 5",
                    "descripcion": "Aprende a contar números básicos",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "basico",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": [1, 2, 3, 4, 5],
                        "instrucciones": "Cuenta los objetos que veas",
                        "objetos": ["manzanas", "pelotas", "cubos"]
                    }),
                    "puntos_recompensa": 10,
                    "tiempo_estimado": 5
                },
                {
                    "titulo": "Números con Dedos",
                    "descripcion": "Muestra números con los dedos",
                    "tipo": "imitacion",
                    "nivel_dificultad": "basico",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": [1, 2, 3, 4, 5],
                        "instrucciones": "Muestra con los dedos el número que veas"
                    }),
                    "puntos_recompensa": 12,
                    "tiempo_estimado": 6
                },
                
                # Nivel Intermedio
                {
                    "titulo": "Contar del 1 al 10",
                    "descripcion": "Extiende el conteo hasta 10",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "intermedio",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        "instrucciones": "Cuenta todos los objetos",
                        "objetos": ["estrellas", "flores", "coches"]
                    }),
                    "puntos_recompensa": 15,
                    "tiempo_estimado": 8
                },
                {
                    "titulo": "Sumas Simples",
                    "descripcion": "Resuelve sumas básicas",
                    "tipo": "operacion",
                    "nivel_dificultad": "intermedio",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "sumas": [
                            {"operacion": "2 + 1", "resultado": 3},
                            {"operacion": "1 + 2", "resultado": 3},
                            {"operacion": "3 + 1", "resultado": 4}
                        ],
                        "instrucciones": "Resuelve la suma que veas"
                    }),
                    "puntos_recompensa": 18,
                    "tiempo_estimado": 10
                },
                
                # Nivel Avanzado
                {
                    "titulo": "Contar hasta 20",
                    "descripcion": "Domina el conteo hasta 20",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "avanzado",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": list(range(1, 21)),
                        "instrucciones": "Cuenta todos los elementos",
                        "objetos": ["puntos", "líneas", "círculos"]
                    }),
                    "puntos_recompensa": 25,
                    "tiempo_estimado": 12
                }
            ]
            
            # Actividades de Colores - Diferentes niveles
            actividades_colores = [
                # Nivel Básico
                {
                    "titulo": "Colores Básicos",
                    "descripcion": "Reconoce los colores principales",
                    "tipo": "asociacion",
                    "nivel_dificultad": "basico",
                    "categoria": "colores",
                    "contenido": json.dumps({
                        "colores": ["rojo", "azul", "amarillo", "verde"],
                        "instrucciones": "Señala el color que te pida",
                        "objetos": ["manzana", "cielo", "sol", "hierba"]
                    }),
                    "puntos_recompensa": 10,
                    "tiempo_estimado": 5
                },
                
                # Nivel Intermedio
                {
                    "titulo": "Colores Secundarios",
                    "descripcion": "Aprende colores como naranja, morado, rosa",
                    "tipo": "asociacion",
                    "nivel_dificultad": "intermedio",
                    "categoria": "colores",
                    "contenido": json.dumps({
                        "colores": ["naranja", "morado", "rosa", "marrón"],
                        "instrucciones": "Identifica el color correcto",
                        "objetos": ["naranja", "uva", "flor", "tierra"]
                    }),
                    "puntos_recompensa": 15,
                    "tiempo_estimado": 8
                },
                
                # Nivel Avanzado
                {
                    "titulo": "Mezcla de Colores",
                    "descripcion": "Entiende cómo se forman los colores",
                    "tipo": "comprension",
                    "nivel_dificultad": "avanzado",
                    "categoria": "colores",
                    "contenido": json.dumps({
                        "mezclas": [
                            {"colores": ["rojo", "azul"], "resultado": "morado"},
                            {"colores": ["amarillo", "azul"], "resultado": "verde"},
                            {"colores": ["rojo", "amarillo"], "resultado": "naranja"}
                        ],
                        "instrucciones": "¿Qué color se forma al mezclar estos dos?"
                    }),
                    "puntos_recompensa": 25,
                    "tiempo_estimado": 12
                }
            ]
            
            # Actividades de Animales - Diferentes niveles
            actividades_animales = [
                # Nivel Básico
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
                    "puntos_recompensa": 12,
                    "tiempo_estimado": 6
                },
                
                # Nivel Intermedio
                {
                    "titulo": "Hábitats de Animales",
                    "descripcion": "Asocia animales con sus hogares",
                    "tipo": "asociacion",
                    "nivel_dificultad": "intermedio",
                    "categoria": "animales",
                    "contenido": json.dumps({
                        "asociaciones": [
                            {"animal": "pez", "habitat": "agua"},
                            {"animal": "pájaro", "habitat": "aire"},
                            {"animal": "conejo", "habitat": "tierra"}
                        ],
                        "instrucciones": "¿Dónde vive este animal?"
                    }),
                    "puntos_recompensa": 18,
                    "tiempo_estimado": 10
                },
                
                # Nivel Avanzado
                {
                    "titulo": "Características de Animales",
                    "descripcion": "Clasifica animales por sus características",
                    "tipo": "clasificacion",
                    "nivel_dificultad": "avanzado",
                    "categoria": "animales",
                    "contenido": json.dumps({
                        "clasificaciones": [
                            {"categoria": "mamíferos", "animales": ["perro", "gato", "vaca"]},
                            {"categoria": "aves", "animales": ["pollo", "pato", "águila"]},
                            {"categoria": "peces", "animales": ["pez dorado", "tiburón", "salmón"]}
                        ],
                        "instrucciones": "Agrupa los animales por su tipo"
                    }),
                    "puntos_recompensa": 25,
                    "tiempo_estimado": 12
                }
            ]
            
            # Combinar todas las actividades
            todas_actividades = (
                actividades_lenguaje + 
                actividades_numeros + 
                actividades_colores + 
                actividades_animales
            )
            
            # Crear actividades en la base de datos
            actividades_creadas = 0
            for act_data in todas_actividades:
                # Verificar si ya existe
                if not ActividadTEA.query.filter_by(titulo=act_data["titulo"]).first():
                    actividad = ActividadTEA(**act_data)
                    db.session.add(actividad)
                    actividades_creadas += 1
                    print(f"✅ Actividad creada: {act_data['titulo']} ({act_data['nivel_dificultad']})")
                else:
                    print(f"ℹ️ Actividad ya existe: {act_data['titulo']}")
            
            db.session.commit()
            print(f"\n🎉 ¡Actividades adaptativas creadas exitosamente!")
            print(f"📊 Total de actividades nuevas: {actividades_creadas}")
            print(f"📚 Categorías: Lenguaje, Números, Colores, Animales")
            print(f"🎯 Niveles: Básico, Intermedio, Avanzado")
            print(f"🧠 Sistema adaptativo listo para usar")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al crear actividades: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_adaptive_activities()






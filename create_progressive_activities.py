# -*- coding: utf-8 -*-
"""
Script para crear actividades con progresión incremental de dificultad
"""
from app import create_app
from app.extensions import db
from app.models.tea_models import ActividadTEA
import json

def create_progressive_activities():
    app = create_app()
    
    with app.app_context():
        try:
            # Actividades de Lenguaje - Progresión Incremental
            actividades_lenguaje = [
                # NIVEL INICIAL
                {
                    "titulo": "Primeras Palabras",
                    "descripcion": "Aprende tus primeras palabras básicas",
                    "tipo": "imitacion",
                    "nivel_dificultad": "inicial",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "palabras": ["mamá", "papá"],
                        "instrucciones": "Repite la palabra que escuches",
                        "tiempo_por_palabra": 5
                    }),
                    "puntos_recompensa": 5,
                    "tiempo_estimado": 3
                },
                
                # BÁSICO NIVEL 1
                {
                    "titulo": "Palabras Familiares",
                    "descripcion": "Aprende palabras de la familia",
                    "tipo": "imitacion",
                    "nivel_dificultad": "basico_1",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "palabras": ["mamá", "papá", "hermano", "hermana"],
                        "instrucciones": "Repite la palabra que escuches",
                        "tiempo_por_palabra": 4
                    }),
                    "puntos_recompensa": 8,
                    "tiempo_estimado": 4
                },
                
                # BÁSICO NIVEL 2
                {
                    "titulo": "Palabras de Casa",
                    "descripcion": "Aprende palabras de objetos de casa",
                    "tipo": "imitacion",
                    "nivel_dificultad": "basico_2",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "palabras": ["casa", "mesa", "silla", "cama", "puerta"],
                        "instrucciones": "Repite la palabra que escuches",
                        "tiempo_por_palabra": 3
                    }),
                    "puntos_recompensa": 10,
                    "tiempo_estimado": 5
                },
                
                # BÁSICO NIVEL 3
                {
                    "titulo": "Palabras de Comida",
                    "descripcion": "Aprende palabras de alimentos básicos",
                    "tipo": "imitacion",
                    "nivel_dificultad": "basico_3",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "palabras": ["agua", "leche", "pan", "manzana", "plátano"],
                        "instrucciones": "Repite la palabra que escuches",
                        "tiempo_por_palabra": 3
                    }),
                    "puntos_recompensa": 12,
                    "tiempo_estimado": 6
                },
                
                # INTERMEDIO NIVEL 1
                {
                    "titulo": "Frases de 2 Palabras",
                    "descripcion": "Construye frases simples de 2 palabras",
                    "tipo": "construccion",
                    "nivel_dificultad": "intermedio_1",
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
                
                # INTERMEDIO NIVEL 2
                {
                    "titulo": "Frases de 3 Palabras",
                    "descripcion": "Construye frases de 3 palabras",
                    "tipo": "construccion",
                    "nivel_dificultad": "intermedio_2",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "frases": [
                            "mamá come pan",
                            "papá juega fútbol",
                            "agua está fría",
                            "casa es grande"
                        ],
                        "instrucciones": "Arma la frase con las palabras que veas"
                    }),
                    "puntos_recompensa": 18,
                    "tiempo_estimado": 10
                },
                
                # INTERMEDIO NIVEL 3
                {
                    "titulo": "Preguntas Simples",
                    "descripcion": "Responde preguntas básicas",
                    "tipo": "comprension",
                    "nivel_dificultad": "intermedio_3",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "preguntas": [
                            {"pregunta": "¿Cómo te llamas?", "respuesta": "Ana"},
                            {"pregunta": "¿Qué color es el sol?", "respuesta": "amarillo"},
                            {"pregunta": "¿Cuántos ojos tienes?", "respuesta": "dos"}
                        ],
                        "instrucciones": "Responde la pregunta que escuches"
                    }),
                    "puntos_recompensa": 20,
                    "tiempo_estimado": 12
                },
                
                # AVANZADO NIVEL 1
                {
                    "titulo": "Historias Cortas",
                    "descripcion": "Cuenta historias de 3-4 oraciones",
                    "tipo": "narrativa",
                    "nivel_dificultad": "avanzado_1",
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
                    "tiempo_estimado": 15
                },
                
                # AVANZADO NIVEL 2
                {
                    "titulo": "Conversaciones",
                    "descripcion": "Mantén una conversación simple",
                    "tipo": "conversacion",
                    "nivel_dificultad": "avanzado_2",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "conversaciones": [
                            {"pregunta": "¿Qué hiciste hoy?", "respuesta": "Jugué con mis juguetes"},
                            {"pregunta": "¿Qué te gusta comer?", "respuesta": "Me gusta la pizza"},
                            {"pregunta": "¿Dónde vives?", "respuesta": "Vivo en una casa"}
                        ],
                        "instrucciones": "Responde como si estuvieras hablando con alguien"
                    }),
                    "puntos_recompensa": 30,
                    "tiempo_estimado": 18
                },
                
                # AVANZADO NIVEL 3
                {
                    "titulo": "Descripciones Detalladas",
                    "descripcion": "Describe objetos con detalles",
                    "tipo": "descripcion",
                    "nivel_dificultad": "avanzado_3",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "objetos": [
                            {"objeto": "manzana", "descripcion": "Es roja, dulce y redonda"},
                            {"objeto": "perro", "descripcion": "Es peludo, grande y amigable"},
                            {"objeto": "casa", "descripcion": "Es grande, blanca y tiene ventanas"}
                        ],
                        "instrucciones": "Describe el objeto con muchos detalles"
                    }),
                    "puntos_recompensa": 35,
                    "tiempo_estimado": 20
                },
                
                # NIVEL EXPERTO
                {
                    "titulo": "Historias Creativas",
                    "descripcion": "Crea tus propias historias",
                    "tipo": "creatividad",
                    "nivel_dificultad": "experto",
                    "categoria": "lenguaje",
                    "contenido": json.dumps({
                        "elementos": ["un dragón", "un castillo", "una princesa", "una varita mágica"],
                        "instrucciones": "Crea una historia usando estos elementos"
                    }),
                    "puntos_recompensa": 50,
                    "tiempo_estimado": 25
                }
            ]
            
            # Actividades de Números - Progresión Incremental
            actividades_numeros = [
                # NIVEL INICIAL
                {
                    "titulo": "Números 1 y 2",
                    "descripcion": "Aprende los primeros números",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "inicial",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": [1, 2],
                        "instrucciones": "Cuenta los objetos que veas",
                        "objetos": ["manzanas", "pelotas"]
                    }),
                    "puntos_recompensa": 5,
                    "tiempo_estimado": 3
                },
                
                # BÁSICO NIVEL 1
                {
                    "titulo": "Números del 1 al 3",
                    "descripcion": "Aprende a contar hasta 3",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "basico_1",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": [1, 2, 3],
                        "instrucciones": "Cuenta los objetos que veas",
                        "objetos": ["cubos", "flores", "estrellas"]
                    }),
                    "puntos_recompensa": 8,
                    "tiempo_estimado": 4
                },
                
                # BÁSICO NIVEL 2
                {
                    "titulo": "Números del 1 al 5",
                    "descripcion": "Aprende a contar hasta 5",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "basico_2",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": [1, 2, 3, 4, 5],
                        "instrucciones": "Cuenta los objetos que veas",
                        "objetos": ["manzanas", "pelotas", "cubos", "flores", "estrellas"]
                    }),
                    "puntos_recompensa": 10,
                    "tiempo_estimado": 5
                },
                
                # BÁSICO NIVEL 3
                {
                    "titulo": "Números con Dedos",
                    "descripcion": "Muestra números con los dedos",
                    "tipo": "imitacion",
                    "nivel_dificultad": "basico_3",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": [1, 2, 3, 4, 5],
                        "instrucciones": "Muestra con los dedos el número que veas"
                    }),
                    "puntos_recompensa": 12,
                    "tiempo_estimado": 6
                },
                
                # INTERMEDIO NIVEL 1
                {
                    "titulo": "Números del 1 al 10",
                    "descripcion": "Aprende a contar hasta 10",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "intermedio_1",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        "instrucciones": "Cuenta todos los objetos",
                        "objetos": ["estrellas", "flores", "coches", "puntos"]
                    }),
                    "puntos_recompensa": 15,
                    "tiempo_estimado": 8
                },
                
                # INTERMEDIO NIVEL 2
                {
                    "titulo": "Sumas Simples",
                    "descripcion": "Resuelve sumas básicas",
                    "tipo": "operacion",
                    "nivel_dificultad": "intermedio_2",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "sumas": [
                            {"operacion": "2 + 1", "resultado": 3},
                            {"operacion": "1 + 2", "resultado": 3},
                            {"operacion": "3 + 1", "resultado": 4},
                            {"operacion": "2 + 2", "resultado": 4}
                        ],
                        "instrucciones": "Resuelve la suma que veas"
                    }),
                    "puntos_recompensa": 18,
                    "tiempo_estimado": 10
                },
                
                # INTERMEDIO NIVEL 3
                {
                    "titulo": "Restas Simples",
                    "descripcion": "Resuelve restas básicas",
                    "tipo": "operacion",
                    "nivel_dificultad": "intermedio_3",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "restas": [
                            {"operacion": "3 - 1", "resultado": 2},
                            {"operacion": "4 - 2", "resultado": 2},
                            {"operacion": "5 - 1", "resultado": 4},
                            {"operacion": "3 - 2", "resultado": 1}
                        ],
                        "instrucciones": "Resuelve la resta que veas"
                    }),
                    "puntos_recompensa": 20,
                    "tiempo_estimado": 12
                },
                
                # AVANZADO NIVEL 1
                {
                    "titulo": "Números del 1 al 20",
                    "descripcion": "Aprende a contar hasta 20",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "avanzado_1",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": list(range(1, 21)),
                        "instrucciones": "Cuenta todos los elementos",
                        "objetos": ["puntos", "líneas", "círculos", "cuadrados"]
                    }),
                    "puntos_recompensa": 25,
                    "tiempo_estimado": 15
                },
                
                # AVANZADO NIVEL 2
                {
                    "titulo": "Sumas y Restas Mixtas",
                    "descripcion": "Resuelve operaciones mixtas",
                    "tipo": "operacion",
                    "nivel_dificultad": "avanzado_2",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "operaciones": [
                            {"operacion": "5 + 3", "resultado": 8},
                            {"operacion": "7 - 2", "resultado": 5},
                            {"operacion": "4 + 4", "resultado": 8},
                            {"operacion": "9 - 3", "resultado": 6}
                        ],
                        "instrucciones": "Resuelve la operación que veas"
                    }),
                    "puntos_recompensa": 30,
                    "tiempo_estimado": 18
                },
                
                # AVANZADO NIVEL 3
                {
                    "titulo": "Problemas de Palabras",
                    "descripcion": "Resuelve problemas matemáticos simples",
                    "tipo": "resolucion_problemas",
                    "nivel_dificultad": "avanzado_3",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "problemas": [
                            {"problema": "Ana tiene 3 manzanas y come 1. ¿Cuántas le quedan?", "respuesta": 2},
                            {"problema": "Pedro tiene 2 pelotas y compra 3 más. ¿Cuántas tiene en total?", "respuesta": 5}
                        ],
                        "instrucciones": "Resuelve el problema que escuches"
                    }),
                    "puntos_recompensa": 35,
                    "tiempo_estimado": 20
                },
                
                # NIVEL EXPERTO
                {
                    "titulo": "Números del 1 al 100",
                    "descripcion": "Domina el conteo hasta 100",
                    "tipo": "reconocimiento",
                    "nivel_dificultad": "experto",
                    "categoria": "numeros",
                    "contenido": json.dumps({
                        "numeros": list(range(1, 101)),
                        "instrucciones": "Cuenta todos los elementos hasta 100",
                        "objetos": ["puntos", "números", "objetos variados"]
                    }),
                    "puntos_recompensa": 50,
                    "tiempo_estimado": 25
                }
            ]
            
            # Combinar todas las actividades
            todas_actividades = actividades_lenguaje + actividades_numeros
            
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
            print(f"\n🎉 ¡Actividades progresivas creadas exitosamente!")
            print(f"📊 Total de actividades nuevas: {actividades_creadas}")
            print(f"📚 Categorías: Lenguaje, Números")
            print(f"🎯 Niveles: Inicial → Básico (1-3) → Intermedio (1-3) → Avanzado (1-3) → Experto")
            print(f"📈 Progresión incremental implementada")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al crear actividades: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_progressive_activities()






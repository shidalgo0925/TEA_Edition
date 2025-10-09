# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, session
from app.extensions import db
from app.models.tea_models import (
    PerfilNino, ActividadTEA, SesionTEA, SesionActividad, 
    ProgresoTEA, LogroNino, RecompensaTEA
)
from datetime import datetime
from .test_data import ensure_test_data
from app.services.adaptive_learning import (
    AdaptiveLearningSystem, obtener_actividades_adaptativas, 
    generar_plan_sesion_adaptativo
)
from app.services.progressive_learning import (
    ProgressiveLearningSystem, obtener_actividades_progresivas,
    generar_plan_progresivo
)
from app.services.permanent_progression import (
    evaluar_progreso_actividad, obtener_actividades_disponibles_nino,
    obtener_estadisticas_progresion_nino
)
from app.services.user_progress import actualizar_progreso_actividad

actividades_bp = Blueprint('actividades', __name__, url_prefix='/actividades')

@actividades_bp.route('/')
@actividades_bp.route('')
def lista_actividades():
    """Lista de actividades progresivas recomendadas"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    if not nino:
        return render_template('tea/error.html', 
                             mensaje="No hay perfil de niño configurado")
    
    # Obtener avatar actual del niño
    from app.models.tea_models import AvatarUsuario, Avatar
    avatar_usuario = AvatarUsuario.query.filter_by(
        usuario_id=nino.id,
        tipo_usuario='nino',
        activo=True
    ).first()
    
    avatar_actual = None
    if avatar_usuario:
        avatar_actual = avatar_usuario.avatar
    
    # Si no hay avatar seleccionado, usar el avatar por defecto
    if not avatar_actual:
        avatar_actual = Avatar.query.filter_by(nombre='Spider-Man').first()
    
    # Obtener actividades progresivas recomendadas
    sistema_progresivo = ProgressiveLearningSystem(nino.id)
    recomendaciones = obtener_actividades_progresivas(nino.id, limite=8)
    
    # Generar plan de sesión progresivo
    plan_sesion = generar_plan_progresivo(nino.id, duracion=nino.tiempo_sesion_min)
    
    # Obtener actividades para mostrar en la lista
    actividades = ActividadTEA.query.filter_by(activa=True).limit(6).all()
    
    return render_template('tea/actividades_lista.html',
                         nino=nino,
                         avatar_actual=avatar_actual,
                         recomendaciones=recomendaciones,
                         plan_sesion=plan_sesion,
                         actividades=actividades)

@actividades_bp.route('/<int:actividad_id>')
def realizar_actividad(actividad_id):
    """Realizar una actividad específica"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividad = ActividadTEA.query.get_or_404(actividad_id)
    
    # Obtener avatar actual del niño
    from app.models.tea_models import AvatarUsuario, Avatar
    avatar_usuario = AvatarUsuario.query.filter_by(
        usuario_id=nino.id,
        tipo_usuario='nino',
        activo=True
    ).first()
    
    avatar_actual = None
    if avatar_usuario:
        avatar_actual = avatar_usuario.avatar
    
    # Si no hay avatar seleccionado, usar el avatar por defecto
    if not avatar_actual:
        avatar_actual = Avatar.query.filter_by(nombre='Spider-Man').first()
    
    # Obtener o crear sesión de hoy
    hoy = datetime.now().date()
    sesion = SesionTEA.query.filter(
        db.func.date(SesionTEA.fecha) == hoy,
        SesionTEA.nino_id == nino.id
    ).first()
    
    if not sesion:
        sesion = SesionTEA(
            nino_id=nino.id,
            estado='iniciada'
        )
        db.session.add(sesion)
        db.session.commit()
    
    return render_template('tea/actividad_detalle.html',
                         nino=nino,
                         actividad=actividad,
                         sesion=sesion,
                         avatar_actual=avatar_actual)

@actividades_bp.route('/api/completar/<int:actividad_id>', methods=['POST'])
def api_completar_actividad(actividad_id):
    """API para completar una actividad"""
    try:
        data = request.get_json()
        nino = PerfilNino.query.first()
        actividad = ActividadTEA.query.get_or_404(actividad_id)
        
        # Obtener o crear sesión de hoy
        hoy = datetime.now().date()
        sesion = SesionTEA.query.filter(
            db.func.date(SesionTEA.fecha) == hoy,
            SesionTEA.nino_id == nino.id
        ).first()
        
        if not sesion:
            sesion = SesionTEA(
                nino_id=nino.id,
                estado='iniciada'
            )
            db.session.add(sesion)
            db.session.commit()
        
        # Crear o actualizar sesión-actividad
        sesion_actividad = SesionActividad.query.filter_by(
            sesion_id=sesion.id,
            actividad_id=actividad_id
        ).first()
        
        if not sesion_actividad:
            sesion_actividad = SesionActividad(
                sesion_id=sesion.id,
                actividad_id=actividad_id,
                orden=1,
                intentos=1,
                tiempo_dedicado=data.get('tiempo_dedicado', 0),
                puntos_obtenidos=actividad.puntos_recompensa,
                fecha_completada=datetime.now()
            )
            db.session.add(sesion_actividad)
        else:
            sesion_actividad.intentos += 1
            sesion_actividad.completada = True
            sesion_actividad.puntos_obtenidos = actividad.puntos_recompensa
            sesion_actividad.fecha_completada = datetime.now()
        
        # Actualizar sesión
        sesion.actividades_completadas += 1
        sesion.puntos_ganados += actividad.puntos_recompensa
        sesion.duracion_minutos += data.get('tiempo_dedicado', 0) // 60
        
        # Actualizar progreso con sistema de progresión permanente
        exito = data.get('exito', True)  # Por defecto considerar exitoso
        evaluar_progreso_actividad(
            nino.id, 
            actividad_id, 
            actividad.puntos_recompensa, 
            exito
        )
        
        # Actualizar progreso real del usuario
        actualizar_progreso_actividad(
            nino.id,
            actividad_id,
            actividad.puntos_recompensa
        )
        
        # Mantener compatibilidad con sistema anterior
        progreso = ProgresoTEA.query.filter_by(
            nino_id=nino.id,
            habilidad=actividad.categoria
        ).first()
        
        if progreso:
            progreso.puntos_totales += actividad.puntos_recompensa
            progreso.sesiones_completadas += 1
            progreso.racha_dias = 1  # Simplificado para demo
            progreso.ultima_actualizacion = datetime.now()
        else:
            progreso = ProgresoTEA(
                nino_id=nino.id,
                habilidad=actividad.categoria,
                nivel_actual=nino.nivel_dificultad,
                puntos_totales=actividad.puntos_recompensa,
                sesiones_completadas=1,
                racha_dias=1,
                ultima_actualizacion=datetime.now()
            )
            db.session.add(progreso)
        
        # Analizar si necesita ajustar el nivel de dificultad progresivo
        sistema_progresivo = ProgressiveLearningSystem(nino.id)
        nivel_actualizado = sistema_progresivo.actualizar_nivel_progresion(actividad.categoria)
        
        if nivel_actualizado:
            print(f"🎯 Nivel actualizado para {actividad.categoria}")
        
        db.session.commit()
        
        # Verificar si desbloquea recompensa
        recompensas_desbloqueadas = []
        recompensas = RecompensaTEA.query.filter(
            RecompensaTEA.puntos_requeridos <= progreso.puntos_totales
        ).all()
        
        for recompensa in recompensas:
            # Verificar si ya la tiene
            logro_existente = LogroNino.query.filter_by(
                nino_id=nino.id,
                recompensa_id=recompensa.id
            ).first()
            
            if not logro_existente:
                logro = LogroNino(
                    nino_id=nino.id,
                    recompensa_id=recompensa.id,
                    sesion_id=sesion.id
                )
                db.session.add(logro)
                recompensas_desbloqueadas.append(recompensa)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'puntos_ganados': actividad.puntos_recompensa,
            'recompensas_desbloqueadas': [
                {
                    'nombre': r.nombre,
                    'icono': r.icono_url,
                    'descripcion': r.descripcion
                } for r in recompensas_desbloqueadas
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@actividades_bp.route('/lenguaje')
def actividades_lenguaje():
    """Actividades de lenguaje"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividades = ActividadTEA.query.filter_by(
        categoria='lenguaje',
        activa=True
    ).all()
    
    # Obtener avatar actual del niño
    from app.models.tea_models import AvatarUsuario, Avatar
    avatar_usuario = AvatarUsuario.query.filter_by(
        usuario_id=nino.id,
        tipo_usuario='nino',
        activo=True
    ).first()
    
    avatar_actual = None
    if avatar_usuario:
        avatar_actual = avatar_usuario.avatar
    
    # Si no hay avatar seleccionado, usar el avatar por defecto
    if not avatar_actual:
        avatar_actual = Avatar.query.filter_by(nombre='Spider-Man').first()
    
    return render_template('tea/actividades_categoria.html',
                         nino=nino,
                         actividades=actividades,
                         categoria='Lenguaje',
                         icono='🗣️',
                         avatar_actual=avatar_actual)

@actividades_bp.route('/numeros')
def actividades_numeros():
    """Actividades de números"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividades = ActividadTEA.query.filter_by(
        categoria='numeros',
        activa=True
    ).all()
    
    # Obtener avatar actual del niño
    from app.models.tea_models import AvatarUsuario, Avatar
    avatar_usuario = AvatarUsuario.query.filter_by(
        usuario_id=nino.id,
        tipo_usuario='nino',
        activo=True
    ).first()
    
    avatar_actual = None
    if avatar_usuario:
        avatar_actual = avatar_usuario.avatar
    
    # Si no hay avatar seleccionado, usar el avatar por defecto
    if not avatar_actual:
        avatar_actual = Avatar.query.filter_by(nombre='Spider-Man').first()
    
    return render_template('tea/actividades_categoria.html',
                         nino=nino,
                         actividades=actividades,
                         categoria='Números',
                         icono='🔢',
                         avatar_actual=avatar_actual)

@actividades_bp.route('/colores')
def actividades_colores():
    """Actividades de colores"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividades = ActividadTEA.query.filter_by(
        categoria='colores',
        activa=True
    ).all()
    
    # Obtener avatar actual del niño
    from app.models.tea_models import AvatarUsuario, Avatar
    avatar_usuario = AvatarUsuario.query.filter_by(
        usuario_id=nino.id,
        tipo_usuario='nino',
        activo=True
    ).first()
    
    avatar_actual = None
    if avatar_usuario:
        avatar_actual = avatar_usuario.avatar
    
    # Si no hay avatar seleccionado, usar el avatar por defecto
    if not avatar_actual:
        avatar_actual = Avatar.query.filter_by(nombre='Spider-Man').first()
    
    return render_template('tea/actividades_categoria.html',
                         nino=nino,
                         actividades=actividades,
                         categoria='Colores',
                         icono='🎨',
                         avatar_actual=avatar_actual)

@actividades_bp.route('/animales')
def actividades_animales():
    """Actividades de animales"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    actividades = ActividadTEA.query.filter_by(
        categoria='animales',
        activa=True
    ).all()
    
    # Obtener avatar actual del niño
    from app.models.tea_models import AvatarUsuario, Avatar
    avatar_usuario = AvatarUsuario.query.filter_by(
        usuario_id=nino.id,
        tipo_usuario='nino',
        activo=True
    ).first()
    
    avatar_actual = None
    if avatar_usuario:
        avatar_actual = avatar_usuario.avatar
    
    # Si no hay avatar seleccionado, usar el avatar por defecto
    if not avatar_actual:
        avatar_actual = Avatar.query.filter_by(nombre='Spider-Man').first()
    
    return render_template('tea/actividades_categoria.html',
                         nino=nino,
                         actividades=actividades,
                         categoria='Animales',
                         icono='🐶',
                         avatar_actual=avatar_actual)

@actividades_bp.route('/api/recomendaciones')
def api_recomendaciones():
    """API para obtener recomendaciones progresivas"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    if not nino:
        return jsonify({'error': 'No hay perfil de niño'}), 404
    
    recomendaciones = obtener_actividades_progresivas(nino.id, limite=5)
    
    # Formatear recomendaciones para JSON
    recomendaciones_json = []
    for rec in recomendaciones:
        actividad = rec['actividad']
        recomendaciones_json.append({
            'id': actividad.id,
            'titulo': actividad.titulo,
            'descripcion': actividad.descripcion,
            'categoria': actividad.categoria,
            'nivel_dificultad': actividad.nivel_dificultad,
            'puntos_recompensa': actividad.puntos_recompensa,
            'tiempo_estimado': actividad.tiempo_estimado,
            'score_progresion': round(rec['score'], 2),
            'nivel_objetivo': rec['nivel_objetivo'],
            'motivo_progresion': rec['motivo_progresion'],
            'evaluacion': {
                'puede_avanzar': rec['evaluacion']['puede_avanzar'],
                'tasa_exito': round(rec['evaluacion']['tasa_exito'], 2),
                'puntos_totales': rec['evaluacion']['puntos_totales']
            }
        })
    
    return jsonify({
        'recomendaciones': recomendaciones_json,
        'nino': {
            'nombre': nino.nombre,
            'nivel_dificultad': nino.nivel_dificultad,
            'tiempo_sesion_min': nino.tiempo_sesion_min
        },
        'tipo': 'progresivo'
    })

@actividades_bp.route('/api/plan-sesion')
def api_plan_sesion():
    """API para generar plan de sesión progresivo"""
    ensure_test_data()
    
    nino = PerfilNino.query.first()
    if not nino:
        return jsonify({'error': 'No hay perfil de niño'}), 404
    
    duracion = request.args.get('duracion', nino.tiempo_sesion_min, type=int)
    plan = generar_plan_progresivo(nino.id, duracion=duracion)
    
    # Formatear plan para JSON
    plan_json = []
    for item in plan['plan']:
        actividad = item['actividad']
        plan_json.append({
            'orden': item['orden'],
            'actividad_id': actividad.id,
            'titulo': actividad.titulo,
            'categoria': actividad.categoria,
            'nivel_dificultad': actividad.nivel_dificultad,
            'tiempo_estimado': item['tiempo_estimado'],
            'nivel_objetivo': item['nivel_objetivo'],
            'motivo_progresion': item['motivo_progresion'],
            'score_progresion': round(item['score_progresion'], 2)
        })
    
    return jsonify({
        'plan': plan_json,
        'tiempo_total_estimado': plan['tiempo_total_estimado'],
        'actividades_incluidas': plan['actividades_incluidas'],
        'fecha_generacion': plan['fecha_generacion'].isoformat(),
        'tipo': 'progresivo'
    })

@actividades_bp.route('/categoria/<categoria>')
def categoria_actividades(categoria):
    """Mostrar actividades de una categoría específica"""
    try:
        # Obtener actividades de la categoría
        actividades = ActividadTEA.query.filter_by(
            categoria=categoria, 
            activa=True
        ).all()
        
        # Obtener progreso del niño en esta categoría
        nino = PerfilNino.query.first()
        progreso = None
        if nino:
            from app.services.user_progress import UserProgressSystem
            progreso = UserProgressSystem.obtener_progreso_categoria(nino.id, categoria)
            
            # Obtener avatar actual del niño
            from app.models.tea_models import AvatarUsuario, Avatar
            avatar_usuario = AvatarUsuario.query.filter_by(
                usuario_id=nino.id,
                tipo_usuario='nino',
                activo=True
            ).first()
            
            avatar_actual = None
            if avatar_usuario:
                avatar_actual = avatar_usuario.avatar
            
            # Si no hay avatar seleccionado, usar el avatar por defecto
            if not avatar_actual:
                avatar_actual = Avatar.query.filter_by(nombre='Spider-Man').first()
        
        # Configurar información de la categoría
        categoria_info = {
            'lenguaje': {
                'icono': '🗣️',
                'descripcion': 'Practica palabras, frases y conversaciones'
            },
            'numeros': {
                'icono': '🔢',
                'descripcion': 'Cuenta, suma, resta y resuelve problemas'
            },
            'colores': {
                'icono': '🎨',
                'descripcion': 'Reconoce y mezcla colores'
            },
            'animales': {
                'icono': '🐶',
                'descripcion': 'Conoce animales y sus sonidos'
            }
        }
        
        info = categoria_info.get(categoria, {
            'icono': '🎯',
            'descripcion': 'Actividades de aprendizaje'
        })
        
        # Preparar datos para el template
        actividades_data = []
        for actividad in actividades:
            # Determinar estado de la actividad
            estado = 'available'
            if progreso:
                # Lógica para determinar si está completada, en progreso, etc.
                # Por ahora, todas están disponibles
                pass
            
            actividades_data.append({
                'id': actividad.id,
                'titulo': actividad.titulo,
                'descripcion': actividad.descripcion or 'Actividad de aprendizaje',
                'icono': '🎯',
                'estado': estado,
                'puntos_recompensa': actividad.puntos_recompensa
            })
        
        return render_template('tea/categoria_actividades.html',
                             categoria=categoria,
                             categoria_icono=info['icono'],
                             categoria_descripcion=info['descripcion'],
                             actividades=actividades_data,
                             progreso_porcentaje=progreso['porcentaje_completado'] if progreso else 0,
                             actividades_completadas=progreso['actividades_completadas'] if progreso else 0,
                             actividades_totales=progreso['actividades_totales'] if progreso else len(actividades),
                             avatar_actual=avatar_actual)
        
    except Exception as e:
        # Fallback a datos mock
        actividades_mock = [
            {
                'id': 1,
                'titulo': f'Actividad 1 de {categoria}',
                'descripcion': 'Descripción de la actividad',
                'icono': '🎯',
                'estado': 'available',
                'puntos_recompensa': 10
            }
        ]
        
        categoria_info = {
            'lenguaje': {'icono': '🗣️', 'descripcion': 'Practica palabras y sonidos'},
            'numeros': {'icono': '🔢', 'descripcion': 'Aprende a contar'},
            'colores': {'icono': '🎨', 'descripcion': 'Reconoce los colores'},
            'animales': {'icono': '🐶', 'descripcion': 'Conoce los animales'}
        }
        
        info = categoria_info.get(categoria, {'icono': '🎯', 'descripcion': 'Actividades de aprendizaje'})
        
        # Obtener avatar por defecto para el fallback
        from app.models.tea_models import Avatar
        avatar_actual = Avatar.query.filter_by(nombre='Spider-Man').first()
        
        return render_template('tea/categoria_actividades.html',
                             categoria=categoria,
                             categoria_icono=info['icono'],
                             categoria_descripcion=info['descripcion'],
                             actividades=actividades_mock,
                             progreso_porcentaje=0,
                             actividades_completadas=0,
                             actividades_totales=1,
                             avatar_actual=avatar_actual)

@actividades_bp.route('/api/categoria/<categoria>')
def api_categoria_actividades(categoria):
    """API para obtener actividades de una categoría específica"""
    try:
        # Obtener actividades de la categoría
        actividades = ActividadTEA.query.filter_by(
            categoria=categoria, 
            activa=True
        ).all()
        
        # Obtener progreso del niño
        nino = PerfilNino.query.first()
        progreso = None
        if nino:
            from app.services.user_progress import UserProgressSystem
            progreso = UserProgressSystem.obtener_progreso_categoria(nino.id, categoria)
        
        # Preparar datos
        actividades_data = []
        for actividad in actividades:
            estado = 'available'
            if progreso:
                # Lógica para determinar estado
                pass
            
            actividades_data.append({
                'id': actividad.id,
                'titulo': actividad.titulo,
                'descripcion': actividad.descripcion or 'Actividad de aprendizaje',
                'icono': '🎯',
                'estado': estado,
                'puntos_recompensa': actividad.puntos_recompensa,
                'tiempo_estimado': actividad.tiempo_estimado
            })
        
        return jsonify({
            'success': True,
            'actividades': actividades_data,
            'progreso': progreso
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'actividades': []
        })

@actividades_bp.route('/mapa')
def mapa_mundos():
    """Mostrar el mapa de mundos desbloqueables"""
    try:
        nino = PerfilNino.query.first()
        if not nino:
            return render_template('tea/error.html', 
                                 mensaje="No hay perfil de niño configurado")
        
        # Obtener progreso del niño
        from app.services.user_progress import UserProgressSystem
        estadisticas = UserProgressSystem.obtener_estadisticas_dashboard(nino.id)
        
        return render_template('tea/mapa_mundos.html',
                             nino=nino,
                             estadisticas=estadisticas)
        
    except Exception as e:
        return render_template('tea/error.html', 
                             mensaje=f"Error cargando mapa: {str(e)}")

@actividades_bp.route('/api/mapa-zonas')
def api_mapa_zonas():
    """API para obtener datos del mapa de zonas"""
    try:
        nino = PerfilNino.query.first()
        if not nino:
            return jsonify({
                'success': False,
                'error': 'No hay perfil de niño configurado'
            })
        
        # Obtener progreso del niño
        from app.services.user_progress import UserProgressSystem
        estadisticas = UserProgressSystem.obtener_estadisticas_dashboard(nino.id)
        progreso_categorias = estadisticas.get('progreso_por_categoria', {})
        
        # Calcular progreso general
        total_completadas = estadisticas.get('actividades_completadas', 0)
        total_actividades = ActividadTEA.query.count()
        porcentaje_general = (total_completadas / total_actividades * 100) if total_actividades > 0 else 0
        
        # Determinar estado de cada zona
        zonas = {}
        for categoria in ['lenguaje', 'numeros', 'colores', 'animales']:
            progreso = progreso_categorias.get(categoria, {})
            completadas = progreso.get('actividades_completadas', 0)
            totales = progreso.get('actividades_totales', 0)
            porcentaje = progreso.get('porcentaje_completado', 0)
            
            # Determinar estado de la zona
            if categoria in ['lenguaje', 'numeros']:
                # Zonas iniciales siempre disponibles
                estado = 'available'
            elif total_completadas >= 15:
                # Desbloquear colores después de 15 actividades
                estado = 'available'
            elif total_completadas >= 20:
                # Desbloquear animales después de 20 actividades
                estado = 'available'
            else:
                estado = 'locked'
            
            zonas[categoria] = {
                'estado': estado,
                'actividades_completadas': completadas,
                'actividades_totales': totales,
                'porcentaje_completado': porcentaje,
                'nivel': 1 if estado == 'available' else 2
            }
        
        return jsonify({
            'success': True,
            'zonas': zonas,
            'progreso_general': {
                'completadas': total_completadas,
                'totales': total_actividades,
                'porcentaje': round(porcentaje_general, 1)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'zonas': {},
            'progreso_general': {
                'completadas': 0,
                'totales': 0,
                'porcentaje': 0
            }
        })






# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from sqlalchemy.orm import relationship

class PerfilNino(db.Model):
    """Perfil del niño con TEA"""
    __tablename__ = 'perfil_nino'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    nivel_dificultad = Column(String(20), default='basico')  # basico, intermedio, avanzado
    tiempo_sesion_min = Column(Integer, default=15)  # minutos por sesión
    avatar_preferido = Column(String(50), default='maestra_ana')
    
    # Sistema de progresión permanente
    nivel_inicial_configurado = Column(String(20), default='inicial')  # Nivel configurado por educador
    nivel_progresion_actual = Column(String(20), default='inicial')  # Nivel actual alcanzado
    nivel_maximo_alcanzado = Column(String(20), default='inicial')  # Nivel más alto alcanzado
    puntos_totales_acumulados = Column(Integer, default=0)  # Puntos totales ganados
    actividades_completadas_total = Column(Integer, default=0)  # Total de actividades completadas
    dias_consecutivos = Column(Integer, default=0)  # Días consecutivos de uso
    fecha_ultima_actividad = Column(DateTime, nullable=True)  # Última vez que jugó
    
    # padre_id = Column(Integer, ForeignKey('usuario_padre.id'), nullable=True)  # Temporalmente comentado
    creado_en = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    sesiones = relationship("SesionTEA", back_populates="nino")
    progresos = relationship("ProgresoTEA", back_populates="nino")
    # padre = relationship("UsuarioPadre", back_populates="ninos")  # Temporalmente comentado

class ActividadTEA(db.Model):
    """Actividades de terapia de lenguaje para TEA"""
    __tablename__ = 'actividades_tea'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(50), nullable=False)  # imitacion, asociacion, construccion, reconocimiento
    nivel_dificultad = Column(String(20), nullable=False)  # basico, intermedio, avanzado
    categoria = Column(String(50), nullable=False)  # lenguaje, numeros, colores, animales
    contenido = Column(Text, nullable=False)  # JSON con datos de la actividad
    imagen_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    puntos_recompensa = Column(Integer, default=10)
    tiempo_estimado = Column(Integer, default=5)  # minutos
    activa = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    sesiones_actividades = relationship("SesionActividad", back_populates="actividad")

class SesionTEA(db.Model):
    """Sesiones diarias del niño"""
    __tablename__ = 'sesiones_tea'
    
    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey('perfil_nino.id'), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    duracion_minutos = Column(Integer, default=0)
    actividades_completadas = Column(Integer, default=0)
    puntos_ganados = Column(Integer, default=0)
    estado = Column(String(20), default='iniciada')  # iniciada, completada, pausada
    notas = Column(Text, nullable=True)
    
    # Relaciones
    nino = relationship("PerfilNino", back_populates="sesiones")
    actividades = relationship("SesionActividad", back_populates="sesion")

class SesionActividad(db.Model):
    """Actividades dentro de una sesión"""
    __tablename__ = 'sesion_actividades'
    
    id = Column(Integer, primary_key=True)
    sesion_id = Column(Integer, ForeignKey('sesiones_tea.id'), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividades_tea.id'), nullable=False)
    orden = Column(Integer, nullable=False)
    completada = Column(Boolean, default=False)
    intentos = Column(Integer, default=0)
    tiempo_dedicado = Column(Integer, default=0)  # segundos
    puntos_obtenidos = Column(Integer, default=0)
    feedback = Column(Text, nullable=True)
    fecha_completada = Column(DateTime, nullable=True)
    
    # Relaciones
    sesion = relationship("SesionTEA", back_populates="actividades")
    actividad = relationship("ActividadTEA", back_populates="sesiones_actividades")

class ProgresoTEA(db.Model):
    """Progreso del niño en diferentes habilidades"""
    __tablename__ = 'progreso_tea'
    
    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey('perfil_nino.id'), nullable=False)
    habilidad = Column(String(50), nullable=False)  # lenguaje, numeros, colores, etc.
    nivel_actual = Column(String(20), nullable=False)
    puntos_totales = Column(Integer, default=0)
    sesiones_completadas = Column(Integer, default=0)
    racha_dias = Column(Integer, default=0)  # días consecutivos
    ultima_actualizacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    nino = relationship("PerfilNino", back_populates="progresos")

class RecompensaTEA(db.Model):
    """Sistema de recompensas y logros"""
    __tablename__ = 'recompensas_tea'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(30), nullable=False)  # estrella, sticker, badge, animacion
    icono_url = Column(String(500), nullable=True)
    puntos_requeridos = Column(Integer, nullable=False)
    categoria = Column(String(50), nullable=True)  # diario, semanal, especial
    activa = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

class LogroNino(db.Model):
    """Logros desbloqueados por el niño"""
    __tablename__ = 'logros_nino'
    
    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey('perfil_nino.id'), nullable=False)
    recompensa_id = Column(Integer, ForeignKey('recompensas_tea.id'), nullable=False)
    fecha_obtenido = Column(DateTime, default=datetime.utcnow)
    sesion_id = Column(Integer, ForeignKey('sesiones_tea.id'), nullable=True)
    
    # Relaciones
    nino = relationship("PerfilNino")
    recompensa = relationship("RecompensaTEA")
    sesion = relationship("SesionTEA")

class UsuarioPadre(db.Model):
    """Usuario padre/tutor del niño"""
    __tablename__ = 'usuario_padre'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(500), nullable=False)
    telefono = Column(String(20))
    relacion_nino = Column(String(50), default='padre')  # padre, madre, tutor, abuelo, etc.
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    ultimo_acceso = Column(DateTime)
    
    # Relaciones
    # ninos = relationship("PerfilNino", back_populates="padre")  # Temporalmente comentado
    
    def set_password(self, password):
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        # Para usuarios de prueba con hash fijo
        if self.password_hash == 'pbkdf2:sha256:260000$test$test' and password == '123':
            return True
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<UsuarioPadre {self.email}>'

class UsuarioNino(db.Model):
    """Usuario niño (perfil simplificado)"""
    __tablename__ = 'usuario_nino'
    
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(500), nullable=False)
    perfil_nino_id = Column(Integer, ForeignKey('perfil_nino.id'), nullable=False)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    ultimo_acceso = Column(DateTime)
    
    # Relaciones
    perfil = relationship("PerfilNino", backref="usuario_nino")
    
    def set_password(self, password):
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        # Para usuarios de prueba con hash fijo
        if self.password_hash == 'pbkdf2:sha256:260000$test$test' and password == '123':
            return True
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<UsuarioNino {self.nombre_usuario}>'

class SesionUsuario(db.Model):
    """Registro de sesiones de usuario"""
    __tablename__ = 'sesion_usuario'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)
    tipo_usuario = Column(String(20), nullable=False)  # 'padre' o 'nino'
    ip_address = Column(String(45))
    user_agent = Column(Text)
    inicio_sesion = Column(DateTime, default=datetime.utcnow)
    fin_sesion = Column(DateTime)
    activa = Column(Boolean, default=True)
    
    def __repr__(self):
        return f'<SesionUsuario {self.usuario_id}>'

class ProgresoUsuario(db.Model):
    """Progreso detallado del usuario por categoría"""
    __tablename__ = 'progreso_usuario'
    
    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey('perfil_nino.id'), nullable=False)
    categoria = Column(String(50), nullable=False)  # lenguaje, numeros, colores, animales
    nivel_actual = Column(String(20), default='inicial')  # nivel de progresión
    actividades_completadas = Column(Integer, default=0)
    actividades_totales = Column(Integer, default=0)
    puntos_categoria = Column(Integer, default=0)
    ultima_actividad_id = Column(Integer, ForeignKey('actividades_tea.id'), nullable=True)
    fecha_ultima_actividad = Column(DateTime, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    nino = relationship("PerfilNino")
    ultima_actividad = relationship("ActividadTEA")
    
    def __repr__(self):
        return f'<ProgresoUsuario {self.nino_id} - {self.categoria}>'

class MedallaUsuario(db.Model):
    """Medallas e insignias desbloqueadas por el usuario"""
    __tablename__ = 'medalla_usuario'
    
    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey('perfil_nino.id'), nullable=False)
    tipo_medalla = Column(String(50), nullable=False)  # primera_actividad, categoria_completa, etc.
    categoria = Column(String(50), nullable=True)  # categoria específica si aplica
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    icono = Column(String(100), default='🏆')  # emoji o URL de icono
    puntos_requeridos = Column(Integer, default=0)
    fecha_obtenida = Column(DateTime, default=datetime.utcnow)
    visible = Column(Boolean, default=True)
    
    # Relaciones
    nino = relationship("PerfilNino")
    
    def __repr__(self):
        return f'<MedallaUsuario {self.nino_id} - {self.titulo}>'

class ConfiguracionUsuario(db.Model):
    """Configuraciones personalizadas del usuario"""
    __tablename__ = 'configuracion_usuario'
    
    id = Column(Integer, primary_key=True)
    nino_id = Column(Integer, ForeignKey('perfil_nino.id'), nullable=False)
    
    # Configuración de colores
    color_primario = Column(String(7), default='#E74C3C')  # Color principal
    color_secundario = Column(String(7), default='#3498DB')  # Color secundario
    color_fondo = Column(String(7), default='#FFE5B4')  # Color de fondo
    color_texto = Column(String(7), default='#2C3E50')  # Color del texto
    color_accento = Column(String(7), default='#FFD700')  # Color de acento
    
    # Configuración de interfaz
    tamaño_fuente = Column(String(20), default='normal')  # pequeño, normal, grande, extra_grande
    modo_alto_contraste = Column(Boolean, default=False)
    animaciones_habilitadas = Column(Boolean, default=True)
    sonidos_habilitados = Column(Boolean, default=True)
    
    # Configuración de dificultad
    nivel_dificultad_global = Column(String(20), default='basico')  # basico, intermedio, avanzado
    tiempo_por_actividad = Column(Integer, default=5)  # minutos
    pausas_automaticas = Column(Boolean, default=True)
    tiempo_pausa = Column(Integer, default=2)  # minutos
    
    # Configuración de avatar
    avatar_preferido = Column(String(50), default='maestra_ana')
    velocidad_voz = Column(Float, default=1.0)  # 0.5 a 2.0
    tono_voz = Column(Float, default=1.0)  # 0.5 a 2.0
    volumen_voz = Column(Float, default=0.8)  # 0.0 a 1.0
    
    # Configuración de gamificación
    mostrar_puntos = Column(Boolean, default=True)
    mostrar_medallas = Column(Boolean, default=True)
    notificaciones_logros = Column(Boolean, default=True)
    musica_fondo = Column(Boolean, default=False)
    
    # Configuración de accesibilidad
    navegacion_teclado = Column(Boolean, default=True)
    lectores_pantalla = Column(Boolean, default=False)
    zoom_habilitado = Column(Boolean, default=True)
    modo_dalto_nico = Column(Boolean, default=False)  # Para daltonismo
    
    # Metadatos
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activa = Column(Boolean, default=True)
    
    # Relaciones
    nino = relationship("PerfilNino")
    
    def __repr__(self):
        return f'<ConfiguracionUsuario {self.nino_id}>'
    
    def to_dict(self):
        """Convertir configuración a diccionario"""
        return {
            'id': self.id,
            'nino_id': self.nino_id,
            'colores': {
                'primario': self.color_primario,
                'secundario': self.color_secundario,
                'fondo': self.color_fondo,
                'texto': self.color_texto,
                'acento': self.color_acento
            },
            'interfaz': {
                'tamaño_fuente': self.tamaño_fuente,
                'alto_contraste': self.modo_alto_contraste,
                'animaciones': self.animaciones_habilitadas,
                'sonidos': self.sonidos_habilitados
            },
            'dificultad': {
                'nivel_global': self.nivel_dificultad_global,
                'tiempo_actividad': self.tiempo_por_actividad,
                'pausas_automaticas': self.pausas_automaticas,
                'tiempo_pausa': self.tiempo_pausa
            },
            'avatar': {
                'preferido': self.avatar_preferido,
                'velocidad_voz': self.velocidad_voz,
                'tono_voz': self.tono_voz,
                'volumen_voz': self.volumen_voz
            },
            'gamificacion': {
                'mostrar_puntos': self.mostrar_puntos,
                'mostrar_medallas': self.mostrar_medallas,
                'notificaciones_logros': self.notificaciones_logros,
                'musica_fondo': self.musica_fondo
            },
            'accesibilidad': {
                'navegacion_teclado': self.navegacion_teclado,
                'lectores_pantalla': self.lectores_pantalla,
                'zoom_habilitado': self.zoom_habilitado,
                'modo_dalto_nico': self.modo_dalto_nico
            }
        }

class Avatar(db.Model):
    """Modelo para avatares personalizados"""
    __tablename__ = 'avatares'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    tipo = Column(String(30), nullable=False)  # superheroe, personaje, animal
    imagen_url = Column(String(500))
    audio_voice = Column(String(100))  # tipo de voz
    personalidad = Column(Text)  # JSON con características
    frases_motivacionales = Column(Text)  # JSON con frases
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Avatar {self.nombre}>'
    
    def get_personalidad(self):
        """Obtener personalidad como diccionario"""
        if self.personalidad:
            try:
                import json
                return json.loads(self.personalidad)
            except:
                return {}
        return {}
    
    def get_frases(self):
        """Obtener frases como lista"""
        if self.frases_motivacionales:
            try:
                import json
                return json.loads(self.frases_motivacionales)
            except:
                return []
        return []

class AvatarUsuario(db.Model):
    """Configuración de avatar por usuario"""
    __tablename__ = 'avatar_usuario'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)  # ID del usuario (padre o niño)
    tipo_usuario = Column(String(20), nullable=False)  # 'padre' o 'nino'
    avatar_id = Column(Integer, ForeignKey('avatares.id'), nullable=False)
    color_preferido = Column(String(20), default='#E74C3C')
    velocidad_voz = Column(Float, default=0.9)  # 0.1 a 2.0
    tono_voz = Column(Float, default=1.1)  # 0.0 a 2.0
    volumen_voz = Column(Float, default=0.8)  # 0.0 a 1.0
    frases_personalizadas = Column(Text)  # JSON con frases personalizadas
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    avatar = relationship("Avatar", backref="configuraciones_usuario")
    
    def __repr__(self):
        return f'<AvatarUsuario {self.usuario_id}:{self.avatar.nombre}>'
    
    def get_frases_personalizadas(self):
        """Obtener frases personalizadas como diccionario"""
        if self.frases_personalizadas:
            try:
                import json
                return json.dumps(self.frases_personalizadas)
            except:
                return {}
        return {}
    
    def set_frases_personalizadas(self, frases_dict):
        """Establecer frases personalizadas"""
        import json
        self.frases_personalizadas = json.dumps(frases_dict)

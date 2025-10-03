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
    creado_en = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    sesiones = relationship("SesionTEA", back_populates="nino")
    progresos = relationship("ProgresoTEA", back_populates="nino")

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
    password_hash = Column(String(128), nullable=False)
    telefono = Column(String(20))
    relacion_nino = Column(String(50), default='padre')  # padre, madre, tutor, abuelo, etc.
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    ultimo_acceso = Column(DateTime)
    
    # Relaciones
    ninos = relationship("PerfilNino", backref="padre_responsable")
    
    def set_password(self, password):
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<UsuarioPadre {self.email}>'

class UsuarioNino(db.Model):
    """Usuario niño (perfil simplificado)"""
    __tablename__ = 'usuario_nino'
    
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
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

# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.extensions import Base
from sqlalchemy.orm import relationship
from app.models.avance_metas import AvanceMeta  # ✅ Import explícito requerido

class MetaPersonal(Base):
    __tablename__ = 'metas_personales'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=True)
    tipo = Column(String(50), nullable=True)
    unidad = Column(String(20), nullable=True)
    valor_objetivo = Column(Float, nullable=False)
    fecha_limite = Column(DateTime, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    avances = relationship("AvanceMeta", back_populates="meta", cascade="all, delete-orphan")

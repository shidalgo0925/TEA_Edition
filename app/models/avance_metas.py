# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import Base

class AvanceMeta(Base):
    __tablename__ = 'avance_metas'

    id = Column(Integer, primary_key=True)
    meta_id = Column(Integer, ForeignKey('metas_personales.id'), nullable=False)
    valor = Column(Float, nullable=False)
    registrado_en = Column(DateTime, default=datetime.utcnow)

    meta = relationship("MetaPersonal", back_populates="avances") 

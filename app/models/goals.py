# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, Date
from ..extensions import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    area = Column(String(32), nullable=False)          # Personal | Económico | Familiar | Físico
    titulo = Column(String(255), nullable=False)
    kpi = Column(String(255), nullable=True)
    fecha_objetivo = Column(Date, nullable=True)
    activo = Column(Boolean, default=True)

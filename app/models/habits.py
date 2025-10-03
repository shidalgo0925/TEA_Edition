# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, Time
from ..extensions import Base

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    area = Column(String(32), nullable=False)          # Personal | Económico | Familiar | Físico
    nombre = Column(String(255), nullable=False)
    frecuencia = Column(String(1), default="D")        # D=Diario, W=Semanal
    hora_sugerida = Column(Time, nullable=True)
    enabled = Column(Boolean, default=True)

# -*- coding: utf-8 -*-
from datetime import date
from app.extensions import Base
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, func

class CierreDia(Base):
    __tablename__ = "cierre_dia"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, default=1)
    fecha = Column(Date, nullable=False, default=date.today)
    emocion = Column(Text)
    reflexion = Column(Text)
    creado_en = Column(DateTime, server_default=func.now())

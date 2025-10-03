# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Date, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..extensions import Base

class PlanDay(Base):
    __tablename__ = "plan_day"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)

    # relación 1..N con items
    items = relationship("PlanItem", back_populates="plan", cascade="all, delete-orphan")

class PlanItem(Base):
    __tablename__ = "plan_item"

    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey("plan_day.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo = Column(String(255), nullable=False)
    categoria = Column(String(64), nullable=True)      # Mariachi | Easytech | Personal | etc.
    prioridad = Column(Integer, nullable=True)         # 1..3
    dur_min = Column(Integer, nullable=True)
    from_calendar = Column(Boolean, default=False)

    plan = relationship("PlanDay", back_populates="items")

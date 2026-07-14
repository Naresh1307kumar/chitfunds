from app.database import Base
from sqlalchemy import Column, Integer, DateTime, Float, Date, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class DrawStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class MonthlyDraw(Base):
    __tablename__ = "monthly_draws"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("chit_plans.id"), nullable=False)
    month_number = Column(Integer, nullable=False)
    draw_date = Column(Date, nullable=False)
    
    total_chit_value = Column(Float, nullable=False)
    admin_commission = Column(Float, nullable=False)
    prize_amount = Column(Float, nullable=False)
    
    winning_ticket_id = Column(Integer, ForeignKey("plan_members.id"), nullable=True)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    status = Column(Enum(DrawStatus), default=DrawStatus.scheduled)
    conducted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    plan = relationship("ChitPlan", back_populates="draws")
    winning_ticket = relationship("PlanMember", foreign_keys=[winning_ticket_id], back_populates="draws_won")
    winner_user = relationship("User", foreign_keys=[winner_id])
    conductor = relationship("User", foreign_keys=[conducted_by])

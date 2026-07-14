from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class PlanType(str, enum.Enum):
    bronze = "bronze"
    silver = "silver"
    gold = "gold"


class PlanStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class ChitPlan(Base):
    __tablename__ = "chit_plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String(100), nullable=False)
    plan_type = Column(Enum(PlanType), default=PlanType.silver)
    monthly_amount = Column(Float, nullable=False)
    total_members = Column(Integer, nullable=False)
    current_members = Column(Integer, default=0)
    duration_months = Column(Integer, nullable=False)
    total_value = Column(Float, nullable=False)        # auto-calculated
    commission_rate = Column(Float, default=5.0)       # percentage
    net_prize_amount = Column(Float, nullable=False)   # auto-calculated
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)            # auto-calculated
    status = Column(Enum(PlanStatus), default=PlanStatus.draft)
    is_deleted = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    creator = relationship("User", foreign_keys=[created_by])
    plan_members = relationship("PlanMember", back_populates="plan")
    draws = relationship("MonthlyDraw", back_populates="plan")
    installments = relationship("Installment", back_populates="plan")

from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class InstallmentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    verified = "verified"
    overdue = "overdue"


class PaymentMethod(str, enum.Enum):
    cash = "cash"
    bank_transfer = "bank_transfer"


class Installment(Base):
    __tablename__ = "installments"

    id = Column(Integer, primary_key=True, index=True)
    plan_member_id = Column(Integer, ForeignKey("plan_members.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("chit_plans.id"), nullable=False)
    month_number = Column(Integer, nullable=False)     # e.g., 1, 2, 3...
    due_date = Column(Date, nullable=False)
    base_amount = Column(Float, nullable=False)
    penalty_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(InstallmentStatus), default=InstallmentStatus.pending)
    paid_date = Column(Date, nullable=True)
    payment_method = Column(String(100), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    receipt_number = Column(String(50), nullable=True, unique=True)
    receipt_path = Column(String(255), nullable=True)
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    plan_member = relationship("PlanMember", back_populates="installments")
    plan = relationship("ChitPlan", back_populates="installments")
    verifier = relationship("User", foreign_keys=[verified_by])

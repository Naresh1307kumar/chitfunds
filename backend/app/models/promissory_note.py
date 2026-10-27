from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class PronoteStatus(str, enum.Enum):
    pending_signature = "pending_signature"
    active = "active"
    paid = "paid"
    overdue = "overdue"


class PromissoryNote(Base):
    __tablename__ = "promissory_notes"

    id = Column(Integer, primary_key=True, index=True)
    pronote_id = Column(String(50), unique=True, index=True, nullable=False)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chit_id = Column(Integer, ForeignKey("chit_plans.id"), nullable=True)
    loan_amount = Column(Float, nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    interest_rate = Column(Float, default=0.0)
    repayment_amount = Column(Float, nullable=False)
    purpose = Column(Text, nullable=True)
    status = Column(Enum(PronoteStatus), default=PronoteStatus.active, nullable=False)
    signature = Column(Text, nullable=True)  # Base64 Data URL string of digital signature
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    member = relationship("User", foreign_keys=[member_id])
    chit = relationship("ChitPlan", foreign_keys=[chit_id])

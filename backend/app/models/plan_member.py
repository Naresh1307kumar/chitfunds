from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class PlanMember(Base):
    __tablename__ = "plan_members"
    __table_args__ = (
        UniqueConstraint('user_id', 'plan_id', name='unique_user_plan'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("chit_plans.id"), nullable=False)
    ticket_number = Column(String(50), nullable=True)  # e.g. TCK-1024-1
    joined_date = Column(Date, nullable=False)
    has_won = Column(Boolean, default=False)           # won a draw with this ticket
    is_active = Column(Boolean, default=True)
    reason = Column(String(50), default="personal")
    priority_score = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="plan_members")
    plan = relationship("ChitPlan", back_populates="plan_members")
    installments = relationship("Installment", back_populates="plan_member")
    draws_won = relationship("MonthlyDraw", back_populates="winning_ticket")

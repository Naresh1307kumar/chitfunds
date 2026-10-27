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

    # --- Core Chit Fund Auction Calculation Fields ---
    chit_value           = Column(Float, nullable=False)   # Total pool = monthly × members
    winning_bid_amount   = Column(Float, nullable=True)    # Amount winner agreed to accept
    discount             = Column(Float, default=0.0)      # chit_value - winning_bid_amount
    company_commission   = Column(Float, default=0.0)      # discount × commission_rate%
    net_discount         = Column(Float, default=0.0)      # discount - commission
    dividend_per_member  = Column(Float, default=0.0)      # net_discount / total_members
    net_payable          = Column(Float, default=0.0)      # monthly_amount - dividend_per_member
    prize_amount         = Column(Float, nullable=False)   # = winning_bid_amount (winner receives)

    # Legacy field kept for API compatibility
    total_chit_value     = Column(Float, nullable=True)
    admin_commission     = Column(Float, nullable=True)

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

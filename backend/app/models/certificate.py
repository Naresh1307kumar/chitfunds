from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class CertificateType(str, enum.Enum):
    membership = "membership"
    auction_winner = "auction_winner"
    plan_completion = "plan_completion"


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("chit_plans.id"), nullable=True)
    certificate_type = Column(Enum(CertificateType), nullable=False)
    certificate_number = Column(String(50), unique=True, nullable=False)  # CERT-2025-0042
    file_path = Column(String(255), nullable=True)
    issued_date = Column(Date, nullable=False)
    issued_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", foreign_keys=[user_id], back_populates="certificates")
    plan = relationship("ChitPlan", foreign_keys=[plan_id])
    issuer = relationship("User", foreign_keys=[issued_by])

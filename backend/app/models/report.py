from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class ReportType(str, enum.Enum):
    members = "members"
    kyc_status = "kyc_status"
    installments = "installments"
    overdue = "overdue"
    auctions = "auctions"
    revenue = "revenue"
    audit_log = "audit_log"


class ReportFormat(str, enum.Enum):
    pdf = "pdf"
    csv = "csv"
    excel = "excel"


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(Enum(ReportType), nullable=False)
    report_format = Column(Enum(ReportFormat), nullable=False)
    file_path = Column(String(255), nullable=True)
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    generator = relationship("User", foreign_keys=[generated_by])

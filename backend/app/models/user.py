from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, Float, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class UserRole(str, enum.Enum):
    member = "member"
    admin = "admin"


class UserStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    active = "active"
    suspended = "suspended"
    rejected = "rejected"


class KYCStatus(str, enum.Enum):
    not_submitted = "not_submitted"
    pending = "pending"
    verified = "verified"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.member, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.pending, nullable=False)

    # Profile
    profile_photo = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    aadhar_number = Column(String(20), nullable=True)
    pan_number = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    occupation = Column(String(100), nullable=True)

    # KYC
    kyc_status = Column(Enum(KYCStatus), default=KYCStatus.not_submitted, nullable=False)

    # Security
    failed_login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    kyc_documents = relationship("KYCDocument", back_populates="user", foreign_keys="KYCDocument.user_id")
    guarantors = relationship("Guarantor", back_populates="member", foreign_keys="Guarantor.member_id")
    plan_members = relationship("PlanMember", back_populates="user", foreign_keys="PlanMember.user_id")
    notifications = relationship("Notification", back_populates="user", foreign_keys="Notification.user_id")
    certificates = relationship("Certificate", back_populates="user", foreign_keys="Certificate.user_id")
    audit_logs = relationship("AuditLog", back_populates="user", foreign_keys="AuditLog.user_id")
    password_resets = relationship("PasswordReset", back_populates="user", foreign_keys="PasswordReset.user_id")

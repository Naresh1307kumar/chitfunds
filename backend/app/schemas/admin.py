from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole, UserStatus, KYCStatus
from app.models.kyc import KYCDocumentStatus, DocumentType

class UserStatusUpdateRequest(BaseModel):
    status: UserStatus

class KYCDocumentResponse(BaseModel):
    id: int
    document_type: DocumentType
    file_path: str
    status: KYCDocumentStatus
    rejection_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class GuarantorResponse(BaseModel):
    id: int
    name: str
    phone: str
    address: str
    relationship_to_member: str
    aadhar_number: str
    document_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AdminUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    role: UserRole
    status: UserStatus
    kyc_status: KYCStatus
    profile_photo: Optional[str] = None
    aadhar_number: Optional[str] = None
    pan_number: Optional[str] = None
    failed_login_attempts: int
    created_at: datetime
    
    kyc_documents: List[KYCDocumentResponse] = []
    guarantors: List[GuarantorResponse] = []

    class Config:
        from_attributes = True

class KYCStatusUpdateRequest(BaseModel):
    kyc_status: KYCStatus
    
class KYCDocumentVerifyRequest(BaseModel):
    status: KYCDocumentStatus
    rejection_reason: Optional[str] = None

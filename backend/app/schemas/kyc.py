from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.kyc import KYCDocumentStatus, DocumentType

class KYCDocumentBase(BaseModel):
    document_type: DocumentType

class KYCDocumentCreate(KYCDocumentBase):
    pass

class KYCDocumentResponse(KYCDocumentBase):
    id: int
    file_path: str
    status: KYCDocumentStatus
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class KYCStatusResponse(BaseModel):
    kyc_status: str
    documents: List[KYCDocumentResponse]

class KYCVerifyRequest(BaseModel):
    action: str  # "approve" or "reject"
    rejection_reason: Optional[str] = None

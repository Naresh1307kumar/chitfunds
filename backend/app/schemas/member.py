from pydantic import BaseModel, constr
from typing import Optional
from datetime import date
from app.models.kyc import DocumentType

class GuarantorCreate(BaseModel):
    name: str
    phone: str
    address: str
    relationship_to_member: str
    aadhar_number: str

class GuarantorResponse(GuarantorCreate):
    id: int
    document_path: Optional[str] = None
    
    class Config:
        from_attributes = True

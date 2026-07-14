from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import uuid

from app.database import get_db
from app.models.user import User, KYCStatus
from app.models.kyc import KYCDocument, DocumentType, KYCDocumentStatus
from app.models.guarantor import Guarantor
from app.schemas.member import GuarantorCreate, GuarantorResponse
from app.schemas.admin import KYCDocumentResponse
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["Member Profile"])

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/kyc", response_model=KYCDocumentResponse)
async def upload_kyc_document(
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.kyc_status == KYCStatus.verified:
        raise HTTPException(status_code=400, detail="KYC is already verified")
        
    # Generate unique filename
    ext = file.filename.split('.')[-1]
    filename = f"{current_user.id}_{document_type.value}_{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    # Check if doc type already exists for user
    existing_doc = db.query(KYCDocument).filter(
        KYCDocument.user_id == current_user.id,
        KYCDocument.document_type == document_type
    ).first()
    
    if existing_doc:
        existing_doc.file_path = file_path
        existing_doc.status = KYCDocumentStatus.pending
        existing_doc.rejection_reason = None
        doc = existing_doc
    else:
        doc = KYCDocument(
            user_id=current_user.id,
            document_type=document_type,
            file_path=file_path,
            status=KYCDocumentStatus.pending
        )
        db.add(doc)
        
    # Update user KYC status to pending if it was not_submitted
    if current_user.kyc_status == KYCStatus.not_submitted:
        current_user.kyc_status = KYCStatus.pending
        
    db.commit()
    db.refresh(doc)
    return doc

@router.get("/kyc", response_model=List[KYCDocumentResponse])
def get_my_kyc(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(KYCDocument).filter(KYCDocument.user_id == current_user.id).all()

@router.post("/guarantor", response_model=GuarantorResponse)
def add_guarantor(data: GuarantorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Guarantor).filter(Guarantor.member_id == current_user.id).first()
    if existing:
        existing.name = data.name
        existing.phone = data.phone
        existing.address = data.address
        existing.relationship_to_member = data.relationship_to_member
        existing.aadhar_number = data.aadhar_number
        guarantor = existing
    else:
        guarantor = Guarantor(
            member_id=current_user.id,
            **data.model_dump()
        )
        db.add(guarantor)
        
    db.commit()
    db.refresh(guarantor)
    return guarantor

@router.get("/guarantor", response_model=List[GuarantorResponse])
def get_my_guarantor(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Guarantor).filter(Guarantor.member_id == current_user.id).all()

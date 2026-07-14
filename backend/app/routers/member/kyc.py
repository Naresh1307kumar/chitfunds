import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User, KYCStatus
from app.models.kyc import KYCDocument, DocumentType, KYCDocumentStatus
from app.schemas.kyc import KYCDocumentResponse

router = APIRouter(tags=["Member KYC"])

UPLOAD_DIR = "uploads/kyc"

@router.post("", response_model=KYCDocumentResponse)
async def upload_kyc_document(
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only allow if not verified
    if current_user.kyc_status == KYCStatus.verified:
        raise HTTPException(status_code=400, detail="KYC is already verified")

    # Validate extension
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png", "pdf"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file format")
    
    # Check if existing doc of this type exists and delete
    existing = db.query(KYCDocument).filter(
        KYCDocument.user_id == current_user.id,
        KYCDocument.document_type == document_type
    ).first()
    if existing:
        db.delete(existing)

    # Save file
    filename = f"{current_user.id}_{document_type.value}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    doc = KYCDocument(
        user_id=current_user.id,
        document_type=document_type,
        file_path=f"/{filepath.replace(chr(92), '/')}",  # normalize slashes
        status=KYCDocumentStatus.pending
    )
    db.add(doc)
    
    # Update user KYC status to pending if it was not submitted or rejected
    if current_user.kyc_status in [KYCStatus.not_submitted, KYCStatus.rejected]:
        current_user.kyc_status = KYCStatus.pending
        
    db.commit()
    db.refresh(doc)
    return doc


@router.get("", response_model=List[KYCDocumentResponse])
async def get_kyc_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    docs = db.query(KYCDocument).filter(KYCDocument.user_id == current_user.id).all()
    return docs

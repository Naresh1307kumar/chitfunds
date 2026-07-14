from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.models.kyc import KYCDocument
from app.schemas.admin import (
    AdminUserResponse, UserStatusUpdateRequest, KYCStatusUpdateRequest, KYCDocumentVerifyRequest
)
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/members", tags=["Admin Members"])

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

@router.get("", response_model=List[AdminUserResponse])
def get_all_members(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    members = db.query(User).filter(User.role == UserRole.member, User.is_deleted == False).all()
    return members

@router.get("/{user_id}", response_model=AdminUserResponse)
def get_member_details(user_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    member = db.query(User).filter(User.id == user_id, User.role == UserRole.member).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@router.put("/{user_id}/status")
def update_member_status(user_id: int, data: UserStatusUpdateRequest, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    member = db.query(User).filter(User.id == user_id, User.role == UserRole.member).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    member.status = data.status
    if data.status == UserStatus.active:
        member.failed_login_attempts = 0
    db.commit()
    return {"message": "Member status updated successfully"}

@router.post("/{user_id}/unlock")
def unlock_member(user_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    member = db.query(User).filter(User.id == user_id, User.role == UserRole.member).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    member.failed_login_attempts = 0
    db.commit()
    return {"message": "Member account unlocked successfully"}

@router.put("/{user_id}/kyc")
def update_member_kyc_status(user_id: int, data: KYCStatusUpdateRequest, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    member = db.query(User).filter(User.id == user_id, User.role == UserRole.member).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    member.kyc_status = data.kyc_status
    
    # Auto-approve member if KYC is verified
    from app.models.user import UserStatus, KYCStatus
    from app.models.kyc import KYCDocumentStatus
    
    if data.kyc_status == KYCStatus.verified:
        member.status = UserStatus.active
        # Mark all pending docs as verified
        for doc in member.kyc_documents:
            doc.status = KYCDocumentStatus.verified
            doc.verified_by = current_admin.id
            doc.verified_at = datetime.utcnow()
            
    elif data.kyc_status == KYCStatus.rejected:
        # Mark all pending docs as rejected
        for doc in member.kyc_documents:
            if doc.status == KYCDocumentStatus.pending:
                doc.status = KYCDocumentStatus.rejected
                doc.verified_by = current_admin.id
                doc.verified_at = datetime.utcnow()

    db.commit()
    return {"message": "Member KYC status updated successfully"}

@router.delete("/{user_id}")
def delete_member(user_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    member = db.query(User).filter(User.id == user_id, User.role == UserRole.member).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    member.is_deleted = True
    db.commit()
    return {"message": "Member soft deleted successfully"}

@router.put("/kyc-documents/{doc_id}/verify")
def verify_kyc_document(doc_id: int, data: KYCDocumentVerifyRequest, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    doc = db.query(KYCDocument).filter(KYCDocument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc.status = data.status
    doc.rejection_reason = data.rejection_reason
    doc.verified_by = current_admin.id
    doc.verified_at = datetime.utcnow()
    db.commit()
    return {"message": "Document verified successfully"}

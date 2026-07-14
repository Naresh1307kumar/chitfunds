from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User, UserRole, KYCStatus, UserStatus
from app.models.kyc import KYCDocument, KYCDocumentStatus
from app.schemas.auth import UserResponse
from app.schemas.kyc import KYCVerifyRequest
from typing import List
from datetime import datetime

router = APIRouter(tags=["Admin KYC"])

def check_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user


@router.get("/pending", response_model=List[UserResponse])
def get_pending_kyc_members(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """Get all members who have submitted KYC but are not verified yet"""
    users = db.query(User).filter(
        User.role == UserRole.member,
        User.kyc_status == KYCStatus.pending,
        User.is_deleted == False
    ).all()
    return users


@router.get("/{user_id}/documents")
def get_member_kyc_documents(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """Get KYC documents for a specific user"""
    docs = db.query(KYCDocument).filter(KYCDocument.user_id == user_id).all()
    return docs


@router.post("/{user_id}/verify")
def verify_kyc(
    user_id: int,
    data: KYCVerifyRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """Approve or Reject a user's KYC"""
    user = db.query(User).filter(User.id == user_id, User.role == UserRole.member).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    docs = db.query(KYCDocument).filter(KYCDocument.user_id == user_id).all()
    if not docs:
        raise HTTPException(status_code=400, detail="User has no KYC documents")

    if data.action == "approve":
        # Update docs
        for doc in docs:
            doc.status = KYCDocumentStatus.verified
            doc.verified_by = admin.id
            doc.verified_at = datetime.utcnow()
        
        # Update user
        user.kyc_status = KYCStatus.verified
        user.status = UserStatus.active
        
    elif data.action == "reject":
        if not data.rejection_reason:
            raise HTTPException(status_code=400, detail="Rejection reason is required")
            
        for doc in docs:
            doc.status = KYCDocumentStatus.rejected
            doc.rejection_reason = data.rejection_reason
            doc.verified_by = admin.id
            doc.verified_at = datetime.utcnow()
            
        user.kyc_status = KYCStatus.rejected
        
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    db.commit()
    return {"message": f"User KYC {data.action}d successfully"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserRole
from app.models.installment import Installment, InstallmentStatus
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentResponse, PaymentUpdateStatus
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["Admin Payments"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@router.get("/", response_model=List[PaymentResponse])
def get_all_payments(
    status: PaymentStatus = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    query = db.query(Payment)
    if status:
        query = query.filter(Payment.status == status)
    
    payments = query.order_by(Payment.created_at.desc()).all()
    return payments

@router.put("/{payment_id}/status", response_model=PaymentResponse)
def update_payment_status(
    payment_id: int,
    status_update: PaymentUpdateStatus,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
        
    installment = db.query(Installment).filter(Installment.id == payment.installment_id).first()
    
    # Update payment status
    payment.status = status_update.status
    if status_update.notes:
        payment.notes = status_update.notes
        
    # Update corresponding installment status
    if status_update.status == PaymentStatus.success:
        installment.status = InstallmentStatus.verified
        installment.paid_date = payment.created_at.date()
        installment.verified_by = admin_user.id
        installment.verified_at = datetime.utcnow()
    elif status_update.status == PaymentStatus.failed:
        installment.status = InstallmentStatus.pending # Revert to pending so user can pay again
        
    db.commit()
    db.refresh(payment)
    db.refresh(installment)
    
    return payment

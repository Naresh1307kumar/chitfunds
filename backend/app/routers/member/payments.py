from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.installment import Installment, InstallmentStatus
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["Member Payments"])

@router.post("/submit", response_model=PaymentResponse)
def submit_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if the installment belongs to the user
    installment = db.query(Installment).filter(
        Installment.id == payment_in.installment_id
    ).first()
    
    if not installment:
        raise HTTPException(status_code=404, detail="Installment not found")
        
    if installment.plan_member.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to pay for this installment")
        
    if installment.status == InstallmentStatus.verified:
        raise HTTPException(status_code=400, detail="Installment is already paid and verified")

    # Check if there is already a pending payment
    existing_payment = db.query(Payment).filter(
        Payment.installment_id == payment_in.installment_id,
        Payment.status == PaymentStatus.pending
    ).first()
    
    if existing_payment:
        raise HTTPException(status_code=400, detail="You already have a pending payment for this installment. Please wait for verification.")

    # Create new payment record
    new_payment = Payment(
        installment_id=payment_in.installment_id,
        user_id=current_user.id,
        amount=payment_in.amount,
        payment_method=payment_in.payment_method,
        transaction_id=payment_in.transaction_id,
        notes=payment_in.notes,
        status=PaymentStatus.pending
    )
    
    db.add(new_payment)
    
    # Optionally update installment status to "paid" (pending verification)
    if installment.status == InstallmentStatus.pending:
        installment.status = InstallmentStatus.paid
        
    db.commit()
    db.refresh(new_payment)
    
    return new_payment

@router.get("/", response_model=List[PaymentResponse])
def get_all_payments_by_member(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payments = db.query(Payment).filter(Payment.user_id == current_user.id).order_by(Payment.created_at.desc()).all()
    return payments

@router.get("/history", response_model=List[PaymentResponse])
def get_payment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payments = db.query(Payment).filter(Payment.user_id == current_user.id).order_by(Payment.created_at.desc()).all()
    return payments


@router.get('/dues')
def get_my_dues(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.installment import Installment
    from app.models.plan_member import PlanMember
    from app.models.chit_plan import ChitPlan
    
    # Find all installments for this user that are pending or overdue
    installments = db.query(Installment, ChitPlan.name).join(
        PlanMember, Installment.plan_member_id == PlanMember.id
    ).join(
        ChitPlan, Installment.plan_id == ChitPlan.id
    ).filter(
        PlanMember.user_id == current_user.id,
        Installment.status.in_([InstallmentStatus.pending, InstallmentStatus.overdue])
    ).order_by(Installment.due_date.asc()).all()
    
    results = []
    for inst, plan_name in installments:
        results.append({
            'id': inst.id,
            'plan_name': plan_name,
            'month_number': inst.month_number,
            'due_date': inst.due_date,
            'total_amount': inst.total_amount,
            'status': inst.status
        })
    return results


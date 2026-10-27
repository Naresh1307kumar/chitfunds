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

@router.get("/")
def get_all_payments(
    status: PaymentStatus = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    from app.models.user import User
    from app.models.chit_plan import ChitPlan
    from app.models.plan_member import PlanMember

    query = db.query(Payment)
    if status:
        query = query.filter(Payment.status == status)
    
    payments = query.order_by(Payment.created_at.desc()).all()
    
    results = []
    for p in payments:
        user = db.query(User).filter(User.id == p.user_id).first()
        inst = db.query(Installment).filter(Installment.id == p.installment_id).first()
        plan_name = "Chit Scheme"
        month_num = 1
        if inst:
            month_num = inst.month_number
            plan = db.query(ChitPlan).filter(ChitPlan.id == inst.plan_id).first()
            if plan:
                plan_name = plan.plan_name

        results.append({
            "id": p.id,
            "installment_id": p.installment_id,
            "user_id": p.user_id,
            "user_name": user.name if user else "Member",
            "user_phone": user.phone if user else "N/A",
            "user_email": user.email if user else "N/A",
            "plan_name": plan_name,
            "month_number": month_num,
            "amount": p.amount,
            "payment_method": p.payment_method,
            "transaction_id": p.transaction_id,
            "status": p.status.value if hasattr(p.status, 'value') else str(p.status),
            "notes": p.notes,
            "created_at": str(p.created_at)
        })

    return results

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

        from app.models.chit_plan import ChitPlan
        plan = db.query(ChitPlan).filter(ChitPlan.id == installment.plan_id).first()
        user = db.query(User).filter(User.id == payment.user_id).first()
        if user:
            from app.services.notification_service import send_payment_verified_notification
            try:
                send_payment_verified_notification(
                    user_id=user.id,
                    user_name=user.name,
                    user_email=user.email,
                    user_phone=user.phone or "N/A",
                    plan_name=plan.plan_name if plan else "Chit Scheme",
                    month_number=installment.month_number,
                    amount=payment.amount,
                    receipt_number=getattr(installment, 'receipt_number', f"REC-2026-{installment.id:04d}")
                )
            except Exception as e:
                print("Failed to send payment verified notification:", e)
    elif status_update.status == PaymentStatus.failed:
        installment.status = InstallmentStatus.pending # Revert to pending so user can pay again
        
    db.commit()
    db.refresh(payment)
    db.refresh(installment)
    
    return payment

@router.post("/send-due-reminders")
def send_due_reminders(
    admin_user: User = Depends(require_admin)
):
    """Trigger 10th monthly due reminders for all unpaid members before 15th draw."""
    from app.services.notification_service import send_10th_due_reminder_notifications
    count = send_10th_due_reminder_notifications()
    return {
        "success": True,
        "message": f"Successfully sent 10th monthly due reminders to {count} unpaid members before the 15th draw.",
        "reminded_members_count": count
    }

@router.delete("/clear-all")
def clear_all_payments(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Delete all payments and reset all installments back to pending status."""
    deleted_count = db.query(Payment).delete()
    updated_count = db.query(Installment).update({
        Installment.status: InstallmentStatus.pending,
        Installment.paid_date: None,
        Installment.payment_method: None,
        Installment.transaction_id: None,
        Installment.receipt_number: None,
        Installment.receipt_path: None,
        Installment.verified_by: None,
        Installment.verified_at: None,
        Installment.notes: None
    })
    db.commit()
    return {
        "success": True,
        "message": f"Deleted {deleted_count} payment records and reset {updated_count} installments to pending status.",
        "deleted_payments": deleted_count,
        "reset_installments": updated_count
    }

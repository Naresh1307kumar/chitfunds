from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import csv
import io
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserRole, KYCStatus
from app.models.payment import Payment, PaymentStatus
from app.models.installment import Installment, InstallmentStatus
from app.models.chit_plan import ChitPlan
from app.models.plan_member import PlanMember
from app.models.draw import MonthlyDraw
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/reports", tags=["Admin Reports"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin authorization required")
    return current_user

@router.get("/members/download")
def download_members_report(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Generate and stream a CSV report listing all members and their registration/KYC statuses."""
    members = db.query(User).filter(User.role == UserRole.member, User.is_deleted == False).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(["Member ID", "Full Name", "Username", "Email", "Phone", "Aadhar Number", "KYC Status", "Joined Date"])
    
    # Rows
    for m in members:
        writer.writerow([
            m.id,
            m.name,
            m.username,
            m.email,
            m.phone,
            m.aadhar_number,
            m.kyc_status.value if m.kyc_status else "pending",
            m.created_at.strftime("%Y-%m-%d %H:%M:%S") if m.created_at else "—"
        ])
        
    output.seek(0)
    
    filename = f"members_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/payments/download")
def download_payments_report(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Generate and stream a CSV report listing all collection history."""
    payments = db.query(Payment).join(User, Payment.user_id == User.id).order_by(Payment.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(["Transaction ID", "Member Name", "Email", "Amount Paid", "Payment Method", "Status", "Paid Timestamp", "Admin Notes"])
    
    # Rows
    for p in payments:
        writer.writerow([
            p.transaction_id or f"TXN-{p.id}",
            p.user.name if p.user else "—",
            p.user.email if p.user else "—",
            f"Rs.{p.amount:,.2f}",
            p.payment_method,
            p.status.value,
            p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else "—",
            p.notes or "—"
        ])
        
    output.seek(0)
    
    filename = f"payments_collection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/overdue/download")
def download_overdue_report(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Generate and stream a CSV report listing all members with overdue/pending installments."""
    overdue_installments = db.query(Installment).join(
        PlanMember, Installment.plan_member_id == PlanMember.id
    ).join(
        User, PlanMember.user_id == User.id
    ).join(
        ChitPlan, Installment.plan_id == ChitPlan.id
    ).filter(
        Installment.status.in_([InstallmentStatus.pending, InstallmentStatus.overdue])
    ).order_by(Installment.due_date.asc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(["Installment ID", "Member Name", "Email", "Phone", "Scheme Name", "Month #", "Amount Due", "Due Date", "Status"])
    
    # Rows
    for ins in overdue_installments:
        writer.writerow([
            ins.id,
            ins.plan_member.user.name if ins.plan_member and ins.plan_member.user else "—",
            ins.plan_member.user.email if ins.plan_member and ins.plan_member.user else "—",
            ins.plan_member.user.phone if ins.plan_member and ins.plan_member.user else "—",
            ins.plan.plan_name if ins.plan else "—",
            ins.month_number,
            f"Rs.{ins.total_amount:,.2f}",
            ins.due_date.strftime("%Y-%m-%d") if ins.due_date else "—",
            ins.status.value
        ])
        
    output.seek(0)
    
    filename = f"overdue_installments_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/revenue/download")
def download_revenue_report(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Generate and stream a CSV report listing all draws, pool values, and admin commissions earned."""
    draws = db.query(MonthlyDraw).join(ChitPlan, MonthlyDraw.plan_id == ChitPlan.id).join(
        User, MonthlyDraw.winner_id == User.id
    ).order_by(MonthlyDraw.draw_date.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(["Draw ID", "Scheme Name", "Month #", "Total Pool Value", "Winner Name", "Prize Payout", "Admin Commission Earned", "Draw Date"])
    
    # Rows
    for d in draws:
        writer.writerow([
            d.id,
            d.plan.plan_name if d.plan else "—",
            d.month_number,
            f"Rs.{d.total_chit_value:,.2f}",
            d.winner.name if d.winner else "—",
            f"Rs.{d.prize_amount:,.2f}",
            f"Rs.{d.admin_commission:,.2f}",
            d.draw_date.strftime("%Y-%m-%d") if d.draw_date else "—"
        ])
        
    output.seek(0)
    
    filename = f"revenue_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

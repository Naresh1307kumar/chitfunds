from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserRole
from app.models.chit_plan import ChitPlan
from app.models.promissory_note import PromissoryNote, PronoteStatus
from app.schemas.promissory_note import PromissoryNoteCreate, PromissoryNoteResponse, PromissoryNoteUpdateStatus
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/pronotes", tags=["Admin Promissory Notes"])


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


def generate_pronote_id(db: Session) -> str:
    year = datetime.now().year
    count = db.query(PromissoryNote).count()
    return f"PRN-{year}-{(count + 1):04d}"


@router.post("/", response_model=PromissoryNoteResponse)
def create_promissory_note(
    pronote_in: PromissoryNoteCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    member = db.query(User).filter(User.id == pronote_in.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    chit = None
    if pronote_in.chit_id:
        chit = db.query(ChitPlan).filter(ChitPlan.id == pronote_in.chit_id).first()

    auto_id = generate_pronote_id(db)

    db_note = PromissoryNote(
        pronote_id=auto_id,
        member_id=pronote_in.member_id,
        chit_id=pronote_in.chit_id,
        loan_amount=pronote_in.loan_amount,
        issue_date=pronote_in.issue_date,
        due_date=pronote_in.due_date,
        interest_rate=pronote_in.interest_rate,
        repayment_amount=pronote_in.repayment_amount,
        purpose=pronote_in.purpose,
        status=pronote_in.status,
        signature=pronote_in.signature
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return PromissoryNoteResponse(
        id=db_note.id,
        pronote_id=db_note.pronote_id,
        member_id=db_note.member_id,
        chit_id=db_note.chit_id,
        loan_amount=db_note.loan_amount,
        issue_date=db_note.issue_date,
        due_date=db_note.due_date,
        interest_rate=db_note.interest_rate,
        repayment_amount=db_note.repayment_amount,
        purpose=db_note.purpose,
        status=db_note.status,
        signature=db_note.signature,
        member_name=member.name or member.username,
        member_phone=member.phone or "N/A",
        member_email=member.email or "N/A",
        chit_name=chit.plan_name if chit else "N/A",
        created_at=db_note.created_at
    )


@router.get("/", response_model=List[PromissoryNoteResponse])
def get_all_promissory_notes(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    # Fetch all promissory notes for admin view
    notes = db.query(PromissoryNote).order_by(PromissoryNote.created_at.desc()).all()
    results = []

    for n in notes:
        member = db.query(User).filter(User.id == n.member_id).first()
        chit = db.query(ChitPlan).filter(ChitPlan.id == n.chit_id).first() if n.chit_id else None

        results.append(PromissoryNoteResponse(
            id=n.id,
            pronote_id=n.pronote_id,
            member_id=n.member_id,
            chit_id=n.chit_id,
            loan_amount=n.loan_amount,
            issue_date=n.issue_date,
            due_date=n.due_date,
            interest_rate=n.interest_rate,
            repayment_amount=n.repayment_amount,
            purpose=n.purpose,
            status=n.status,
            signature=n.signature,
            member_name=member.name if member else f"Member #{n.member_id}",
            member_phone=member.phone if member else "N/A",
            member_email=member.email if member else "N/A",
            chit_name=chit.plan_name if chit else "N/A",
            created_at=n.created_at
        ))

    return results


@router.get("/{note_id}", response_model=PromissoryNoteResponse)
def get_promissory_note(
    note_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    n = db.query(PromissoryNote).filter(PromissoryNote.id == note_id).first()
    if not n:
        raise HTTPException(status_code=404, detail="Promissory Note not found")

    member = db.query(User).filter(User.id == n.member_id).first()
    chit = db.query(ChitPlan).filter(ChitPlan.id == n.chit_id).first() if n.chit_id else None

    return PromissoryNoteResponse(
        id=n.id,
        pronote_id=n.pronote_id,
        member_id=n.member_id,
        chit_id=n.chit_id,
        loan_amount=n.loan_amount,
        issue_date=n.issue_date,
        due_date=n.due_date,
        interest_rate=n.interest_rate,
        repayment_amount=n.repayment_amount,
        purpose=n.purpose,
        status=n.status,
        signature=n.signature,
        member_name=member.name if member else f"Member #{n.member_id}",
        member_phone=member.phone if member else "N/A",
        member_email=member.email if member else "N/A",
        chit_name=chit.plan_name if chit else "N/A",
        created_at=n.created_at
    )


@router.put("/{note_id}/status", response_model=PromissoryNoteResponse)
def update_promissory_note_status(
    note_id: int,
    status_in: PromissoryNoteUpdateStatus,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    n = db.query(PromissoryNote).filter(PromissoryNote.id == note_id).first()
    if not n:
        raise HTTPException(status_code=404, detail="Promissory Note not found")

    n.status = status_in.status
    db.commit()
    db.refresh(n)

    member = db.query(User).filter(User.id == n.member_id).first()
    chit = db.query(ChitPlan).filter(ChitPlan.id == n.chit_id).first() if n.chit_id else None

    return PromissoryNoteResponse(
        id=n.id,
        pronote_id=n.pronote_id,
        member_id=n.member_id,
        chit_id=n.chit_id,
        loan_amount=n.loan_amount,
        issue_date=n.issue_date,
        due_date=n.due_date,
        interest_rate=n.interest_rate,
        repayment_amount=n.repayment_amount,
        purpose=n.purpose,
        status=n.status,
        signature=n.signature,
        member_name=member.name if member else f"Member #{n.member_id}",
        member_phone=member.phone if member else "N/A",
        member_email=member.email if member else "N/A",
        chit_name=chit.plan_name if chit else "N/A",
        created_at=n.created_at
    )


@router.delete("/{note_id}")
def delete_promissory_note(
    note_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    n = db.query(PromissoryNote).filter(PromissoryNote.id == note_id).first()
    if not n:
        raise HTTPException(status_code=404, detail="Promissory Note not found")

    db.delete(n)
    db.commit()
    return {"success": True, "message": "Promissory Note deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.user import User
from app.models.chit_plan import ChitPlan
from app.models.promissory_note import PromissoryNote, PronoteStatus
from app.schemas.promissory_note import PromissoryNoteResponse, PromissoryNoteSign
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/pronotes", tags=["Member Promissory Notes"])


@router.get("/my-pronotes", response_model=List[PromissoryNoteResponse])
def get_my_promissory_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves all promissory notes issued to the logged-in member."""
    notes = db.query(PromissoryNote).filter(
        PromissoryNote.member_id == current_user.id
    ).order_by(PromissoryNote.created_at.desc()).all()

    results = []
    for n in notes:
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
            member_name=current_user.name or current_user.username,
            member_phone=current_user.phone or "N/A",
            member_email=current_user.email or "N/A",
            chit_name=chit.plan_name if chit else "General Security",
            created_at=n.created_at
        ))

    return results


@router.put("/{note_id}/sign", response_model=PromissoryNoteResponse)
def sign_my_promissory_note(
    note_id: int,
    sign_in: PromissoryNoteSign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Allows winning member to draw & submit their digital signature to sign their Promissory Note."""
    note = db.query(PromissoryNote).filter(
        PromissoryNote.id == note_id,
        PromissoryNote.member_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Promissory Note not found for current user")

    if not sign_in.signature or len(sign_in.signature.strip()) < 20:
        raise HTTPException(status_code=400, detail="Invalid digital signature provided")

    note.signature = sign_in.signature
    note.status = PronoteStatus.active
    db.commit()
    db.refresh(note)

    chit = db.query(ChitPlan).filter(ChitPlan.id == note.chit_id).first() if note.chit_id else None

    return PromissoryNoteResponse(
        id=note.id,
        pronote_id=note.pronote_id,
        member_id=note.member_id,
        chit_id=note.chit_id,
        loan_amount=note.loan_amount,
        issue_date=note.issue_date,
        due_date=note.due_date,
        interest_rate=note.interest_rate,
        repayment_amount=note.repayment_amount,
        purpose=note.purpose,
        status=note.status,
        signature=note.signature,
        member_name=current_user.name or current_user.username,
        member_phone=current_user.phone or "N/A",
        member_email=current_user.email or "N/A",
        chit_name=chit.plan_name if chit else "General Security",
        created_at=note.created_at
    )

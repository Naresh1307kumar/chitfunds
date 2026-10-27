from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.promissory_note import PronoteStatus


class PromissoryNoteBase(BaseModel):
    member_id: int
    chit_id: Optional[int] = None
    loan_amount: float
    issue_date: date
    due_date: date
    interest_rate: float = 0.0
    repayment_amount: float
    purpose: Optional[str] = None
    status: PronoteStatus = PronoteStatus.active
    signature: Optional[str] = None


class PromissoryNoteCreate(PromissoryNoteBase):
    pass


class PromissoryNoteUpdateStatus(BaseModel):
    status: PronoteStatus


class PromissoryNoteSign(BaseModel):
    signature: str



class PromissoryNoteResponse(PromissoryNoteBase):
    id: int
    pronote_id: str
    member_name: Optional[str] = None
    member_phone: Optional[str] = None
    member_email: Optional[str] = None
    chit_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

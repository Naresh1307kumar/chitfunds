from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.payment import PaymentStatus

class PaymentCreate(BaseModel):
    installment_id: int
    amount: float
    payment_method: str
    transaction_id: str
    notes: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    installment_id: int
    user_id: int
    amount: float
    payment_method: str
    transaction_id: Optional[str]
    status: PaymentStatus
    notes: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PaymentUpdateStatus(BaseModel):
    status: PaymentStatus
    notes: Optional[str] = None

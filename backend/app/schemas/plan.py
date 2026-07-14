from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from app.models.chit_plan import PlanType, PlanStatus

class ChitPlanBase(BaseModel):
    plan_name: str
    plan_type: PlanType
    monthly_amount: float
    total_members: int
    duration_months: int
    commission_rate: float
    start_date: date

class ChitPlanCreate(ChitPlanBase):
    pass

class ChitPlanUpdate(BaseModel):
    plan_name: Optional[str] = None
    plan_type: Optional[PlanType] = None
    monthly_amount: Optional[float] = None
    total_members: Optional[int] = None
    duration_months: Optional[int] = None
    commission_rate: Optional[float] = None
    start_date: Optional[date] = None
    status: Optional[PlanStatus] = None

class ChitPlanResponse(ChitPlanBase):
    id: int
    current_members: int
    total_value: float
    net_prize_amount: float
    end_date: date
    status: PlanStatus
    is_deleted: bool
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

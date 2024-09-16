from pydantic import BaseModel
from datetime import datetime,date
from typing import Optional

class LeaveRequestBase(BaseModel):
    user_id: int
    leave_type: str
    start_date: date
    end_date: date
    status: Optional[str] = 'pending'

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequest(LeaveRequestBase):
    leave_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                leave_id=obj.leave_id,
                user_id=obj.user_id,
                leave_type=obj.leave_type,
                start_date=obj.start_date,
                end_date=obj.end_date,
                status=obj.status,
                created_at=obj.created_at,
                updated_at=obj.updated_at
            )

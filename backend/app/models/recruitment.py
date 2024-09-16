from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RecruitmentBase(BaseModel):
    job_title: str
    job_description: Optional[str] = None
    recruiter_id: Optional[int] = None
    closing_date: Optional[datetime] = None
    status: Optional[str] = 'open'

class RecruitmentCreate(RecruitmentBase):
    pass

class Recruitment(RecruitmentBase):
    recruitment_id: int
    posting_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                recruitment_id=obj.recruitment_id,
                job_title=obj.job_title,
                job_description=obj.job_description,
                recruiter_id=obj.recruiter_id,
                posting_date=obj.posting_date,
                closing_date=obj.closing_date,
                status=obj.status,
                created_at=obj.created_at,
                updated_at=obj.updated_at
            )

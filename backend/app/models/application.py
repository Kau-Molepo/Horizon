from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ApplicationBase(BaseModel):
    recruitment_id: int
    applicant_name: str
    applicant_email: EmailStr
    resume: Optional[str] = None
    status: Optional[str] = 'applied'

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    application_id: int
    applied_on: datetime
    updated_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                application_id=obj.application_id,
                recruitment_id=obj.recruitment_id,
                applicant_name=obj.applicant_name,
                applicant_email=obj.applicant_email,
                resume=obj.resume,
                status=obj.status,
                applied_on=obj.applied_on,
                updated_at=obj.updated_at
            )

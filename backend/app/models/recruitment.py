from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    position: str
    application_date: date

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int
    status: Optional[str] = "pending"  # Default status

    class Config:
        orm_mode = True

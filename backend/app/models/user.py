from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = None

class UserCreate(UserBase):
    password: str  # To be hashed before storing

class User(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                user_id=obj.user_id,
                username=obj.username,
                email=obj.email,
                full_name=obj.full_name,
                role=obj.role,
                created_at=obj.created_at,
                updated_at=obj.updated_at
            )

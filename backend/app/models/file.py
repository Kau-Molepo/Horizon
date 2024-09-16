from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileBase(BaseModel):
    user_id: Optional[int] = None
    file_name: str
    file_type: str
    file_size: Optional[int] = None

class FileCreate(FileBase):
    pass

class File(FileBase):
    file_id: int
    uploaded_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                file_id=obj.file_id,
                user_id=obj.user_id,
                file_name=obj.file_name,
                file_type=obj.file_type,
                file_size=obj.file_size,
                uploaded_at=obj.uploaded_at
            )

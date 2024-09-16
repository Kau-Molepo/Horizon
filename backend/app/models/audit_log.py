from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditLogBase(BaseModel):
    user_id: int
    action: str
    table_name: str
    record_id: int
    changes: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    audit_id: int
    created_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                audit_id=obj.audit_id,
                user_id=obj.user_id,
                action=obj.action,
                table_name=obj.table_name,
                record_id=obj.record_id,
                changes=obj.changes,
                created_at=obj.created_at
            )

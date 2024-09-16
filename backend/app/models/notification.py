from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    user_id: int
    message: str
    is_read: Optional[bool] = False

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    notification_id: int
    sent_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                notification_id=obj.notification_id,
                user_id=obj.user_id,
                message=obj.message,
                is_read=obj.is_read,
                sent_at=obj.sent_at
            )

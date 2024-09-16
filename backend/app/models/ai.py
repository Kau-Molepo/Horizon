from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AIAnalyticsBase(BaseModel):
    user_id: int
    ai_model_type: Optional[str] = None
    input_data: Optional[str] = None
    output_data: Optional[str] = None
    confidence_level: Optional[float] = None

class AIAnalyticsCreate(AIAnalyticsBase):
    pass

class AIAnalytics(AIAnalyticsBase):
    ai_id: int
    interaction_date: datetime
    created_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                ai_id=obj.ai_id,
                user_id=obj.user_id,
                ai_model_type=obj.model_type,
                input_data=obj.input_data,
                output_data=obj.output_data,
                confidence_level=obj.confidence_level,
                interaction_date=obj.interaction_date,
                created_at=obj.created_at
            )

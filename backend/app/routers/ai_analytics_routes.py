from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db.schemas import AIAnalyticsCreate, AIAnalyticsOut, AIAnalyticsUpdate
from models import AIAnalytics
from database import get_db

ai_analytics_router = APIRouter()

@ai_analytics_router.post("/", response_model=AIAnalyticsOut)
def create_ai_analytics(ai_analytics: AIAnalyticsCreate, db: Session = Depends(get_db)):
    db_ai_analytics = AIAnalytics.create(ai_analytics, db)
    if not db_ai_analytics:
        raise HTTPException(status_code=400, detail="AI Analytics creation failed")
    return db_ai_analytics

@ai_analytics_router.get("/{ai_id}", response_model=AIAnalyticsOut)
def get_ai_analytics(ai_id: int, db: Session = Depends(get_db)):
    db_ai_analytics = AIAnalytics.get(ai_id, db)
    if not db_ai_analytics:
        raise HTTPException(status_code=404, detail="AI Analytics not found")
    return db_ai_analytics

@ai_analytics_router.put("/{ai_id}", response_model=AIAnalyticsOut)
def update_ai_analytics(ai_id: int, ai_analytics: AIAnalyticsUpdate, db: Session = Depends(get_db)):
    db_ai_analytics = AIAnalytics.update(ai_id, ai_analytics, db)
    if not db_ai_analytics:
        raise HTTPException(status_code=404, detail="AI Analytics not found")
    return db_ai_analytics

@ai_analytics_router.delete("/{ai_id}", response_model=dict)
def delete_ai_analytics(ai_id: int, db: Session = Depends(get_db)):
    result = AIAnalytics.delete(ai_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="AI Analytics not found")
    return {"status": "AI Analytics deleted"}

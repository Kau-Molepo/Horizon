from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db.schemas import NotificationCreate, NotificationOut, NotificationUpdate
from models import Notification
from database import get_db

notification_router = APIRouter()

@notification_router.post("/", response_model=NotificationOut)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = Notification.create(notification, db)
    if not db_notification:
        raise HTTPException(status_code=400, detail="Notification creation failed")
    return db_notification

@notification_router.get("/{notification_id}", response_model=NotificationOut)
def get_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = Notification.get(notification_id, db)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@notification_router.put("/{notification_id}", response_model=NotificationOut)
def update_notification(notification_id: int, notification: NotificationUpdate, db: Session = Depends(get_db)):
    db_notification = Notification.update(notification_id, notification, db)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@notification_router.delete("/{notification_id}", response_model=dict)
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    result = Notification.delete(notification_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "Notification deleted"}

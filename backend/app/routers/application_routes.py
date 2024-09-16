from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db.schemas import ApplicationCreate, ApplicationOut, ApplicationUpdate
from models import Application
from database import get_db

application_router = APIRouter()

@application_router.post("/", response_model=ApplicationOut)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    db_application = Application.create(application, db)
    if not db_application:
        raise HTTPException(status_code=400, detail="Application creation failed")
    return db_application

@application_router.get("/{application_id}", response_model=ApplicationOut)
def get_application(application_id: int, db: Session = Depends(get_db)):
    db_application = Application.get(application_id, db)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application

@application_router.put("/{application_id}", response_model=ApplicationOut)
def update_application(application_id: int, application: ApplicationUpdate, db: Session = Depends(get_db)):
    db_application = Application.update(application_id, application, db)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application

@application_router.delete("/{application_id}", response_model=dict)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    result = Application.delete(application_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"status": "Application deleted"}

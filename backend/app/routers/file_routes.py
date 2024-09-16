from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from db.schemas import FileCreate, FileOut, FileUpdate
from models import File
from database import get_db

file_router = APIRouter()

@file_router.post("/", response_model=FileOut)
def create_file(file: FileCreate, db: Session = Depends(get_db)):
    db_file = File.create(file, db)
    if not db_file:
        raise HTTPException(status_code=400, detail="File creation failed")
    return db_file

@file_router.get("/{file_id}", response_model=FileOut)
def get_file(file_id: int, db: Session = Depends(get_db)):
    db_file = File.get(file_id, db)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@file_router.put("/{file_id}", response_model=FileOut)
def update_file(file_id: int, file: FileUpdate, db: Session = Depends(get_db)):
    db_file = File.update(file_id, file, db)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@file_router.delete("/{file_id}", response_model=dict)
def delete_file(file_id: int, db: Session = Depends(get_db)):
    result = File.delete(file_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="File not found")
    return {"status": "File deleted"}

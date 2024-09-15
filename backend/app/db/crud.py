from sqlalchemy.orm import Session
from . import models
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from models import user as user_model
from models import payroll as payroll_model
from models import recruitment as recruitment_model

# User CRUD
def create_user(db: Session, user: user_model.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Payroll CRUD
def create_payroll(db: Session, payroll: payroll_model.PayrollCreate):
    net_salary = payroll.gross_salary - payroll.taxes
    db_payroll = models.Payroll(**payroll.dict(), net_salary=net_salary)
    db.add(db_payroll)
    db.commit()
    db.refresh(db_payroll)
    return db_payroll

def get_payrolls(db: Session, employee_id: int):
    return db.query(models.Payroll).filter(models.Payroll.employee_id == employee_id).all()

# Candidate CRUD
def create_candidate(db: Session, candidate: recruitment_model.CandidateCreate):
    db_candidate = models.Candidate(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def get_candidates(db: Session):
    return db.query(models.Candidate).all()

def update_candidate_status(db: Session, candidate_id: int, status: str):
    db_candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    db_candidate.status = status
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

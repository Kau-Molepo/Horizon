from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from .base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

class Payroll(Base):
    __tablename__ = "payrolls"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True)
    gross_salary = Column(Float)
    taxes = Column(Float)
    net_salary = Column(Float)
    payroll_date = Column(Date)

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    position = Column(String)
    application_date = Column(Date)
    status = Column(String, default="pending")

from pydantic import BaseModel
from typing import Optional
from datetime import date

class PayrollBase(BaseModel):
    employee_id: int
    gross_salary: float
    taxes: float
    payroll_date: date

class PayrollCreate(PayrollBase):
    pass

class Payroll(PayrollBase):
    id: int
    net_salary: float

    class Config:
        orm_mode = True

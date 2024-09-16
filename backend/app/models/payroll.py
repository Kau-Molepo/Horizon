from pydantic import BaseModel
from datetime import date
from typing import Optional

class PayrollBase(BaseModel):
    user_id: int
    base_salary: float
    bonuses: Optional[float] = 0
    deductions: Optional[float] = 0
    pay_period: date

class PayrollCreate(PayrollBase):
    pass

class Payroll(PayrollBase):
    payroll_id: int
    total_salary: float  # This will be computed elsewhere

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                payroll_id=obj.payroll_id,
                user_id=obj.user_id,
                base_salary=obj.base_salary,
                bonuses=obj.bonuses,
                deductions=obj.deductions,
                pay_period=obj.pay_period,
                total_salary=obj.total_salary
            )

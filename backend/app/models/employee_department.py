from pydantic import BaseModel
from datetime import datetime

class EmployeeDepartmentBase(BaseModel):
    employee_id: int
    department_id: int

class EmployeeDepartmentCreate(EmployeeDepartmentBase):
    pass

class EmployeeDepartment(EmployeeDepartmentBase):
    assigned_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                employee_id=obj.employee_id,
                department_id=obj.department_id,
                assigned_at=obj.assigned_at
            )

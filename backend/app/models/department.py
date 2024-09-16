from pydantic import BaseModel
from datetime import datetime

class DepartmentBase(BaseModel):
    department_name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    department_id: int
    created_at: datetime

    class Config:
        @classmethod
        def from_orm(cls, obj):
            return cls(
                department_id=obj.department_id,
                department_name=obj.department_name,
                created_at=obj.created_at
            )

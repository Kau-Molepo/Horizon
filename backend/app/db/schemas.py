from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    hashed_password: str
    role: Optional[str] = None

class UserOut(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    hashed_password: Optional[str] = None
    role: Optional[str] = None

# Payroll Schemas
class PayrollCreate(BaseModel):
    user_id: int
    base_salary: float
    bonuses: Optional[float] = 0
    deductions: Optional[float] = 0
    pay_period: date

class PayrollOut(BaseModel):
    payroll_id: int
    user_id: int
    base_salary: float
    bonuses: float
    deductions: float
    total_salary: float  # Computed field
    pay_period: date
    created_at: datetime
    updated_at: datetime

class PayrollUpdate(BaseModel):
    base_salary: Optional[float] = None
    bonuses: Optional[float] = None
    deductions: Optional[float] = None
    pay_period: Optional[date] = None

# Recruitment Schemas
class RecruitmentCreate(BaseModel):
    job_title: str
    job_description: Optional[str] = None
    recruiter_id: Optional[int] = None
    posting_date: datetime
    closing_date: Optional[datetime] = None
    status: Optional[str] = 'open'

class RecruitmentOut(BaseModel):
    recruitment_id: int
    job_title: str
    job_description: Optional[str] = None
    recruiter_id: Optional[int] = None
    posting_date: datetime
    closing_date: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: datetime

class RecruitmentUpdate(BaseModel):
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    recruiter_id: Optional[int] = None
    posting_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    status: Optional[str] = None

# Application Schemas
class ApplicationCreate(BaseModel):
    recruitment_id: int
    applicant_name: str
    applicant_email: EmailStr
    resume: Optional[str] = None
    status: Optional[str] = 'applied'

class ApplicationOut(BaseModel):
    application_id: int
    recruitment_id: int
    applicant_name: str
    applicant_email: EmailStr
    resume: Optional[str] = None
    status: str
    applied_on: datetime
    updated_at: datetime

class ApplicationUpdate(BaseModel):
    applicant_name: Optional[str] = None
    applicant_email: Optional[EmailStr] = None
    resume: Optional[str] = None
    status: Optional[str] = None

# AI Analytics Schemas
class AIAnalyticsCreate(BaseModel):
    user_id: int
    ai_model_type: Optional[str] = None
    input_data: Optional[str] = None
    output_data: Optional[str] = None
    confidence_level: Optional[float] = None

class AIAnalyticsOut(BaseModel):
    ai_id: int
    user_id: int
    ai_model_type: Optional[str] = None
    input_data: Optional[str] = None
    output_data: Optional[str] = None
    confidence_level: Optional[float] = None
    interaction_date: datetime
    created_at: datetime

class AIAnalyticsUpdate(BaseModel):
    ai_model_type: Optional[str] = None
    input_data: Optional[str] = None
    output_data: Optional[str] = None
    confidence_level: Optional[float] = None

# Leave Request Schemas
class LeaveRequestCreate(BaseModel):
    user_id: int
    leave_type: str
    start_date: date
    end_date: date
    status: Optional[str] = 'pending'

class LeaveRequestUpdate(BaseModel):
    leave_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None

class LeaveRequestOut(BaseModel):
    leave_id: int
    user_id: int
    leave_type: str
    start_date: date
    end_date: date
    status: str
    created_at: datetime
    updated_at: datetime

# File Schemas
class FileCreate(BaseModel):
    user_id: Optional[int] = None
    file_name: str
    file_type: str
    file_size: Optional[int] = None

class FileOut(BaseModel):
    file_id: int
    user_id: Optional[int] = None
    file_name: str
    file_type: str
    file_size: Optional[int] = None
    uploaded_at: datetime

class FileUpdate(BaseModel):
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None

# Audit Log Schemas
class AuditLogCreate(BaseModel):
    user_id: Optional[int] = None  # The user who performed the action
    action: str  # The type of action (e.g., 'create', 'update', 'delete')
    entity_type: str  # The type of entity affected (e.g., 'user', 'payroll', 'application')
    entity_id: Optional[int] = None  # The ID of the affected entity (if applicable)
    details: Optional[str] = None  # Additional details about the action

class AuditLogOut(BaseModel):
    audit_id: int  # Unique ID of the audit log entry
    user_id: Optional[int] = None  # The user who performed the action
    action: str  # The type of action performed
    entity_type: str  # The type of entity affected
    entity_id: Optional[int] = None  # The ID of the affected entity
    details: Optional[str] = None  # Additional details about the action
    timestamp: datetime  # When the action took place

class AuditLogUpdate(BaseModel):
    action: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    details: Optional[str] = None

# Notification Schemas
class NotificationCreate(BaseModel):
    user_id: int  # The user to whom the notification will be sent
    message: str  # The content of the notification
    notification_type: Optional[str] = None  # Type of notification (e.g., 'info', 'warning', 'error')
    is_read: bool = False  # Indicates if the notification has been read
    timestamp: Optional[datetime] = None  # When the notification was created (default to now)

class NotificationOut(BaseModel):
    notification_id: int  # Unique ID of the notification
    user_id: int  # The user who received the notification
    message: str  # The content of the notification
    notification_type: Optional[str] = None  # Type of notification
    is_read: bool  # Indicates if the notification has been read
    timestamp: datetime  # When the notification was created

class NotificationUpdate(BaseModel):
    message: Optional[str] = None  # The content of the notification
    notification_type: Optional[str] = None  # Type of notification
    is_read: Optional[bool] = None  # Update the read status

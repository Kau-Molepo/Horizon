from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, DECIMAL, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    payroll = relationship('Payroll', back_populates='user')
    recruitment = relationship('Recruitment', back_populates='recruiter')
    ai_analytics = relationship('AIAnalytics', back_populates='user')
    audit_logs = relationship('AuditLog', back_populates='user')
    notifications = relationship('Notification', back_populates='user')
    leave_requests = relationship('LeaveRequest', back_populates='user')

class Payroll(Base):
    __tablename__ = 'payroll'
    
    payroll_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    base_salary = Column(DECIMAL(12, 2), nullable=False)
    bonuses = Column(DECIMAL(12, 2), default=0)
    deductions = Column(DECIMAL(12, 2), default=0)
    total_salary = Column(DECIMAL(12, 2), nullable=False)  # Total salary is computed elsewhere
    pay_period = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship('User', back_populates='payroll')

class Recruitment(Base):
    __tablename__ = 'recruitment'
    
    recruitment_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(100), nullable=False)
    job_description = Column(Text)
    recruiter_id = Column(Integer, ForeignKey('users.user_id', ondelete="SET NULL"))
    posting_date = Column(TIMESTAMP, server_default=func.now())
    closing_date = Column(TIMESTAMP)
    status = Column(String(50), default='open')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    recruiter = relationship('User', back_populates='recruitment')
    applications = relationship('Application', back_populates='recruitment')

class Application(Base):
    __tablename__ = 'applications'
    
    application_id = Column(Integer, primary_key=True, index=True)
    recruitment_id = Column(Integer, ForeignKey('recruitment.recruitment_id', ondelete="CASCADE"), nullable=False)
    applicant_name = Column(String(100), nullable=False)
    applicant_email = Column(String(100), nullable=False)
    resume = Column(Text)
    status = Column(String(50), default='applied')
    applied_on = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    recruitment = relationship('Recruitment', back_populates='applications')

class AIAnalytics(Base):
    __tablename__ = 'ai_analytics'
    
    ai_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    ai_model_type = Column(String(50))
    input_data = Column(Text)
    output_data = Column(Text)
    confidence_level = Column(DECIMAL(5, 4))
    interaction_date = Column(TIMESTAMP, server_default=func.now())
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship('User', back_populates='ai_analytics')

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    audit_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    action = Column(String(255), nullable=False)
    table_name = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    changes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship('User', back_populates='audit_logs')

class Notification(Base):
    __tablename__ = 'notifications'
    
    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    sent_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship('User', back_populates='notifications')

class LeaveRequest(Base):
    __tablename__ = 'leave_requests'
    
    leave_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    leave_type = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(50), default='pending')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship('User', back_populates='leave_requests')

# Add more models for departments, files, and employee-department relationships if needed.

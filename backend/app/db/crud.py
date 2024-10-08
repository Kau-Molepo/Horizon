import bcrypt
import jwt
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from .models import *
from .schemas import *
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from dotenv import load_dotenv
from firebase.auth import *

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SECRET_KEY =  os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

# === USERS CRUD ===

def create_user(db: Session, user: UserCreate):
    try:
        # 1. Create Firebase user
        firebase_user = auth.create_user(
            email=user.email,
            password=user.password,
            display_name=user.full_name
        )

        firebase_uid = firebase_user.uid
        # print(firebase_uid)
        # 2. Check if user already exists in backend
        existing_user = db.query(User).filter(User.hashed_firebase_uid == firebase_uid).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # 3. Hash the Firebase UID before storing
        hashed_firebase_uid = bcrypt.hashpw(firebase_uid.encode('utf-8'), bcrypt.gensalt())

        # 4. Hash the password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        # 5. Create user in backend database
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password.decode('utf-8'),
            full_name=user.full_name,
            role=user.role,
            hashed_firebase_uid=hashed_firebase_uid.decode('utf-8')  # Store hashed UID
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating user in database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.error(f"Error during Firebase authentication: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def authenticate_user(db: Session, user: UserLogin):
    try:
        # 1. Authenticate with Firebase and get the Firebase UID
        firebase_user = firebase_login(user.email, user.password)  # Your function to log in via Firebase
        
        # 2. Verify Firebase ID token and extract the UID
        firebase_uid = firebase_user['localId']
        
        # 3. Find the user in the FastAPI database using the email
        db_user = db.query(User).filter(User.email == user.email).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found in FastAPI database")

        # 4. Compare the stored hashed Firebase UID with the one returned from Firebase
        stored_hashed_firebase_uid = db_user.hashed_firebase_uid.encode('utf-8')
        if not bcrypt.checkpw(firebase_uid.encode('utf-8'), stored_hashed_firebase_uid):
            raise HTTPException(status_code=401, detail="Invalid Firebase UID")

        # 5. If Firebase UID matches, create a FastAPI JWT token
        access_token = create_access_token(
            data={"sub": db_user.email, "role": db_user.role}  # Adding user's email and role to token
        )

        # 6. Attach the JWT to the db_user object
        db_user.access_token = access_token  # Assume we modify the model or schema to handle tokens

        # Return the db_user object itself (it will be used in user-routes and will be serialized properly)
        return db_user

    except SQLAlchemyError as e:
        # Handle any database-related errors
        print(f"Error authenticating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        # Log and raise other exceptions
        print(f"Error during authentication: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db: Session, user_id: int):
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    except SQLAlchemyError as e:
        print(f"Error retrieving user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_user_by_username(db: Session, username: str):
    try:
        return db.query(User).filter(User.username == username).first()
    except SQLAlchemyError as e:
        print(f"Error retrieving user with username {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user:
            for key, value in user_update.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_user(db: Session, user_id: int):
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user:
            # Delete user from Firebase
            delete_firebase_user(db_user.hashed_firebase_uid)
            
            # Delete user from database
            db.delete(db_user)
            db.commit()
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# === PAYROLL CRUD ===

def create_payroll(db: Session, payroll: PayrollCreate):
    try:
        db_payroll = Payroll(
            user_id=payroll.user_id,
            base_salary=payroll.base_salary,
            bonuses=payroll.bonuses,
            deductions=payroll.deductions,
            total_salary=payroll.base_salary + payroll.bonuses - payroll.deductions,
            pay_period=payroll.pay_period
        )
        db.add(db_payroll)
        db.commit()
        db.refresh(db_payroll)
        return db_payroll
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error creating payroll record: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_payroll_by_user(db: Session, user_id: int):
    try:
        return db.query(Payroll).filter(Payroll.user_id == user_id).all()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving payroll records for user ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_payroll(db: Session, payroll_id: int):
    try:
        return db.query(Payroll).filter(Payroll.payroll_id == payroll_id).first()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving payroll record with ID {payroll_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def update_payroll(db: Session, payroll_id: int, payroll_update: PayrollCreate):
    try:
        db_payroll = db.query(Payroll).filter(Payroll.payroll_id == payroll_id).first()
        if db_payroll:
            db_payroll.base_salary = payroll_update.base_salary
            db_payroll.bonuses = payroll_update.bonuses
            db_payroll.deductions = payroll_update.deductions
            db_payroll.total_salary = payroll_update.base_salary + payroll_update.bonuses - payroll_update.deductions
            db_payroll.pay_period = payroll_update.pay_period
            db.commit()
            db.refresh(db_payroll)
            return db_payroll
        else:
            raise HTTPException(status_code=404, detail="Payroll record not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error updating payroll record with ID {payroll_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_payroll(db: Session, payroll_id: int):
    try:
        db_payroll = db.query(Payroll).filter(Payroll.payroll_id == payroll_id).first()
        if db_payroll:
            db.delete(db_payroll)
            db.commit()
            return db_payroll
        else:
            raise HTTPException(status_code=404, detail="Payroll record not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error deleting payroll record with ID {payroll_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# === RECRUITMENT CRUD ===

def create_recruitment(db: Session, recruitment: RecruitmentCreate):
    try:
        db_recruitment = Recruitment(
            job_title=recruitment.job_title,
            job_description=recruitment.job_description,
            recruiter_id=recruitment.recruiter_id,
            posting_date=recruitment.posting_date,
            closing_date=recruitment.closing_date,
            status=recruitment.status
        )
        db.add(db_recruitment)
        db.commit()
        db.refresh(db_recruitment)
        return db_recruitment
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error creating recruitment record: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_recruitment(db: Session, recruitment_id: int):
    try:
        return db.query(Recruitment).filter(Recruitment.recruitment_id == recruitment_id).first()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving recruitment record with ID {recruitment_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_all_recruitments(db: Session):
    try:
        return db.query(Recruitment).all()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving all recruitment records: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def update_recruitment(db: Session, recruitment_id: int, recruitment_update: RecruitmentCreate):
    try:
        db_recruitment = db.query(Recruitment).filter(Recruitment.recruitment_id == recruitment_id).first()
        if db_recruitment:
            db_recruitment.job_title = recruitment_update.job_title
            db_recruitment.job_description = recruitment_update.job_description
            db_recruitment.closing_date = recruitment_update.closing_date
            db_recruitment.status = recruitment_update.status
            db.commit()
            db.refresh(db_recruitment)
            return db_recruitment
        else:
            raise HTTPException(status_code=404, detail="Recruitment record not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error updating recruitment record with ID {recruitment_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_recruitment(db: Session, recruitment_id: int):
    try:
        db_recruitment = db.query(Recruitment).filter(Recruitment.recruitment_id == recruitment_id).first()
        if db_recruitment:
            db.delete(db_recruitment)
            db.commit()
            return db_recruitment
        else:
            raise HTTPException(status_code=404, detail="Recruitment record not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error deleting recruitment record with ID {recruitment_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# === APPLICATION CRUD ===

def create_application(db: Session, application: ApplicationCreate):
    try:
        db_application = Application(
            recruitment_id=application.recruitment_id,
            applicant_name=application.applicant_name,
            resume=application.resume,
            cover_letter=application.cover_letter,
            status=application.status
        )
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        return db_application
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error creating application record: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_application(db: Session, application_id: int):
    try:
        return db.query(Application).filter(Application.application_id == application_id).first()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving application record with ID {application_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_applications_by_recruitment(db: Session, recruitment_id: int):
    try:
        return db.query(Application).filter(Application.recruitment_id == recruitment_id).all()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving applications for recruitment ID {recruitment_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def update_application(db: Session, application_id: int, application_update: ApplicationCreate):
    try:
        db_application = db.query(Application).filter(Application.application_id == application_id).first()
        if db_application:
            db_application.resume = application_update.resume
            db_application.cover_letter = application_update.cover_letter
            db_application.status = application_update.status
            db.commit()
            db.refresh(db_application)
            return db_application
        else:
            raise HTTPException(status_code=404, detail="Application record not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error updating application record with ID {application_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_application(db: Session, application_id: int):
    try:
        db_application = db.query(Application).filter(Application.application_id == application_id).first()
        if db_application:
            db.delete(db_application)
            db.commit()
            return db_application
        else:
            raise HTTPException(status_code=404, detail="Application record not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error deleting application record with ID {application_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# === AI ANALYTICS CRUD ===

def create_ai_analytics(db: Session, ai_analytics: AIAnalyticsCreate):
    try:
        db_ai_analytics = AIAnalytics(
            user_id=ai_analytics.user_id,
            data=ai_analytics.data,
            analysis_results=ai_analytics.analysis_results
        )
        db.add(db_ai_analytics)
        db.commit()
        db.refresh(db_ai_analytics)
        return db_ai_analytics
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error creating AI analytics record: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_ai_analytics(db: Session, ai_analytics_id: int):
    try:
        return db.query(AIAnalytics).filter(AIAnalytics.ai_analytics_id == ai_analytics_id).first()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving AI analytics record with ID {ai_analytics_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_ai_analytics_by_user(db: Session, user_id: int):
    try:
        return db.query(AIAnalytics).filter(AIAnalytics.user_id == user_id).all()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving AI analytics records for user ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_ai_analytics(db: Session, ai_analytics_id: int):
    try:
        db_ai_analytics = db.query(AIAnalytics).filter(AIAnalytics.ai_analytics_id == ai_analytics_id).first()
        if db_ai_analytics:
            db.delete(db_ai_analytics)
            db.commit()
            return db_ai_analytics
        else:
            raise HTTPException(status_code=404, detail="AI analytics record not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error deleting AI analytics record with ID {ai_analytics_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# === AUDIT LOG CRUD ===

def create_audit_log(db: Session, audit_log: AuditLogCreate):
    try:
        db_audit_log = AuditLog(
            user_id=audit_log.user_id,
            action=audit_log.action,
            details=audit_log.details,
            timestamp=audit_log.timestamp
        )
        db.add(db_audit_log)
        db.commit()
        db.refresh(db_audit_log)
        return db_audit_log
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error creating audit log entry: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_audit_log(db: Session, audit_log_id: int):
    try:
        return db.query(AuditLog).filter(AuditLog.audit_log_id == audit_log_id).first()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving audit log entry with ID {audit_log_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_audit_logs_by_user(db: Session, user_id: int):
    try:
        return db.query(AuditLog).filter(AuditLog.user_id == user_id).all()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving audit logs for user ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# === NOTIFICATIONS CRUD ===

def create_notification(db: Session, notification: NotificationCreate):
    try:
        db_notification = Notification(
            user_id=notification.user_id,
            content=notification.content,
            read=notification.read,
            timestamp=notification.timestamp
        )
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error creating notification: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_notifications_by_user(db: Session, user_id: int):
    try:
        return db.query(Notification).filter(Notification.user_id == user_id).all()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving notifications for user ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def mark_notification_as_read(db: Session, notification_id: int):
    try:
        db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
        if db_notification:
            db_notification.read = True
            db.commit()
            db.refresh(db_notification)
            return db_notification
        else:
            raise HTTPException(status_code=404, detail="Notification not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error marking notification as read with ID {notification_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# === LEAVE REQUEST CRUD ===

def create_leave_request(db: Session, leave_request: LeaveRequestCreate):
    try:
        db_leave_request = LeaveRequest(
            user_id=leave_request.user_id,
            start_date=leave_request.start_date,
            end_date=leave_request.end_date,
            reason=leave_request.reason,
            status=leave_request.status
        )
        db.add(db_leave_request)
        db.commit()
        db.refresh(db_leave_request)
        return db_leave_request
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error creating leave request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_leave_request(db: Session, leave_request_id: int):
    try:
        return db.query(LeaveRequest).filter(LeaveRequest.leave_request_id == leave_request_id).first()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving leave request with ID {leave_request_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_leave_requests_by_user(db: Session, user_id: int):
    try:
        return db.query(LeaveRequest).filter(LeaveRequest.user_id == user_id).all()
    except SQLAlchemyError as e:
        # Log error
        print(f"Error retrieving leave requests for user ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def update_leave_request(db: Session, leave_request_id: int, leave_request_update: LeaveRequestUpdate):
    try:
        db_leave_request = db.query(LeaveRequest).filter(LeaveRequest.leave_request_id == leave_request_id).first()
        if db_leave_request:
            db_leave_request.start_date = leave_request_update.start_date
            db_leave_request.end_date = leave_request_update.end_date
            db_leave_request.reason = leave_request_update.reason
            db_leave_request.status = leave_request_update.status
            db.commit()
            db.refresh(db_leave_request)
            return db_leave_request
        else:
            raise HTTPException(status_code=404, detail="Leave request not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error updating leave request with ID {leave_request_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_leave_request(db: Session, leave_request_id: int):
    try:
        db_leave_request = db.query(LeaveRequest).filter(LeaveRequest.leave_request_id == leave_request_id).first()
        if db_leave_request:
            db.delete(db_leave_request)
            db.commit()
            return db_leave_request
        else:
            raise HTTPException(status_code=404, detail="Leave request not found")
    except SQLAlchemyError as e:
        db.rollback()
        # Log error
        print(f"Error deleting leave request with ID {leave_request_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

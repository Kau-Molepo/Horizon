---
noteId: "602f16b0784511ef8c3fed53ac353645"
tags: []

---

Horizon Project Documentation
Recruitment and Payroll Management System

Table of Contents
Introduction
System Architecture
Modules Overview
Recruitment
Payroll
User Roles
Administrator
Recruiter
Employee
Payroll Manager
Features
Recruitment Features
Payroll Features
Technical Details
Backend
Frontend
Database
API Endpoints
Recruitment APIs
Payroll APIs
Deployment and Setup
Future Enhancements

1. Introduction
The Horizon Project is designed to streamline the recruitment and payroll processes for organizations. The system enables recruiters to manage job postings, track applicants, and coordinate interviews, while also allowing HR managers to handle payroll efficiently. The system is built with scalability and security in mind, offering various tools and automation features to optimize workflows.

2. System Architecture
The Horizon Project follows a modular microservices architecture, separating core functionalities like recruitment and payroll into distinct services. The architecture ensures scalability, maintainability, and ease of integration with third-party services.

Key Components:
Frontend: Flutter-based mobile and web applications.
Backend: FastAPI for API development, integrated with Firebase for authentication and PostgreSQL/MySQL for database management.
Database: PostgreSQL/MySQL to store user data, job applications, and payroll information.
Authentication: Firebase for handling user authentication and authorization.
Deployment: Hosted on AWS/Vercel with CI/CD pipelines for continuous updates.
3. Modules Overview
Recruitment Module
The Recruitment module helps organizations post job openings, manage candidates, and schedule interviews.

Payroll Module
The Payroll module automates the payroll process, ensuring that employees are paid on time and their pay slips are accurately generated.

4. User Roles
Administrator
Has access to all features of the system.
Manages users, job postings, payroll processing, and system settings.
Recruiter
Responsible for posting jobs, managing applications, and scheduling interviews.
Employee
Can view job openings, apply for jobs, track application status, and view their payroll information.
Payroll Manager
Responsible for payroll processing, generating pay slips, and managing employee payment data.
5. Features
Recruitment Features
Job Postings: Recruiters can create and publish job listings.
Candidate Management: Manage candidate profiles, track application statuses, and move candidates through the recruitment pipeline.
Interview Scheduling: Integrated calendar feature for scheduling interviews.
Application Tracking System (ATS): A dashboard for recruiters to see where each candidate is in the hiring process.
Payroll Features
Payroll Calculation: Automates salary calculations based on employee data, deductions, and bonuses.
Employee Self-Service: Employees can view their pay slips and salary breakdown through a secure portal.
Tax Management: Automatically deducts taxes based on employee profiles and local tax laws.
Overtime and Bonuses: Payroll system supports overtime tracking and bonus calculations.
6. Technical Details
Backend
FastAPI: Used for creating RESTful APIs for recruitment and payroll functionalities.
Firebase: Handles authentication using Firebase Admin SDK. The backend validates Firebase tokens before processing any user requests.
Database: PostgreSQL/MySQL databases store user information, job postings, and payroll data.
Frontend
Flutter: A cross-platform mobile and web framework used to create the user interface.
Web App: Supports recruiters, employees, and admins on web platforms.
7. API Endpoints
Recruitment APIs
POST /jobs: Create a new job posting.
GET /jobs: Retrieve a list of job postings.
POST /applications: Submit a new job application.
GET /applications: Retrieve applications based on job ID or user ID.
PUT /applications/{id}: Update the status of a job application.
Payroll APIs
POST /payroll: Process payroll for all employees.
GET /payroll/{employee_id}: Retrieve payroll information for a specific employee.
PUT /payroll/{id}: Update payroll information (e.g., for adjustments).
GET /payroll/slip/{employee_id}: Generate and retrieve the employee’s pay slip for the current period.
8. Deployment and Setup
Environment Configuration:

Ensure environment variables for Firebase, PostgreSQL/MySQL, and other services are correctly set up in .env files.
Set up CI/CD pipelines with GitHub Actions or GitLab for automated testing and deployment.
Deployment to AWS/Vercel:

The backend is hosted on AWS Lambda, with API Gateway handling HTTP requests.
The frontend Flutter application is deployed using Vercel for web access and packaged for mobile deployment (iOS and Android).
9. Future Enhancements
Advanced Analytics: Add real-time data analytics for recruitment success rates and payroll processing trends.
AI-based Candidate Screening: Implement machine learning models to help recruiters shortlist candidates based on resume parsing and skill matching.
Payroll Customizations: Provide country-specific payroll configurations to account for local laws and regulations.
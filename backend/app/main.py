from fastapi import FastAPI
from routers import (
    user_routes,
    payroll_routes,
    recruitment_routes,
    application_routes,
    ai_analytics_routes,
    leave_request_routes,
    file_routes,
    audit_log_routes,
    notification_routes
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.user_router, prefix="/users", tags=["Users"])
app.include_router(payroll_routes.payroll_router, prefix="/payrolls", tags=["Payrolls"])
app.include_router(recruitment_routes.recruitment_router, prefix="/recruitments", tags=["Recruitments"])
app.include_router(application_routes.application_router, prefix="/applications", tags=["Applications"])
app.include_router(ai_analytics_routes.ai_analytics_router, prefix="/ai-analytics", tags=["AI Analytics"])
app.include_router(leave_request_routes.leave_request_router, prefix="/leave-requests", tags=["Leave Requests"])
app.include_router(file_routes.file_router, prefix="/files", tags=["Files"])
app.include_router(audit_log_routes.audit_log_router, prefix="/audit-logs", tags=["Audit Logs"])
app.include_router(notification_routes.notification_router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Horizon API!"}

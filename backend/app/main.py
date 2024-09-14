from fastapi import FastAPI
from app.routers import auth, payroll, recruitment, ai, user

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(payroll.router, prefix="/payroll", tags=["payroll"])
app.include_router(recruitment.router, prefix="/recruitment", tags=["recruitment"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(user.router, prefix="/user", tags=["user"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Horizon API!"}

from fastapi import FastAPI
from routers import auth, payroll, recruitment, ai, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(payroll.router, prefix="/payroll", tags=["payroll"])
app.include_router(recruitment.router, prefix="/recruitment", tags=["recruitment"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(user.router, prefix="/user", tags=["user"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Horizon API!"}

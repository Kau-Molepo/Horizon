from fastapi import HTTPException

def verify_role(user_role: str, required_role: str):
    if user_role != required_role:
        raise HTTPException(status_code=403, detail="Not authorized")

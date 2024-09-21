from .config import *
from firebase_admin import auth
from fastapi import HTTPException


def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

def create_firebase_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create Firebase user")

def delete_firebase_user(uid):
    try:
        auth.delete_user(uid)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to delete Firebase user")

def get_firebase_user(uid):
    try:
        return auth.get_user(uid)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Firebase user not found")
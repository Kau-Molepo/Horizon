from .config import *
from firebase_admin import auth
from fastapi import HTTPException
import os
import requests
from dotenv import load_dotenv

load_dotenv()

FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:"

# Firebase Admin SDK functions
def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

def create_firebase_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return user
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to create Firebase user")

def delete_firebase_user(uid):
    try:
        auth.delete_user(uid)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to delete Firebase user")

def get_firebase_user(uid):
    try:
        return auth.get_user(uid)
    except Exception:
        raise HTTPException(status_code=404, detail="Firebase user not found")

# User authentication functions using REST API
def firebase_login(email, password):
    try:
        response = requests.post(
            FIREBASE_AUTH_URL + "signInWithPassword?key=" + os.getenv('FIREBASE_API_KEY'),
            json={"email": email, "password": password, "returnSecureToken": True}
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise HTTPException(status_code=401, detail=str(e))

def firebase_register(email, password):
    try:
        response = requests.post(
            FIREBASE_AUTH_URL + "signUp?key=" + os.getenv('FIREBASE_API_KEY'),
            json={"email": email, "password": password, "returnSecureToken": True}
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Function to refresh ID token
def firebase_refresh_token(refresh_token):
    try:
        response = requests.post(
            FIREBASE_AUTH_URL + "token?key=" + os.getenv('FIREBASE_API_KEY'),
            json={"grant_type": "refresh_token", "refresh_token": refresh_token}
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise HTTPException(status_code=401, detail=str(e))

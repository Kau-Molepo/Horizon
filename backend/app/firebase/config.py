import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebase/horizon-315bd-firebase-adminsdk-lt3zd-5e44c71b82.json")
firebase_admin.initialize_app(cred)

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./horizon-315bd-firebase-adminsdk-lt3zd-5e44c71b82.json")
firebase_admin.initialize_app(cred)

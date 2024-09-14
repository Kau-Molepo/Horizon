from firebase_admin import auth

def get_user(uid):
    return auth.get_user(uid)

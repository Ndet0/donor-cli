# donor/user_manager.py
import os
from .db import SessionLocal, Base, engine
from .models import User

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# File to store the logged-in username temporarily
SESSION_FILE = os.path.join(os.path.dirname(__file__), "session.txt")


# User Management

def register_user(username, password):
    db = SessionLocal()
    if db.query(User).filter(User.username == username).first():
        return False, "Username already exists"
    user = User(username=username)
    user.set_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return True, user

def authenticate_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user and user.check_password(password):
        # Save username to session file
        with open(SESSION_FILE, "w") as f:
            f.write(username)
        return True, user
    return False, "Invalid credentials"

def logout_user():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        return True
    return False

def current_user():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        username = f.read().strip()
    db = SessionLocal()
    return db.query(User).filter(User.username == username).first()

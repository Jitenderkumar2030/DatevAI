# auth_service.py
from backend.models import SessionLocal, User  
from passlib.hash import bcrypt
import jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET", "testsecret")

def create_user(email, password, role="free"):
    db = SessionLocal()
    hashed_pw = bcrypt.hash(password)
    user = User(email=email, password=hashed_pw, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def authenticate_user(email, password):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    if user and bcrypt.verify(password, user.password):
        token = jwt.encode({"email": user.email, "role": user.role}, SECRET_KEY, algorithm="HS256")
        return token
    return None

import jwt
import os
from passlib.context import CryptContext

# Secret Key
SECRET = os.getenv("JWT_SECRET", "testsecret")

# Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash the user's password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_token(token: str) -> dict or None:
    """
    Verify and decode a JWT token. Return payload (email, role) if valid, else None.
    """
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload  # e.g. { "email": "...", "role": "pro" }
    except:
        return None

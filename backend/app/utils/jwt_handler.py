# jwt_handler.py — Tools for creating and verifying JWT tokens

from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# These values come from your .env file
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")          # HS256 = a symmetric signing algorithm
EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict) -> str:
    """
    Create a JWT token.
    
    'data' is a dictionary of information you want to bake into the token.
    Typically: {"user_id": 5, "role": "user"}
    
    The token is a string like: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    It is NOT encrypted — anyone can read it.
    But it IS signed — the server can verify it was created by us and not tampered with.
    """
    to_encode = data.copy()
    
    # Add an expiry time to the token
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # "exp" is a standard JWT field for expiry
    
    # Sign and encode the token using our secret key
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str) -> dict:
    """
    Verify and decode a JWT token.
    
    Returns the data that was encoded in the token (user_id, role, etc.)
    Raises an exception if the token is invalid, expired, or tampered with.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # e.g. {"user_id": 5, "role": "user", "exp": ...}
    except JWTError:
        return None  # Token is invalid or expired
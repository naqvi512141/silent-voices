# user_schema.py — Defines the shape of JSON data coming in and out of the auth endpoints

from pydantic import BaseModel, EmailStr
from typing import Optional

# --- INPUT SCHEMAS (what the API receives from the frontend) ---

class UserRegisterSchema(BaseModel):
    """
    This is what the frontend must send to POST /auth/register.
    Pydantic automatically validates that:
    - full_name is a string
    - email is a valid email format
    - password is a string
    If any field is wrong type or missing, FastAPI returns a 422 error automatically.
    """
    full_name: str
    email: EmailStr   # EmailStr validates it looks like a real email
    password: str

class UserLoginSchema(BaseModel):
    """What the frontend sends to POST /auth/login"""
    email: EmailStr
    password: str

# --- OUTPUT SCHEMAS (what the API sends back to the frontend) ---

class UserResponseSchema(BaseModel):
    """
    What we return about a user.
    Notice: password is NOT here — we never send the password back.
    """
    id: int
    full_name: str
    email: str
    role: str

    class Config:
        # This tells Pydantic it can read data from SQLAlchemy model objects
        # (not just plain dictionaries)
        from_attributes = True

class TokenSchema(BaseModel):
    """What we return after a successful login"""
    access_token: str
    token_type: str   # Always "bearer" — this is the HTTP standard
# auth.py — The authentication router
# Contains all endpoints under the /auth prefix

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import (
    UserRegisterSchema,
    UserLoginSchema,
    UserResponseSchema,
    TokenSchema
)
from app.utils.password_handler import hash_password, verify_password
from app.utils.jwt_handler import create_access_token, verify_access_token

# APIRouter is like a mini-application that groups related endpoints
# prefix="/auth" means all routes here are under /auth/...
router = APIRouter(prefix="/auth", tags=["Authentication"])

# OAuth2PasswordBearer tells FastAPI WHERE to find the token in the request
# It looks in the Authorization header for "Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ── REGISTRATION ─────────────────────────────────────────────────────────────

@router.post("/register", response_model=UserResponseSchema, status_code=201)
def register(user_data: UserRegisterSchema, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Steps:
    1. Check if the email is already taken
    2. Hash the password
    3. Save the new user to the database
    4. Return the user data (without password)
    """
    # Step 1: Check if a user with this email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        # 400 Bad Request — the client made an error (duplicate email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists"
        )
    
    # Step 2: Hash the password — NEVER save plain text
    hashed = hash_password(user_data.password)
    
    # Step 3: Create the User object and save to database
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed,
        role="user"   # New users are always 'user', not 'admin'
    )
    db.add(new_user)       # Stage the new row
    db.commit()            # Write it to the database permanently
    db.refresh(new_user)   # Reload the object to get the auto-assigned id
    
    # Step 4: Return the new user (Pydantic strips the password automatically)
    return new_user


# ── LOGIN ─────────────────────────────────────────────────────────────────────

@router.post("/login", response_model=TokenSchema)
def login(credentials: UserLoginSchema, db: Session = Depends(get_db)):
    """
    Log in and receive a JWT token.
    
    Steps:
    1. Find the user by email
    2. Verify the password
    3. Create a JWT token
    4. Return the token
    """
    # Step 1: Find the user
    user = db.query(User).filter(User.email == credentials.email).first()
    
    # Step 2: Verify — use a vague error message intentionally
    # Never tell the attacker whether the email or the password was wrong
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Step 3: Create the JWT token with useful claims baked in
    token = create_access_token(data={
        "user_id": user.id,
        "role": user.role,
        "email": user.email
    })
    
    # Step 4: Return it
    return {"access_token": token, "token_type": "bearer"}


# ── PROFILE (Protected Route) ─────────────────────────────────────────────────

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    This is a DEPENDENCY — FastAPI will call this function automatically
    for any endpoint that declares it as a dependency.
    
    It extracts the token from the request header, verifies it,
    and returns the current User object.
    
    If the token is invalid or missing, it raises a 401 error automatically.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user


@router.get("/profile", response_model=UserResponseSchema)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get the current logged-in user's profile.
    This is a protected endpoint — it requires a valid JWT token.
    
    Depends(get_current_user) tells FastAPI to call get_current_user first,
    and if it succeeds, pass the returned User object as 'current_user'.
    If it fails (invalid token), the endpoint never executes.
    """
    return current_user
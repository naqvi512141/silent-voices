# main.py — The entry point of your FastAPI application
# This is the first file that runs when you start the server

# Add these two imports alongside the existing user import
from app.models import user, session   # This tells Base about the new tables

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base


# Import the models so that Base knows about them
# Without this import, Base would not know the User table exists
from app.models import user

# Import and include the auth router
from app.routers import auth

# Create all tables that are defined in models that inherit from Base
# This is safe to call multiple times — it skips tables that already exist
Base.metadata.create_all(bind=engine)

# Create the FastAPI application instance
# This is your "app" — all routes and settings attach to this object
app = FastAPI(
    title="Silent Voices API",
    description="ASL to Text Translation System",
    version="1.0.0"
)

# CORS — Cross-Origin Resource Sharing
# This is necessary because your React frontend (running on port 3000)
# and your FastAPI backend (running on port 8000) are on different "origins".
# Without this, the browser will block all requests from React to FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's development URL
    allow_credentials=True,
    allow_methods=["*"],     # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],     # Allow all headers including Authorization
)

# Register the auth router — all its endpoints are now part of the app
app.include_router(auth.router)

# A simple test route — if you visit http://localhost:8000/ you should see this
@app.get("/")
def root():
    return {"message": "Silent Voices API is running"}
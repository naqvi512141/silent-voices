# main.py
#
# PURPOSE: Entry point of the FastAPI application.
# IMPORTANT ORDERING: Model imports must come BEFORE Base.metadata.create_all().
# SQLAlchemy's Base only knows about a table if its model class has been imported.
# If you call create_all() before importing session.py, the sessions and
# gesture_results tables will NOT be created in the database.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

# ── Import ALL models before create_all() ─────────────────────────
# Each import registers the table with SQLAlchemy's Base registry.
# Missing an import here = missing table in the database.
from app.models import user     # Registers the 'users' table
from app.models import session  # Registers the 'sessions' and 'gesture_results' tables

# ── Create tables in PostgreSQL ────────────────────────────────────
# safe to call multiple times — skips tables that already exist
Base.metadata.create_all(bind=engine)

# ── Import routers ─────────────────────────────────────────────────
from app.routers import auth    # /auth/register, /auth/login, /auth/profile
from app.routers import video   # /translate/upload

# ── Create the FastAPI application instance ────────────────────────
app = FastAPI(
    title="Silent Voices API",
    description="ASL to Text Translation System — FAST-NUCES SE Spring 2026",
    version="2.0.0"
)

# ── CORS — Cross-Origin Resource Sharing ──────────────────────────
# Without this, the browser blocks all requests from React (port 3000)
# to FastAPI (port 8000) because they are on different "origins."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ── Register all routers ───────────────────────────────────────────
app.include_router(auth.router)
app.include_router(video.router)

# ── Health check endpoint ──────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Silent Voices API is online",
        "docs": "/docs"
    }
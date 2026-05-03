# main.py — Entry point of the Silent Voices FastAPI application.
# CRITICAL: All model imports must come BEFORE Base.metadata.create_all().

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

# ── Import ALL models BEFORE create_all() ──────────────────────────
from app.models import user      # registers 'users' table
from app.models import session   # registers 'sessions' + 'gesture_results'
from app.models import feedback  # registers 'feedback' table  ← NEW Sprint 3

# Create any tables that don't exist yet
Base.metadata.create_all(bind=engine)

# ── Import all routers ──────────────────────────────────────────────
from app.routers import auth        # /auth/*
from app.routers import video       # /translate/upload
from app.routers import history     # /history/*        ← NEW Sprint 3
from app.routers import feedback    # /feedback/*       ← NEW Sprint 3
from app.routers import admin       # /admin/*          ← NEW Sprint 3
from app.routers import vocabulary  # /vocabulary/*     ← NEW Sprint 3

app = FastAPI(
    title="Silent Voices API",
    description="ASL to Text Translation System — FAST-NUCES SE Spring 2026",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register all routers
app.include_router(auth.router)
app.include_router(video.router)
app.include_router(history.router)
app.include_router(feedback.router)
app.include_router(admin.router)
app.include_router(vocabulary.router)

@app.get("/")
def root():
    return {"status": "running", "message": "Silent Voices API v3.0", "docs": "/docs"}
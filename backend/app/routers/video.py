# video.py
#
# PURPOSE: Handles POST /translate/upload — the core endpoint of the application.
# Receives a video, runs the ML pipeline, saves results to the database,
# and returns the translation with confidence scores.
#
# FIXES APPLIED:
# 1. db.commit() is called ONCE after the gesture results loop, not inside it.
#    Inside the loop = one disk write per gesture (slow).
#    After the loop = one disk write for all gestures together (correct).

import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session as DBSession

from app.database import get_db
from app.models.session import Session as SessionModel, GestureResult
from app.models.user import User
from app.routers.auth import get_current_user
from app.ml.pipeline import process_video

router = APIRouter(prefix="/translate", tags=["Translation"])

# Directory where uploaded videos are saved temporarily during processing
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".webm"}
MAX_FILE_SIZE_MB = 50


@router.post("/upload")
async def upload_and_translate(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """
    Receive a video file, translate ASL gestures, and return the result.

    Full flow:
        1. Validate file type and size
        2. Save to uploads/ with a unique UUID filename
        3. Run the ML pipeline (frame extraction → landmarks → classification)
        4. Save the session record and all gesture results to the database
        5. Delete the uploaded file (cleanup)
        6. Return the translation result as JSON
    """

    # ── Step 1: Validate the uploaded file ────────────────────────
    file_ext = os.path.splitext(file.filename or "")[1].lower()

    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{file_ext}' is not supported. "
                   f"Please upload an MP4, MOV, AVI, or WebM file."
        )

    file_contents = await file.read()

    if len(file_contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {MAX_FILE_SIZE_MB}MB size limit."
        )

    # ── Step 2: Save to disk with a unique filename ────────────────
    # uuid4() generates a random unique identifier — prevents filename collisions
    # when multiple users upload files with the same name simultaneously.
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file_contents)

    # Use try/finally to guarantee file cleanup even if something goes wrong
    try:

        # ── Step 3: Run the ML pipeline ───────────────────────────
        result = process_video(file_path)

        # ── Step 4: Persist the session record ────────────────────
        new_session = SessionModel(
            user_id=current_user.id,
            video_filename=file.filename,
            translated_text=result["translated_text"],
            avg_confidence=result["avg_confidence"]
        )
        db.add(new_session)

        # flush() writes the session to the database and assigns it an auto-increment id,
        # but does NOT commit the transaction yet. We need the id immediately so
        # the GestureResult rows can reference it via their session_id foreign key.
        db.flush()

        # ── Step 5: Persist all gesture results in one batch ──────
        # All db.add() calls here stage the rows in memory.
        # The single db.commit() BELOW sends them all to PostgreSQL in one transaction.
        # This is far more efficient than committing inside the loop.
        for gesture in result["gesture_sequence"]:
            if gesture["label"] is not None:
                gesture_result = GestureResult(
                    session_id=new_session.id,
                    gesture_label=gesture["label"],
                    confidence=gesture["confidence"],
                    frame_number=gesture["frame"]
                )
                db.add(gesture_result)

        # ── ONE commit after the loop — not inside it ──────────────
        # This writes the session + all gesture results to disk in a single
        # atomic transaction. If anything fails, nothing is partially saved.
        db.commit()
        db.refresh(new_session)

        return {
            "session_id": new_session.id,
            "translated_text": result["translated_text"],
            "avg_confidence": result["avg_confidence"],
            "gesture_sequence": result["gesture_sequence"],
            "frames_processed": result["frames_processed"],
            "frames_with_hands": result["frames_with_hands"]
        }

    except Exception as e:
        db.rollback()  # Undo any staged database changes if the pipeline failed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )

    finally:
        # Always delete the uploaded file after processing — whether success or failure.
        # Videos can be large and must not accumulate in the uploads/ directory.
        if os.path.exists(file_path):
            os.remove(file_path)
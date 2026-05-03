# history.py
# Provides session history for the logged-in user.
# Also handles TXT and PDF export of individual sessions.

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session as DBSession
from typing import List
from io import BytesIO

from app.database import get_db
from app.models.session import Session as SessionModel
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.history_schema import SessionListItem, SessionDetail

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/", response_model=List[SessionListItem])
def get_history(
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Return all sessions for the logged-in user, newest first."""
    sessions = (
        db.query(SessionModel)
        .filter(SessionModel.user_id == current_user.id)
        .order_by(SessionModel.created_at.desc())
        .all()
    )
    return sessions


@router.get("/{session_id}", response_model=SessionDetail)
def get_session_detail(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Return full detail of one session including all gesture results."""
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id  # users can only see their own sessions
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/{session_id}/export/txt")
def export_txt(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Export a session's translation as a plain text file download."""
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Build the text content
    content = (
        f"Silent Voices — Translation Export\n"
        f"{'='*40}\n"
        f"Date:       {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"File:       {session.video_filename or 'Unknown'}\n"
        f"Confidence: {session.avg_confidence:.1f}%\n"
        f"{'='*40}\n\n"
        f"TRANSLATED TEXT:\n{session.translated_text or 'No translation available'}\n\n"
        f"GESTURE BREAKDOWN:\n"
    )
    for gr in session.gesture_results:
        content += f"  Frame {gr.frame_number:4d}: {gr.gesture_label} ({gr.confidence:.1f}%)\n"
    
    # StreamingResponse sends the content as a downloadable file
    return StreamingResponse(
        BytesIO(content.encode("utf-8")),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename=translation_{session_id}.txt"}
    )


@router.get("/{session_id}/export/pdf")
def export_pdf(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Export a session's translation as a formatted PDF file download."""
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Generate PDF using fpdf2
    from fpdf import FPDF
    
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(27, 58, 107)   # Navy
    pdf.cell(0, 12, "Silent Voices — Translation Export", ln=True, align="C")
    
    pdf.set_draw_color(13, 115, 119)  # Teal
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    
    # Metadata
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(40, 8, "Date:", ln=False)
    pdf.cell(0, 8, session.created_at.strftime("%Y-%m-%d %H:%M:%S"), ln=True)
    
    pdf.cell(40, 8, "File:", ln=False)
    pdf.cell(0, 8, session.video_filename or "Unknown", ln=True)
    
    pdf.cell(40, 8, "Avg. Confidence:", ln=False)
    pdf.cell(0, 8, f"{session.avg_confidence:.1f}%", ln=True)
    pdf.ln(4)
    
    # Translated text box
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(13, 115, 119)
    pdf.cell(0, 10, "Translated Text", ln=True)
    
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(27, 58, 107)
    pdf.set_fill_color(214, 228, 240)
    pdf.multi_cell(0, 10, session.translated_text or "No translation available",
                   fill=True, border=1)
    pdf.ln(6)
    
    # Gesture breakdown
    if session.gesture_results:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(13, 115, 119)
        pdf.cell(0, 10, "Gesture Breakdown", ln=True)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(27, 58, 107)
        pdf.cell(30, 8, "Frame", fill=True, border=1)
        pdf.cell(60, 8, "Gesture", fill=True, border=1)
        pdf.cell(0, 8, "Confidence", fill=True, border=1, ln=True)
        
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        for i, gr in enumerate(session.gesture_results):
            fill = i % 2 == 0
            pdf.set_fill_color(240, 248, 255) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.cell(30, 7, str(gr.frame_number), fill=True, border=1)
            pdf.cell(60, 7, gr.gesture_label, fill=True, border=1)
            pdf.cell(0, 7, f"{gr.confidence:.1f}%", fill=True, border=1, ln=True)
    
    # Return as downloadable PDF
    pdf_bytes = pdf.output()  # returns bytes in fpdf2
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=translation_{session_id}.pdf"}
    )
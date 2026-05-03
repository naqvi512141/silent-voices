# vocabulary.py
# Returns the static vocabulary of supported ASL signs.
# This is a simple GET endpoint that returns a hardcoded list —
# no database query needed. In a future sprint, this could be
# made dynamic (stored in a database table that admins can edit).

from fastapi import APIRouter

router = APIRouter(prefix="/vocabulary", tags=["Vocabulary"])

# The full vocabulary supported by the trained model.
# Matches exactly the class labels in gesture_model.pkl.
VOCABULARY = [
    # ASL Alphabet
    {"id": "A", "label": "A", "type": "letter", "description": "Closed fist with thumb resting on the side"},
    {"id": "B", "label": "B", "type": "letter", "description": "Four fingers extended upward, thumb tucked"},
    {"id": "C", "label": "C", "type": "letter", "description": "Curved hand forming a C shape"},
    {"id": "D", "label": "D", "type": "letter", "description": "Index finger up, other fingers curved touching thumb"},
    {"id": "E", "label": "E", "type": "letter", "description": "All fingers bent, thumb tucked under"},
    {"id": "F", "label": "F", "type": "letter", "description": "Index and thumb form a circle, other fingers up"},
    {"id": "G", "label": "G", "type": "letter", "description": "Index finger and thumb point sideways"},
    {"id": "H", "label": "H", "type": "letter", "description": "Index and middle fingers extended sideways"},
    {"id": "I", "label": "I", "type": "letter", "description": "Pinky finger extended upward, fist closed"},
    {"id": "J", "label": "J", "type": "letter", "description": "Pinky extended, draw a J shape in the air"},
    {"id": "K", "label": "K", "type": "letter", "description": "Index up, middle angled out, thumb between them"},
    {"id": "L", "label": "L", "type": "letter", "description": "Index finger up, thumb extended out to form L"},
    {"id": "M", "label": "M", "type": "letter", "description": "Three fingers folded over tucked thumb"},
    {"id": "N", "label": "N", "type": "letter", "description": "Two fingers folded over tucked thumb"},
    {"id": "O", "label": "O", "type": "letter", "description": "All fingers curved to form an O with the thumb"},
    {"id": "P", "label": "P", "type": "letter", "description": "Like K but pointing downward"},
    {"id": "Q", "label": "Q", "type": "letter", "description": "Like G but pointing downward"},
    {"id": "R", "label": "R", "type": "letter", "description": "Index and middle fingers crossed"},
    {"id": "S", "label": "S", "type": "letter", "description": "Closed fist with thumb over fingers"},
    {"id": "T", "label": "T", "type": "letter", "description": "Thumb tucked between index and middle finger"},
    {"id": "U", "label": "U", "type": "letter", "description": "Index and middle fingers extended together upward"},
    {"id": "V", "label": "V", "type": "letter", "description": "Index and middle fingers spread in a V"},
    {"id": "W", "label": "W", "type": "letter", "description": "Index, middle and ring fingers spread upward"},
    {"id": "X", "label": "X", "type": "letter", "description": "Index finger hooked/bent"},
    {"id": "Y", "label": "Y", "type": "letter", "description": "Thumb and pinky extended outward"},
    {"id": "Z", "label": "Z", "type": "letter", "description": "Index finger draws a Z in the air"},
    # Common words/phrases from the Kaggle dataset
    {"id": "space",  "label": "SPACE",  "type": "control", "description": "Flat open hand — signals a space between words"},
    {"id": "del",    "label": "DELETE", "type": "control", "description": "Delete/backspace the last gesture"},
    {"id": "nothing","label": "NOTHING","type": "control", "description": "No gesture detected — used as a boundary marker"},
]


@router.get("/")
def get_vocabulary():
    """Return the full list of supported ASL signs."""
    return {
        "total": len(VOCABULARY),
        "vocabulary": VOCABULARY
    }


@router.get("/letters")
def get_letters():
    """Return only the alphabet signs."""
    return [v for v in VOCABULARY if v["type"] == "letter"]
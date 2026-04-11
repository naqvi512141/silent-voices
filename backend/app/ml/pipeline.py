# pipeline.py
#
# PURPOSE: The orchestrator — calls frame_extractor, landmark_detector, and
# gesture_classifier in the right order and assembles the results into a sentence.
#
# SENTENCE BUILDING LOGIC:
# The raw output of processing a video is something like:
#   [A, A, A, A, B, B, B, B, B, A, A, ...]  ← same gesture held for many frames
# We collapse consecutive identical labels into a single token using run-length encoding.
# A gap of frames with no hand detected is treated as a word boundary.

from app.ml.frame_extractor import extract_frames
from app.ml.landmark_detector import extract_landmarks
from app.ml.gesture_classifier import predict_gesture


def process_video(video_path: str) -> dict:
    """
    Full pipeline: video file → translated text + confidence scores.
    
    Returns a dictionary containing:
      - 'translated_text': The assembled sentence (e.g., "HELLO WORLD")
      - 'gesture_sequence': List of individual gesture predictions with confidences
      - 'avg_confidence': Average confidence across all detected gestures
      - 'frames_processed': Total number of frames that were processed
      - 'frames_with_hands': Number of frames where a hand was detected
    """
    
    # ── Step 1: Extract frames from the video ─────────────────────
    frames = extract_frames(video_path, frame_interval=5)
    frames_processed = len(frames)
    
    # ── Step 2: Run landmark detection on each frame ──────────────
    # For each frame, either get 63 landmark values or None (no hand detected)
    raw_predictions = []
    frames_with_hands = 0
    
    for frame_number, frame_image in frames:
        landmarks = extract_landmarks(frame_image)
        
        if landmarks is None:
            # No hand in this frame — record as a gap
            raw_predictions.append({"frame": frame_number, "label": None, "confidence": 0})
        else:
            frames_with_hands += 1
            prediction = predict_gesture(landmarks)
            raw_predictions.append({
                "frame": frame_number,
                "label": prediction["label"],
                "confidence": prediction["confidence"]
            })
    
    # ── Step 3: Build gesture sequence (collapse consecutive duplicates) ──
    # This turns [A, A, A, B, B, None, None, C, C, C] into [A, B, C]
    gesture_sequence = _collapse_predictions(raw_predictions)
    
    # ── Step 4: Assemble into a sentence ──────────────────────────
    # Filter out None entries and join all labels with spaces
    labels = [g["label"] for g in gesture_sequence if g["label"] is not None]
    translated_text = " ".join(labels) if labels else "No gestures detected"
    
    # ── Step 5: Calculate average confidence ──────────────────────
    confidences = [g["confidence"] for g in gesture_sequence if g["label"] is not None]
    avg_confidence = round(sum(confidences) / len(confidences), 1) if confidences else 0.0
    
    return {
        "translated_text": translated_text,
        "gesture_sequence": gesture_sequence,
        "avg_confidence": avg_confidence,
        "frames_processed": frames_processed,
        "frames_with_hands": frames_with_hands
    }


def _collapse_predictions(predictions: list) -> list:
    """
    Collapse consecutive identical predictions into single tokens.
    A None (no hand) entry longer than 3 consecutive frames is treated
    as a boundary — it separates one token from the next.
    
    Example input:  [A, A, A, None, B, B, None, None, None, None, C, C]
    Example output: [A, B, (boundary), C]
    """
    if not predictions:
        return []
    
    collapsed = []
    none_streak = 0
    
    for pred in predictions:
        if pred["label"] is None:
            none_streak += 1
            # A streak of 4+ frames with no hand = word boundary
            if none_streak == 4:
                collapsed.append({"frame": pred["frame"], "label": None, "confidence": 0})
        else:
            none_streak = 0
            # Only add this label if it is different from the last one added
            if not collapsed or collapsed[-1]["label"] != pred["label"]:
                collapsed.append(pred)
    
    return collapsed
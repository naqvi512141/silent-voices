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

# pipeline.py
#
# SPRINT 3 FIXES:
#
# 1. CONFIDENCE_THRESHOLD = 60.0
#    Any prediction below 60% confidence is treated as if no hand was detected.
#    This is the single most impactful change. A model that is only 16-30%
#    confident is essentially guessing — we must not write those guesses down.
#
# 2. MIN_CONSECUTIVE_FRAMES = 3
#    A gesture only counts if the same label appears in 3 consecutive processed
#    frames. At frame_interval=5 and 30fps, 3 processed frames ≈ 0.5 seconds.
#    This means the signer must hold each sign clearly for half a second.
#    Transitional hand shapes (moving from one sign to the next) appear for only
#    1-2 frames and are completely ignored. This eliminates most noise.
#
# 3. WORD_BOUNDARY_FRAMES = 6
#    A gap of 6+ frames with no confident detection is treated as a space.
#    This gives the signer time between letters/words.

from app.ml.frame_extractor import extract_frames
from app.ml.landmark_detector import extract_landmarks
from app.ml.gesture_classifier import predict_gesture

# ── Tunable parameters ────────────────────────────────────────────────────────
CONFIDENCE_THRESHOLD  = 60.0   # Reject predictions below this percentage
MIN_CONSECUTIVE_FRAMES = 3     # Require this many identical frames before accepting
WORD_BOUNDARY_FRAMES   = 6     # This many no-hand frames = insert a space/boundary
# ─────────────────────────────────────────────────────────────────────────────


def process_video(video_path: str) -> dict:
    """
    Full pipeline: video file → translated text + confidence scores.
    
    The pipeline now applies a confidence threshold so that uncertain 
    predictions are discarded rather than included as noise in the output.
    Gestures must also appear in multiple consecutive frames before being 
    accepted, which eliminates transitional hand positions.
    """

    # Step 1: Extract frames at regular intervals
    frames = extract_frames(video_path, frame_interval=5)
    frames_processed = len(frames)

    # Step 2: Get a raw prediction for each frame
    raw_predictions = []
    frames_with_hands = 0

    for frame_number, frame_image in frames:
        landmarks = extract_landmarks(frame_image)

        if landmarks is None:
            raw_predictions.append({
                "frame": frame_number,
                "label": None,
                "confidence": 0.0
            })
        else:
            prediction = predict_gesture(landmarks)

            # Apply confidence threshold here.
            # A prediction below the threshold is treated exactly like
            # "no hand detected" — it contributes to the gap counter
            # rather than polluting the output with a wrong letter.
            if prediction["confidence"] < CONFIDENCE_THRESHOLD:
                raw_predictions.append({
                    "frame": frame_number,
                    "label": None,
                    "confidence": prediction["confidence"],
                    "below_threshold": True   # flag for debugging
                })
            else:
                frames_with_hands += 1
                raw_predictions.append({
                    "frame": frame_number,
                    "label": prediction["label"],
                    "confidence": prediction["confidence"]
                })

    # Step 3: Apply minimum consecutive frames rule, then collapse
    gesture_sequence = _build_gesture_sequence(raw_predictions)

    # Step 4: Assemble into a sentence
    labels = [g["label"] for g in gesture_sequence if g["label"] is not None]
    translated_text = " ".join(labels) if labels else "No confident gestures detected"

    # Step 5: Calculate average confidence over accepted gestures only
    confidences = [g["confidence"] for g in gesture_sequence if g["label"] is not None]
    avg_confidence = round(sum(confidences) / len(confidences), 1) if confidences else 0.0

    return {
        "translated_text": translated_text,
        "gesture_sequence": gesture_sequence,
        "avg_confidence": avg_confidence,
        "frames_processed": frames_processed,
        "frames_with_hands": frames_with_hands,
        "total_accepted_gestures": len(labels)
    }


def _build_gesture_sequence(predictions: list) -> list:
    """
    Convert a raw list of per-frame predictions into a clean gesture sequence.
    
    This function does two things:
    
    First, it applies the MIN_CONSECUTIVE_FRAMES rule using a sliding window.
    A gesture is only accepted if the same label appears in at least
    MIN_CONSECUTIVE_FRAMES consecutive frames. This means:
      - [A, A, A, B, A, C, C, C] → accepts A and C, ignores the lone B
      - [A, B, C, D, E] → accepts nothing (all single-frame, likely noise)
    
    Second, it inserts word boundaries (None) when there is a gap of
    WORD_BOUNDARY_FRAMES or more consecutive frames with no confident detection.
    """
    if not predictions:
        return []

    accepted = []
    i = 0

    while i < len(predictions):
        current = predictions[i]

        if current["label"] is None:
            # Count the length of this gap
            gap_start = i
            while i < len(predictions) and predictions[i]["label"] is None:
                i += 1
            gap_length = i - gap_start

            # A long gap is a word boundary (space between signs)
            if gap_length >= WORD_BOUNDARY_FRAMES and accepted and accepted[-1]["label"] is not None:
                accepted.append({
                    "frame": predictions[gap_start]["frame"],
                    "label": None,
                    "confidence": 0.0,
                    "is_boundary": True
                })
        else:
            # Count how many consecutive frames share this label
            label = current["label"]
            run_start = i
            total_confidence = 0.0
            run_length = 0

            while (i < len(predictions)
                   and predictions[i]["label"] == label):
                total_confidence += predictions[i]["confidence"]
                run_length += 1
                i += 1

            # Only accept if the run is long enough
            if run_length >= MIN_CONSECUTIVE_FRAMES:
                avg_conf = round(total_confidence / run_length, 1)
                # Only add if this is different from the last accepted gesture
                if not accepted or accepted[-1]["label"] != label:
                    accepted.append({
                        "frame": predictions[run_start]["frame"],
                        "label": label,
                        "confidence": avg_conf,
                        "frames_held": run_length
                    })
            # If the run was too short, we simply move on without recording it.
            # This discards transitional hand positions.

    return accepted
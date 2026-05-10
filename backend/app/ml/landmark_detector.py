# landmark_detector.py
#
# PURPOSE: Runs MediaPipe Hands on a single image frame and returns a
# normalised feature vector of 63 floats, or None if no hand is found.
#
# KEY DESIGN DECISIONS:
# 1. MediaPipe is initialised ONCE at module level — not inside the function.
#    Creating a new instance per frame is expensive. Module-level creation
#    means it is built once when the server starts and reused for every frame.
#
# 2. Coordinates are normalised relative to the wrist (landmark 0).
#    Raw coordinates depend on WHERE in the frame the hand appears.
#    Subtracting the wrist position makes all coordinates RELATIVE to the wrist,
#    so the model learns the SHAPE of the hand, not its screen position.
#
# 3. The return statement is AFTER the loop, not inside it.
#    This is critical — returning inside the loop would exit after the first
#    landmark and give us 3 numbers instead of the required 63.

import cv2
import mediapipe as mp
import numpy as np

_mp_hands = mp.solutions.hands

# Create detector at module level for efficiency.
# static_image_mode=False enables tracking between consecutive frames.
_hands_detector = _mp_hands.Hands(
    static_image_mode=False,          # ← FIXED: was True, now False for video
    max_num_hands=1,
    min_detection_confidence=0.6,     # ← Raised from 0.5 — reject weaker detections
    min_tracking_confidence=0.6       # ← Raised from 0.5
)


def extract_landmarks(frame_bgr: np.ndarray) -> list | None:
    """
    Extract normalised hand landmark coordinates from one video frame.
    
    Returns a list of 63 floats (21 landmarks × 3 coordinates), each value
    normalised relative to the wrist position. Returns None if no hand is
    detected with sufficient confidence in this frame.
    """
    # MediaPipe requires RGB; OpenCV provides BGR
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    results = _hands_detector.process(frame_rgb)

    if not results.multi_hand_landmarks:
        return None

    hand_landmarks = results.multi_hand_landmarks[0]

    # Normalise relative to the wrist (landmark 0)
    wrist = hand_landmarks.landmark[0]
    wrist_x, wrist_y, wrist_z = wrist.x, wrist.y, wrist.z

    feature_vector = []
    for lm in hand_landmarks.landmark:
        feature_vector.extend([
            lm.x - wrist_x,
            lm.y - wrist_y,
            lm.z - wrist_z
        ])

    # The return is AFTER the loop — this is critical.
    # Returning inside the loop would give only 3 values instead of 63.
    return feature_vector
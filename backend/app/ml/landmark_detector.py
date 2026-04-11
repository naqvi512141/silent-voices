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

# Initialise MediaPipe ONCE — module-level initialisation
_mp_hands = mp.solutions.hands
_hands_detector = _mp_hands.Hands(
    static_image_mode=True,          # True = each frame is independent (correct for video processing)
    max_num_hands=1,                  # One signing hand
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


def extract_landmarks(frame_bgr: np.ndarray) -> list | None:
    """
    Extract normalised hand landmark coordinates from one video frame.

    Args:
        frame_bgr: A numpy array from OpenCV in BGR format, shape (H, W, 3).

    Returns:
        A list of 63 floats [x0, y0, z0, x1, y1, z1, ..., x20, y20, z20]
        where each value is the coordinate RELATIVE to the wrist (landmark 0).
        Returns None if no hand is detected in this frame.
    """

    # MediaPipe requires RGB; OpenCV gives BGR — must convert before processing
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    results = _hands_detector.process(frame_rgb)

    # multi_hand_landmarks is None when no hand is visible in the frame
    if not results.multi_hand_landmarks:
        return None

    # We only track one hand, so take the first (and only) detected hand
    hand_landmarks = results.multi_hand_landmarks[0]

    # Get the wrist position — landmark index 0 in MediaPipe's hand model
    wrist = hand_landmarks.landmark[0]
    wrist_x = wrist.x
    wrist_y = wrist.y
    wrist_z = wrist.z

    feature_vector = []

    # Iterate through all 21 landmarks and normalise each coordinate
    for lm in hand_landmarks.landmark:
        feature_vector.extend([
            lm.x - wrist_x,   # x relative to wrist
            lm.y - wrist_y,   # y relative to wrist
            lm.z - wrist_z    # z (depth estimate) relative to wrist
        ])

    # ── CRITICAL: return is HERE, AFTER the loop completes ──────────
    # If this return were indented inside the for loop above, Python would
    # exit after the very first landmark (3 numbers), not all 21 (63 numbers).
    # The model expects exactly 63 values — returning 3 would break everything.
    return feature_vector  # Always exactly 63 floats when a hand is detected


def get_landmark_count() -> int:
    """Returns the expected length of a feature vector (always 63)."""
    return 21 * 3  # 21 landmarks × 3 coordinates (x, y, z)
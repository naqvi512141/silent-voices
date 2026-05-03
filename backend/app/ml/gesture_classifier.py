# gesture_classifier.py
#
# PURPOSE: Loads the trained model from disk and provides a predict() function
# that takes a feature vector and returns a predicted gesture label + confidence score.
#
# DESIGN DECISION: We load the model ONCE at module level (same pattern as landmark_detector).
# If we loaded it inside predict(), it would be re-read from disk on every single prediction,
# which is ~100ms per call and would make processing a video unbearably slow.

import joblib
import numpy as np
import os

# The path to the trained model file, relative to where the server runs
# os.path.dirname(__file__) gives us the directory of this file (backend/app/ml/)
_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "gesture_model.pkl")
_MODEL_PATH = os.path.normpath(_MODEL_PATH)  # Clean up the path separators

# Load the model when this module is first imported
# If the model file does not exist yet, this raises an error with a clear message
if not os.path.exists(_MODEL_PATH):
    raise FileNotFoundError(
        f"Trained model not found at {_MODEL_PATH}. "
        f"Please run ml_training/train_model.py first to generate the model."
    )

_model = joblib.load(_MODEL_PATH)

# Get the list of class names from the model (e.g., ['A', 'B', 'C', ...])
_class_names = _model.classes_


def predict_gesture(feature_vector: list) -> dict:
    """
    Classify a hand gesture from a feature vector.
    
    Args:
        feature_vector: A list of 63 floats from landmark_detector.extract_landmarks().
    
    Returns:
        A dictionary with:
          - 'label': The predicted gesture (e.g., "A", "B", "Hello")
          - 'confidence': The model's confidence as a percentage (e.g., 87.3)
          - 'all_probabilities': Dict mapping each class to its probability (for debugging)
    """
    
    # Convert list to numpy array and reshape to (1, 63) — scikit-learn expects 2D arrays
    # Shape (63,) is a 1D array; (1, 63) is a 2D array with 1 row and 63 columns
    features = np.array(feature_vector).reshape(1, -1)
    
    # predict() returns the most likely class label
    label = _model.predict(features)[0]
    
    # predict_proba() returns probabilities for ALL classes
    # e.g., [0.87, 0.08, 0.02, 0.01, ...] where each value is the probability
    # of the input belonging to that class. They sum to 1.0.
    probabilities = _model.predict_proba(features)[0]
    
    # The confidence is the probability of the predicted class
    confidence = float(max(probabilities)) * 100  # Convert to percentage
    
    # Build a readable dictionary of all class probabilities for transparency
    all_probs = {
        cls: round(float(prob) * 100, 2)
        for cls, prob in zip(_class_names, probabilities)
    }
    
    return {
        "label": str(label),
        "confidence": round(confidence, 1),
        "all_probabilities": all_probs
    }
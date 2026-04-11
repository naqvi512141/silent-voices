# train_model.py
#
# PURPOSE: Load the CSV built by build_dataset.py, train a classifier,
# evaluate it, and save the model to gesture_model.pkl.
#
# RUN THIS AFTER build_dataset.py finishes.

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

CSV_PATH   = os.path.join(os.path.dirname(__file__), "asl_landmarks.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "gesture_model.pkl")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(CSV_PATH)

print(f"Dataset shape: {df.shape}")          # e.g., (75000, 64) — rows × columns
print(f"Classes: {df['label'].unique()}")     # e.g., ['A' 'B' 'C' ... 'Z']
print(f"Class distribution:\n{df['label'].value_counts()}")

# ── DATA CLEANING ────────────────────────────────────────────────
# Drop rows where any landmark value is NaN (corrupted images)
initial_count = len(df)
df = df.dropna()
print(f"Dropped {initial_count - len(df)} rows with missing values.")

# ── FEATURE / LABEL SEPARATION ───────────────────────────────────
X = df.drop("label", axis=1).values   # Feature matrix: (n_samples, 63)
y = df["label"].values                 # Label vector:   (n_samples,)

print(f"Feature matrix shape: {X.shape}")

# ── TRAIN / TEST SPLIT ───────────────────────────────────────────
# 80% for training, 20% for testing. stratify=y ensures each class has
# proportional representation in both sets (important for balanced evaluation).
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

# ── MODEL TRAINING ────────────────────────────────────────────────
# Random Forest with 100 trees. n_jobs=-1 uses all CPU cores for faster training.
# Random Forest is chosen because:
#   1. Works well with tabular data (our 63-column feature vectors)
#   2. Handles multi-class classification natively (26+ classes)
#   3. Robust to noisy features
#   4. Returns probability estimates (needed for confidence scores)
#   5. Trains in minutes, not hours
print("Training Random Forest classifier...")
model = RandomForestClassifier(
    n_estimators=100,    # Number of decision trees in the forest
    max_depth=None,      # Trees grow until all leaves are pure (or min_samples_split)
    random_state=42,     # For reproducibility
    n_jobs=-1,           # Use all CPU cores
    verbose=1            # Print progress
)
model.fit(X_train, y_train)

# ── EVALUATION ────────────────────────────────────────────────────
print("\n--- EVALUATION RESULTS ---")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report (Precision, Recall, F1 per class):")
print(classification_report(y_test, y_pred))

# ── SAVE MODEL ────────────────────────────────────────────────────
joblib.dump(model, MODEL_PATH)
print(f"\nModel saved to: {MODEL_PATH}")
print("Training complete!")
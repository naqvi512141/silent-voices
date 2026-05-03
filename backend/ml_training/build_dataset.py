import cv2
import mediapipe as mp
import csv
import os
import sys
from concurrent.futures import ProcessPoolExecutor

# --- CONFIGURATION ---
# IMPORTANT: Update this path to your actual extracted Kaggle folder!
DATASET_PATH = r"C:\Users\HP\Downloads\Compressed\archive\asl_alphabet_train\asl_alphabet_train" 
OUTPUT_CSV   = os.path.join(os.path.dirname(__file__), "asl_landmarks.csv")

# We are increasing this to 800 as per your requirement
IMAGES_PER_CLASS = 800  
# ---------------------

def process_single_image(img_info):
    """Worker function: Processes one image and returns the landmark row."""
    img_path, label = img_info
    
    # Initialize MediaPipe for this specific worker process
    mp_hands = mp.solutions.hands
    try:
        with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
            image = cv2.imread(img_path)
            if image is None: 
                return None
            
            # Convert BGR to RGB
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
            
            if not results.multi_hand_landmarks:
                return None
            
            # Extract landmarks
            hand_landmarks = results.multi_hand_landmarks[0]
            wrist = hand_landmarks.landmark[0]
            
            row = []
            for lm in hand_landmarks.landmark:
                # Normalization relative to the wrist
                row.extend([lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z])
            
            # Add the label (e.g., 'A', 'B', 'C') at the end
            row.append(label)
            return row
    except Exception as e:
        # If an error happens with one image, just skip it and move to the next
        return None

if __name__ == "__main__":
    tasks = []
    print("--- Silent Voices: Dataset Builder ---")
    print(f"Scanning directory: {DATASET_PATH}")
    
    # 1. Gather the file paths
    if not os.path.exists(DATASET_PATH):
        print(f"ERROR: Path not found! Please check DATASET_PATH in the script.")
        sys.exit()

    for label in sorted(os.listdir(DATASET_PATH)):
        label_path = os.path.join(DATASET_PATH, label)
        if not os.path.isdir(label_path): 
            continue
        
        # Grab images up to your limit of 800
        images = [f for f in os.listdir(label_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for img_file in images[:IMAGES_PER_CLASS]:
            tasks.append((os.path.join(label_path, img_file), label))

    print(f"Total images to process: {len(tasks)}")
    print(f"Using all available CPU cores (2 cores detected)...")

    # 2. Process in Parallel
    with open(OUTPUT_CSV, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        # Write Header: 63 columns for landmarks (x,y,z for 21 points) + 1 label
        header = []
        for i in range(21): 
            header.extend([f"x{i}", f"y{i}", f"z{i}"])
        header.append("label")
        writer.writerow(header)

        # ProcessPoolExecutor manages the 2 workers for you
        with ProcessPoolExecutor() as executor:
            # map() runs process_single_image for every task in the list
            results = list(executor.map(process_single_image, tasks))
            
            # 3. Save successful results
            count = 0
            for r in results:
                if r is not None:
                    writer.writerow(r)
                    count += 1
                    # Progress update every 1000 images
                    if count % 1000 == 0:
                        print(f"Progress: {count} images saved...")

    print("-" * 30)
    print(f"SUCCESS! Created {OUTPUT_CSV}")
    print(f"Total Landmark Rows: {count}")
    print(f"Skipped: {len(tasks) - count} (No hand detected)")
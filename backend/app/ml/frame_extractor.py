# frame_extractor.py
# 
# PURPOSE: Takes a video file and returns a list of image frames (as numpy arrays).
# 
# WHY NOT PROCESS EVERY FRAME?
# A 10-second video at 30fps = 300 frames. Running MediaPipe on all 300 is wasteful
# because sign language gestures are held for ~0.5 seconds (15 frames). Processing
# every 5th frame gives us 60 frames and still captures each held sign at least once.
# This makes the pipeline 5x faster with almost no loss in accuracy.

import cv2
import os

def extract_frames(video_path: str, frame_interval: int = 5) -> list:
    """
    Extract frames from a video file at regular intervals.
    
    Args:
        video_path: Full path to the uploaded video file.
        frame_interval: Process every Nth frame (default: every 5th frame).
    
    Returns:
        A list of (frame_number, frame_image) tuples, where each frame_image
        is a numpy array with shape (height, width, 3) in BGR colour format.
        OpenCV always produces BGR — we convert to RGB before passing to MediaPipe.
    """
    
    # Validate the file exists before trying to open it
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # VideoCapture opens the video file. If the path is wrong, it opens silently
    # but cap.isOpened() returns False — always check this.
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}. "
                         f"Check the file format (MP4, AVI, MOV are supported).")
    
    frames = []
    frame_count = 0
    
    while cap.isOpened():
        success, frame = cap.read()  # Read the next frame
        
        if not success:
            # No more frames — video has ended
            break
        
        frame_count += 1
        
        # Only keep every Nth frame to avoid redundancy
        if frame_count % frame_interval == 0:
            frames.append((frame_count, frame))
    
    cap.release()  # ALWAYS release the VideoCapture — it holds a file lock
    
    if len(frames) == 0:
        raise ValueError("No frames could be extracted. The video may be empty or corrupted.")
    
    return frames


def get_video_info(video_path: str) -> dict:
    """
    Get basic metadata about a video file.
    Useful for logging and debugging.
    """
    cap = cv2.VideoCapture(video_path)
    info = {
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "total_frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "duration_seconds": cap.get(cv2.CAP_PROP_FRAME_COUNT) / max(cap.get(cv2.CAP_PROP_FPS), 1)
    }
    cap.release()
    return info
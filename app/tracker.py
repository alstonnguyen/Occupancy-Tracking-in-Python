### tracker.py (Handles video processing, tracking, waiting times, and occupancy)
import cv2
import torch
import pandas as pd
import numpy as np
import hashlib
import os
import json
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from encryptor import encrypt_data, load_key

# Load YOLOv8 Model
yolo_model = YOLO("yolov8n.pt")  # Using YOLOv8 nano for efficiency

# Initialize DeepSORT tracker
deep_sort_tracker = DeepSort(max_age=30)

# Load encryption key
fernet = load_key()

# Load video file
video_path = "data/input_video.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Data storage
tracking_data = []
frame_count = 0
entry_times = {}  # Track entry times
exit_times = {}  # Track exit times
occupancy_count = []  # Store occupancy per frame
frame_skip = 2  # Process every 2nd frame

# Define zones (Example: Waiting Area, Tables, Exit)
zones = {
    "waiting_area": (100, 300, 500, 700),  # Example X1, Y1, X2, Y2
    "tables": (500, 700, 900, 1000),
    "exit": (900, 1000, 1200, 1300)
}

def get_zone(x, y):
    for zone, (x1, y1, x2, y2) in zones.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            return zone
    return "unknown"

def anonymize_id(track_id):
    return hashlib.sha256(str(track_id).encode()).hexdigest()[:10]  # Short hash ID

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # End of video
    
    frame_count += 1
    if frame_count % frame_skip != 0:
        continue  # Skip frames to improve performance
    
    timestamp = frame_count / fps  # Convert frame count to seconds
    
    # Run YOLO detection with reduced input size for efficiency
    resized_frame = cv2.resize(frame, (640, 640))
    results = yolo_model(resized_frame)
    detections = []
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            
            if cls == 0 and conf > 0.3:  # Class 0 is 'person'
                detections.append(([x1, y1, x2, y2], conf, cls))
    
    # Run DeepSORT tracking
    tracked_objects = deep_sort_tracker.update_tracks(detections, frame=frame)
    
    current_occupancy = {"waiting_area": 0, "tables": 0, "exit": 0}
    
    for track in tracked_objects:
        if not track.is_confirmed():
            continue
        
        track_id = anonymize_id(track.track_id)  # Anonymized ID
        x1, y1, x2, y2 = map(int, track.to_tlbr())  # Get bounding box
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
        
        zone = get_zone(center_x, center_y)
        if zone in current_occupancy:
            current_occupancy[zone] += 1
        
        if track_id not in entry_times:
            entry_times[track_id] = timestamp  # First appearance
        
        data_entry = {
            "id": track_id,
            "timestamp": round(timestamp, 2),
            "position": (center_x, center_y),
            "zone": zone
        }
        
        # Encrypt data entry
        encrypted_data = encrypt_data(data_entry)
        tracking_data.append({"encrypted": encrypted_data})
    
    occupancy_count.append({"timestamp": round(timestamp, 2), "occupancy": current_occupancy})
    
cap.release()

# Calculate exit times
for track_id in entry_times:
    if track_id not in exit_times:
        exit_times[track_id] = frame_count / fps  # Assume last frame is exit time

# Save encrypted tracking data
if tracking_data:  # Only save if there is data
    tracking_df = pd.DataFrame(tracking_data)
    tracking_df.to_csv("output/tracking_output_encrypted.csv", index=False)
    tracking_df.to_json("output/tracking_output_encrypted.json", orient="records", indent=4)
    
    # Save occupancy tracking data
    occupancy_df = pd.DataFrame(occupancy_count)
    occupancy_df.to_csv("output/occupancy_data.csv", index=False)
    occupancy_df.to_json("output/occupancy_data.json", orient="records", indent=4)
    
    # Save waiting times (entry and exit logs)
    waiting_times = [{"id": k, "entry_time": v, "exit_time": exit_times[k], "total_wait": exit_times[k] - v} for k, v in entry_times.items()]
    with open("output/waiting_times.json", "w") as f:
        json.dump(waiting_times, f, indent=4)
    
    print("Tracking, occupancy, and waiting time data saved securely!")
else:
    print("No tracking data detected. Check video input or tracking logic.")

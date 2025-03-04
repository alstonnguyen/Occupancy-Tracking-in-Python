# Occupancy & Wait Time Tracking  

A **computer vision-based tracking system** designed to monitor **occupancy levels and waiting times** in spaces like waiting rooms, restaurants, and public areas. Using **YOLOv8 for object detection** and **DeepSORT for tracking**, this project anonymously tracks individuals, estimates how long they stay, and analyzes movement patterns in defined zones.

---

## Features  

- **Real-Time Person Tracking** – Uses **YOLOv8 + DeepSORT** to detect and track people in video footage.  
- **Anonymized Data Processing** – Tracks individuals **without storing personal data**, ensuring privacy compliance.  
- **Zone-Based Occupancy Analysis** – Detects movement within predefined zones (**waiting areas, tables, exits**).  
- **Wait Time Calculation** – Measures **entry & exit times** to estimate **average wait times per individual**.  
- **Data Visualization** – Generates **scatter plots, occupancy trends, and wait time analytics** using Matplotlib.  

---

## Technologies Used  

- **Python** – Main programming language  
- **OpenCV** – Image processing and real-time video handling  
- **YOLOv8** – Person detection  
- **DeepSORT** – Multi-object tracking  
- **Pandas** – Data processing and handling  
- **Matplotlib** – Visualization of movement patterns and occupancy trends  
- **Cryptography** – Data encryption for privacy  

---

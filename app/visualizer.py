### visualizer.py (Enhanced Visualization for Occupancy and Wait Time Tracking)
import pandas as pd
import matplotlib
matplotlib.use('MacOSX')  # Use 'Agg' if running without display
import matplotlib.pyplot as plt

import json
from encryptor import decrypt_data

# Load and decrypt tracking data
def load_tracking_data(csv_file):
    df = pd.read_csv(csv_file)
    if df.empty:
        print("No tracking data available for visualization.")
        return None
    df["data"] = df["encrypted"].apply(lambda x: decrypt_data(x))
    df = pd.json_normalize(df["data"])

    # Print columns to debug the issue
    print("Extracted columns from decrypted data:", df.columns)

    return df


# Load occupancy data
def load_occupancy_data(json_file):
    with open(json_file, "r") as f:
        return json.load(f)

# Load waiting time data
def load_waiting_time_data(json_file):
    with open(json_file, "r") as f:
        return json.load(f)

# Scatter plot of movement data
def plot_movement(df):
    plt.figure(figsize=(8, 6))
    # Extract X and Y positions correctly from decrypted data
    df["x"] = df["position"].apply(lambda pos: pos[0] if isinstance(pos, (list, tuple)) else pos.get("x", None))
    df["y"] = df["position"].apply(lambda pos: pos[1] if isinstance(pos, (list, tuple)) else pos.get("y", None))

    print("First few rows of movement data:\n", df.head())

    if df.empty or df["x"].isnull().all() or df["y"].isnull().all():
        print("No valid position data available for visualization.")
    return

    print("Extracted X positions:", df["x"].dropna().tolist())
    print("Extracted Y positions:", df["y"].dropna().tolist())
   
    plt.scatter(df["x"], df["y"], c='blue', alpha=0.5, label='People Positions', s=10)
    plt.title("Movement Heatmap")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend()

    print("Displaying scatter plot...")

    plt.draw()
    plt.pause(0.001)  # Ensures GUI updates
    plt.show(block=True)  # Forces the plot to remain open

# Plot occupancy over time
def plot_occupancy(occupancy_data):
    timestamps = [entry["timestamp"] for entry in occupancy_data]
    waiting_areas = [entry["occupancy"]["waiting_area"] for entry in occupancy_data]
    tables = [entry["occupancy"]["tables"] for entry in occupancy_data]
    exits = [entry["occupancy"]["exit"] for entry in occupancy_data]
    
    plt.figure(figsize=(8, 6))
    plt.plot(timestamps, waiting_areas, label="Waiting Area", marker='o')
    plt.plot(timestamps, tables, label="Tables", marker='s')
    plt.plot(timestamps, exits, label="Exit", marker='x')
    
    plt.title("Occupancy Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Number of People")
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot average wait times
def plot_wait_times(waiting_time_data):
    ids = [entry["id"] for entry in waiting_time_data]
    wait_times = [entry["total_wait"] for entry in waiting_time_data]
    
    plt.figure(figsize=(8, 6))
    plt.bar(ids, wait_times, color='green')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Person ID")
    plt.ylabel("Wait Time (seconds)")
    plt.title("Wait Times Per Person")
    plt.show()

# Load and visualize all data
tracking_df = load_tracking_data("output/tracking_output_encrypted.csv")
occupancy_data = load_occupancy_data("output/occupancy_data.json")
waiting_time_data = load_waiting_time_data("output/waiting_times.json")

if tracking_df is not None:
    plot_movement(tracking_df)
if occupancy_data:
    plot_occupancy(occupancy_data)
if waiting_time_data:
    plot_wait_times(waiting_time_data)
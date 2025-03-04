import cv2
import os

# Set paths
image_folder = "/Users/alstonnguyen/Documents/occupant_tracking_project/generate_video/MOT17-04-SDP/img1"  # Change to your MOT17 dataset folder
output_video = "data/sample_video.mp4"

# Get list of images in sorted order
images = sorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")])

# Read first image to get dimensions
first_image = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = first_image.shape

# Define video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
video = cv2.VideoWriter(output_video, fourcc, 30, (width, height))

# Loop through images and add to video
for image in images:
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    video.write(frame)

video.release()
print(f"Video saved as {output_video}")

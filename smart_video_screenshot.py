# pip install opencv-python scikit-image
# script to take screenshot everytime a scene changes in a video
# python smart_video_screenshot.py file.mp4

import cv2
import sys
import os
from skimage.metrics import structural_similarity as ssim

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py video_file_path")
        sys.exit(1)

    video_file_path = sys.argv[1]

    if not os.path.isfile(video_file_path):
        print(f"File not found: {video_file_path}")
        sys.exit(1)

    cap = cv2.VideoCapture(video_file_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_file_path}")
        sys.exit(1)

    prev_frame = None
    frame_count = 0
    scene_num = 0
    output_dir = "output_frames"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    threshold = 0.7  # Adjust this value as needed (0 < threshold <= 1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is None:
            prev_frame = gray
            continue

        ssim_index, _ = ssim(prev_frame, gray, full=True)

        if ssim_index < threshold:
            scene_num += 1
            output_path = os.path.join(output_dir, f"scene_{scene_num:04d}.jpg")
            cv2.imwrite(output_path, frame)
            print(f"Scene change detected at frame {frame_count}, SSIM {ssim_index:.4f}, saved {output_path}")

        prev_frame = gray

    cap.release()
    print("Processing complete.")

if __name__ == "__main__":
    main()

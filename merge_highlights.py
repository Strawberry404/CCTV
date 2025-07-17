import os
import cv2
import numpy as np
import glob

def merge_videos(input_dir, output_file):
    """Merge all highlight videos in the input directory into a single output file."""
    print(f"Searching for highlight videos in {input_dir}...")
    
    # Find all highlight videos and sort them
    video_files = glob.glob(os.path.join(input_dir, "highlight_*.mp4"))
    
    if not video_files:
        print("No highlight videos found!")
        return False
    
    # Sort files by their sequence number
    video_files.sort(key=lambda x: int(os.path.basename(x).split('_')[1]))
    
    print(f"Found {len(video_files)} highlight videos:")
    for video in video_files:
        print(f"  - {os.path.basename(video)}")
    
    # Open the first video to get properties
    cap = cv2.VideoCapture(video_files[0])
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    # Process each video file
    total_frames = 0
    
    for video_file in video_files:
        print(f"Processing {os.path.basename(video_file)}...")
        cap = cv2.VideoCapture(video_file)
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            out.write(frame)
            frame_count += 1
            
        total_frames += frame_count
        cap.release()
        print(f"  - Added {frame_count} frames")
    
    out.release()
    
    duration = total_frames / fps
    minutes, seconds = divmod(duration, 60)
    print(f"Successfully created merged video: {output_file}")
    print(f"Duration: {int(minutes)}m {seconds:.2f}s ({total_frames} frames @ {fps} fps)")
    
    return True

if __name__ == "__main__":
    input_dir = "highlights"
    output_file = "merged_highlights.mp4"
    
    merge_videos(input_dir, output_file)

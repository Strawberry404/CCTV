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
    
    # Create video writer with a more compatible codec
    # Try H.264 codec which is more widely supported
    try:
        # First try H.264
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        if not out.isOpened():
            raise Exception("H264 codec not available")
    except Exception as e:
        print(f"Could not use H264 codec: {e}")
        try:
            # Then try XVID
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output_file = output_file.replace('.mp4', '.avi')
            out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
            if not out.isOpened():
                raise Exception("XVID codec not available")
        except Exception as e:
            print(f"Could not use XVID codec: {e}")
            # Fall back to MP4V
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_file = output_file.replace('.avi', '.mp4')
            out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    print(f"Creating video with codec: {chr(fourcc & 0xFF)} {chr((fourcc >> 8) & 0xFF)} {chr((fourcc >> 16) & 0xFF)} {chr((fourcc >> 24) & 0xFF)}")
    
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
    output_file = "merged_highlights_v2.mp4"
    
    merge_videos(input_dir, output_file)

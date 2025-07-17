import os
import glob
import subprocess
import imageio_ffmpeg

def merge_videos_with_ffmpeg(input_dir, output_file):
    """Merge all highlight videos in the input directory into a single output file using FFmpeg."""
    print(f"Searching for highlight videos in {input_dir}...")
    
    # Find all highlight videos and sort them
    video_files = glob.glob(os.path.join(input_dir, "highlight_*.mp4"))
    
    if not video_files:
        print("No highlight videos found!")
        return False
    
    # Sort files by their sequence number
    video_files.sort(key=lambda x: int(os.path.basename(x).split("_")[1]))
    
    print(f"Found {len(video_files)} highlight videos:")
    for video in video_files:
        print(f"  - {os.path.basename(video)}")
    
    # Create a text file listing all the input videos
    list_file = "filelist.txt"
    with open(list_file, "w") as f:
        for video_file in video_files:
            f.write(f"file \'{video_file}\'\n")
    
    # Get the path to FFmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"Using FFmpeg: {ffmpeg_exe}")
    
    # Construct the FFmpeg command
    cmd = [
        ffmpeg_exe,
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264",  # Use H.264 codec
        "-preset", "medium",  # Balance between speed and quality
        "-crf", "23",  # Quality level (lower is better)
        "-c:a", "aac",  # Audio codec
        "-b:a", "128k",  # Audio bitrate
        "-y",  # Overwrite output file if it exists
        output_file
    ]
    
    # Run FFmpeg
    print("Running FFmpeg to merge videos...")
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully created merged video: {output_file}")
        
        # Clean up the list file
        os.remove(list_file)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error merging videos: {e}")
        return False

if __name__ == "__main__":
    input_dir = "highlights"
    output_file = "merged_highlights_ffmpeg.mp4"
    
    merge_videos_with_ffmpeg(input_dir, output_file)

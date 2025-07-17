from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import glob

def merge_videos_with_moviepy(input_dir, output_file):
    """Merge all highlight videos in the input directory into a single output file using MoviePy."""
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
    
    # Load all video clips
    clips = []
    total_duration = 0
    
    for video_file in video_files:
        print(f"Loading {os.path.basename(video_file)}...")
        clip = VideoFileClip(video_file)
        clips.append(clip)
        total_duration += clip.duration
        print(f"  - Duration: {clip.duration:.2f} seconds")
    
    # Concatenate all clips
    print("Concatenating clips...")
    final_clip = concatenate_videoclips(clips)
    
    # Write the final video
    print(f"Writing final video to {output_file}...")
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
    
    # Close all clips
    for clip in clips:
        clip.close()
    final_clip.close()
    
    minutes, seconds = divmod(total_duration, 60)
    print(f"Successfully created merged video: {output_file}")
    print(f"Duration: {int(minutes)}m {seconds:.2f}s")
    
    return True

if __name__ == "__main__":
    input_dir = "highlights"
    output_file = "merged_highlights_moviepy.mp4"
    
    merge_videos_with_moviepy(input_dir, output_file)

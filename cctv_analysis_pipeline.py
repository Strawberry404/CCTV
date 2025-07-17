#!/usr/bin/env python
"""
CCTV Analysis Pipeline with Ultra-Sensitive Detection and Highlight Merging

This script provides an end-to-end solution for:
1. Processing CCTV footage with ultra-sensitive detection settings
2. Generating individual highlight clips for detected events
3. Automatically merging all highlight clips into a single video file

The settings are calibrated for maximum sensitivity to detect even the
most subtle movements or activities in the footage.
"""

import argparse
import json
import pathlib
import sys
import os
import glob
import subprocess
import imageio_ffmpeg
from typing import List, Optional

from src.cctv_analyzer.pipeline import process_cctv_video
from src.cctv_analyzer.config import (
    MotionDetectorConfig,
    ObjectDetectorConfig,
    ObjectTrackerConfig,
    EventAnalyzerConfig,
    VideoExporterConfig,
)


def create_ultra_sensitive_configs():
    """Create configurations with extremely low thresholds for maximum event detection."""
    # Ultra-sensitive motion detection
    motion_cfg = MotionDetectorConfig(
        min_area=100,  # Even lower minimum area (previous 150, default 300)
        var_threshold=15,  # Even lower variance threshold (previous 20, default 25)
    )
    
    # Ultra-sensitive object detection
    objdet_cfg = ObjectDetectorConfig(
        confidence_threshold=0.3,  # Even lower confidence threshold (previous 0.4, default 0.5)
    )
    
    # Even more forgiving object tracking
    tracker_cfg = ObjectTrackerConfig(
        iou_threshold=0.2,  # Even lower IOU threshold (previous 0.25, default 0.3)
        max_disappeared=20,  # Allow objects to disappear even longer (previous 15, default 10)
        min_track_length=3,  # Even shorter required track length (previous 5, default 8)
    )
    
    # Ultra-sensitive event analysis
    event_cfg = EventAnalyzerConfig(
        motion_sensitivity=0.01,  # Even lower threshold (previous 0.02, default 0.05)
        speed_threshold_multiplier=1.2,  # Even lower multiplier (previous 1.5, default 2.0)
        loitering_frames=15,  # Even fewer frames for loitering (previous 20, default 40)
        loitering_variance_threshold=400.0,  # Even higher variance allowed (previous 300.0, default 200.0)
    )
    
    # Even longer buffer for highlight clips
    export_cfg = VideoExporterConfig(
        buffer_seconds=6,  # Even longer buffer (previous 5, default 4)
        merge_threshold=4.0,  # Even more aggressive merging (previous 3.0, default 2.0)
    )
    
    return motion_cfg, objdet_cfg, tracker_cfg, event_cfg, export_cfg


def patch_event_analyzer():
    """
    Monkey patch the EventAnalyzer._filter_events method to use a lower threshold.
    
    This is a bit of a hack, but it allows us to lower the hardcoded 0.3 threshold
    without modifying the source files.
    """
    from src.cctv_analyzer.core.event_analyzer import EventAnalyzer
    from src.cctv_analyzer.models.event_models import Event
    from typing import List
    
    # Store the original method
    original_filter = EventAnalyzer._filter_events
    
    # Define our replacement with a lower threshold
    def patched_filter_events(self, events: List[Event]) -> List[Event]:
        filtered = [e for e in events if e.score >= 0.05]  # Lower from 0.1 to 0.05 (original default 0.3)
        filtered.sort(key=lambda ev: ev.score, reverse=True)
        return filtered[:40]  # Return even more events (previous 30, default 20)
    
    # Replace the method
    EventAnalyzer._filter_events = patched_filter_events
    
    return original_filter


def merge_highlights(input_dir: str, output_file: str) -> bool:
    """Merge all highlight videos in the input directory into a single output file using FFmpeg."""
    print(f"\nMerging highlight videos...")
    print(f"Searching for highlight videos in {input_dir}...")
    
    # Find all highlight videos and sort them
    video_files = glob.glob(os.path.join(input_dir, "highlight_*.mp4"))
    
    if not video_files:
        print("No highlight videos found to merge!")
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
            f.write(f"file '{video_file}'\n")
    
    # Get the path to FFmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"Using FFmpeg: {ffmpeg_exe}")
    
    # Make sure the output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
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


def process_video(
    video_path: str, 
    output_dir: str, 
    skip_frames: int = 1, 
    merged_output: Optional[str] = None
) -> int:
    """
    Process a video with ultra-sensitive settings and optionally merge highlights.
    
    Args:
        video_path: Path to the input video file
        output_dir: Directory to save highlights and summary
        skip_frames: Process every Nth frame (1 = process all frames)
        merged_output: If provided, merge highlights into this output file
    
    Returns:
        0 on success, 1 on failure
    """
    # Validate video file exists
    if not pathlib.Path(video_path).exists():
        print(f"Error: Video file not found: {video_path}")
        return 1
    
    # Create output directory
    out_path = pathlib.Path(output_dir)
    out_path.mkdir(exist_ok=True, parents=True)
    
    print(f"Processing video: {video_path}")
    print(f"Output directory: {output_dir}")
    print("Using ultra-sensitive detection thresholds...")
    
    # Get ultra-sensitive configurations
    motion_cfg, objdet_cfg, tracker_cfg, event_cfg, export_cfg = create_ultra_sensitive_configs()
    
    # Patch the event analyzer to use a lower threshold
    original_filter = patch_event_analyzer()
    
    try:
        # Process the video with our sensitive settings
        results = process_cctv_video(
            video_path,
            motion_cfg=motion_cfg,
            objdet_cfg=objdet_cfg,
            tracker_cfg=tracker_cfg,
            event_cfg=event_cfg,
            export_cfg=export_cfg,
            skip_frames=skip_frames
        )
        
        # Save the report
        report = results["report"]
        (out_path / "sensitive_summary.json").write_text(
            json.dumps(report, indent=2)
        )
        
        # Also save detailed events information
        events_data = [
            {
                "type": e.type,
                "timestamp": e.timestamp,
                "frame_idx": e.frame_idx,
                "score": e.score,
                "confidence": e.confidence,
                "metadata": e.metadata
            }
            for e in results["events"]
        ]
        (out_path / "events_detail.json").write_text(
            json.dumps(events_data, indent=2)
        )
        
        # Print summary
        print("\nAnalysis complete!")
        print(f"Total video duration: {report['total_video_duration']:.2f} seconds")
        print(f"Events detected: {report['total_events']}")
        print(f"Highlight clips created: {report['highlight_count']}")
        
        if report['highlight_count'] > 0:
            print(f"\nHighlight videos saved to: {output_dir}")
            
            # If merged output file is specified, merge the highlights
            if merged_output and report['highlight_count'] > 1:
                merge_highlights(output_dir, merged_output)
        else:
            print("\nNo highlight videos were generated.")
            print("The sensitivity settings are already extremely low. If no highlights were detected,")
            print("there might not be any significant activity in the video or there might be an issue with the footage.")
        
        # Detection summary
        print("\nObject detections:")
        for obj_class, count in report['class_counts'].items():
            print(f"  - {obj_class}: {count}")
            
        return 0
        
    except Exception as e:
        print(f"Error processing video: {e}")
        return 1
    finally:
        # Restore the original filter method
        from src.cctv_analyzer.core.event_analyzer import EventAnalyzer
        EventAnalyzer._filter_events = original_filter


def main():
    """Main entry point with command-line argument handling."""
    parser = argparse.ArgumentParser(
        description="CCTV Analysis with Ultra-Sensitive Detection and Highlight Merging"
    )
    parser.add_argument("video", help="Path to source video file")
    parser.add_argument(
        "-o", "--output", default="highlights", 
        help="Output folder for highlights and summary (default: highlights)"
    )
    parser.add_argument(
        "--skip-frames", type=int, default=1,
        help="Process every Nth frame (default: 1, meaning process all frames)"
    )
    parser.add_argument(
        "--merge", action="store_true",
        help="Merge all highlight clips into a single video"
    )
    parser.add_argument(
        "--merged-output", default="output/merged_highlights.mp4",
        help="Output file for merged highlights (default: output/merged_highlights.mp4)"
    )
    args = parser.parse_args()
    
    # Ensure the output directory for the merged file exists
    if args.merge:
        merged_output_dir = os.path.dirname(args.merged_output)
        if merged_output_dir and not os.path.exists(merged_output_dir):
            os.makedirs(merged_output_dir)
        merged_output = args.merged_output
    else:
        merged_output = None
    
    return process_video(args.video, args.output, args.skip_frames, merged_output)


if __name__ == "__main__":
    sys.exit(main())

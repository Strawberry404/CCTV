#!/usr/bin/env python
"""
Generate CCTV highlights with extremely low event detection thresholds.

This script runs the CCTV analysis pipeline with ultra-sensitive settings
to make it easier to generate highlight clips even from videos with
very subtle movements or activities. These settings have been modified
to use even lower thresholds than the original sensitive version.
"""

import argparse
import json
import pathlib
import sys

from src.cctv_analyzer.pipeline import process_cctv_video
from src.cctv_analyzer.config import (
    MotionDetectorConfig,
    ObjectDetectorConfig,
    ObjectTrackerConfig,
    EventAnalyzerConfig,
    VideoExporterConfig,
)


def create_sensitive_configs():
    """Create configurations with lower thresholds for easier event detection."""
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


def main():
    """Run the CCTV analysis with more sensitive settings."""
    parser = argparse.ArgumentParser(
        description="Generate CCTV highlights with lower detection thresholds"
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
    args = parser.parse_args()
    
    video_path = args.video
    output_dir = args.output
    
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
    
    # Get more sensitive configurations
    motion_cfg, objdet_cfg, tracker_cfg, event_cfg, export_cfg = create_sensitive_configs()
    
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
            skip_frames=args.skip_frames
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


if __name__ == "__main__":
    sys.exit(main())


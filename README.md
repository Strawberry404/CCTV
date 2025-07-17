# CCTV Analysis System

## Overview

This CCTV analysis system provides an end-to-end solution for processing surveillance footage, detecting events of interest, and generating highlight clips. The system is designed to:

1. Process video files with ultra-sensitive motion and object detection
2. Identify events based on movements, object interactions, and unusual activities
3. Generate individual highlight clips for each detected event
4. Optionally merge all highlight clips into a single continuous video

The system is built on a pipeline architecture that combines multiple specialized components:
- Motion detection for identifying any pixel changes
- Object detection for recognizing and classifying entities (people, vehicles, etc.)
- Object tracking for following entities across frames
- Event analysis for identifying patterns of interest
- Video export for creating highlight clips

## Key Features

- **Ultra-sensitive detection settings** - Calibrated to detect even subtle movements
- **Configurable sensitivity thresholds** - Adjust to your specific environment
- **Highlight generation** - Automatically create clips of interesting events
- **Highlight merging** - Combine all clips into a single review video
- **Detailed event reports** - JSON output with comprehensive event data

## Directory Structure

```
CCTV/
├── data/                  # Directory for input video files
├── highlights/            # Output directory for individual highlight clips
├── output/                # Output directory for merged highlight videos
├── src/                   # Source code for the CCTV analyzer
├── generate_highlights.py # Script for generating highlights with sensitive settings
├── merge_highlights*.py   # Scripts for merging highlight clips
└── cctv_analysis_pipeline.py # Integrated pipeline script
```

## Requirements

- Python 3.8 or higher
- OpenCV
- FFmpeg (automatically installed via imageio_ffmpeg)
- YOLOv8 for object detection

## Quick Start

1. Place your CCTV footage in the `data` directory
2. Run the integrated pipeline:
   ```
   python cctv_analysis_pipeline.py data/your_video.mp4 --merge
   ```
3. View the generated highlight clips in the `highlights` directory
4. Find the merged highlights video in the `output` directory

For detailed usage instructions, see [USAGE.md](USAGE.md).
For configuration options, see [CONFIGURATION.md](CONFIGURATION.md).
For troubleshooting help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

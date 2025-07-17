# Usage Guide for CCTV Analysis System

This guide explains how to use the CCTV analysis system to process videos, generate highlights, and merge them into a single review video.

## Basic Usage

### Integrated Pipeline (Recommended)

The integrated pipeline script `cctv_analysis_pipeline.py` combines both highlight generation and merging into a single command:

```bash
python cctv_analysis_pipeline.py VIDEO_PATH [options]
```

For example:
```bash
python cctv_analysis_pipeline.py data/security_cam.mp4 --merge
```

This will:
1. Process the video with ultra-sensitive settings
2. Generate highlight clips in the "highlights" directory
3. Merge all highlights into "output/merged_highlights.mp4"

### Command-line Arguments

The integrated pipeline supports the following arguments:

| Argument | Description | Default |
|----------|-------------|---------|
| `video` | Path to the source video file | (required) |
| `-o`, `--output` | Output folder for highlight clips | "highlights" |
| `--skip-frames` | Process every Nth frame (1 = process all) | 1 |
| `--merge` | Enable merging of highlight clips | disabled |
| `--merged-output` | Path for the merged video file | "output/merged_highlights.mp4" |

### Examples

Process a video and generate highlights only:
```bash
python cctv_analysis_pipeline.py data/video.mp4
```

Process a video, generate highlights, and merge them:
```bash
python cctv_analysis_pipeline.py data/video.mp4 --merge
```

Process a video with custom output locations:
```bash
python cctv_analysis_pipeline.py data/video.mp4 --output my_highlights --merge --merged-output my_folder/merged.mp4
```

Process only every 2nd frame (faster but less accurate):
```bash
python cctv_analysis_pipeline.py data/video.mp4 --skip-frames 2 --merge
```

## Advanced Usage

### Separate Components

If you prefer to run the pipeline in separate steps, you can use:

1. **Generate highlights only**:
   ```bash
   python generate_highlights.py data/video.mp4 -o highlights
   ```

2. **Merge highlights separately**:
   ```bash
   python merge_highlights_ffmpeg.py
   ```

### Batch Processing Multiple Videos

To process multiple videos in a batch, you can use a simple batch script or loop.

Windows example (PowerShell):
```powershell
foreach ($video in Get-ChildItem -Path "data" -Filter "*.mp4") {
    python cctv_analysis_pipeline.py $video.FullName --merge --merged-output "output/merged_$($video.BaseName).mp4"
}
```

Linux/Mac example (Bash):
```bash
for video in data/*.mp4; do
    python cctv_analysis_pipeline.py "$video" --merge --merged-output "output/merged_$(basename "$video")"
done
```

## Understanding the Output

### Highlight Clips

Highlight clips are named using the following format:
```
highlight_NNN_EVENT_TYPE_SCORE.mp4
```

For example:
- `highlight_001_motion_detected_0.21.mp4`
- `highlight_002_person_moving_0.45.mp4`

The numeric score indicates the confidence level of the event (higher is more significant).

### Output Files

The system generates several files:

| File | Description |
|------|-------------|
| `highlights/*.mp4` | Individual highlight video clips |
| `highlights/sensitive_summary.json` | Summary of detection results |
| `highlights/events_detail.json` | Detailed event information |
| `output/merged_highlights.mp4` | Combined video of all highlights |

### Event Types

The system can detect various event types:

- **Motion detected**: General movement in the scene
- **Object appeared**: New object entered the scene
- **Object disappeared**: Object left the scene
- **Fast movement**: Unusually fast motion
- **Loitering**: Object staying in one area for extended time
- **Unusual activity**: Movement patterns that differ from normal

## Best Practices

1. **Start with default settings**: The ultra-sensitive settings work well for most environments
2. **Process shorter videos first**: Start with 5-10 minute clips before processing hours of footage
3. **Review and refine**: Check the generated highlights and adjust settings if needed
4. **Use proper lighting**: Better lighting conditions lead to better detection results
5. **Position cameras strategically**: Minimize background movement (trees, flags, etc.)

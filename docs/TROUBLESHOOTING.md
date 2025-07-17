# Troubleshooting Guide for CCTV Analysis System

This guide helps you solve common problems that may occur when using the CCTV analysis system.

## No Highlights Generated

### Problem: The system processes the video but generates no highlight clips.

#### Possible causes and solutions:

1. **Video is too short**
   - The system needs enough frames to detect patterns and events
   - Solution: Use videos that are at least 30 seconds long

2. **No significant movement in the video**
   - Even with ultra-sensitive settings, there needs to be some movement
   - Solution: Verify the video contains actual movement or activity

3. **Settings not sensitive enough**
   - Solution: Edit `cctv_analysis_pipeline.py` and lower the thresholds further:
     ```python
     # Make detection even more sensitive
     motion_cfg = MotionDetectorConfig(
         min_area=50,  # Lower than the current 100
         var_threshold=10,  # Lower than the current 15
     )
     ```

4. **Video format or codec issues**
   - Solution: Convert the video to a standard format like H.264 MP4:
     ```
     ffmpeg -i your_video.mp4 -c:v libx264 -crf 23 converted_video.mp4
     ```

## Poor Quality Highlights

### Problem: Highlights are generated but are not capturing meaningful events.

#### Possible causes and solutions:

1. **Too many false positives**
   - Solution: Increase the confidence threshold:
     ```python
     objdet_cfg = ObjectDetectorConfig(
         confidence_threshold=0.4,  # Higher than the current 0.3
     )
     ```

2. **Highlights are too short**
   - Solution: Increase the buffer seconds:
     ```python
     export_cfg = VideoExporterConfig(
         buffer_seconds=10,  # Higher than the current 6
     )
     ```

3. **Highlights are capturing the wrong moments**
   - Solution: Adjust the event analyzer settings to focus on specific types of events

## Merging Issues

### Problem: Highlight merging fails or produces corrupted videos.

#### Possible causes and solutions:

1. **FFmpeg not found**
   - Solution: The system should automatically use the embedded FFmpeg, but if it fails:
     ```bash
     pip install --upgrade imageio_ffmpeg
     ```

2. **Incompatible video formats**
   - Solution: Ensure all highlight clips are in the same format
   - If needed, convert them manually before merging

3. **File permission issues**
   - Solution: Ensure you have write permissions to the output directory

4. **Merged video is too large**
   - Solution: Use the FFmpeg command directly with higher compression:
     ```
     ffmpeg -f concat -safe 0 -i filelist.txt -c:v libx264 -crf 28 -preset slower output.mp4
     ```

## Performance Issues

### Problem: The system is running too slowly.

#### Possible causes and solutions:

1. **Processing all frames**
   - Solution: Use the `--skip-frames` option to process fewer frames:
     ```bash
     python cctv_analysis_pipeline.py video.mp4 --skip-frames 2
     ```

2. **Video resolution is too high**
   - Solution: Pre-process the video to a lower resolution:
     ```
     ffmpeg -i input.mp4 -vf "scale=640:360" -c:v libx264 smaller_video.mp4
     ```

3. **System resources are limited**
   - Solution: Close other applications while processing
   - Try processing shorter video segments

## Error Messages

### "No module named 'src.cctv_analyzer'"

- **Cause**: Python cannot find the module
- **Solution**: Make sure you're running the script from the root directory of the project
  ```bash
  cd C:\Users\fatim\metime\CCTV
  python cctv_analysis_pipeline.py video.mp4
  ```

### "Failed to load OpenH264 library"

- **Cause**: Warning message from OpenCV about codec
- **Solution**: This is usually just a warning and can be ignored
- If needed, download the OpenH264 library from the Cisco website

### "Error processing video"

- **Cause**: General error during processing
- **Solution**: 
  1. Check that the video file is valid and not corrupted
  2. Try with a different video file
  3. Check the logs for more specific error messages

## Video Playback Issues

### Problem: Generated videos won't play in some players.

#### Possible causes and solutions:

1. **Codec compatibility issues**
   - Solution: Install the K-Lite Codec Pack (Windows) or VLC media player
   - Alternatively, convert the video to a more compatible format:
     ```
     ffmpeg -i highlight.mp4 -c:v libx264 -profile:v baseline -level 3.0 compatible.mp4
     ```

2. **Container format issues**
   - Solution: Try changing the output format to AVI or MKV:
     ```python
     # Change the output file extension
     merged_output = "output/merged_highlights.mkv"
     ```

## Dependencies and Installation

### Missing dependencies

If you encounter missing dependencies, install them with pip:

```bash
pip install opencv-python
pip install imageio_ffmpeg
pip install numpy
```

### YOLOv8 model issues

If the object detection fails:
1. Check that the YOLOv8 model file exists (`yolov8n.pt`)
2. If missing, download it manually:
   ```bash
   curl -o yolov8n.pt https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
   ```

## Advanced Troubleshooting

### Debugging the pipeline

1. Add print statements to track progress
2. Enable logging by adding at the top of the script:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

### Examining internal data

1. Save intermediate frames to examine what the system "sees":
   ```python
   # In the process_video function
   cv2.imwrite(f"debug_frame_{frame_idx}.jpg", frame)
   ```

2. Print detection data for debugging:
   ```python
   print("Detections:", detections)
   ```

## Getting Help

If you continue to experience issues:

1. Check the GitHub repository for updates
2. Look for similar issues in the project's issue tracker
3. Provide a detailed description of your problem including:
   - The exact command you ran
   - Any error messages
   - Your system specifications
   - A sample of the video you're trying to process

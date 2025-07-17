# Configuration Guide for CCTV Analysis System

This guide explains the various configuration options and sensitivity settings available in the CCTV analysis system.

## Sensitivity Settings

The system uses ultra-sensitive settings by default, which are designed to detect even the most subtle movements. These settings are defined in the `create_ultra_sensitive_configs()` function in `cctv_analysis_pipeline.py`.

### Motion Detection Settings

| Parameter | Default | Ultra-Sensitive | Description |
|-----------|---------|----------------|-------------|
| `min_area` | 300 | 100 | Minimum area (in pixels) required to consider a motion region |
| `var_threshold` | 25 | 15 | Variance threshold for background subtraction |

Lower values make the system more sensitive to small movements.

### Object Detection Settings

| Parameter | Default | Ultra-Sensitive | Description |
|-----------|---------|----------------|-------------|
| `confidence_threshold` | 0.5 | 0.3 | Minimum confidence score to accept an object detection |

Lower values allow the system to detect objects with less confidence, potentially increasing false positives but catching more subtle appearances.

### Object Tracking Settings

| Parameter | Default | Ultra-Sensitive | Description |
|-----------|---------|----------------|-------------|
| `iou_threshold` | 0.3 | 0.2 | Intersection over Union threshold for matching objects |
| `max_disappeared` | 10 | 20 | Maximum frames an object can disappear before losing track |
| `min_track_length` | 8 | 3 | Minimum number of frames required to establish a track |

These settings make the tracker more forgiving, allowing it to maintain tracking through occlusions and brief disappearances.

### Event Analysis Settings

| Parameter | Default | Ultra-Sensitive | Description |
|-----------|---------|----------------|-------------|
| `motion_sensitivity` | 0.05 | 0.01 | Threshold for motion-based event detection |
| `speed_threshold_multiplier` | 2.0 | 1.2 | Multiplier for determining unusual speed |
| `loitering_frames` | 40 | 15 | Number of frames to consider as loitering |
| `loitering_variance_threshold` | 200.0 | 400.0 | Variance threshold for loitering detection |

These settings affect how the system identifies meaningful events from the detected motions and objects.

### Video Exporting Settings

| Parameter | Default | Ultra-Sensitive | Description |
|-----------|---------|----------------|-------------|
| `buffer_seconds` | 4 | 6 | Seconds to include before/after the event |
| `merge_threshold` | 2.0 | 4.0 | Threshold for merging nearby events |

These settings control how highlight clips are generated from detected events.

### Event Filtering Thresholds

| Parameter | Default | Ultra-Sensitive | Description |
|-----------|---------|----------------|-------------|
| Score threshold | 0.3 | 0.05 | Minimum score to include an event |
| Maximum events | 20 | 40 | Maximum number of events to include |

The score threshold is particularly important - it filters out events based on their significance score.

## Customizing Configurations

If you need to adjust these settings, you can modify the `create_ultra_sensitive_configs()` function in `cctv_analysis_pipeline.py`.

For example, to make motion detection even more sensitive:

```python
# Ultra-sensitive motion detection
motion_cfg = MotionDetectorConfig(
    min_area=50,  # Even lower than the ultra-sensitive default
    var_threshold=10,  # Even lower threshold
)
```

## Advanced Configuration Files

The system also supports configuration through the core configuration files in the `src/cctv_analyzer/config.py` module. This file defines the configuration classes that are used throughout the system.

The main configuration classes are:

1. `MotionDetectorConfig` - Settings for motion detection
2. `ObjectDetectorConfig` - Settings for object detection
3. `ObjectTrackerConfig` - Settings for object tracking
4. `EventAnalyzerConfig` - Settings for event analysis
5. `VideoExporterConfig` - Settings for video export

## Environment-Specific Tuning

Different environments may require different settings:

### Indoor Office/Home
- Lower `min_area` (50-100)
- Lower `var_threshold` (10-15)
- Higher `confidence_threshold` (0.4-0.5)

### Outdoor Environments
- Higher `min_area` (150-300)
- Higher `var_threshold` (20-25)
- Lower `confidence_threshold` (0.3-0.4)

### Low-Light Conditions
- Lower `confidence_threshold` (0.2-0.3)
- Higher `max_disappeared` (25-30)
- Lower `motion_sensitivity` (0.01-0.02)

## Custom Event Types

The system primarily detects these event types:
- Motion events
- Object appearance/disappearance
- Speed-related events
- Loitering events

To add custom event types, you would need to modify the `EventAnalyzer` class in the source code.

## Performance Considerations

More sensitive settings generally require more computational resources. If performance is an issue:

1. Increase `skip_frames` to process fewer frames
2. Increase `min_area` to ignore smaller movements
3. Increase `confidence_threshold` to reduce processing of low-confidence detections
4. Decrease `max_disappeared` to abandon tracking sooner

## YOLOv8 Model Configuration

The system uses YOLOv8 for object detection. The model can be configured by modifying the `ObjectDetector` class in the source code.

By default, it detects these classes:
- person
- bicycle
- car
- motorcycle
- bus
- truck
- cat
- dog

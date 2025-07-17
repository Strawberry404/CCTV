"""Strongly-typed configuration objects for every core component."""

from dataclasses import dataclass, field
from typing import List


# ─────────────────── Motion - detector ────────────────────
@dataclass
class MotionDetectorConfig:
    algorithm: str = "MOG2"               # or "KNN"
    detect_shadows: bool = True
    var_threshold: int = 25
    history: int = 500
    morphology_kernel_size: int = 5
    min_area: int = 300                   # px²


# ─────────────────── Object - detector ────────────────────
@dataclass
class ObjectDetectorConfig:
    model: str = "yolov8n.pt"
    relevant_classes: List[str] = field(
        default_factory=lambda: ["person", "car", "truck", "bicycle"]
    )
    confidence_threshold: float = 0.5
    nms_threshold: float = 0.4
    device: str = "cuda"                  # "cpu" or "cuda"


# ─────────────────── Object - tracker ─────────────────────
@dataclass
class ObjectTrackerConfig:
    iou_threshold: float = 0.3
    max_disappeared: int = 10
    min_track_length: int = 8


# ─────────────────── Event - analyzer ─────────────────────
@dataclass
class EventAnalyzerConfig:
    motion_sensitivity: float = 0.05
    speed_threshold_multiplier: float = 2.0
    loitering_frames: int = 40
    loitering_variance_threshold: float = 200.0


# ─────────────────── Video - exporter ─────────────────────
@dataclass
class VideoExporterConfig:
    buffer_seconds: int = 4
    merge_threshold: float = 2.0          # s
    output_format: str = "mp4"
    video_codec: str = "mp4v"
    add_annotations: bool = True

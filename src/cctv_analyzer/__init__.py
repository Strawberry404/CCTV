"""
High-level package initialisation for CCTV Analyzer.
Imports the most commonly-used classes so users can write:

    from cctv_analyzer import process_video, Config

without digging through sub-modules.
"""

from .config import (
    MotionDetectorConfig,
    ObjectDetectorConfig,
    ObjectTrackerConfig,
    EventAnalyzerConfig,
    VideoExporterConfig,
)
from .pipeline import process_cctv_video as process_video

__all__ = [
    "MotionDetectorConfig",
    "ObjectDetectorConfig",
    "ObjectTrackerConfig",
    "EventAnalyzerConfig",
    "VideoExporterConfig",
    "process_video",
]

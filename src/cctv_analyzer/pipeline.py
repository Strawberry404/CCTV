# src/cctv_analyzer/pipeline.py
"""Single entry‑point that wires all components together."""

import json
import pathlib
from collections import defaultdict
from typing import Dict, Any, List

from .core.motion_detector import MotionDetector
from .core.object_detector import ObjectDetector
from .core.object_tracker import ObjectTracker
from .core.event_analyzer import EventAnalyzer
from .core.video_exporter import VideoExporter
from .core import video_utils
from .config import (
    MotionDetectorConfig,
    ObjectDetectorConfig,
    ObjectTrackerConfig,
    EventAnalyzerConfig,
    VideoExporterConfig,
)
from .models.event_models import Event, VideoSegment


def process_cctv_video(
    video_path: str,
    *,
    motion_cfg: MotionDetectorConfig = MotionDetectorConfig(),
    objdet_cfg: ObjectDetectorConfig = ObjectDetectorConfig(),
    tracker_cfg: ObjectTrackerConfig = ObjectTrackerConfig(),
    event_cfg: EventAnalyzerConfig = EventAnalyzerConfig(),
    export_cfg: VideoExporterConfig = VideoExporterConfig(),
    skip_frames: int = 2,
) -> Dict[str, Any]:
    """End‑to‑end CCTV analysis pipeline."""

    # 1 ▸ Extract frames & timestamps
    frames, timestamps, fps = video_utils.extract_frames(
        video_path, skip_frames=skip_frames
    )

    # 2 ▸ Motion detection
    motion = MotionDetector(motion_cfg)
    motion_data = motion.detect_motion(frames)

    # 3 ▸ Object detection
    detector = ObjectDetector(objdet_cfg)
    detections = detector.detect_objects(frames)
    filtered = [
        [d for d in frame_det if d["class"] in objdet_cfg.relevant_classes]
        for frame_det in detections
    ]

    # 4 ▸ Object tracking
    tracker = ObjectTracker(tracker_cfg)
    tracked_history = defaultdict(list)
    for idx, frame_det in enumerate(filtered):
        tracks = tracker.track_objects([frame_det], timestamps[idx : idx + 1])
        for obj_id, data in tracks.items():
            tracked_history[obj_id].append(data)

    # 5 ▸ Event analysis
    analyzer = EventAnalyzer(event_cfg)
    events: List[Event] = analyzer.analyze_events(
        motion_data, tracked_history, timestamps, fps
    )

    # 6 ▸ Highlight export
    exporter = VideoExporter(export_cfg)
    segments: List[VideoSegment] = exporter.create_highlights(
        video_path, events, timestamps, "highlights"
    )

    report = {
        "total_video_duration": timestamps[-1] if timestamps else 0,
        "total_events": len(events),
        "highlight_count": len(segments),
        "class_counts": detector.get_detection_summary(filtered)["class_counts"],
    }

    return {"segments": segments, "events": events, "report": report}


# CLI helper
if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Run CCTV video analysis")
    ap.add_argument("video", help="Path to source video file")
    ap.add_argument("-o", "--out", default="highlights", help="Output folder")
    ns = ap.parse_args()

    pathlib.Path(ns.out).mkdir(exist_ok=True)
    results = process_cctv_video(ns.video)
    (pathlib.Path(ns.out) / "summary.json").write_text(
        json.dumps(results["report"], indent=2)
    )
    print("✅ Analysis complete; see", ns.out)

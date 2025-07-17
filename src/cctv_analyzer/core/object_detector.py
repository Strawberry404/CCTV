# core/object_detector.py
"""Object detection module using YOLO."""

import logging
from typing import List, Dict

import cv2
import numpy as np
from ultralytics import YOLO

logger = logging.getLogger(__name__)


class ObjectDetector:
    """Handles object detection using YOLO models."""

    def __init__(self, config):
        """Initialize object detector with configuration."""
        self.config = config
        self.model = YOLO(config.model)
        self.relevant_classes = set(config.relevant_classes)
        logger.info("Loaded YOLO model: %s", config.model)

    def detect_objects(self, frames: List[np.ndarray]) -> List[List[Dict]]:
        """Detect objects in a sequence of frames."""
        all_detections: List[List[Dict]] = []
        logger.info("Processing %d frames for object detection", len(frames))

        for frame in frames:
            results = self.model(
                frame,
                conf=self.config.confidence_threshold,
                iou=self.config.nms_threshold,
                device=self.config.device,
                verbose=False,
            )

            frame_detections: List[Dict] = []

            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = float(box.conf[0].cpu().numpy())
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = self.model.names[class_id]

                        if class_name in self.relevant_classes:
                            frame_detections.append(
                                {
                                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                                    "confidence": confidence,
                                    "class": class_name,
                                    "class_id": class_id,
                                    "area": (x2 - x1) * (y2 - y1),
                                }
                            )

            all_detections.append(frame_detections)

        return all_detections

    def get_detection_summary(self, detections: List[List[Dict]]) -> Dict:
        """Get summary statistics of detections."""
        total_detections = sum(len(frame) for frame in detections)
        class_counts: Dict[str, int] = {}

        for frame_detections in detections:
            for det in frame_detections:
                class_name = det["class"]
                class_counts[class_name] = class_counts.get(class_name, 0) + 1

        return {
            "total_detections": total_detections,
            "frames_with_detections": sum(1 for frame in detections if frame),
            "class_counts": class_counts,
            "average_detections_per_frame": total_detections / len(detections)
            if detections
            else 0,
        }

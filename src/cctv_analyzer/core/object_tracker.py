# core/object_tracker.py
"""Object tracking module using IoU-based tracking."""

import logging
from collections import defaultdict
from typing import Dict, List

import numpy as np

logger = logging.getLogger(__name__)


class ObjectTracker:
    """Simple IoU-based object tracker."""

    def __init__(self, config):
        self.config = config
        self.next_id = 0
        self.objects: Dict[int, Dict] = {}
        self.disappeared: Dict[int, int] = defaultdict(int)

    def track_objects(
        self, detections: List[List[Dict]], timestamps: List[float]
    ) -> Dict[int, List[Dict]]:
        """Track objects across frames and build history."""
        history: Dict[int, List[Dict]] = defaultdict(list)

        for frame_idx, (frame_dets, ts) in enumerate(zip(detections, timestamps)):
            tracked = self._update_tracks(frame_dets)

            for obj_id, data in tracked.items():
                track = data.copy()
                track["timestamp"] = ts
                track["frame_idx"] = frame_idx
                track["centroid"] = self._get_centroid(track["bbox"])
                history[obj_id].append(track)

        return {
            obj_id: hist
            for obj_id, hist in history.items()
            if len(hist) >= self.config.min_track_length
        }

    # internal helpers
    def _update_tracks(self, detections: List[Dict]) -> Dict[int, Dict]:
        if not detections:
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.config.max_disappeared:
                    self._deregister(obj_id)
            return self.objects

        if not self.objects:
            for det in detections:
                self._register(det)
        else:
            self._match_detections(detections)

        return self.objects

    def _match_detections(self, detections: List[Dict]):
        object_ids = list(self.objects.keys())
        ious = np.zeros((len(object_ids), len(detections)))

        for i, obj_id in enumerate(object_ids):
            for j, det in enumerate(detections):
                ious[i, j] = self._calculate_iou(self.objects[obj_id]["bbox"], det["bbox"])

        used_objects = set()
        used_dets = set()

        matches = [
            (i, j, ious[i, j])
            for i in range(len(object_ids))
            for j in range(len(detections))
            if ious[i, j] > self.config.iou_threshold
        ]
        matches.sort(key=lambda x: x[2], reverse=True)

        for i, j, _ in matches:
            if i in used_objects or j in used_dets:
                continue
            obj_id = object_ids[i]
            self.objects[obj_id] = detections[j].copy()
            self.objects[obj_id]["id"] = obj_id
            self.disappeared[obj_id] = 0
            used_objects.add(i)
            used_dets.add(j)

        # unmatched objects
        for i, obj_id in enumerate(object_ids):
            if i not in used_objects:
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.config.max_disappeared:
                    self._deregister(obj_id)

        # unmatched detections
        for j, det in enumerate(detections):
            if j not in used_dets:
                self._register(det)

    def _register(self, detection: Dict):
        detection_copy = detection.copy()
        detection_copy["id"] = self.next_id
        self.objects[self.next_id] = detection_copy
        self.disappeared[self.next_id] = 0
        self.next_id += 1

    def _deregister(self, object_id: int):
        self.objects.pop(object_id, None)
        self.disappeared.pop(object_id, None)

    @staticmethod
    def _calculate_iou(box1: List[float], box2: List[float]) -> float:
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2
        x1_inter = max(x1_1, x1_2)
        y1_inter = max(y1_1, y1_2)
        x2_inter = min(x2_1, x2_2)
        y2_inter = min(y2_1, y2_2)
        if x2_inter <= x1_inter or y2_inter <= y1_inter:
            return 0.0
        inter = (x2_inter - x1_inter) * (y2_inter - y1_inter)
        area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        area2 = (x2_2 - x1_2) * (y2_2 - y2_2)
        union = area1 + area2 - inter
        return inter / union if union else 0.0

    @staticmethod
    def _get_centroid(bbox: List[float]) -> tuple:
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)

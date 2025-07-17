# core/event_analyzer.py
"""Event analysis module for detecting unusual activities."""

import logging
import math
from typing import Dict, List

import numpy as np

from ..models.event_models import Event

logger = logging.getLogger(__name__)


class EventAnalyzer:
    """Analyzes motion and tracking data to detect events."""

    def __init__(self, config):
        self.config = config

    def analyze_events(
        self,
        motion_data: Dict,
        tracking_data: Dict,
        timestamps: List[float],
        fps: float,
    ) -> List[Event]:
        events: List[Event] = []

        events.extend(self._analyze_motion_events(motion_data, timestamps))
        events.extend(self._analyze_behavior_events(tracking_data, fps))

        events = self._score_events(events, motion_data)
        return self._filter_events(events)

    def _analyze_motion_events(
        self, motion_data: Dict, timestamps: List[float]
    ) -> List[Event]:
        events: List[Event] = []
        for idx, (is_motion, score, ts) in enumerate(
            zip(
                motion_data["motion_events"],
                motion_data["motion_scores"],
                timestamps,
            )
        ):
            if is_motion and score > self.config.motion_sensitivity:
                events.append(
                    Event(
                        type="motion_detected",
                        timestamp=ts,
                        frame_idx=idx,
                        score=score,
                        confidence=min(score * 10, 1.0),
                        metadata={"motion_score": score},
                    )
                )
        return events

    def _analyze_behavior_events(
        self, tracking_data: Dict, fps: float
    ) -> List[Event]:
        events: List[Event] = []
        for obj_id, hist in tracking_data.items():
            if len(hist) < 10:
                continue
            speeds = self._calculate_speeds(hist, fps)
            positions = [t["centroid"] for t in hist]
            events.extend(self._detect_sudden_movements(obj_id, hist, speeds, fps))
            events.extend(self._detect_loitering(obj_id, hist, positions, fps))
            events.extend(self._detect_direction_changes(obj_id, hist, positions))
        return events

    @staticmethod
    def _calculate_speeds(history: List[Dict], fps: float) -> List[float]:
        speeds = []
        for i in range(1, len(history)):
            prev = history[i - 1]["centroid"]
            curr = history[i]["centroid"]
            dist = math.hypot(curr[0] - prev[0], curr[1] - prev[1])
            speeds.append(dist * fps)  # pixels per second
        return speeds

    def _detect_sudden_movements(
        self, obj_id: int, hist: List[Dict], speeds: List[float], fps: float
    ) -> List[Event]:
        events = []
        if not speeds:
            return events
        avg_speed = np.mean(speeds)
        threshold = avg_speed * self.config.speed_threshold_multiplier
        for i, speed in enumerate(speeds):
            if speed > threshold and speed > 5.0:
                track = hist[i + 1]
                events.append(
                    Event(
                        type="sudden_movement",
                        timestamp=track["timestamp"],
                        frame_idx=track["frame_idx"],
                        score=min(speed / avg_speed, 10.0) / 10.0,
                        confidence=0.8,
                        object_id=obj_id,
                        bbox=track["bbox"],
                        metadata={
                            "speed": speed,
                            "average_speed": avg_speed,
                            "object_class": track.get("class", "unknown"),
                        },
                    )
                )
        return events

    def _detect_loitering(
        self, obj_id: int, hist: List[Dict], positions: List[tuple], fps: float
    ) -> List[Event]:
        events = []
        if len(hist) < self.config.loitering_frames:
            return events
        var = np.var(np.array(positions), axis=0).sum()
        if var < self.config.loitering_variance_threshold:
            duration = len(hist) / fps
            last = hist[-1]
            events.append(
                Event(
                    type="loitering",
                    timestamp=last["timestamp"],
                    frame_idx=last["frame_idx"],
                    score=min(duration / 60.0, 1.0),
                    confidence=0.7,
                    object_id=obj_id,
                    bbox=last["bbox"],
                    metadata={
                        "duration": duration,
                        "variance": var,
                        "object_class": last.get("class", "unknown"),
                    },
                )
            )
        return events

    def _detect_direction_changes(
        self, obj_id: int, hist: List[Dict], positions: List[tuple]
    ) -> List[Event]:
        events = []
        if len(positions) < 5:
            return events
        for i in range(2, len(positions)):
            prev_vec = (
                positions[i - 1][0] - positions[i - 2][0],
                positions[i - 1][1] - positions[i - 2][1],
            )
            curr_vec = (
                positions[i][0] - positions[i - 1][0],
                positions[i][1] - positions[i - 1][1],
            )
            if np.linalg.norm(prev_vec) == 0 or np.linalg.norm(curr_vec) == 0:
                continue
            angle = np.arccos(
                np.clip(
                    np.dot(prev_vec, curr_vec)
                    / (np.linalg.norm(prev_vec) * np.linalg.norm(curr_vec)),
                    -1.0,
                    1.0,
                )
            )
            if angle > np.pi / 2:
                track = hist[i]
                events.append(
                    Event(
                        type="direction_change",
                        timestamp=track["timestamp"],
                        frame_idx=track["frame_idx"],
                        score=angle / np.pi,
                        confidence=0.6,
                        object_id=obj_id,
                        bbox=track["bbox"],
                        metadata={
                            "angle_radians": angle,
                            "angle_degrees": np.degrees(angle),
                            "object_class": track.get("class", "unknown"),
                        },
                    )
                )
        return events

    def _score_events(self, events: List[Event], motion_data: Dict) -> List[Event]:
        motion_scores = motion_data["motion_scores"]
        type_weights = {
            "sudden_movement": 0.8,
            "loitering": 0.6,
            "direction_change": 0.5,
            "motion_detected": 0.4,
        }

        for e in events:
            motion_bonus = (
                motion_scores[e.frame_idx] * 0.2 if e.frame_idx < len(motion_scores) else 0
            )
            e.score = min(e.score + motion_bonus, 1.0) * type_weights.get(e.type, 0.5)
        return events

    def _filter_events(self, events: List[Event]) -> List[Event]:
        filtered = [e for e in events if e.score >= 0.3]
        filtered.sort(key=lambda ev: ev.score, reverse=True)
        return filtered[:20]

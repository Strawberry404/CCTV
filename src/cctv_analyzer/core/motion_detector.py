# core/motion_detector.py
"""Motion detection module using background subtraction."""

import cv2
import numpy as np
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class MotionDetector:
    """Handles motion detection using various background subtraction algorithms."""

    def __init__(self, config):
        """Initialize motion detector with configuration."""
        self.config = config
        self.bg_subtractor = self._create_background_subtractor()
        self.kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (config.morphology_kernel_size, config.morphology_kernel_size),
        )

    def _create_background_subtractor(self):
        """Create background subtractor based on configuration."""
        if self.config.algorithm == "MOG2":
            return cv2.createBackgroundSubtractorMOG2(
                detectShadows=self.config.detect_shadows,
                varThreshold=self.config.var_threshold,
                history=self.config.history,
            )
        elif self.config.algorithm == "KNN":
            return cv2.createBackgroundSubtractorKNN(
                detectShadows=self.config.detect_shadows,
                dist2Threshold=self.config.var_threshold * 8,
                history=self.config.history,
            )
        else:
            raise ValueError(f"Unknown algorithm: {self.config.algorithm}")

    def detect_motion(self, frames: List[np.ndarray]) -> Dict:
        """Detect motion in a sequence of frames."""
        motion_masks = []
        motion_scores = []

        logger.info("Processing %d frames for motion detection", len(frames))

        for frame in frames:
            fg_mask = self.bg_subtractor.apply(frame)

            if self.config.detect_shadows:
                fg_mask[fg_mask == 127] = 0

            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, self.kernel)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, self.kernel)

            contours, _ = cv2.findContours(
                fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            filtered_mask = np.zeros_like(fg_mask)

            for contour in contours:
                if cv2.contourArea(contour) >= self.config.min_area:
                    cv2.fillPoly(filtered_mask, [contour], 255)

            motion_score = np.sum(filtered_mask > 0) / (
                filtered_mask.shape[0] * filtered_mask.shape[1]
            )

            motion_masks.append(filtered_mask)
            motion_scores.append(motion_score)

        motion_events = self._adaptive_threshold(motion_scores)

        return {
            "motion_masks": motion_masks,
            "motion_scores": motion_scores,
            "motion_events": motion_events,
        }

    def _adaptive_threshold(
        self, motion_scores: List[float], window_size: int = 30
    ) -> List[bool]:
        """Apply adaptive thresholding for motion detection."""
        motion_events = []
        for i in range(len(motion_scores)):
            start_idx = max(0, i - window_size)
            end_idx = min(len(motion_scores), i + window_size)
            local_scores = motion_scores[start_idx:end_idx]
            local_mean = np.mean(local_scores)
            local_std = np.std(local_scores)
            threshold = local_mean + 2 * local_std
            is_motion = motion_scores[i] > max(threshold, 0.01)
            motion_events.append(is_motion)
        return motion_events
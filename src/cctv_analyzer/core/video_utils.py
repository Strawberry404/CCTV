"""Tiny helpers for frame extraction and timestamp generation."""

from typing import List, Tuple
import cv2
import numpy as np


def extract_frames(
    video_path: str,
    *,
    skip_frames: int = 0,
) -> Tuple[List[np.ndarray], List[float], float]:
    """Return list(frames), list(timestamps), fps."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frames: List[np.ndarray] = []
    timestamps: List[float] = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if skip_frames and (idx % (skip_frames + 1)):
            idx += 1
            continue
        frames.append(frame)
        timestamps.append(idx / fps)
        idx += 1
    cap.release()
    return frames, timestamps, fps

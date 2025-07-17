# core/video_exporter.py
"""Video export module for creating highlight clips."""

import logging
from pathlib import Path
from typing import List

import cv2
import numpy as np

from ..models.event_models import Event, VideoSegment

logger = logging.getLogger(__name__)


class VideoExporter:
    """Handles creation and export of highlight video clips."""

    def __init__(self, config):
        self.config = config

    def create_highlights(
        self,
        video_path: str,
        events: List[Event],
        timestamps: List[float],
        output_dir: str,
    ) -> List[VideoSegment]:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        segments = self._create_segments(events, timestamps)
        segments = self._merge_segments(segments)

        return self._export_segments(video_path, segments, output_dir)

    def _create_segments(
        self, events: List[Event], timestamps: List[float]
    ) -> List[VideoSegment]:
        buffer = self.config.buffer_seconds
        segs = []

        for e in events:
            start_time = max(0, e.timestamp - buffer)
            end_time = min(timestamps[-1], e.timestamp + buffer)
            segs.append(
                VideoSegment(
                    start_time=start_time,
                    end_time=end_time,
                    start_frame=self._find_frame_index(timestamps, start_time),
                    end_frame=self._find_frame_index(timestamps, end_time),
                    duration=end_time - start_time,
                    events=[e],
                )
            )
        return segs

    @staticmethod
    def _find_frame_index(timestamps: List[float], target: float) -> int:
        return min(range(len(timestamps)), key=lambda i: abs(timestamps[i] - target))

    def _merge_segments(self, segments: List[VideoSegment]) -> List[VideoSegment]:
        if not segments:
            return []
        segments.sort(key=lambda s: s.start_time)
        merged = [segments[0]]
        for cur in segments[1:]:
            last = merged[-1]
            if cur.start_time - last.end_time <= self.config.merge_threshold:
                last.end_time = max(last.end_time, cur.end_time)
                last.end_frame = max(last.end_frame, cur.end_frame)
                last.duration = last.end_time - last.start_time
                last.events.extend(cur.events)
            else:
                merged.append(cur)
        return merged

    def _export_segments(
        self, video_path: str, segments: List[VideoSegment], output_dir: Path
    ) -> List[VideoSegment]:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        exported = []

        fourcc = cv2.VideoWriter_fourcc(*self.config.video_codec)

        for i, seg in enumerate(segments):
            primary_event = max(seg.events, key=lambda e: e.score)
            filename = (
                f"highlight_{i+1:03d}_{primary_event.type}_{primary_event.score:.2f}."
                f"{self.config.output_format}"
            )
            output_file = output_dir / filename
            writer = cv2.VideoWriter(
                str(output_file), fourcc, fps, (frame_width, frame_height)
            )

            start_frame = int(seg.start_time * fps)
            end_frame = int(seg.end_time * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            for frame_num in range(start_frame, min(end_frame, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
                ret, frame = cap.read()
                if not ret:
                    break
                if self.config.add_annotations:
                    frame = self._add_annotations(frame, seg, frame_num - start_frame, fps)
                writer.write(frame)
            writer.release()

            seg.output_file = output_file
            exported.append(seg)

        cap.release()
        return exported

    def _add_annotations(
        self, frame: np.ndarray, segment: VideoSegment, rel_frame: int, fps: float
    ) -> np.ndarray:
        current_time = segment.start_time + (rel_frame / fps)
        cv2.putText(
            frame,
            f"Time: {current_time:.1f}s",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        if segment.events:
            ev = max(segment.events, key=lambda e: e.score)
            cv2.putText(
                frame,
                f"Event: {ev.type.replace('_', ' ').title()}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
            )
            cv2.putText(
                frame,
                f"Score: {ev.score:.2f}",
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )
        return frame

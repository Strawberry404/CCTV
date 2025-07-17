"""Lightweight model objects passed between pipeline stages."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path


@dataclass
class Event:
    type: str
    timestamp: float
    frame_idx: int
    score: float
    confidence: float
    object_id: Optional[int] = None
    bbox: Optional[List[float]] = None  # [x1,y1,x2,y2]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VideoSegment:
    start_time: float
    end_time: float
    start_frame: int
    end_frame: int
    duration: float
    events: List[Event]
    output_file: Optional[Path] = None

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class MeshStats:
    vertex_count: int
    face_count: int
    has_vertex_normals: bool
    bbox_min: np.ndarray
    bbox_max: np.ndarray


@dataclass
class Point3D:
    x: float
    y: float
    z: float

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z], dtype=float)


@dataclass
class LandmarkSet:
    points: List[Point3D]
    seed: Point3D | None = None

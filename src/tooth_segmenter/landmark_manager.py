from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import trimesh

from .models import LandmarkSet, Point3D


@dataclass
class LandmarkManager:
    points: list[np.ndarray] = field(default_factory=list)
    seed: np.ndarray | None = None

    def add_point(self, point: np.ndarray) -> None:
        self.points.append(np.asarray(point, dtype=float))

    def remove_last(self) -> None:
        if self.points:
            self.points.pop()

    def clear_points(self) -> None:
        self.points.clear()

    def validate_min_points(self, min_points: int = 4) -> None:
        if len(self.points) < min_points:
            raise ValueError(f"At least {min_points} control points are required for segmentation.")


def nearest_vertex(mesh: trimesh.Trimesh, point: np.ndarray) -> int:
    deltas = mesh.vertices - point
    return int(np.argmin(np.einsum("ij,ij->i", deltas, deltas)))


def load_landmarks_json(path: str | Path) -> LandmarkSet:
    raw = json.loads(Path(path).read_text())
    points = [Point3D(**p) for p in raw["points"]]
    seed = Point3D(**raw["seed"]) if raw.get("seed") else None
    return LandmarkSet(points=points, seed=seed)

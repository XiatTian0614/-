from __future__ import annotations

from pathlib import Path

import trimesh


def export_segment(mesh: trimesh.Trimesh, output_dir: str | Path, stem: str = "tooth_segment") -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    idx = 1
    while True:
        path = output_dir / f"{stem}_{idx:03d}.stl"
        if not path.exists():
            mesh.export(path)
            return path
        idx += 1

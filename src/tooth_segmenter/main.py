from __future__ import annotations

"""Simple Python program entrypoint for tooth mesh segmentation MVP."""

import argparse
import json
from pathlib import Path

from .boundary_builder import build_closed_boundary
from .export_service import export_segment
from .graph_geodesic import build_vertex_graph
from .landmark_manager import nearest_vertex
from .mesh_io import load_mesh, mesh_stats
from .mesh_segmenter import extract_submesh, segment_faces
from .models import Point3D


def _load_landmark_points(path: str | Path) -> tuple[list[Point3D], Point3D | None]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    points = [Point3D(**item) for item in data.get("points", [])]
    seed_raw = data.get("seed")
    seed = Point3D(**seed_raw) if seed_raw else None
    return points, seed


def run(mesh_path: str, landmarks_path: str, out_dir: str, invert: bool = False) -> Path:
    mesh = load_mesh(mesh_path)
    stats = mesh_stats(mesh)
    print(
        "Mesh loaded:",
        f"vertices={stats.vertex_count}",
        f"faces={stats.face_count}",
        f"bbox_min={stats.bbox_min.tolist()}",
        f"bbox_max={stats.bbox_max.tolist()}",
    )

    points, seed = _load_landmark_points(landmarks_path)
    if len(points) < 4:
        raise ValueError("控制點不足：至少需要 4 個 points 才能形成封閉邊界。")

    graph = build_vertex_graph(mesh)
    control_vertices = [nearest_vertex(mesh, p.as_array()) for p in points]
    boundary = build_closed_boundary(graph, control_vertices)

    seed_point = seed.as_array() if seed else mesh.vertices[control_vertices[0]]
    seed_face = int(mesh.nearest.on_surface([seed_point])[2][0])

    selected_faces = segment_faces(mesh, boundary, seed_face, invert=invert)
    segmented = extract_submesh(mesh, selected_faces)
    output_path = export_segment(segmented, out_dir)
    print(f"Segment exported: {output_path}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Tooth mesh segmentation Python program")
    parser.add_argument("mesh", help="Input mesh file path: STL/OBJ/PLY")
    parser.add_argument("landmarks", help="Landmarks JSON file path")
    parser.add_argument("--out", default="outputs", help="Output folder")
    parser.add_argument("--invert", action="store_true", help="Select outside region")
    args = parser.parse_args()
    run(args.mesh, args.landmarks, args.out, invert=args.invert)


if __name__ == "__main__":
    main()

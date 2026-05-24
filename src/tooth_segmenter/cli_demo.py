from __future__ import annotations

import argparse

from .boundary_builder import build_closed_boundary
from .export_service import export_segment
from .graph_geodesic import build_vertex_graph
from .landmark_manager import load_landmarks_json, nearest_vertex
from .mesh_io import load_mesh
from .mesh_segmenter import extract_submesh, segment_faces


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mesh")
    parser.add_argument("landmarks")
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()

    mesh = load_mesh(args.mesh)
    lm = load_landmarks_json(args.landmarks)
    if len(lm.points) < 4:
        raise ValueError("At least 4 control points are required.")

    graph = build_vertex_graph(mesh)
    control_vertices = [nearest_vertex(mesh, p.as_array()) for p in lm.points]
    boundary = build_closed_boundary(graph, control_vertices)
    seed_point = lm.seed.as_array() if lm.seed else mesh.vertices[control_vertices[0]]
    seed_face = int(mesh.nearest.on_surface([seed_point])[2][0])
    selected = segment_faces(mesh, boundary, seed_face)
    submesh = extract_submesh(mesh, selected)
    out = export_segment(submesh, args.out)
    print(f"Exported: {out}")


if __name__ == "__main__":
    main()

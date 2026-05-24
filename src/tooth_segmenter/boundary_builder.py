from __future__ import annotations

from .graph_geodesic import dijkstra_path


def build_closed_boundary(graph: dict[int, list[tuple[int, float]]], control_vertices: list[int]) -> list[int]:
    if len(control_vertices) < 4:
        raise ValueError("Need at least 4 control vertices to form closed boundary.")
    boundary: list[int] = []
    for i in range(len(control_vertices)):
        a = control_vertices[i]
        b = control_vertices[(i + 1) % len(control_vertices)]
        segment = dijkstra_path(graph, a, b)
        if not boundary:
            boundary.extend(segment)
        else:
            boundary.extend(segment[1:])
    if boundary[0] != boundary[-1]:
        boundary.append(boundary[0])
    return boundary

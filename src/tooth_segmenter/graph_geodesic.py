from __future__ import annotations

from collections import defaultdict
import heapq

import numpy as np
import trimesh


def build_vertex_graph(mesh: trimesh.Trimesh) -> dict[int, list[tuple[int, float]]]:
    graph: dict[int, list[tuple[int, float]]] = defaultdict(list)
    for a, b in mesh.edges_unique:
        w = float(np.linalg.norm(mesh.vertices[a] - mesh.vertices[b]))
        graph[int(a)].append((int(b), w))
        graph[int(b)].append((int(a), w))
    return dict(graph)


def dijkstra_path(graph: dict[int, list[tuple[int, float]]], start: int, goal: int) -> list[int]:
    heap: list[tuple[float, int]] = [(0.0, start)]
    dist = {start: 0.0}
    prev: dict[int, int] = {}
    seen: set[int] = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        if u == goal:
            break
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    if goal not in dist:
        raise ValueError("No path found between control points.")
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()
    return path

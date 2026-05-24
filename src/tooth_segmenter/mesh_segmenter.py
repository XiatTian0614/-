from __future__ import annotations

from collections import deque

import trimesh


def _barrier_edges(boundary_vertices: list[int]) -> set[tuple[int, int]]:
    edges = set()
    for a, b in zip(boundary_vertices, boundary_vertices[1:]):
        edges.add(tuple(sorted((a, b))))
    return edges


def _face_adjacency(mesh: trimesh.Trimesh) -> list[set[int]]:
    adj = [set() for _ in range(len(mesh.faces))]
    for (f1, f2), edge in zip(mesh.face_adjacency, mesh.face_adjacency_edges):
        adj[int(f1)].add((int(f2), tuple(sorted((int(edge[0]), int(edge[1]))))))
        adj[int(f2)].add((int(f1), tuple(sorted((int(edge[0]), int(edge[1]))))))
    return adj


def segment_faces(mesh: trimesh.Trimesh, boundary_vertices: list[int], seed_face: int, invert: bool = False) -> set[int]:
    barriers = _barrier_edges(boundary_vertices)
    adj = _face_adjacency(mesh)
    selected: set[int] = set()
    q = deque([seed_face])
    selected.add(seed_face)
    while q:
        f = q.popleft()
        for nb, crossing_edge in adj[f]:
            if crossing_edge in barriers:
                continue
            if nb not in selected:
                selected.add(nb)
                q.append(nb)
    if invert:
        return set(range(len(mesh.faces))) - selected
    return selected


def extract_submesh(mesh: trimesh.Trimesh, face_ids: set[int]) -> trimesh.Trimesh:
    if not face_ids:
        raise ValueError("Selected region is empty; cannot export.")
    return mesh.submesh([sorted(face_ids)], append=True, repair=True)

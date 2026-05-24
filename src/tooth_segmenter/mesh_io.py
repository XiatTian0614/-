from __future__ import annotations

from pathlib import Path

import trimesh

from .models import MeshStats


def load_mesh(path: str | Path) -> trimesh.Trimesh:
    mesh = trimesh.load_mesh(path, process=False)
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("Only single triangle mesh is supported.")
    return mesh


def mesh_stats(mesh: trimesh.Trimesh) -> MeshStats:
    bounds = mesh.bounds
    return MeshStats(
        vertex_count=len(mesh.vertices),
        face_count=len(mesh.faces),
        has_vertex_normals=mesh.vertex_normals is not None,
        bbox_min=bounds[0],
        bbox_max=bounds[1],
    )


def save_mesh(mesh: trimesh.Trimesh, path: str | Path) -> None:
    path = Path(path)
    mesh.export(path)

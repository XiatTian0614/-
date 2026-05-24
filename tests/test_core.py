from __future__ import annotations

import tempfile

import trimesh

from tooth_segmenter.boundary_builder import build_closed_boundary
from tooth_segmenter.graph_geodesic import build_vertex_graph, dijkstra_path
from tooth_segmenter.mesh_io import load_mesh, save_mesh
from tooth_segmenter.mesh_segmenter import extract_submesh, segment_faces


def square_mesh() -> trimesh.Trimesh:
    vertices = [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0.5, 0.5, 0],
    ]
    faces = [
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
    ]
    return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)


def test_adjacency_graph_nonempty() -> None:
    g = build_vertex_graph(square_mesh())
    assert 0 in g and len(g[0]) >= 2


def test_dijkstra_connects_vertices() -> None:
    g = build_vertex_graph(square_mesh())
    p = dijkstra_path(g, 0, 2)
    assert p[0] == 0 and p[-1] == 2


def test_boundary_loop_closed() -> None:
    g = build_vertex_graph(square_mesh())
    loop = build_closed_boundary(g, [0, 1, 2, 3])
    assert loop[0] == loop[-1]


def test_region_growing_respects_boundary() -> None:
    mesh = square_mesh()
    boundary = [0, 1, 2, 3, 0]
    selected = segment_faces(mesh, boundary, seed_face=0)
    assert len(selected) >= 1


def test_extracted_mesh_indices_valid() -> None:
    mesh = square_mesh()
    sub = extract_submesh(mesh, {0, 1})
    assert sub.faces.max() < len(sub.vertices)


def test_export_reload_formats() -> None:
    mesh = square_mesh()
    with tempfile.TemporaryDirectory() as td:
        for ext in ["stl", "obj", "ply"]:
            p = f"{td}/out.{ext}"
            save_mesh(mesh, p)
            re = load_mesh(p)
            assert len(re.faces) > 0

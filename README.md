# Tooth Segmenter MVP

MVP implementation for interactive tooth mesh segmentation inspired by MeshInspector Segment Mesh Tool.

## Features
- Load STL / OBJ / PLY mesh files
- Landmark JSON ingestion and control-point validation
- Mesh vertex adjacency graph construction
- Dijkstra shortest paths for closed boundary generation
- Flood-fill based face segmentation with boundary barriers
- Segment extraction and STL export service
- CLI demo pipeline
- Unit tests for core topology, boundary, segmentation, and I/O checks

## Landmarks JSON

```json
{
  "points": [
    {"x": 0.0, "y": 0.0, "z": 0.0},
    {"x": 1.0, "y": 0.0, "z": 0.0},
    {"x": 1.0, "y": 1.0, "z": 0.0},
    {"x": 0.0, "y": 1.0, "z": 0.0}
  ],
  "seed": {"x": 0.5, "y": 0.5, "z": 0.0}
}
```

## CLI Demo

```bash
python -m tooth_segmenter.main input_mesh.stl landmarks.json --out outputs
# or
python -m tooth_segmenter.cli_demo input_mesh.stl landmarks.json --out outputs
```

## Modules
- `mesh_io`
- `landmark_manager`
- `graph_geodesic`
- `boundary_builder`
- `mesh_segmenter`
- `export_service`
- `cli_demo`

## TODO
- Interactive viewer module with point picking (PyVista/Open3D)
- True geodesic computation beyond graph shortest path
- Curvature-aware snapping
- Undo/redo and brush selection
- AI-assisted initial boundary proposals

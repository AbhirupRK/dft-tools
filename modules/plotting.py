import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def DrawArrow(ax, start, direction, head_size=0.3, shaft_thickness=0.05, head_thickness=0.1, color='r'):
    """
    Draw a 3D arrow with adjustable shaft and arrowhead thickness.
    
    Parameters:
        ax : matplotlib 3D axis
        start : (x, y, z) starting point
        direction : (dx, dy, dz) arrow direction vector
        head_size : length of the arrowhead (absolute size)
        shaft_thickness : thickness of the arrow shaft (absolute size)
        head_thickness : thickness of the arrowhead base (absolute size)
        color : arrow color
    """
    direction = np.array(direction, dtype=float)
    length = np.linalg.norm(direction)
    if length == 0:
        return
    
    direction = direction / length
    
    # Shaft Start and End
    head_base = start + direction * (length - head_size)

    # Generate two perpendicular vectors for the shaft and head base
    perp1 = np.cross(direction, np.array([1, 0, 0]))
    if np.linalg.norm(perp1) == 0:
        perp1 = np.cross(direction, np.array([0, 1, 0]))
    perp1 = perp1 / np.linalg.norm(perp1)

    perp2 = np.cross(direction, perp1)
    perp2 = perp2 / np.linalg.norm(perp2)

    # Scale perpendicular vectors
    perp1_shaft = perp1 * shaft_thickness
    perp2_shaft = perp2 * shaft_thickness
    perp1_head = perp1 * head_thickness
    perp2_head = perp2 * head_thickness

    # Shaft Vertices (Square Tube)
    shaft_vertices = np.array([
        start + perp1_shaft, start - perp1_shaft, start + perp2_shaft, start - perp2_shaft,
        head_base + perp1_shaft, head_base - perp1_shaft, head_base + perp2_shaft, head_base - perp2_shaft
    ])
    
    # Shaft Faces
    shaft_faces = [
        [shaft_vertices[0], shaft_vertices[1], shaft_vertices[5], shaft_vertices[4]],
        [shaft_vertices[2], shaft_vertices[3], shaft_vertices[7], shaft_vertices[6]],
        [shaft_vertices[0], shaft_vertices[2], shaft_vertices[6], shaft_vertices[4]],
        [shaft_vertices[1], shaft_vertices[3], shaft_vertices[7], shaft_vertices[5]],
    ]

    ax.add_collection3d(Poly3DCollection(shaft_faces, color=color, alpha=1))

    # Arrowhead Tip
    tip = start + direction * length
    
    # Arrowhead Vertices
    head_vertices = [
        tip,
        head_base + perp1_head, head_base - perp1_head,
        head_base + perp2_head, head_base - perp2_head
    ]
    
    # Arrowhead Faces (Pyramid)
    arrow_head_faces = [
        [tip, head_vertices[1], head_vertices[3]],
        [tip, head_vertices[1], head_vertices[4]],
        [tip, head_vertices[2], head_vertices[3]],
        [tip, head_vertices[2], head_vertices[4]],
        [head_vertices[1], head_vertices[2], head_vertices[4], head_vertices[3]]
    ]

    ax.add_collection3d(Poly3DCollection(arrow_head_faces, color=color, alpha=1))
import numpy as np
import math


class Sphere:
    """
    A class to generate the geometry of a 3D sphere including vertex positions,
    texture coordinates, and indices for rendering using triangle and line primitives.

    Attributes:
        r (float): Radius of the sphere.
        sectors (int): Number of longitudinal slices (vertical divisions).
        stacks (int): Number of latitudinal slices (horizontal divisions).
    """

    def __init__(self, r, sectors=36, stacks=18):
        """
        Initialize the sphere with given radius and resolution.

        Args:
            r (float): Radius of the sphere.
            sectors (int): Number of vertical subdivisions (default: 36).
            stacks (int): Number of horizontal subdivisions (default: 18).
        """
        self.r = r
        self.sectors = sectors
        self.stacks = stacks

    def build_sphere_points(self):
        """
        Generate vertex positions, texture coordinates, and normals for the sphere.

        Returns:
            tuple:
                - xy_coords (list of float): Flattened list of 3D vertex positions [x, y, z].
                - tex_coords (list of float): Flattened list of 2D texture coordinates [u, v].
                - normals (list of float): Flattened list of normal vectors [nx, ny, nz].
        """
        xy_coords, tex_coords, normals = [], [], []

        theta_step = 2 * np.pi / self.sectors
        phi_step = np.pi / self.stacks

        for i in range(self.stacks + 1):
            phi = np.pi / 2 - i * phi_step
            xy = self.r * math.cos(phi)
            z = self.r * math.sin(phi)

            for j in range(self.sectors + 1):
                theta = j * theta_step
                x = xy * math.cos(theta)
                y = xy * math.sin(theta)

                # Position
                xy_coords.extend([x, y, z])
                # Texture Coord
                tex_coords.extend([j / self.sectors, i / self.stacks])
                # Normal (normalized position for sphere)
                length = math.sqrt(x * x + y * y + z * z)
                nx, ny, nz = x / length, y / length, z / length
                normals.extend([nx, ny, nz])

        return xy_coords, tex_coords, normals


    def combine_coordinates(self, xy_coords, tex_coords, normals):
        """
        Combine vertex positions, normals, and texture coordinates into a single buffer.

        Args:
            xy_coords (list of float): Flattened list of 3D vertex positions.
            tex_coords (list of float): Flattened list of 2D texture coordinates.
            normals (list of float): Flattened list of 3D normals.

        Returns:
            np.ndarray: Flattened array of combined vertex attributes [x, y, z, nx, ny, nz, u, v].
        """
        xy_coords = np.asarray(xy_coords, dtype=np.float32).reshape(-1, 3)
        tex_coords = np.asarray(tex_coords, dtype=np.float32).reshape(-1, 2)
        normals = np.asarray(normals, dtype=np.float32).reshape(-1, 3)
        vertex_data = (
            np.column_stack((xy_coords, normals, tex_coords)).flatten().astype(np.float32)
        )
        return vertex_data


    def build_indices(self):
        """
        Build index buffers for rendering the sphere using triangles and lines.

        Returns:
            tuple:
                - indices (list of int): Indices for rendering triangles.
                - lineIndices (list of int): Indices for rendering wireframe lines.
        """
        k1, k2 = 0, 0
        indices, lineIndices = [], []

        for i in range(self.stacks):
            k1 = i * (self.sectors + 1)
            k2 = k1 + self.sectors + 1

            for _ in range(self.sectors):
                if i != 0:
                    indices.append(k1)
                    indices.append(k2)
                    indices.append(k1 + 1)

                if i != (self.stacks - 1):
                    indices.append(k1 + 1)
                    indices.append(k2)
                    indices.append(k2 + 1)

                lineIndices.append(k1)
                lineIndices.append(k2)

                if i != 0:
                    lineIndices.append(k1)
                    lineIndices.append(k1 + 1)

                k1 += 1
                k2 += 1

        return indices, lineIndices

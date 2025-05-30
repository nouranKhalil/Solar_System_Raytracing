import numpy as np
import math
from PIL import Image
from OpenGL.GL import *
import pyrr
from objects.sphere import Sphere


class Planet:
    """
    A class to represent a textured, rotating 3D planet using OpenGL.

    Attributes:
        radius (float): Radius of the sphere representing the planet.
        texture_path (str): Path to the texture image.
        sectors (int): Number of longitudinal slices of the sphere.
        stacks (int): Number of latitudinal slices of the sphere.
        rotation_speed (float): Rotation speed around the Y-axis.
        vao, vbo, ebo: OpenGL buffer identifiers.
    """

    def __init__(
        self,
        r,
        texture_path,
        sectors=36,
        stacks=18,
        orbit_radius=0.0,
        orbit_speed=0.0,
        rotation_speed=0.5,
        parent=None,
    ):
        """
        Initialize the planet with geometry and texture.

        Args:
            r (float): Radius of the planet.
            texture_path (str): File path to the texture image.
            sectors (int): Number of vertical subdivisions (default: 36).
            stacks (int): Number of horizontal subdivisions (default: 18).
            rotation_speed (float): Rotation speed around Y-axis (default: 0.5).
        """
        self.radius = r
        self.texture_path = texture_path
        self.sectors = sectors
        self.stacks = stacks
        self.rotation_speed = rotation_speed
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.parent = parent

        # Generate sphere geometry
        self.sphere = Sphere(r=self.radius, sectors=self.sectors, stacks=self.stacks)
        self.vertices, self.tex_coords = self.sphere.build_sphere_points()
        self.indices, self.line_indices = self.sphere.build_indices()

        # Prepare OpenGL buffers and load texture
        self._prepare_buffers()
        self._load_texture()

    def _load_texture(self):
        """
        Load and configure a 2D texture in OpenGL using the image at self.texture_path.
        """
        image = Image.open(self.texture_path)
        img_data = np.array(image.convert("RGBA")).tobytes()

        # Generate and bind a texture object
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        # Upload image data to the GPU
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            image.width,
            image.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            img_data,
        )

        # Set texture filtering and wrapping
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    def draw(self, model_loc, model_matrix, time_elapsed, rotation_speed):
        """
        Render the planet by applying rotation and drawing using OpenGL.

        Args:
            model_loc (int): Location of the 'model' uniform in the shader program.
            model_matrix (np.ndarray): Initial model transformation matrix (4x4).
            time_elapsed (float): Time passed (used to animate rotation).
        """

        # Create rotation around X and Y axes (same as before)
        rot_x = pyrr.Matrix44.from_x_rotation(1.5)
        rot_y = pyrr.Matrix44.from_y_rotation(rotation_speed * time_elapsed)
        rotation_matrix = pyrr.matrix44.multiply(rot_x, rot_y)
        model_matrix = pyrr.matrix44.multiply(rotation_matrix, model_matrix)

        # Send model matrix to shader
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model_matrix)

        # --- Bind the planet's texture and set the sampler uniform ---
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        # Get the currently active shader program
        program = glGetIntegerv(GL_CURRENT_PROGRAM)
        tex_loc = glGetUniformLocation(program, "samplerTex")  # Use your sampler name
        if tex_loc != -1:
            glUniform1i(tex_loc, 0)  # Texture unit 0

        # Bind VAO and draw the elements
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

        # Unbind to avoid side effects
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def _prepare_buffers(self):
        """
        Set up OpenGL buffers: VAO, VBO, and EBO for the planet geometry.
        """
        # Generate and bind Vertex Array Object
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Combine position and texture coordinates into one vertex array
        vertex_data = self.sphere.combine_coordinates(self.vertices, self.tex_coords)

        # Generate and bind Vertex Buffer Object
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

        # Define position attribute (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Define texture coordinate attribute (location = 1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)

        # Generate and bind Element Buffer Object (for indexed drawing)
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            np.array(self.indices, dtype=np.uint32),
            GL_STATIC_DRAW,
        )

    def draw_atmosphere(
        self, model_loc, model_matrix, color=(0.4, 0.6, 1.0), alpha=0.25
    ):
        """
        Draw a semi-transparent, slightly larger sphere to simulate atmosphere.
        Args:
            model_loc (int): Location of the 'model' uniform in the shader program.
            model_matrix (np.ndarray): Model transformation matrix (4x4).
            color (tuple): RGB color of the atmosphere.
            alpha (float): Alpha transparency.
        """
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Scale up the model matrix for the atmosphere shell
        scale = pyrr.matrix44.create_from_scale([1.25, 1.25, 1.25])
        atmosphere_matrix = pyrr.matrix44.multiply(
            scale, model_matrix
        )  # <-- scale first, then translate/rotate
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, atmosphere_matrix)
        # Use solid color (set in main loop)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        glDisable(GL_BLEND)

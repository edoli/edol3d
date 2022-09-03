import numpy as np
from gl.camera_utils import look_at

from gl.mesh import Mesh
from gl.vector import vec3

class View():
    def __init__(self, width=640, height=480):
        self.view_matrix = look_at(vec3(0, 0, -3), vec3(0, 0, 0), vec3(0, -1, 0))
        self.model_matrix = np.eye(4)
        self.width = width
        self.height = height

        self.num_column = 1

        self.mesh: Mesh = None
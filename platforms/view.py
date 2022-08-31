import numpy as np

from gl.mesh import Mesh

class View():
    def __init__(self):
        self.project_matrix = np.eye(4)
        self.view_matrix = np.eye(4)
        self.model_matrix = np.eye(4)
        self.width = 0
        self.height = 0

        self.num_column = 1

        self.mesh: Mesh = None
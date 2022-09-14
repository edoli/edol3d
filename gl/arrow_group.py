from matplotlib.pyplot import axis
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import ShaderProgram

class ArrowGroup():

    def __init__(self, position: np.ndarray, direction: np.ndarray):

        assert position.dtype == np.float32
        assert direction.dtype == np.float32
        assert position.shape == direction.shape

        vertices = np.concatenate([
            position, position + direction
        ], axis=1).reshape([-1, 3])

        self.vertex_count = vertices.shape[0]

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.dtype.itemsize * 3, ctypes.c_void_p(0))
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


    def __del__(self):
        glDeleteVertexArrays(1, self.vao)
        glDeleteBuffers(1, self.vbo)

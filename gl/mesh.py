import numpy as np
from scipy.spatial.transform import Rotation as R
from typing import List
from OpenGL.GL import *
from OpenGL.GL.shaders import ShaderProgram


class Texture():
    def __init__(self, texture, texture_type):
        self.texture = texture
        self.texture_type = texture_type


class MeshData():
    def __init__(self, vertices: np.ndarray, faces: np.ndarray, extra=None):
        self.vertices = vertices
        self.faces = faces
        self.extra = extra

class Mesh():
    def __init__(self, data: MeshData, shader: ShaderProgram, textures: List[Texture] = []):
        self.data = data
        vertices = data.vertices
        faces = data.faces
        extra = data.extra

        self.vertices = vertices
        self.faces = faces
        self.textures = textures

        self.is_visible = True

        if vertices.dtype != np.float32:
            raise Error('vertices should be float32 type ndarray')
            
        
        if faces.dtype == np.uint8:
            self.face_type = GL_UNSIGNED_BYTE
        elif faces.dtype == np.uint16:
            self.face_type = GL_UNSIGNED_SHORT
        elif faces.dtype == np.uint32:
            self.face_type = GL_UNSIGNED_INT
        else:
            raise Error('faces should be uint8 or uint16 or uint32 type ndarray')

        self.faces_size = faces.size
        self.shader = shader

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.dtype.itemsize * 3, ctypes.c_void_p(0))

        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)

        if extra is not None:
            for key in extra:
                self.bind_data(key, extra[key])

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def bind_data(self, name, data):    
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

        gl_location = glGetAttribLocation(self.shader, name)

        if gl_location != -1:
            if data.dtype != np.float32:
                raise Error('data should be float32 type ndarray')

            if len(data.shape) == 1:
                data_size = 1
            else:
                data_size = data.shape[1]

            glEnableVertexAttribArray(gl_location)
            glVertexAttribPointer(gl_location, data_size, GL_FLOAT, GL_FALSE,
                                data.dtype.itemsize * data_size, ctypes.c_void_p(0))
        else:
            print('GL attrib not exists: ', name)
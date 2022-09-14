import numpy as np
from scipy.spatial.transform import Rotation as R
from typing import List
from OpenGL.GL import *
from OpenGL.GL.shaders import ShaderProgram


class Texture():
    def __init__(self, texture, target):
        self.texture = texture
        self.target = target


class MeshData():
    def __init__(self, vertices: np.ndarray, faces: np.ndarray, vertex_attribs=None, face_attribs=None):
        self.vertices = vertices
        self.faces = faces
        self.vertex_attribs = vertex_attribs
        self.face_attribs = face_attribs

class Mesh():
    def __init__(self, data: MeshData, textures: List[Texture] = []):
        self.data = data
        vertices = data.vertices
        faces = data.faces

        self.vertices = vertices
        self.faces = faces
        self.textures = textures

        self.vertices -= vertices.mean(axis=0, keepdims=True)

        self.center = vertices.mean(axis=0)
        self.bbox = np.stack([vertices.min(axis=0), vertices.max(axis=0)])
        self.is_visible = True
        self.binded_buffer = {}

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

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.dtype.itemsize * 3, ctypes.c_void_p(0))

        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)

        vertex_attribs = self.data.vertex_attribs

        if vertex_attribs is not None:
            for key in vertex_attribs:
                self.bind_data(key, vertex_attribs[key])

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def bind_data(self, name, data):    
        if data.dtype != np.float32:
            raise Error('data should be float32 type ndarray')

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

        self.binded_buffer[name] = vbo

    def bind_shader(self, shader):
        glBindVertexArray(self.vao)
        vertex_attribs = self.data.vertex_attribs

        if vertex_attribs is not None:
            for name in vertex_attribs:
                gl_location = glGetAttribLocation(shader, name)

                if gl_location != -1:
                    data = vertex_attribs[name]
                    glBindBuffer(GL_ARRAY_BUFFER, self.binded_buffer[name])

                    if len(data.shape) == 1:
                        data_size = 1
                    else:
                        data_size = data.shape[1]

                    glEnableVertexAttribArray(gl_location)
                    glVertexAttribPointer(gl_location, data_size, GL_FLOAT, GL_FALSE,
                                        data.dtype.itemsize * data_size, ctypes.c_void_p(0))
                else:
                    print('GL attrib not exists: ', name)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def has_attrib(self, name):
        vertex_attribs = self.data.vertex_attribs
        return vertex_attribs is not None and name is not None and name in vertex_attribs

    def bind_shader(self, shader, name):
        glBindVertexArray(self.vao)
        vertex_attribs = self.data.vertex_attribs

        if self.has_attrib(name):
            gl_location = glGetAttribLocation(shader, 'value')

            if gl_location != -1:
                data = vertex_attribs[name]
                glBindBuffer(GL_ARRAY_BUFFER, self.binded_buffer[name])

                if len(data.shape) == 1:
                    data_size = 1
                else:
                    data_size = data.shape[1]

                glEnableVertexAttribArray(gl_location)
                glVertexAttribPointer(gl_location, data_size, GL_FLOAT, GL_FALSE,
                                    data.dtype.itemsize * data_size, ctypes.c_void_p(0))
            else:
                print('GL attrib not exists: ', name)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

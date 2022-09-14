from enum import Enum
from typing import List
import numpy as np

from OpenGL.GL import *
from gl.arrow_group import ArrowGroup

from gl.mesh import Mesh

class DrawType(Enum):
    MESH = 0
    ARROW = 1

class RenderView:
    def __init__(self, shader):
        self.width = 0
        self.height = 0
        self.shader = shader
        self.image_callback = None
        self.attrib = None
        self.draw_type = DrawType.MESH

        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        self.generate_fbo_buffer()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def draw(self, meshes: List[Mesh]):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.shader)

        for mesh in meshes:
            if not mesh.is_visible and self.attrib is None:
                continue
            
            
            if self.draw_type == DrawType.MESH:
                mesh.bind_shader(self.shader, self.attrib)

                for i, texture in enumerate(mesh.textures):
                    if texture is not None:
                        glActiveTexture(GL_TEXTURE0 + i)
                        glBindTexture(texture.target, texture.texture)

                glBindVertexArray(mesh.vao)
                glDrawElements(GL_TRIANGLES, mesh.faces_size, mesh.face_type, None)

                glBindVertexArray(0)

            elif self.draw_type == DrawType.ARROW:
                glUniform3fv(glGetUniformLocation(self.shader, 'color'), 1, np.array([1.0, 1.0, 1.0]))

                vertex_attribs = mesh.data.vertex_attribs
                data = vertex_attribs[self.attrib]
                if not mesh.has_attrib(self.attrib) or data.shape[1] != 3:
                    continue
                
                if not hasattr(mesh, 'arrow_group'):
                    mesh.arrow_group = ArrowGroup(mesh.vertices[::1000, :], data[::1000, :] / 25)

                glBindVertexArray(mesh.arrow_group.vao)
                glDrawArrays(GL_LINES, 0, mesh.arrow_group.vertex_count)

                glBindVertexArray(0)

        if self.image_callback is not None:
            img_data = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_FLOAT)
            img_data = np.frombuffer(img_data, dtype=np.float32)
            img_data = np.reshape(img_data, (self.height, self.width, 3))[::-1, :, :]
            self.image_callback(img_data)

    def resize(self, width, height):
        if width == self.width and height == self.height:
            return

        self.width = width
        self.height = height

        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        self.generate_fbo_buffer()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def generate_fbo_buffer(self):
        if self.width == 0 or self.height == 0:
            return

        self.fbo_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.fbo_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, self.width, self.height, 0, GL_RGB, GL_FLOAT, None)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  
        
        self.fbo_depth = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.fbo_depth)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, self.width, self.height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.fbo_texture, 0)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.fbo_depth, 0)
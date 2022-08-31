from typing import List
import numpy as np

from OpenGL.GL import *

from gl.mesh import Mesh

class RenderView:
    def __init__(self, width, height, shader):
        self.width = width
        self.height = height
        self.shader = shader
        self.image_callback = None

        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        self.rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.rbo)
        
        self.fbo_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.fbo_texture)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, width, height, 0, GL_RGB, GL_FLOAT, None)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.fbo_texture, 0)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def draw(self, meshes: List[Mesh]):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.shader)

        for mesh in meshes:
            if not mesh.is_visible:
                continue
            
            mesh.bind_shader_rgb(self.shader, 'rho')

            for i, texture in enumerate(mesh.textures):
                if texture is not None:
                    glActiveTexture(GL_TEXTURE0 + i)
                    glBindTexture(texture.target, texture.texture)

            glBindVertexArray(mesh.vao)
            glDrawElements(GL_TRIANGLES, mesh.faces_size, mesh.face_type, None)

            glBindVertexArray(0)

        if self.image_callback is not None:
            img_data = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_FLOAT)
            img_data = np.frombuffer(img_data, dtype=np.float32)
            img_data = np.reshape(img_data, (self.height, self.width, 3))[::-1, :, :]
            self.image_callback(img_data)

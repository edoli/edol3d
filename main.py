from turtle import width
from typing import List
import numpy as np
from OpenGL.GL import *
from gl.camera_utils import perspective_fov
from gl.utils import create_shader_program

from platforms.platform_glfw import PlatformGLFW
from render_view import RenderView

def main():
    init_width = 640
    init_height = 480

    platform = PlatformGLFW(init_width, init_height)

    render_views: List[RenderView] = []

    shader = create_shader_program('color.vs', 'color.fs')
    from loader import test_loader
    mesh = test_loader.prepare(shader, 'tmp/meshCurrent.mat')
    meshes = [mesh]

    project_matrix = perspective_fov(np.pi / 4, init_width / init_height, 0.01, 100)
    view_matrix = np.eye(4)
    model_matrix = np.eye(4)
    
    glUniformMatrix4fv(glGetUniformLocation(shader, 'u_project'), 1, GL_TRUE, project_matrix)
    glUniformMatrix4fv(glGetUniformLocation(shader, 'u_view'), 1, GL_TRUE, view_matrix)
    # glUniformMatrix4fv(glGetUniformLocation(shader, 'u_model'), 1, GL_TRUE, model_matrix)

    render_view = RenderView(init_width, init_height, shader)
    render_views.append(render_view)

    while True:
        platform.loop_prepare()

        glEnable(GL_MULTISAMPLE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glViewport(0, 0, platform.width, platform.height)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for i, render_view in enumerate(render_views):
            render_view.draw(meshes)
            glBindFramebuffer(GL_READ_FRAMEBUFFER, render_view.fbo)
            glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
            glBlitFramebuffer(0, 0, render_view.width, render_view.height, \
                0, 0, render_view.width, render_view.height, GL_COLOR_BUFFER_BIT, GL_NEAREST)


        platform.loop_finish()

        if platform.should_close():
            platform.close()
            break

if __name__ == '__main__':
    main()
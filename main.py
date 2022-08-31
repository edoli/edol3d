from turtle import width
from typing import List
import numpy as np
from OpenGL.GL import *
from gl.camera_utils import look_at, perspective_fov
from gl.utils import create_shader_program
from gl.vector import vec3

from platforms.platform_glfw import PlatformGLFW
from platforms.view import View
from render_view.render_view import RenderView

def main():
    init_width = 640
    init_height = 480

    view = View()
    view.project_matrix = perspective_fov(np.pi / 4, init_width / init_height, 0.01, 100)
    view.view_matrix = look_at(vec3(0, 0, -3), vec3(0, 0, 0), vec3(0, -1, 0))
    view.model_matrix = np.eye(4)
    view.width = init_width
    view.height = init_height

    platform = PlatformGLFW(view)

    render_views: List[RenderView] = []

    shader = create_shader_program('color.vs', 'color.fs')
    from loader import test_loader
    mesh = test_loader.prepare(shader, 'tmp/meshCurrent.mat')
    meshes = [mesh]

    render_view = RenderView(init_width, init_height, shader)
    render_views.append(render_view)

    while True:
        platform.loop_prepare()

        glEnable(GL_MULTISAMPLE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glViewport(0, 0, view.width, view.height)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for i, render_view in enumerate(render_views):
            glUniformMatrix4fv(glGetUniformLocation(render_view.shader, 'u_project'), 1, GL_TRUE, view.project_matrix)
            glUniformMatrix4fv(glGetUniformLocation(render_view.shader, 'u_view'), 1, GL_TRUE, view.view_matrix)
            glUniformMatrix4fv(glGetUniformLocation(render_view.shader, 'u_model'), 1, GL_TRUE, view.model_matrix)

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
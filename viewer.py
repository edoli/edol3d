
from gl.camera_utils import perspective_fov
from platforms.platform import Platform

import numpy as np
import time
from OpenGL.GL import *


def show_viewer(platform: Platform):
    
    view = platform.view
    render_views = platform.render_views

    while True:
        platform.loop_prepare()

        if view.width == 0 or view.height == 0:
            time.sleep(0.01)
            continue

        glEnable(GL_MULTISAMPLE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glViewport(0, 0, view.width, view.height)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        num_column = view.num_column
        num_row = 1 + (len(render_views) - 1) // view.num_column

        cell_width = view.width // num_column
        cell_height = view.height // num_row

        project_matrix = perspective_fov(np.pi / 4, cell_width / cell_height, 0.01, 100)
        mvp_matrix = project_matrix @ view.view_matrix @ view.model_matrix
        mvp_normal_matrix = view.view_matrix[:3, :3] @ np.linalg.inv(view.model_matrix).T[:3, :3]

        for i, render_view in enumerate(render_views):
            col = i % num_column
            row = i // num_column

            shader = render_view.shader

            glUseProgram(shader)

            glUniformMatrix4fv(glGetUniformLocation(shader, 'u_project'), 1, GL_TRUE, project_matrix)
            glUniformMatrix4fv(glGetUniformLocation(shader, 'u_view'), 1, GL_TRUE, view.view_matrix)
            glUniformMatrix4fv(glGetUniformLocation(shader, 'u_model'), 1, GL_TRUE, view.model_matrix)
            glUniformMatrix4fv(glGetUniformLocation(shader, 'u_mvp'), 1, GL_TRUE, mvp_matrix)
            glUniformMatrix3fv(glGetUniformLocation(shader, 'u_mvp_normal'), 1, GL_TRUE, mvp_normal_matrix)

            render_view.resize(cell_width, cell_height)
            render_view.draw([view.mesh])

            dst_x = cell_width * col
            dst_y = cell_height * row
            glBindFramebuffer(GL_READ_FRAMEBUFFER, render_view.fbo)
            glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
            glBlitFramebuffer(0, 0, cell_width, cell_height, \
                dst_x, dst_y, dst_x + cell_width, dst_y + cell_height, GL_COLOR_BUFFER_BIT, GL_NEAREST)


        platform.loop_finish()

        if platform.should_close():
            platform.close()
            break
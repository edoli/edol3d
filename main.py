from turtle import width
from typing import List
import time
import numpy as np
from OpenGL.GL import *
from gl.camera_utils import look_at, perspective_fov
from shaders import create_shader_colormap_program, create_shader_program
from gl.vector import vec3

from platforms.platform_glfw import PlatformGLFW
from platforms.view import View
from render_view.render_view import RenderView
from util.observable_list import ObservableList


def main():
    init_width = 640
    init_height = 480
    
    view = View()
    view.view_matrix = look_at(vec3(0, 0, -3), vec3(0, 0, 0), vec3(0, -1, 0))
    view.model_matrix = np.eye(4)
    view.width = init_width
    view.height = init_height
    view.num_column = 3

    render_views: List[RenderView] = ObservableList()
    platform = PlatformGLFW(view, render_views)

    rgb_shader = create_shader_program('color.vs', 'color.fs')
    rgb_shader.name = 'color'
    normal_shader = create_shader_program('normal_view.vs', 'normal_view.fs')
    normal_shader.name = 'normal_view'
    viridis_shader = create_shader_colormap_program('viridis')
    viridis_shader.name = 'colormap_viridis'
    from loader import test_loader
    mesh = test_loader.prepare('tmp/meshCurrent.mat')
    view.mesh = mesh

    render_view1 = RenderView(init_width, init_height, rgb_shader)
    render_view1.attrib = 'rho'
    render_view2 = RenderView(init_width, init_height, normal_shader)
    render_view2.attrib = 'normal'
    render_view3 = RenderView(init_width, init_height, viridis_shader)
    render_view3.attrib = 'm1'
    render_view4 = RenderView(init_width, init_height, viridis_shader)
    render_view4.attrib = 'eta'
    render_view5 = RenderView(init_width, init_height, viridis_shader)
    render_view5.attrib = 'eta'
    render_view6 = RenderView(init_width, init_height, viridis_shader)
    render_view6.attrib = 'eta'
    render_views.append(render_view1)
    render_views.append(render_view2)
    render_views.append(render_view3)
    render_views.append(render_view4)
    render_views.append(render_view5)
    render_views.append(render_view6)

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

            glUseProgram(render_view.shader)

            glUniformMatrix4fv(glGetUniformLocation(render_view.shader, 'u_project'), 1, GL_TRUE, view.project_matrix)
            glUniformMatrix4fv(glGetUniformLocation(render_view.shader, 'u_view'), 1, GL_TRUE, view.view_matrix)
            glUniformMatrix4fv(glGetUniformLocation(render_view.shader, 'u_model'), 1, GL_TRUE, view.model_matrix)
            glUniformMatrix4fv(glGetUniformLocation(render_view.shader, 'u_mvp'), 1, GL_TRUE, mvp_matrix)
            glUniformMatrix3fv(glGetUniformLocation(render_view.shader, 'u_mvp_normal'), 1, GL_TRUE, mvp_normal_matrix)

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


if __name__ == '__main__':
    main()
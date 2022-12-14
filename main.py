from turtle import width
from typing import List
import time
import numpy as np
from gl.arrow_group import ArrowGroup
import shader_store
from OpenGL.GL import *
from gl.camera_utils import look_at, perspective_fov
from shader_store import create_shader_colormap_program, create_shader_program
from gl.vector import vec3

from platforms.platform_glfw import PlatformGLFW
from platforms.view import View
from render_view.render_view import RenderView
from util.observable_list import ObservableList
from viewer import show_viewer


def main():
    view = View()
    view.num_column = 3

    render_views: List[RenderView] = ObservableList()
    platform = PlatformGLFW(view, render_views)

    rgb_shader = shader_store.visualizer_shaders['color']
    normal_view_shader = shader_store.visualizer_shaders['normal_view']
    viridis_shader = shader_store.visualizer_shaders['colormap_viridis']

    shader_store.get_shader_uniforms(rgb_shader)

    from loader import test_loader
    mesh = test_loader.prepare('tmp/meshCurrent.mat')
    view.mesh = mesh

    render_view1 = RenderView(rgb_shader)
    render_view1.attrib = 'rho'
    render_view2 = RenderView(viridis_shader)
    render_view2.attrib = 'normal'
    render_view2.draw_arrow = True
    render_view3 = RenderView(viridis_shader)
    render_view3.attrib = 'm1'
    render_view4 = RenderView(viridis_shader)
    render_view4.attrib = 'eta'
    render_view5 = RenderView(viridis_shader)
    render_view5.attrib = 'eta'
    render_view6 = RenderView(viridis_shader)
    render_view6.attrib = 'eta'
    render_views.append(render_view1)
    render_views.append(render_view2)
    render_views.append(render_view3)
    render_views.append(render_view4)
    render_views.append(render_view5)
    render_views.append(render_view6)

    show_viewer(platform)


if __name__ == '__main__':
    main()
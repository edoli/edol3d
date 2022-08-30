import numpy as np
from OpenGL.GL import *
from typing import List

import os
from scipy import io as sio

from gl.mesh import Mesh, MeshData


def prepare(shader, path) -> Mesh:
    glUseProgram(shader)

    obj_mat = sio.loadmat(path)
    vertices = obj_mat['meshCurrent']['vertices'][0, 0]
    vertices = np.transpose(vertices)
    
    rho = obj_mat['meshCurrent']['rho'][0, 0]
    rho = np.float32(np.transpose(rho))

    normal = obj_mat['meshCurrent']['normals'][0, 0]
    normal = np.float32(np.transpose(normal))

    eta = obj_mat['meshCurrent']['eta'][0, 0]
    eta = np.float32(np.transpose(eta))

    m1 = obj_mat['meshCurrent']['m1'][0, 0]
    m1 = np.float32(np.transpose(m1))

    m2 = obj_mat['meshCurrent']['m2'][0, 0]
    m2 = np.float32(np.transpose(m2))

    ks1 = obj_mat['meshCurrent']['ks1'][0, 0]
    ks1 = np.float32(np.transpose(ks1))

    rho1 = obj_mat['meshCurrent']['ks2'][0, 0]
    rho1 = np.float32(np.transpose(rho1))

    faces = obj_mat['meshCurrent']['faces'][0, 0]
    faces = np.reshape(np.transpose(faces), -1)
    faces -= 1

    return Mesh(MeshData(vertices, faces, {
        'normal': normal,
        'rho': rho,
        'eta': eta,
        'm1': m1,
        'm2': m2,
        'ks1': ks1,
        'rho1': rho1,
    }))


def update(shader, controller, render_data, offset):
    glUseProgram(shader)

    lPos = controller.emitter_position
    vPos = controller.camera_position

    project_matrix = controller.project_matrix
    view_matrix = controller.view_matrix
    model_matrix = controller.model_matrix.copy()
    if offset is not None:
        model_matrix[:3, 3:4] += view_matrix[:3, :3] @ offset.reshape([3, 1])
        
    glUniform3fv(glGetUniformLocation(shader, 'y_l'), 1, np.array([0.0, -1.0, 0.0]))
    glUniform3fv(glGetUniformLocation(shader, 'y_v'), 1, np.array([0.0, -1.0, 0.0]))
    
    # glUniform4fv(glGetUniformLocation(shader, 'light_stokes'), 1, )
    if render_data.light_stokes is None:
        l_polar_efficiency = render_data.l_polar_efficiency
        light_stokes = polarizer_muller(render_data.l_polar_degree) @ np.array([1.0, 0.0, 0.0, 0.0]) * l_polar_efficiency + \
                    np.array([render_data.l_amplitude, 0.0, 0.0, 0.0]) * (1 - l_polar_efficiency)
    else:
        light_stokes = render_data.light_stokes * render_data.l_amplitude
    glUniform4fv(glGetUniformLocation(shader, 'light_stokes'), 1, light_stokes)

    # glUniform4fv(glGetUniformLocation(shader, 'view_stokes'), 1, polarizer_muller(render_data.v_polar_degree) @ np.array([1.0, 0.0, 0.0, 0.0]))
    if render_data.view_stokes is None:
        v_polar_efficiency = render_data.v_polar_efficiency
        view_stokes = polarizer_muller(render_data.v_polar_degree) @ np.array([1.0, 0.0, 0.0, 0.0]) * v_polar_efficiency + \
                    np.array([1.0, 0.0, 0.0, 0.0]) * (1 - v_polar_efficiency)
    else:
        view_stokes = render_data.view_stokes
    glUniform4fv(glGetUniformLocation(shader, 'view_stokes'), 1, view_stokes)

    glUniform3fv(glGetUniformLocation(shader, 'select_rendering'), 1, np.array([
        render_data.select_diffuse, 
        render_data.select_specular, 
        render_data.select_single_scattering
    ]))

    glUniform3fv(glGetUniformLocation(shader, 'lPos'), 1, lPos)
    glUniform3fv(glGetUniformLocation(shader, 'vPos'), 1, vPos)

    glUniform1i(glGetUniformLocation(shader, 'numSamplePerPI'), render_data.sampler_per_pi)
    glUniform1f(glGetUniformLocation(shader, 'gamma'), render_data.gamma)

    glUniformMatrix4fv(glGetUniformLocation(shader, 'u_project'), 1, GL_TRUE, project_matrix)
    glUniformMatrix4fv(glGetUniformLocation(shader, 'u_view'), 1, GL_TRUE, view_matrix)
    glUniformMatrix4fv(glGetUniformLocation(shader, 'u_model'), 1, GL_TRUE, model_matrix)


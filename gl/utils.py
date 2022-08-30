import numpy as np
import os
from OpenGL.GL import *


def read_file(file):
    f = open(file, 'r')
    content = f.read()
    f.close()
    return content


def create_shader_program(vshader_path, fshader_path):
    v_shader_code = read_file(os.path.join('shader', vshader_path))
    f_shader_code = read_file(os.path.join('shader', fshader_path))
    return OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(v_shader_code, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(f_shader_code, GL_FRAGMENT_SHADER))

def create_sphere(cx, cy, cz, r, resolution=360):
    phi = np.linspace(0, 2 * np.pi, 2 * resolution)
    theta = np.linspace(0, np.pi, resolution)

    theta, phi = np.meshgrid(theta, phi)

    r_xy = r * np.sin(theta)
    x = cx + np.cos(phi) * r_xy
    y = cy + np.sin(phi) * r_xy
    z = cz + r * np.cos(theta)

    return np.stack([x, y, z])

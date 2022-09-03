import os
from typing import List
from OpenGL.GL import *

shader_dict ={}

def init_shaders():

    for fn in os.listdir('shader'):
        if fn[-3:] == '.vs' and os.path.exists(os.path.join('shader', fn[:-3] + '.fs')):
            name = fn[:-3]
            if not name in shader_dict:
                shader = create_shader_program(f'{name}.vs', f'{name}.fs')
                shader.name = name
                shader.uniforms = get_shader_uniforms(shader)
                shader_dict[name] = shader

    for fn in os.listdir('shader/colormap'):
        if fn[-5:] == '.glsl':
            colormap_name = fn.split(os.sep)[-1][:-5]
            name = f'colormap_{colormap_name}'
            shader = create_shader_colormap_program(colormap_name)
            shader.name = name
            shader.uniforms = get_shader_uniforms(shader)
            shader_dict[name] = shader

    return shader_dict
            

def get_default_shader():
    return shader_dict['color']


class Uniform():
    def __init__(self, name, gl_type):
        self.name = name
        self.gl_type = gl_type


def get_shader_uniforms(shader) -> List[Uniform]:

    count = glGetProgramiv(shader, GL_ACTIVE_UNIFORMS)
    uniforms: List[Uniform] = []

    for i in range(count):
        bufsize = 64
        buf = (GLchar * bufsize)()
        namesize = GLsizei()
        size = GLint()
        kind = GLenum()

        glGetActiveUniform(shader, i, bufsize, namesize, size, kind, buf)
        name = buf.value.decode('utf-8')
        uniforms.append(Uniform(name, kind.value))
        
    return uniforms


def read_file(file):
    f = open(file, 'r')
    content = f.read()
    f.close()
    return content


def create_shader_program(v_shader_path, f_shader_path):
    v_shader_code = read_file(os.path.join('shader', v_shader_path))
    f_shader_code = read_file(os.path.join('shader', f_shader_path))
    return OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(v_shader_code, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(f_shader_code, GL_FRAGMENT_SHADER))


def create_shader_colormap_program(name):
    v_shader_colormap = read_file(os.path.join('shader', 'colormap', f'{name}.glsl'))


    v_shader_code = f'''
#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in float value;

uniform mat4 u_mvp;

out vec4 vColor;




mat3 rgb2xyz_mat = mat3(
0.4124564, 0.3575761, 0.1804375,
0.2126729, 0.7151522, 0.0721750,
0.0193339, 0.1191920, 0.9503041
);

mat3 xyz2rgb_mat = mat3(
3.2404542, -1.5371385, -0.4985314,
-0.9692660, 1.8760108, 0.0415560,
0.0556434, -0.2040259, 1.0572252
);

// d65 white reference
float xn = 0.95047;
float yn = 1.0;
float zn = 1.08883;

vec3 gamma_f(vec3 rgb) {{
    return vec3(
    pow(rgb.r, 1.0 / 2.2),
    pow(rgb.g, 1.0 / 2.2),
    pow(rgb.b, 1.0 / 2.2)
    );
}}

vec3 inv_gamma_f(vec3 rgb) {{
    return vec3(
    pow(rgb.r, 2.2),
    pow(rgb.g, 2.2),
    pow(rgb.b, 2.2)
    );
}}

float f(float c) {{
    return c > 0.008856 ? pow(c, 1.0 / 3.0) : (903.3 * c + 16.0) / 116.0;
}}

vec3 xyz2lab(vec3 xyz){{
    float fx = f(xyz.x / xn);
    float fy = f(xyz.y / yn);
    float fz = f(xyz.z / zn);
    return vec3(
    116.0 * fx - 16.0,
    500.0 * (fx - fy),
    200.0 * (fy - fz)
    );
}}

float f_inv(float c) {{
    float t = pow(c, 3);
    return t > 0.008856 ? t : (116.0 * c - 16.0) / 903.3;
}}

vec3 lab2xyz(vec3 lab) {{
    float L = lab.x;
    float a = lab.y;
    float b = lab.z;

    float fy = (L + 16.0) / 116.0;
    float fz = fy - b / 200.0;
    float fx = a / 500.0 + fy;

    return vec3(f_inv(fx) * xn, f_inv(fy) * yn, f_inv(fz) * zn);
}}

vec3 rgb2xyz(vec3 rgb) {{
    return inv_gamma_f(rgb) * rgb2xyz_mat;
}}

vec3 xyz2rgb(vec3 xyz) {{
    return gamma_f(xyz * xyz2rgb_mat);
}}

vec3 lab2rgb(vec3 lab) {{
    return xyz2rgb(lab2xyz(lab));
}}

vec3 rgb2lab(vec3 rgb) {{
    return xyz2lab(rgb2xyz(rgb));
}}

{v_shader_colormap}

void main()
{{
    gl_Position = u_mvp * vec4(position, 1.0);
	vColor = vec4({name}_colormap(value), 1.0);
}}
    '''
    f_shader_code = read_file(os.path.join('shader', 'color.fs'))
    return OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(v_shader_code, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(f_shader_code, GL_FRAGMENT_SHADER))
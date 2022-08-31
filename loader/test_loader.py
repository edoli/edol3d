import numpy as np
from OpenGL.GL import *
from typing import List

from scipy import io as sio

from gl.mesh import Mesh, MeshData


def prepare(path) -> Mesh:
    obj_mat = sio.loadmat(path)
    vertices = obj_mat['meshCurrent']['vertices'][0, 0]
    vertices = np.transpose(vertices)
    
    rho = obj_mat['meshCurrent']['rho'][0, 0]
    rho = np.float32(np.transpose(rho)) / 16

    normal = obj_mat['meshCurrent']['normals'][0, 0]
    normal = np.float32(np.transpose(normal))

    eta = obj_mat['meshCurrent']['eta'][0, 0]
    eta = np.float32(np.transpose(eta))
    eta = (eta - eta.min()) / (eta.max() - eta.min())

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

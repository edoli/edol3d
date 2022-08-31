import numpy as np

class Vector3(np.ndarray):
    @property
    def r(self):
        return self[0]

    @property
    def g(self):
        return self[1]

    @property
    def b(self):
        return self[2]

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]
        
    @property
    def z(self):
        return self[2]


class Vector4(Vector3):
        
    @property
    def a(self):
        return self[3]

    @property
    def w(self):
        return self[3]

def vec3(vec: np.ndarray) -> Vector3:
    return vec.view(Vector3)

def vec3(v: float) -> Vector3:
    return np.array([v, v, v], np.float32).view(Vector3)

def vec3(v1: float, v2: float, v3: float) -> Vector3:
    return np.array([v1, v2, v3], np.float32).view(Vector3)
    
def vec4(vec: np.ndarray) -> Vector4:
    return vec.view(Vector4)

def vec4(vec: Vector3, v: float) -> Vector4:
    return np.array([vec[0], vec[1], vec[2], v], np.float32).view(Vector4)

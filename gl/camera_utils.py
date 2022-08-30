import numpy as np


def perspective_fov(fov, aspect_ratio, near_plane, far_plane):
    num = 1.0 / np.tan(fov / 2.0)
    num9 = num / aspect_ratio
    return np.array([
        [num9, 0.0, 0.0, 0.0],
        [0.0, num, 0.0, 0.0],
        [0.0, 0.0, far_plane / (near_plane - far_plane), (near_plane * far_plane) / (near_plane - far_plane)],
        [0.0, 0.0, -1.0, 0.0]
    ], dtype=np.float32)

def look_at(camera_position, camera_target, up_vector):
    up_vector = up_vector / np.linalg.norm(up_vector)

    vector = camera_position - camera_target
    vector = vector / np.linalg.norm(vector)

    vector2 = np.cross(up_vector, vector)
    vector2 = vector2 / np.linalg.norm(vector2)

    vector3 = np.cross(vector, vector2)
    return np.array([
        [vector2[0], vector2[1], vector2[2], -np.dot(vector2, camera_position)],
        [vector3[0], vector3[1], vector3[2], -np.dot(vector3, camera_position)],
        [vector[0], vector[1], vector[2], -np.dot(vector, camera_position)],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)
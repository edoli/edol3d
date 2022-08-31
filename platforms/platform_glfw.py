import glfw
import numpy as np
from scipy.spatial.transform import Rotation as R
from OpenGL.GL import *

from platforms.platform import Platform

class PlatformGLFW(Platform):
    def init(self):
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.rotation_speed = 3

        if not glfw.init():
            return
                
        glfw.window_hint(glfw.SAMPLES, 4)
        self.window = glfw.create_window(self.view.width, self.view.height, "Render", None, None)
        
        if not self.window:
            glfw.terminate()
            return
        
        glfw.make_context_current(self.window)
        glfw.set_window_size_callback(self.window, self.window_size_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_pos_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)

    def loop_prepare(self):
        glfw.poll_events()

    def loop_finish(self):
        glfw.swap_buffers(self.window)
    
    def should_close(self):
        return glfw.window_should_close(self.window)

    def close(self):
        glfw.terminate()

    def window_size_callback(self, window, width, height):
        self.view.width = width
        self.view.height = height

    def cursor_pos_callback(self, window, xpos, ypos):
        if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
            delta_x = xpos - self.last_mouse_x
            delta_y = ypos - self.last_mouse_y

            view = self.view

            if glfw.get_key(window, glfw.KEY_LEFT_SHIFT):
                rot = R.from_euler('z', self.rotation_speed * delta_x / view.width)

            else:
                rot = R.from_euler('yx', [-self.rotation_speed * delta_x / view.width, \
                                        self.rotation_speed * delta_y / view.height])

            
            if glfw.get_key(window, glfw.KEY_LEFT_CONTROL):
                view.view_matrix[:3, :3] = rot.as_matrix() @ view.view_matrix[:3, :3]
            else:
                view.model_matrix[:3, :3] = rot.as_matrix() @ view.model_matrix[:3, :3]

            
        self.last_mouse_x = xpos
        self.last_mouse_y = ypos

    def scroll_callback(self, window, xoffset, yoffset):
        view = self.view
        view.view_matrix[:3, 3] = view.view_matrix[:3, 3] * (1 - yoffset * 0.1)
        
import glfw
from OpenGL.GL import *

from platforms.platform import Platform

class PlatformGLFW(Platform):
    def init(self):
        self.last_mouse_x = 0
        self.last_mouse_y = 0

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

            
        self.last_mouse_x = xpos
        self.last_mouse_y = ypos

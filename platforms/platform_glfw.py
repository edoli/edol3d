import glfw
from OpenGL.GL import *

class PlatformGLFW():
    def __init__(self, init_width, init_height):
        self.width = init_width
        self.height = init_height

        if not glfw.init():
            return
                
        glfw.window_hint(glfw.SAMPLES, 4)
        self.window = glfw.create_window(self.width, self.height, "Render", None, None)
        
        if not self.window:
            glfw.terminate()
            return
        
        glfw.make_context_current(self.window)
        glfw.set_window_size_callback(self.window, self.window_size_callback)

    def loop_prepare(self):
        glfw.poll_events()

    def loop_finish(self):
        glfw.swap_buffers(self.window)
    
    def should_close(self):
        return glfw.window_should_close(self.window)

    def close(self):
        glfw.terminate()

    def window_size_callback(self, window, width, height):
        self.width = width
        self.height = height

from typing import List
import glfw
import numpy as np
import sys
from scipy.spatial.transform import Rotation as R
from OpenGL.GL import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gl.utils import create_shader_program

from platforms.platform import Platform
from platforms.view import View
from render_view.render_view import RenderView
from util.observable_list import ObservableList

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

        self.app = QApplication(sys.argv)
        self.ui = ControlUI(self.view, self.render_views)

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
        

class ControlUI(QWidget):

    def __init__(self, view: View, render_views: ObservableList[RenderView]):
        super().__init__()

        self.view = view
        self.render_views = render_views
        self.initUI()

        self.render_views.subscribe(self.refresh_render_view_list)


    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Main Control')
        # self.setWindowIcon(QIcon('web.png'))

        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add_render_view)

        self.remove_button = QPushButton('Remove')
        self.remove_button.clicked.connect(self.remove_render_view)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.remove_button)

        self.render_view_list = QListWidget()
        self.refresh_render_view_list(self.render_views)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.render_view_list)

        self.setLayout(self.layout)

        self.show()


    def refresh_render_view_list(self, render_views):
        self.render_view_list.clear()

        for i, render_view in enumerate(render_views):
            render_view_list_item = RenderViewListItem(i, self.view, render_view)

            item = QListWidgetItem(self.render_view_list)
            item.setSizeHint(render_view_list_item.sizeHint())
            self.render_view_list.addItem(item)
            self.render_view_list.setItemWidget(item, render_view_list_item)

    def add_render_view(self):
        rgb_shader = create_shader_program('color.vs', 'color.fs')
        render_view = RenderView(0, 0, rgb_shader)
        self.render_views.append(render_view)

    def remove_render_view(self):
        index = self.render_view_list.currentRow()
        if index == -1:
            return
            
        self.render_views.pop(index)


class RenderViewListItem(QWidget):
    
    def __init__(self, i, view: View, render_view: RenderView):
        super().__init__()

        self.view = view
        self.render_view = render_view
        self.index = i

        self.index_label = QLabel()

        self.attrib_name = QComboBox()
        self.attrib_name.currentTextChanged.connect(self.attrib_name_changed)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.index_label)
        self.layout.addWidget(self.attrib_name)

        self.setLayout(self.layout)

        self.refresh()

    def refresh(self):
        self.index_label.setText(str(self.index))
        
        name = self.render_view.attrib
        self.attrib_name.clear()
        self.attrib_name.addItems(self.view.mesh.data.vertex_attribs)
        self.attrib_name.setCurrentText(name)

    def attrib_name_changed(self, text):
        self.render_view.attrib = text
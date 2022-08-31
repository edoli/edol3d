from abc import ABCMeta, abstractmethod
from typing import List

from platforms.view import View
from render_view.render_view import RenderView

class Platform(metaclass = ABCMeta):
    def __init__(self, view: View, render_views: List[RenderView]):
        self.view = view
        self.render_views = render_views
        
        self.init()
    
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def loop_prepare(self):
        pass

    @abstractmethod
    def loop_finish(self):
        pass
    
    @abstractmethod
    def should_close(self):
        pass
    
    @abstractmethod
    def close(self):
        pass

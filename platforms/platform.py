from abc import ABCMeta, abstractmethod

from platforms.view import View

class Platform(metaclass = ABCMeta):
    def __init__(self, view: View):
        self.view = view
        
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

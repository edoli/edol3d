from typing import Callable, List, TypeVar


_T = TypeVar('_T')


class ObservableList(List[_T]):
    def __init__(self):
        super().__init__()

        self._callbacks: List[Callable] = []

    def append(self, __object: _T) -> None:
        res = super().append(__object)
        self.fire()
        return res

    def remove(self, __value: _T) -> None:
        res = super().remove(__value)
        self.fire()
        return res

    def pop(self, __index) -> _T:
        res = super().pop(__index)
        self.fire()
        return res

    def subscribe(self, func: Callable):
        self._callbacks.append(func)

    def fire(self):
        for callback in self._callbacks:
            callback(self)
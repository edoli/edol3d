from typing import Callable, List, TypeVar
from rx.subject.behaviorsubject import BehaviorSubject
from rx.core import typing


_T = TypeVar('_T')


class ObservableList(List[_T]):
    def __init__(self):
        super().__init__()

        self.subject = BehaviorSubject(self)

    def append(self, __object: _T) -> None:
        res = super().append(__object)
        self.subject.on_next(self)
        return res

    def remove(self, __value: _T) -> None:
        res = super().remove(__value)
        self.subject.on_next(self)
        return res

    def pop(self, __index) -> _T:
        res = super().pop(__index)
        self.subject.on_next(self)
        return res

    def subscribe(self, func: typing.OnNext):
        self.subject.subscribe(func)
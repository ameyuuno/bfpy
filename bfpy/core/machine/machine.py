__all__ = ["Machine"]

import abc
import typing as t


class Machine(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, code: t.Text) -> None: ...

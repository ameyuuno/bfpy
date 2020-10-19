__all__ = ["Repl"]

import abc
import typing as t


class Repl(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, reader: t.TextIO, writer: t.TextIO) -> None: ...

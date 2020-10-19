__all__ = ["Repl"]

import abc
from typing import io


class Repl(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, reader: io.TextIO, writer: io.TextIO) -> None: ...

import abc
import io


class IoError(Exception):
    pass


class ByteInputStream(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self) -> int: ...


class ByteOutputStream(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(self, byte: int) -> None: ...

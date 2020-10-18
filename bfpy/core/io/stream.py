__all__ = ["IoError", "ByteInputStream", "ByteOutputStream", "BytesBidirectionalStreamOverTextIo"]

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


class BytesBidirectionalStreamOverTextIo(ByteInputStream, ByteOutputStream):
    def __init__(self, source: io.TextIOBase) -> None:
        self.__source = source

    def read(self) -> int:
        char = self.__source.read(1)
        if len(char) == 0:
            raise IoError("Can not read byte from empty byte input stream")

        byte = ord(char)
        self.__validate_byte(byte)

        return byte

    def write(self, byte: int) -> None:
        self.__validate_byte(byte)
        char = chr(byte)

        self.__source.write(char)
        self.__source.flush()

    @staticmethod
    def __validate_byte(byte: int) -> None:
        if not (0 <= byte < 256):
            raise IoError("Byte should be in range [0, 255]")

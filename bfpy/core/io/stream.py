__all__ = ["IoError", "ByteInputStream", "ByteOutputStream", "BytesBidirectionalStreamOverBinaryIo"]

import abc
import typing as t


class IoError(Exception):
    pass


class ByteInputStream(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self) -> int: ...


class ByteOutputStream(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(self, byte: int) -> None: ...


class BytesBidirectionalStreamOverBinaryIo(ByteInputStream, ByteOutputStream):
    def __init__(self, source: t.BinaryIO) -> None:
        self.__source = source

    def read(self) -> int:
        char = self.__source.read(1)
        if len(char) == 0:
            char = b"\x00"

        byte = ord(char.decode())
        self.__validate_byte(byte)

        return byte

    def write(self, byte: int) -> None:
        self.__validate_byte(byte)
        char = chr(byte)

        self.__source.write(char.encode())
        self.__source.flush()

    @staticmethod
    def __validate_byte(byte: int) -> None:
        if not (0 <= byte < 256):
            raise IoError("Byte should be in range [0, 255]")

__all__ = ["TapeError", "OutOfBoundsError", "Tape", "FiniteTape"]

import abc
import typing as t


class TapeError(Exception):
    pass


class OutOfBoundsError(TapeError):
    def __init__(self, pointer: int) -> None:
        super().__init__(f"Pointer is out of tape bounds (pointer={pointer})")


class Tape(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self) -> int: ...

    @abc.abstractmethod
    def set(self, value: int) -> None: ...

    @abc.abstractmethod
    def shift_left(self, steps: int) -> None: ...

    @abc.abstractmethod
    def shift_right(self, steps: int) -> None: ...


class FiniteTape(Tape):
    __DEFAULT_LENGTH = 30_000

    def __init__(self, length: t.Optional[int] = None) -> None:
        self.__length = length if length is not None else self.__DEFAULT_LENGTH
        if self.__length <= 0:
            raise ValueError("Length of finite tape should be >= 0")

        self.__cells = bytearray(self.__length)
        self.__pointer = 0

    def get(self) -> int:
        return self.__cells[self.__pointer]

    def set(self, value: int) -> None:
        self.__cells[self.__pointer] = value

    def shift_left(self, steps: int) -> None:
        self.__pointer = self.__get_update_pointer_if_allowed(-steps)

    def shift_right(self, steps: int) -> None:
        self.__pointer = self.__get_update_pointer_if_allowed(steps)

    def __get_update_pointer_if_allowed(self, delta: int) -> int:
        updated_pointer = self.__pointer + delta

        if not (0 <= updated_pointer < self.__length):
            raise OutOfBoundsError(self.__pointer)

        return updated_pointer

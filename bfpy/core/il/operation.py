__all__ = ["Operation", "Addition", "Subtraction", "LeftShift", "RightShift", "ReadByte", "WriteByte", "Loop",
           "Program"]

import dataclasses as dc
import typing as t


@dc.dataclass(frozen=True)
class Operation:
    def __post_init__(self) -> None:
        if self.__class__ == Operation:
            raise TypeError("Can not create an instance of class `Operation`")


@dc.dataclass(frozen=True)
class Addition(Operation):
    delta: int


@dc.dataclass(frozen=True)
class Subtraction(Operation):
    delta: int


@dc.dataclass(frozen=True)
class LeftShift(Operation):
    delta: int


@dc.dataclass(frozen=True)
class RightShift(Operation):
    delta: int


@dc.dataclass(frozen=True)
class ReadByte(Operation):
    pass


@dc.dataclass(frozen=True)
class WriteByte(Operation):
    pass


@dc.dataclass(frozen=True)
class Loop(Operation):
    body: t.Sequence[Operation]


@dc.dataclass(frozen=True)
class Program(Operation):
    instructions: t.Sequence[Operation]

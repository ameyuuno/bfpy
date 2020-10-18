__all__ = ["Interpreter", "InterpreterImpl"]

import abc
import typing as t

from bfpy.core.il.operation import (Program, Loop, Addition, Subtraction, LeftShift, RightShift, ReadByte, WriteByte,
                                    Operation)
from bfpy.core.interpreter.tape import Tape
from bfpy.core.io.stream import ByteInputStream, ByteOutputStream


class Interpreter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, byte_input_stream: ByteInputStream, byte_output_stream: ByteOutputStream,
                 program: Program) -> None: ...


class InterpreterImpl(Interpreter):
    class _OperationIterator(t.Iterator[Operation]):
        def __init__(self, tape: Tape, program: Program) -> None:
            self.__tape = tape
            self.__program = program

            self.__next_operations = [*self.__program.instructions]

        def __iter__(self) -> 'InterpreterImpl._OperationIterator':
            return self

        def __next__(self) -> Operation:
            try:
                operation = self.__next_operations.pop(0)
            except IndexError:
                raise StopIteration

            if isinstance(operation, Loop) and self.__tape.get() != 0:
                self.__next_operations = [*operation.body, operation, *self.__next_operations]

                return next(self)

            return operation

    def __init__(self, tape: Tape) -> None:
        self.__tape = tape

    def evaluate(self, byte_input_stream: ByteInputStream, byte_output_stream: ByteOutputStream,
                 program: Program) -> None:
        operations = self.__create_operation_iterator(program)

        for operation in operations:
            if isinstance(operation, Addition):
                value = (self.__tape.get() + operation.delta) % 256
                self.__tape.set(value)

            elif isinstance(operation, Subtraction):
                value = (self.__tape.get() - operation.delta) % 256
                self.__tape.set(value)

            elif isinstance(operation, LeftShift):
                self.__tape.shift_left(operation.delta)

            elif isinstance(operation, RightShift):
                self.__tape.shift_right(operation.delta)

            elif isinstance(operation, ReadByte):
                byte = byte_input_stream.read()
                self.__tape.set(byte)

            elif isinstance(operation, WriteByte):
                byte = self.__tape.get()
                byte_output_stream.write(byte)

    def __create_operation_iterator(self, program: Program) -> 'InterpreterImpl._OperationIterator':
        return self._OperationIterator(self.__tape, program)

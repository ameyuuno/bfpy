import abc

from bfpy.core.il.operation import Program
from bfpy.core.interpreter.tape import Tape
from bfpy.core.io.stream import ByteInputStream, ByteOutputStream


class Interpreter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, byte_input_stream: ByteInputStream, byte_output_stream: ByteOutputStream,
                 program: Program) -> None: ...


class InterpreterImpl(Interpreter):
    def __init__(self, tape: Tape) -> None:
        self.__tape = tape

    def evaluate(self, byte_input_stream: ByteInputStream, byte_output_stream: ByteOutputStream,
                 program: Program) -> None:
        raise NotImplementedError

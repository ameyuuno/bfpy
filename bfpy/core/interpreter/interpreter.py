import abc

from bfpy.core.il.operation import Operation
from bfpy.core.interpreter.tape import Tape
from bfpy.core.io.stream import ByteInputStream, ByteOutputStream


class Interpreter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, byte_input_stream: ByteInputStream, byte_output_stream: ByteOutputStream,
                 operation: Operation) -> None: ...


class InterpreterImpl(Interpreter):
    def evaluate(self, byte_input_stream: ByteInputStream, byte_output_stream: ByteOutputStream,
                 operation: Operation) -> None:
        raise NotImplementedError

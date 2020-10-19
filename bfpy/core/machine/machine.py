__all__ = ["MachineError", "Machine", "MachineImpl"]

import abc
import typing as t

from bfpy.core.il.translator import Translator
from bfpy.core.interpreter.interpreter import Interpreter
from bfpy.core.interpreter.tape import TapeError
from bfpy.core.io.stream import ByteInputStream, ByteOutputStream
from bfpy.core.lexer.lexer import Lexer, LexicalError
from bfpy.core.parser.parser import Parser, SyntacticError


class MachineError(Exception):
    pass


class Machine(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, code: t.Text) -> None: ...


class MachineImpl(Machine):
    def __init__(self, lexer: Lexer, parser: Parser, translator: Translator, interpreter: Interpreter,
                 byte_input_stream: ByteInputStream, byte_output_stream: ByteOutputStream) -> None:
        self.__lexer = lexer
        self.__parser = parser
        self.__translator = translator
        self.__interpreter = interpreter

        self.__byte_input_stream = byte_input_stream
        self.__byte_output_stream = byte_output_stream

    def execute(self, code: t.Text) -> None:
        try:
            self.__execute(code)

        except LexicalError as error:
            raise MachineError(f"Lexical error: {error}") from error

        except SyntacticError as error:
            raise MachineError(f"Syntax error: {error}") from error

        except TapeError as error:
            raise MachineError(f"Evaluation error: {error}") from error

    def __execute(self, code: t.Text) -> None:
        tokens = self.__lexer.tokenize(code)
        ast = self.__parser.parse(tokens)
        program = self.__translator.translate(ast)

        self.__interpreter.evaluate(self.__byte_input_stream, self.__byte_output_stream, program)

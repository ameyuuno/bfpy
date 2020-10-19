__all__ = ["Machine", "MachineImpl"]

import abc
import typing as t

from bfpy.core.il.translator import Translator
from bfpy.core.interpreter.interpreter import Interpreter
from bfpy.core.lexer.lexer import Lexer
from bfpy.core.parser.parser import Parser


class Machine(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, code: t.Text) -> None: ...


class MachineImpl(Machine):
    def __init__(self, lexer: Lexer, parser: Parser, translator: Translator, interpreter: Interpreter) -> None:
        self.__lexer = lexer
        self.__parser = parser
        self.__translator = translator
        self.__interpreter = interpreter

    def execute(self, code: t.Text) -> None:
        raise NotImplementedError

__all__ = ["Translator", "TranslatorImpl"]

import abc

from bfpy.core.il.operation import Operation
from bfpy.core.parser.ast import AstNode


class Translator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate(self, ast: AstNode) -> Operation: ...


class TranslatorImpl(Translator):
    def translate(self, ast: AstNode) -> Operation:
        raise NotImplementedError

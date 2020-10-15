import abc
import typing as t

from bfpy.lexer.token import Token
from bfpy.parser.ast import AstNode


class SyntacticError(Exception):
    """Syntax Error.

    Error is named "syntactic", not "syntax", because `SyntaxError` is built-in exception in Python.
    """
    pass


class Parser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, tokens: t.Sequence[Token]) -> AstNode: ...


class ParserImpl(Parser):
    def parse(self, tokens: t.Sequence[Token]) -> AstNode:
        raise NotImplementedError

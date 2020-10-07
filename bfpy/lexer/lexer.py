__all__ = ["Lexer", "LexerImpl"]

import abc
import typing as t

from overrides import overrides

from bfpy.lexer.token import Token


class Lexer(abc.ABC):
    @abc.abstractmethod
    def tokenize(self, text: t.Text) -> t.Sequence[Token]: ...


class LexerImpl(Lexer):
    @overrides
    def tokenize(self, text: t.Text) -> t.Sequence[Token]:
        raise NotImplementedError

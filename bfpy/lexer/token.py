__all__ = ["Lexeme", "TokenType", "Token"]

import dataclasses as dc
import enum
import typing as t


Lexeme = t.NewType("Lexeme", t.Text)


@enum.unique
class TokenType(enum.Enum):
    LSHIFT = enum.auto()
    RSHIFT = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    RB = enum.auto()
    WB = enum.auto()
    OLOOP = enum.auto()
    CLOOP = enum.auto()
    WHITESPACE = enum.auto()
    EOF = enum.auto()


@dc.dataclass(frozen=True)
class Token:
    lexeme: Lexeme
    type_: TokenType

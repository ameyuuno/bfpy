__all__ = ["Lexer", "LexerImpl", "LexicalError"]

import abc
import typing as t

from bfpy.core.lexer.token import Token, TokenType, Lexeme


class LexicalError(Exception):
    pass


class Lexer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def tokenize(self, text: t.Text) -> t.Sequence[Token]: ...


class LexerImpl(Lexer):
    __TOKENS_TYPES: t.Mapping[t.Text, TokenType] = {
        "<": TokenType.LSHIFT,
        ">": TokenType.RSHIFT,
        "+": TokenType.INC,
        "-": TokenType.DEC,
        ",": TokenType.RB,
        ".": TokenType.WB,
        "[": TokenType.OLOOP,
        "]": TokenType.CLOOP,
    }

    def tokenize(self, text: t.Text) -> t.Sequence[Token]:
        return [self.__parse_token(char) for char in text if not char.isspace()]

    def __parse_token(self, char: t.Text) -> Token:
        try:
            token_type = self.__TOKENS_TYPES[char]
        except KeyError as exc:
            raise LexicalError(f"Unknown token (lexeme={char})") from exc

        return Token(Lexeme(char), token_type)

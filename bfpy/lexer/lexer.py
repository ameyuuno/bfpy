__all__ = ["Lexer", "LexerImpl", "LexerError"]

import abc
import typing as t

from bfpy.lexer.token import Token, TokenType, Lexeme


class LexerError(Exception):
    pass


class Lexer(abc.ABC):
    @abc.abstractmethod
    def tokenize(self, text: t.Text) -> t.Sequence[Token]: ...


class LexerImpl(Lexer):
    __TOKENS: t.Mapping[t.Text, Token] = {
        "<": Token(Lexeme("<"), TokenType.LSHIFT),
        ">": Token(Lexeme(">"), TokenType.RSHIFT),
        "+": Token(Lexeme("+"), TokenType.INC),
        "-": Token(Lexeme("-"), TokenType.DEC),
        ",": Token(Lexeme(","), TokenType.RB),
        ".": Token(Lexeme("."), TokenType.WB),
        "[": Token(Lexeme("["), TokenType.OLOOP),
        "]": Token(Lexeme("]"), TokenType.CLOOP),
        " ": Token(Lexeme(" "), TokenType.WHITESPACE),
        "\t": Token(Lexeme("\t"), TokenType.WHITESPACE),
        "\n": Token(Lexeme("\n"), TokenType.WHITESPACE),
    }

    __TOKEN_EOF = Token(Lexeme(""), TokenType.EOF)

    def tokenize(self, text: t.Text) -> t.Sequence[Token]:
        return [*(self.__parse_token(char) for char in text), self.__TOKEN_EOF]

    def __parse_token(self, char: t.Text) -> Token:
        try:
            return self.__TOKENS[char]

        except KeyError as exc:
            raise LexerError(f"Unknown token (lexeme={char})") from exc

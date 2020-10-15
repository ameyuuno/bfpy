__all__ = ["Translator", "TranslatorImpl", "TranslationError"]

import abc

from bfpy.core.il.operation import (Operation, CompositeOperation, Addition, Subtraction, LeftShift, RightShift,
                                    ReadByte, WriteByte)
from bfpy.core.lexer.token import TokenType
from bfpy.core.parser.ast import AstNode, LeafNode, ListNode


class TranslationError(Exception):
    pass


class Translator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate(self, ast: AstNode) -> Operation: ...


class TranslatorImpl(Translator):
    def translate(self, ast: AstNode) -> Operation:
        if isinstance(ast, ListNode):
            return CompositeOperation([self.translate(node) for node in ast.nodes])

        elif isinstance(ast, LeafNode):
            if ast.token.type_ is TokenType.INC:
                return Addition(1)
            elif ast.token.type_ is TokenType.DEC:
                return Subtraction(1)
            elif ast.token.type_ is TokenType.LSHIFT:
                return LeftShift(1)
            elif ast.token.type_ is TokenType.RSHIFT:
                return RightShift(1)
            elif ast.token.type_ is TokenType.RB:
                return ReadByte()
            elif ast.token.type_ is TokenType.WB:
                return WriteByte()
            else:
                raise TranslationError(f"Unknown type of token in AST leaf node (token={ast.token})")

        else:
            raise TranslationError(f"Unknown type of AST node (ast={ast}).")

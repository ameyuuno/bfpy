__all__ = ["Translator", "TranslatorImpl", "TranslationError"]

import abc

from bfpy.core.il.operation import (Operation, Program, Addition, Subtraction, LeftShift, RightShift,
                                    ReadByte, WriteByte, Loop)
from bfpy.core.lexer.token import TokenType
from bfpy.core.parser.ast import AstNode, LeafNode, ListNode, Ast


class TranslationError(Exception):
    pass


class Translator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate(self, ast: Ast) -> Program: ...


class TranslatorImpl(Translator):
    def translate(self, ast: Ast) -> Program:
        return Program([self.__translate_node(node) for node in ast.nodes])

    def __translate_node(self, ast_node: AstNode) -> Operation:
        if isinstance(ast_node, ListNode):
            return Loop([self.__translate_node(node) for node in ast_node.nodes])

        elif isinstance(ast_node, LeafNode):
            if ast_node.token.type_ is TokenType.INC:
                return Addition(1)
            elif ast_node.token.type_ is TokenType.DEC:
                return Subtraction(1)
            elif ast_node.token.type_ is TokenType.LSHIFT:
                return LeftShift(1)
            elif ast_node.token.type_ is TokenType.RSHIFT:
                return RightShift(1)
            elif ast_node.token.type_ is TokenType.RB:
                return ReadByte()
            elif ast_node.token.type_ is TokenType.WB:
                return WriteByte()
            else:
                raise TranslationError(f"Unknown type of token in AST leaf node (token={ast_node.token})")

        else:
            raise TranslationError(f"Unknown type of AST node (ast_node={ast_node}).")

__all__ = ["SyntacticError", "Parser", "ParserImpl"]

import abc
import typing as t

from bfpy.core.lexer.token import Token, TokenType
from bfpy.core.parser.ast import AstNode, ListNode, LeafNode, Ast


class SyntacticError(Exception):
    """Syntax Error.

    Error is named "syntactic", not "syntax", because `SyntaxError` is built-in exception in Python.
    """
    pass


class Parser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, tokens: t.Sequence[Token]) -> Ast: ...


class ParserImpl(Parser):
    def parse(self, tokens: t.Sequence[Token]) -> Ast:
        root_nodes: t.MutableSequence[AstNode] = []

        nodes: t.MutableSequence[AstNode] = root_nodes
        loop_bodies: t.MutableSequence[t.MutableSequence[AstNode]] = []

        for token in tokens:
            if token.type_ is TokenType.OLOOP:
                loop_bodies.append(nodes)
                nodes = []

            elif token.type_ is TokenType.CLOOP:
                try:
                    prev_nodes = loop_bodies.pop()
                except IndexError as exc:
                    raise SyntacticError(f"Unexpected token (token={token})") from exc

                prev_nodes.append(ListNode(nodes))
                nodes = prev_nodes

            else:
                nodes.append(LeafNode(token))

        if len(loop_bodies) > 0:
            raise SyntacticError(f"Missing token `[` (token_type={TokenType.OLOOP})")

        return Ast(root_nodes)

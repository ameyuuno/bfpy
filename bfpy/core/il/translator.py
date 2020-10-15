__all__ = ["Translator", "TranslatorImpl"]

import abc
import typing as t

from bfpy.core.il.operation import Operation, CompositeOperation, Addition, Subtraction, LeftShift, RightShift, \
    ReadByte, WriteByte
from bfpy.core.lexer.token import TokenType
from bfpy.core.parser.ast import AstNode, LeafNode, ListNode


class Translator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate(self, ast: AstNode) -> Operation: ...


class TranslatorImpl(Translator):
    def translate(self, ast: AstNode) -> Operation:
        ss = []
        sss = []

        node_level = [ast]  # queue
        node_levels = []  # stack

        while True:
            if len(node_level) == 0:
                if len(node_levels) == 0:
                    break

                node_level = node_levels.pop(-1)
                s = CompositeOperation(ss)
                ss = sss.pop(-1)
                ss.append(s)
                continue

            node = node_level.pop(0)

            if isinstance(node, ListNode):
                node_levels.append(node_level)
                sss.append(ss)

                node_level = list(node.nodes)
                ss = []

            elif isinstance(node, LeafNode):
                if node.token.type_ is TokenType.INC:
                    ss.append(Addition(1))
                elif node.token.type_ is TokenType.DEC:
                    ss.append(Subtraction(1))
                elif node.token.type_ is TokenType.LSHIFT:
                    ss.append(LeftShift(1))
                elif node.token.type_ is TokenType.RSHIFT:
                    ss.append(RightShift(1))
                elif node.token.type_ is TokenType.RB:
                    ss.append(ReadByte())
                elif node.token.type_ is TokenType.WB:
                    ss.append(WriteByte())

        return ss[0]

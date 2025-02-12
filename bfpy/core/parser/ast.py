__all__ = ["Ast", "AstNode", "ListNode", "LeafNode"]

import dataclasses as dc
import typing as t

from bfpy.core.lexer.token import Token


@dc.dataclass(frozen=True)
class AstNode:
    def __post_init__(self) -> None:
        if self.__class__ == AstNode:
            raise TypeError("Can not create an instance of class `AstNode`")


@dc.dataclass(frozen=True)
class ListNode(AstNode):
    nodes: t.Sequence[AstNode]


@dc.dataclass(frozen=True)
class LeafNode(AstNode):
    token: Token


@dc.dataclass(frozen=True)
class Ast:
    nodes: t.Sequence[AstNode]

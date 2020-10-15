__all__ = ["AstNode", "ListNode", "LeafNode"]

import dataclasses as dc
import typing as t

from bfpy.lexer.token import Token


@dc.dataclass(frozen=True)
class AstNode:
    pass


@dc.dataclass(frozen=True)
class ListNode(AstNode):
    nodes: t.Sequence[AstNode]


@dc.dataclass(frozen=True)
class LeafNode(AstNode):
    token: Token

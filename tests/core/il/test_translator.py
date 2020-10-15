import typing as t

import pytest

from bfpy.core.il.operation import (Operation, CompositeOperation, Addition, Subtraction, LeftShift, RightShift,
                                    WriteByte, ReadByte)
from bfpy.core.il.translator import TranslatorImpl, TranslationError
from bfpy.core.lexer.token import Token, Lexeme, TokenType
from bfpy.core.parser.ast import AstNode, ListNode, LeafNode


class TestTranslatorImpl:
    LSHIFT = Token(Lexeme("<"), TokenType.LSHIFT)
    RSHIFT = Token(Lexeme(">"), TokenType.RSHIFT)
    INC = Token(Lexeme("+"), TokenType.INC)
    DEC = Token(Lexeme("-"), TokenType.DEC)
    RB = Token(Lexeme(","), TokenType.RB)
    WB = Token(Lexeme("."), TokenType.WB)
    OLOOP = Token(Lexeme("["), TokenType.OLOOP)
    CLOOP = Token(Lexeme("]"), TokenType.CLOOP)

    @pytest.mark.parametrize("ast, expected_operation", [
        pytest.param(
            ListNode([]),
            CompositeOperation([]),
            id="''",
        ),
        pytest.param(
            ListNode([LeafNode(INC)]),
            CompositeOperation([Addition(1)]),
            id="'+'",
        ),
        pytest.param(
            ListNode([LeafNode(INC), LeafNode(DEC)]),
            CompositeOperation([Addition(1), Subtraction(1)]),
            id="'+-'",
        ),
        pytest.param(
            ListNode([ListNode([LeafNode(RB), LeafNode(WB)])]),
            CompositeOperation([CompositeOperation([ReadByte(), WriteByte()])]),
            id="'[,.]'",
        ),
        pytest.param(
            ListNode([
                ListNode([
                    LeafNode(LSHIFT),
                    LeafNode(RSHIFT),
                ])
            ]),
            CompositeOperation([
                CompositeOperation([
                    LeftShift(1),
                    RightShift(1),
                ])
            ]),
            id="'[<>]'",
        ),
        pytest.param(
            ListNode([
                LeafNode(INC),
                ListNode([
                    LeafNode(DEC),
                    ListNode([
                        LeafNode(LSHIFT),
                        LeafNode(LSHIFT),
                        ListNode([
                            LeafNode(INC),
                            ListNode([
                                LeafNode(DEC),
                                LeafNode(DEC),
                                LeafNode(RSHIFT),
                            ]),
                            LeafNode(DEC),
                            ListNode([
                                LeafNode(LSHIFT),
                                LeafNode(LSHIFT),
                                LeafNode(LSHIFT),
                            ]),
                        ]),
                    ]),
                    LeafNode(RSHIFT),
                    LeafNode(RSHIFT),
                    LeafNode(RSHIFT),
                    LeafNode(DEC),
                ]),
                LeafNode(RSHIFT),
                LeafNode(DEC),
                LeafNode(WB),
            ]),
            CompositeOperation([
                Addition(1),
                CompositeOperation([
                    Subtraction(1),
                    CompositeOperation([
                        LeftShift(1),
                        LeftShift(1),
                        CompositeOperation([
                            Addition(1),
                            CompositeOperation([
                                Subtraction(1),
                                Subtraction(1),
                                RightShift(1),
                            ]),
                            Subtraction(1),
                            CompositeOperation([
                                LeftShift(1),
                                LeftShift(1),
                                LeftShift(1),
                            ]),
                        ]),
                    ]),
                    RightShift(1),
                    RightShift(1),
                    RightShift(1),
                    Subtraction(1),
                ]),
                RightShift(1),
                Subtraction(1),
                WriteByte(),
            ]),
            id="'+[-[<<[+[-->]-[<<<]]]>>>-]>-.'",
        ),
    ])
    def test_translate(self, ast: AstNode, expected_operation: Operation) -> None:
        translator = TranslatorImpl()

        actual_operation = translator.translate(ast)

        assert actual_operation == expected_operation

    def test_translate_unknown_ast_node(self) -> None:
        class UnknownAstNode(AstNode):
            pass

        translator = TranslatorImpl()

        with pytest.raises(TranslationError) as exc_info:
            translator.translate(UnknownAstNode())

        assert "Unknown type of AST node" in str(exc_info.value)

    def test_translate_ast_with_unknown_token(self) -> None:
        ast = ListNode([LeafNode(Token(Lexeme("?"), t.cast(TokenType, None)))])
        translator = TranslatorImpl()

        with pytest.raises(TranslationError) as exc_info:
            translator.translate(ast)

        assert "Unknown type of token in AST leaf node " in str(exc_info.value)

import pytest

from bfpy.il.operation import Operation, CompositeOperation, Addition, Subtraction, LeftShift, RightShift, WriteByte
from bfpy.il.translator import TranslatorImpl
from bfpy.lexer.token import Token, Lexeme, TokenType
from bfpy.parser.ast import AstNode, ListNode, LeafNode


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
            ListNode([ListNode([])]),
            CompositeOperation([CompositeOperation([])]),
            id="'[]'",
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

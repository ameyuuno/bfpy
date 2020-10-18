import typing as t

import pytest

from bfpy.core.il.operation import (Operation, Program, Addition, Subtraction, LeftShift, RightShift,
                                    WriteByte, ReadByte, Loop)
from bfpy.core.il.translator import Translator, TranslationError
from bfpy.core.lexer.token import Token, Lexeme, TokenType
from bfpy.core.parser.ast import AstNode, ListNode, LeafNode, Ast


class TestTranslator:
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
            Ast([]),
            Program([]),
            id="''",
        ),
        pytest.param(
            Ast([LeafNode(INC)]),
            Program([Addition(1)]),
            id="'+'",
        ),
        pytest.param(
            Ast([LeafNode(INC), LeafNode(DEC)]),
            Program([Addition(1), Subtraction(1)]),
            id="'+-'",
        ),
        pytest.param(
            Ast([ListNode([LeafNode(RB), LeafNode(WB)])]),
            Program([Loop([ReadByte(), WriteByte()])]),
            id="'[,.]'",
        ),
        pytest.param(
            Ast([
                ListNode([
                    LeafNode(LSHIFT),
                    LeafNode(RSHIFT),
                ])
            ]),
            Program([
                Loop([
                    LeftShift(1),
                    RightShift(1),
                ])
            ]),
            id="'[<>]'",
        ),
        pytest.param(
            Ast([
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
            Program([
                Addition(1),
                Loop([
                    Subtraction(1),
                    Loop([
                        LeftShift(1),
                        LeftShift(1),
                        Loop([
                            Addition(1),
                            Loop([
                                Subtraction(1),
                                Subtraction(1),
                                RightShift(1),
                            ]),
                            Subtraction(1),
                            Loop([
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
    def test_translate(self, translator: Translator, ast: Ast, expected_operation: Operation) -> None:
        actual_operation = translator.translate(ast)

        assert actual_operation == expected_operation

    def test_translate_unknown_ast_node(self, translator: Translator) -> None:
        class UnknownAstNode(AstNode):
            pass

        with pytest.raises(TranslationError) as exc_info:
            translator.translate(Ast([UnknownAstNode()]))

        assert "Unknown type of AST node" in str(exc_info.value)

    def test_translate_ast_with_unknown_token(self, translator: Translator) -> None:
        ast = Ast([LeafNode(Token(Lexeme("?"), t.cast(TokenType, None)))])

        with pytest.raises(TranslationError) as exc_info:
            translator.translate(ast)

        assert "Unknown type of token in AST leaf node " in str(exc_info.value)

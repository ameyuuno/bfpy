import typing as t

import pytest

from bfpy.core.lexer.token import Token, Lexeme, TokenType
from bfpy.core.parser.ast import AstNode, ListNode, LeafNode
from bfpy.core.parser.parser import ParserImpl, SyntacticError


class TestParserImpl:
    LSHIFT = Token(Lexeme("<"), TokenType.LSHIFT)
    RSHIFT = Token(Lexeme(">"), TokenType.RSHIFT)
    INC = Token(Lexeme("+"), TokenType.INC)
    DEC = Token(Lexeme("-"), TokenType.DEC)
    RB = Token(Lexeme(","), TokenType.RB)
    WB = Token(Lexeme("."), TokenType.WB)
    OLOOP = Token(Lexeme("["), TokenType.OLOOP)
    CLOOP = Token(Lexeme("]"), TokenType.CLOOP)

    @pytest.mark.parametrize("tokens, expected_ast", [
        pytest.param(
            [],
            ListNode([]),
            id="''",
        ),
        pytest.param(
            [INC],
            ListNode([LeafNode(INC)]),
            id="'+'",
        ),
        pytest.param(
            [INC, DEC],
            ListNode([LeafNode(INC), LeafNode(DEC)]),
            id="'+-'",
        ),
        pytest.param(
            [OLOOP, CLOOP],
            ListNode([ListNode([])]),
            id="'[]'",
        ),
        pytest.param(
            [OLOOP, LSHIFT, RSHIFT, CLOOP],
            ListNode([
                ListNode([
                    LeafNode(LSHIFT),
                    LeafNode(RSHIFT),
                ])
            ]),
            id="'[<>]'",
        ),
        pytest.param(
            [INC, OLOOP, DEC, OLOOP, LSHIFT, LSHIFT, OLOOP, INC, OLOOP, DEC, DEC, DEC, RSHIFT, CLOOP, DEC, OLOOP,
             LSHIFT, LSHIFT, LSHIFT, CLOOP, CLOOP, CLOOP, RSHIFT, RSHIFT, RSHIFT, DEC, CLOOP, RSHIFT, DEC, WB],
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
            id="'+[-[<<[+[--->]-[<<<]]]>>>-]>-.'",
        ),
    ])
    def test_parse(self, tokens: t.Sequence[Token], expected_ast: AstNode) -> None:
        parser = ParserImpl()

        actual_ast = parser.parse(tokens)

        assert actual_ast == expected_ast

    @pytest.mark.parametrize("tokens, expected_error", [
        pytest.param(
            [OLOOP],
            "Missing token",
            id="Missing close-loop bracket for open-loop bracket",
        ),
        pytest.param(
            [CLOOP],
            "Unexpected token",
            id="Close-loop bracket without open-loop bracket before",
        ),
    ])
    def test_parsing_token_sequence_with_syntax_error(self, tokens: t.Sequence[Token], expected_error: t.Text) -> None:
        parser = ParserImpl()

        with pytest.raises(SyntacticError) as exc_info:
            parser.parse(tokens)

        assert expected_error in str(exc_info.value)

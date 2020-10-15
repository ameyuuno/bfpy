import typing as t

import pytest

from bfpy.core.lexer.lexer import LexerImpl, LexicalError
from bfpy.core.lexer.token import Token, TokenType, Lexeme


class TestLexerImpl:
    LSHIFT = Token(Lexeme("<"), TokenType.LSHIFT)
    RSHIFT = Token(Lexeme(">"), TokenType.RSHIFT)
    INC = Token(Lexeme("+"), TokenType.INC)
    DEC = Token(Lexeme("-"), TokenType.DEC)
    RB = Token(Lexeme(","), TokenType.RB)
    WB = Token(Lexeme("."), TokenType.WB)
    OLOOP = Token(Lexeme("["), TokenType.OLOOP)
    CLOOP = Token(Lexeme("]"), TokenType.CLOOP)

    @pytest.mark.parametrize("text, expected_tokens", [
        pytest.param(
            "<",
            [LSHIFT],
            id="'<'"
        ),
        pytest.param(
            ">",
            [RSHIFT],
            id="'>'"
        ),
        pytest.param(
            "+",
            [INC],
            id="'+'"
        ),
        pytest.param(
            "-",
            [DEC],
            id="'-'"
        ),
        pytest.param(
            ",",
            [RB],
            id="','"
        ),
        pytest.param(
            ".",
            [WB],
            id="'.'"
        ),
        pytest.param(
            "[",
            [OLOOP],
            id="'['"
        ),
        pytest.param(
            "]",
            [CLOOP],
            id="']'"
        ),
        pytest.param(
            " ",
            [],
            id="' '"
        ),
        pytest.param(
            "\t",
            [],
            id="'\t'"
        ),
        pytest.param(
            "\n",
            [],
            id="'\n'"
        ),
        pytest.param(
            "",
            [],
            id="''"
        ),
        pytest.param(
            "++",
            [INC, INC],
            id="'++'"
        ),
        pytest.param(
            "+ +",
            [INC, INC],
            id="'+ +'"
        ),
        pytest.param(
            "+[-[<<[+[--->]-[<<<]]]>>>-]>-.",
            [INC, OLOOP, DEC, OLOOP, LSHIFT, LSHIFT, OLOOP, INC, OLOOP, DEC, DEC, DEC, RSHIFT, CLOOP, DEC, OLOOP,
             LSHIFT, LSHIFT, LSHIFT, CLOOP, CLOOP, CLOOP, RSHIFT, RSHIFT, RSHIFT, DEC, CLOOP, RSHIFT, DEC, WB],
            id="'+[-[<<[+[--->]-[<<<]]]>>>-]>-.'"
        ),
    ])
    def test_tokenize(self, text: t.Text, expected_tokens: t.Sequence[Token]) -> None:
        lexer = LexerImpl()

        actual_tokens = lexer.tokenize(text)

        assert actual_tokens == expected_tokens

    @pytest.mark.parametrize("text, unknown_lexeme", [
        pytest.param("p", "p", id="Unknown lexeme: letter"),
        pytest.param("=", "=", id="Unknown lexeme: sign"),
        pytest.param("+- < =  .--", "=", id="Unknown lexeme: letter among known lexemes"),
        pytest.param("++(-+>>).--", "(", id="Unknown lexeme: wrong bracket type for loop"),
    ])
    def test_tokenize_text_with_unknown_lexemes(self, text: t.Text, unknown_lexeme: t.Text) -> None:
        lexer = LexerImpl()

        with pytest.raises(LexicalError) as exc_info:
            lexer.tokenize(text)

        assert f"Unknown token (lexeme={unknown_lexeme})" == str(exc_info.value)

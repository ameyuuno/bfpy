import typing as t

import pytest

from bfpy.lexer.lexer import LexerImpl, LexerError
from bfpy.lexer.token import Token, TokenType


class TestLexerImpl:
    TOKEN_LSHIFT = Token("<", TokenType.LSHIFT)
    TOKEN_RSHIFT = Token(">", TokenType.RSHIFT)
    TOKEN_INC = Token("+", TokenType.INC)
    TOKEN_DEC = Token("-", TokenType.DEC)
    TOKEN_RB = Token(",", TokenType.RB)
    TOKEN_WB = Token(".", TokenType.WB)
    TOKEN_OLOOP = Token("[", TokenType.OLOOP)
    TOKEN_CLOOP = Token("]", TokenType.CLOOP)
    TOKEN_WS_SPACE = Token(" ", TokenType.WHITESPACE)
    TOKEN_WS_TAB = Token("\t", TokenType.WHITESPACE)
    TOKEN_WS_NL = Token("\n", TokenType.WHITESPACE)
    TOKEN_EOF = Token("", TokenType.EOF)

    @pytest.mark.parametrize("text, expected_tokens", [
        pytest.param("<", [TOKEN_LSHIFT, TOKEN_EOF], id="'<'"),
        pytest.param(">", [TOKEN_RSHIFT, TOKEN_EOF], id="'>'"),
        pytest.param("+", [TOKEN_INC, TOKEN_EOF], id="'+'"),
        pytest.param("-", [TOKEN_DEC, TOKEN_EOF], id="'-'"),
        pytest.param(",", [TOKEN_RB, TOKEN_EOF], id="','"),
        pytest.param(".", [TOKEN_WB, TOKEN_EOF], id="'.'"),
        pytest.param("[", [TOKEN_OLOOP, TOKEN_EOF], id="'['"),
        pytest.param("]", [TOKEN_CLOOP, TOKEN_EOF], id="']'"),
        pytest.param(" ", [TOKEN_WS_SPACE, TOKEN_EOF], id="' '"),
        pytest.param("\t", [TOKEN_WS_TAB, TOKEN_EOF], id="'\t'"),
        pytest.param("\n", [TOKEN_WS_NL, TOKEN_EOF], id="'\n'"),
        pytest.param("", [TOKEN_EOF], id="'EOF'"),
        pytest.param("++", [TOKEN_INC, TOKEN_INC, TOKEN_EOF], id="'++'"),
        pytest.param("+ +", [TOKEN_INC, TOKEN_WS_SPACE, TOKEN_INC, TOKEN_EOF], id="'+ +'"),
        pytest.param("+[-[<<[+[--->]-[<<<]]]>>>-]>-.",
                     [TOKEN_INC, TOKEN_OLOOP, TOKEN_DEC, TOKEN_OLOOP, TOKEN_LSHIFT, TOKEN_LSHIFT, TOKEN_OLOOP,
                      TOKEN_INC, TOKEN_OLOOP, TOKEN_DEC, TOKEN_DEC, TOKEN_DEC, TOKEN_RSHIFT, TOKEN_CLOOP, TOKEN_DEC,
                      TOKEN_OLOOP, TOKEN_LSHIFT, TOKEN_LSHIFT, TOKEN_LSHIFT, TOKEN_CLOOP, TOKEN_CLOOP, TOKEN_CLOOP,
                      TOKEN_RSHIFT, TOKEN_RSHIFT, TOKEN_RSHIFT, TOKEN_DEC, TOKEN_CLOOP, TOKEN_RSHIFT, TOKEN_DEC,
                      TOKEN_WB, TOKEN_EOF],
                     id="'+[-[<<[+[--->]-[<<<]]]>>>-]>-.'"),
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

        with pytest.raises(LexerError) as exc_info:
            lexer.tokenize(text)

        assert f"Unknown token (lexeme={unknown_lexeme})" == str(exc_info.value)

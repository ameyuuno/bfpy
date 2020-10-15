import typing as t

import pytest

from bfpy.lexer.lexer import LexerImpl, LexicalError
from bfpy.lexer.token import Token, TokenType, Lexeme


class TestLexerImpl:
    TOKEN_LSHIFT = Token(Lexeme("<"), TokenType.LSHIFT)
    TOKEN_RSHIFT = Token(Lexeme(">"), TokenType.RSHIFT)
    TOKEN_INC = Token(Lexeme("+"), TokenType.INC)
    TOKEN_DEC = Token(Lexeme("-"), TokenType.DEC)
    TOKEN_RB = Token(Lexeme(","), TokenType.RB)
    TOKEN_WB = Token(Lexeme("."), TokenType.WB)
    TOKEN_OLOOP = Token(Lexeme("["), TokenType.OLOOP)
    TOKEN_CLOOP = Token(Lexeme("]"), TokenType.CLOOP)

    @pytest.mark.parametrize("text, expected_tokens", [
        pytest.param("<", [TOKEN_LSHIFT], id="'<'"),
        pytest.param(">", [TOKEN_RSHIFT], id="'>'"),
        pytest.param("+", [TOKEN_INC], id="'+'"),
        pytest.param("-", [TOKEN_DEC], id="'-'"),
        pytest.param(",", [TOKEN_RB], id="','"),
        pytest.param(".", [TOKEN_WB], id="'.'"),
        pytest.param("[", [TOKEN_OLOOP], id="'['"),
        pytest.param("]", [TOKEN_CLOOP], id="']'"),
        pytest.param(" ", [], id="' '"),
        pytest.param("\t", [], id="'\t'"),
        pytest.param("\n", [], id="'\n'"),
        pytest.param("", [], id="'EOF'"),
        pytest.param("++", [TOKEN_INC, TOKEN_INC], id="'++'"),
        pytest.param("+ +", [TOKEN_INC, TOKEN_INC], id="'+ +'"),
        pytest.param("+[-[<<[+[--->]-[<<<]]]>>>-]>-.",
                     [TOKEN_INC, TOKEN_OLOOP, TOKEN_DEC, TOKEN_OLOOP, TOKEN_LSHIFT, TOKEN_LSHIFT, TOKEN_OLOOP,
                      TOKEN_INC, TOKEN_OLOOP, TOKEN_DEC, TOKEN_DEC, TOKEN_DEC, TOKEN_RSHIFT, TOKEN_CLOOP, TOKEN_DEC,
                      TOKEN_OLOOP, TOKEN_LSHIFT, TOKEN_LSHIFT, TOKEN_LSHIFT, TOKEN_CLOOP, TOKEN_CLOOP, TOKEN_CLOOP,
                      TOKEN_RSHIFT, TOKEN_RSHIFT, TOKEN_RSHIFT, TOKEN_DEC, TOKEN_CLOOP, TOKEN_RSHIFT, TOKEN_DEC,
                      TOKEN_WB],
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

        with pytest.raises(LexicalError) as exc_info:
            lexer.tokenize(text)

        assert f"Unknown token (lexeme={unknown_lexeme})" == str(exc_info.value)

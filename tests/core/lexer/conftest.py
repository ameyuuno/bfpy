import pytest

from bfpy.core.lexer.lexer import Lexer, LexerImpl


@pytest.fixture
def lexer() -> Lexer:
    return LexerImpl()

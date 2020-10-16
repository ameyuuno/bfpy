import pytest

from bfpy.core.lexer.lexer import Lexer, LexerImpl


@pytest.fixture  # type: ignore
def lexer() -> Lexer:
    return LexerImpl()

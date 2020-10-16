import pytest

from bfpy.core.parser.parser import Parser, ParserImpl


@pytest.fixture
def parser() -> Parser:
    return ParserImpl()

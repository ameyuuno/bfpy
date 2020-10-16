import pytest

from bfpy.core.parser.parser import Parser, ParserImpl


@pytest.fixture  # type: ignore
def parser() -> Parser:
    return ParserImpl()

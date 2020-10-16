import pytest

from bfpy.core.il.translator import Translator, TranslatorImpl


@pytest.fixture  # type: ignore
def translator() -> Translator:
    return TranslatorImpl()

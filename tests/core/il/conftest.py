import pytest

from bfpy.core.il.translator import Translator, TranslatorImpl


@pytest.fixture
def translator() -> Translator:
    return TranslatorImpl()

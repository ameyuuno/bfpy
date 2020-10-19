import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.core.il.translator import TranslatorImpl
from bfpy.core.interpreter.interpreter import InterpreterImpl
from bfpy.core.interpreter.tape import FiniteTape
from bfpy.core.lexer.lexer import LexerImpl
from bfpy.core.machine.machine import Machine, MachineImpl
from bfpy.core.parser.parser import ParserImpl


@pytest.fixture
def input_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def output_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def machine() -> Machine:
    lexer = LexerImpl()
    parser = ParserImpl()
    translator = TranslatorImpl()
    interpreter = InterpreterImpl(FiniteTape())

    return MachineImpl(lexer, parser, translator, interpreter)

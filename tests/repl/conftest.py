import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.core.il.translator import TranslatorImpl
from bfpy.core.interpreter.interpreter import InterpreterImpl
from bfpy.core.interpreter.tape import FiniteTape
from bfpy.core.lexer.lexer import LexerImpl
from bfpy.core.machine.machine import MachineImpl
from bfpy.core.parser.parser import ParserImpl
from bfpy.repl.repl import Repl, ReplImpl


@pytest.fixture
def reader_byte_stream(request: SubRequest) -> io.BytesIO:
    if not hasattr(request, "param"):
        return io.BytesIO()

    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def writer_byte_stream(request: SubRequest) -> io.BytesIO:
    if not hasattr(request, "param"):
        return io.BytesIO()

    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def reader(reader_byte_stream: io.BytesIO) -> t.TextIO:
    return io.TextIOWrapper(reader_byte_stream)


@pytest.fixture
def writer(writer_byte_stream: io.BytesIO) -> t.TextIO:
    return io.TextIOWrapper(writer_byte_stream, write_through=True)


@pytest.fixture
def repl() -> Repl:
    return ReplImpl(
        MachineImpl(
            LexerImpl(),
            ParserImpl(),
            TranslatorImpl(),
            InterpreterImpl(FiniteTape()),
        ),
    )

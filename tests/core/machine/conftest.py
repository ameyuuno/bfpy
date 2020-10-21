import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.core.il.translator import TranslatorImpl
from bfpy.core.interpreter.interpreter import InterpreterImpl
from bfpy.core.interpreter.tape import FiniteTape
from bfpy.core.io.stream import ByteInputStream, ByteOutputStream, BytesBidirectionalStreamOverTextIo
from bfpy.core.lexer.lexer import LexerImpl
from bfpy.core.machine.machine import Machine, MachineImpl
from bfpy.core.parser.parser import ParserImpl


@pytest.fixture
def input_bytes(request: SubRequest) -> io.BytesIO:
    if not hasattr(request, "param"):
        return io.BytesIO()

    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def byte_input_stream(input_bytes: io.BytesIO) -> ByteInputStream:
    return BytesBidirectionalStreamOverTextIo(io.TextIOWrapper(input_bytes))


@pytest.fixture
def output_bytes(request: SubRequest) -> io.BytesIO:
    if not hasattr(request, "param"):
        return io.BytesIO()

    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def byte_output_stream(output_bytes: io.BytesIO) -> ByteOutputStream:
    return BytesBidirectionalStreamOverTextIo(io.TextIOWrapper(output_bytes))


@pytest.fixture
def machine() -> Machine:
    lexer = LexerImpl()
    parser = ParserImpl()
    translator = TranslatorImpl()
    interpreter = InterpreterImpl(FiniteTape())

    return MachineImpl(lexer, parser, translator, interpreter)

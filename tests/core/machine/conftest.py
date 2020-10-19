import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.core.il.translator import TranslatorImpl
from bfpy.core.interpreter.interpreter import InterpreterImpl
from bfpy.core.interpreter.tape import FiniteTape
from bfpy.core.io.stream import BytesBidirectionalStreamOverBinaryIo
from bfpy.core.lexer.lexer import LexerImpl
from bfpy.core.machine.machine import Machine, MachineImpl
from bfpy.core.parser.parser import ParserImpl


@pytest.fixture
def input_bytes(request: SubRequest) -> io.BytesIO:
    if not hasattr(request, "param"):
        return io.BytesIO()

    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def output_bytes(request: SubRequest) -> io.BytesIO:
    if not hasattr(request, "param"):
        return io.BytesIO()

    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def machine(input_bytes: io.BytesIO, output_bytes: io.BytesIO) -> Machine:
    lexer = LexerImpl()
    parser = ParserImpl()
    translator = TranslatorImpl()
    interpreter = InterpreterImpl(FiniteTape())

    input_stream = BytesBidirectionalStreamOverBinaryIo(input_bytes)
    output_stream = BytesBidirectionalStreamOverBinaryIo(output_bytes)

    return MachineImpl(lexer, parser, translator, interpreter, input_stream, output_stream)

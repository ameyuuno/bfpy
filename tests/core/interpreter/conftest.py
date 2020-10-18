import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.core.interpreter.interpreter import Interpreter, InterpreterImpl
from bfpy.core.interpreter.tape import FiniteTape
from bfpy.core.io.stream import ByteInputStream, ByteOutputStream, BytesBidirectionalStreamOverBinaryIo


@pytest.fixture
def input_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def input_stream(input_bytes: io.BytesIO) -> ByteInputStream:
    return BytesBidirectionalStreamOverBinaryIo(input_bytes)


@pytest.fixture
def output_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def output_stream(output_bytes: io.BytesIO) -> ByteOutputStream:
    return BytesBidirectionalStreamOverBinaryIo(output_bytes)


@pytest.fixture(params=[lambda: InterpreterImpl(FiniteTape())])
def interpreter(request: SubRequest) -> Interpreter:
    interpreter_builder: t.Callable[[], Interpreter] = request.param

    return interpreter_builder()

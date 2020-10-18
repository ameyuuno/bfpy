import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.core.interpreter.interpreter import Interpreter, InterpreterImpl
from bfpy.core.interpreter.tape import FiniteTape
from bfpy.core.io.stream import ByteInputStream, BytesBidirectionalStreamOverTextIo


@pytest.fixture
def input_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def input_stream(input_bytes: io.BytesIO) -> ByteInputStream:
    return BytesBidirectionalStreamOverTextIo(io.TextIOWrapper(input_bytes))  # type: ignore


@pytest.fixture
def output_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def output_stream(output_bytes: io.BytesIO) -> ByteInputStream:
    return BytesBidirectionalStreamOverTextIo(io.TextIOWrapper(output_bytes))  # type: ignore


@pytest.fixture(params=[InterpreterImpl(FiniteTape())])
def interpreter(request: SubRequest) -> Interpreter:
    return t.cast(Interpreter, request.param)

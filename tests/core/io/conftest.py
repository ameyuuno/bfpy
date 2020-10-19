import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.core.io.stream import ByteInputStream, ByteOutputStream, BytesBidirectionalStreamOverBinaryIo


@pytest.fixture
def input_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def byte_input_stream(input_bytes: io.BytesIO) -> ByteInputStream:
    return BytesBidirectionalStreamOverBinaryIo(input_bytes)


@pytest.fixture
def output_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def byte_output_stream(output_bytes: io.BytesIO) -> ByteOutputStream:
    return BytesBidirectionalStreamOverBinaryIo(output_bytes)

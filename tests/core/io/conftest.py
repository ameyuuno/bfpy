import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest
from _pytest.mark import Mark

from bfpy.core.io.stream import ByteInputStream, BytesBidirectionalStreamOverTextIo, ByteOutputStream


@pytest.fixture
def input_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture(params=[BytesBidirectionalStreamOverTextIo])
def byte_input_stream(request: SubRequest, input_bytes: io.BytesIO) -> ByteInputStream:
    stream_type: t.Type[ByteInputStream] = request.param

    if stream_type == BytesBidirectionalStreamOverTextIo:
        return BytesBidirectionalStreamOverTextIo(io.TextIOWrapper(input_bytes))  # type: ignore

    raise ValueError("Can not build an instance of unknown implementation of byte input stream.")


@pytest.fixture
def output_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture(params=[BytesBidirectionalStreamOverTextIo])
def byte_output_stream(request: SubRequest, output_bytes: io.BytesIO) -> ByteOutputStream:
    stream_type: t.Type[ByteOutputStream] = request.param

    if stream_type == BytesBidirectionalStreamOverTextIo:
        return BytesBidirectionalStreamOverTextIo(io.TextIOWrapper(output_bytes))  # type: ignore

    raise ValueError("Can not build an instance of unknown implementation of byte output stream.")

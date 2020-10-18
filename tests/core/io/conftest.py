import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest
from _pytest.mark import Mark

from bfpy.core.io.stream import ByteInputStream, BytesBidirectionalStreamOverTextIo, ByteOutputStream


@pytest.fixture(params=[BytesBidirectionalStreamOverTextIo])
def byte_input_stream(request: SubRequest) -> ByteInputStream:
    stream_type: t.Type[ByteInputStream] = request.param
    marker: t.Optional[Mark] = request.node.get_closest_marker("source_bytes")
    if marker is None:
        raise ValueError("Missing required source bytes to build `byte_input_stream` fixture")

    source_bytes: t.ByteString = marker.args[0]

    if stream_type == BytesBidirectionalStreamOverTextIo:
        text_io = io.StringIO(bytearray(source_bytes).decode())

        # ? NOTE: MyPy raises an error with message that `io.StringIO` is incompatible with `io.TextIOBase`.
        # ?     It is strange because Python's documentation tells that "It (io.StringIO) inherits TextIOBase."
        # ?     https://docs.python.org/3/library/io.html#io.StringIO
        # ?     It seems like a false-positive error of MyPy, so just suppressed it.
        return BytesBidirectionalStreamOverTextIo(text_io)  # type: ignore

    raise ValueError("Can not build an instance of unknown implementation of byte input stream.")


@pytest.fixture
def collected_written_bytes() -> io.BytesIO:
    return io.BytesIO()


@pytest.fixture(params=[BytesBidirectionalStreamOverTextIo])
def byte_output_stream(request: SubRequest, collected_written_bytes: io.BytesIO) -> ByteOutputStream:
    stream_type: t.Type[ByteOutputStream] = request.param

    if stream_type == BytesBidirectionalStreamOverTextIo:
        text_io = io.TextIOWrapper(collected_written_bytes)

        # ? NOTE: MyPy raises an error with message that `io.StringIO` is incompatible with `io.TextIOBase`.
        # ?     It is strange because Python's documentation tells that "It (io.StringIO) inherits TextIOBase."
        # ?     https://docs.python.org/3/library/io.html#io.StringIO
        # ?     It seems like a false-positive error of MyPy, so just suppressed it.
        return BytesBidirectionalStreamOverTextIo(text_io)  # type: ignore

    raise ValueError("Can not build an instance of unknown implementation of byte output stream.")

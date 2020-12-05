import io
import typing as t

import pytest

from bfpy.core.io.stream import ByteInputStream, ByteOutputStream, IoError


class TestByteInputStream:
    @pytest.mark.parametrize("input_bytes", [io.BytesIO()], indirect=True)
    def test_read_from_empty_stream(self, byte_input_stream: ByteInputStream, input_bytes: io.BytesIO) -> None:
        expected_byte = 0
        actual_byte = byte_input_stream.read()

        assert actual_byte == expected_byte

    @pytest.mark.parametrize("expected_read_bytes, input_bytes", [
        pytest.param(
            b"",
            io.BytesIO(b""),
            id="Empty byte string",
        ),
        pytest.param(
            b"Hello, World!",
            io.BytesIO(b"Hello, World!"),
            id="Hello, World!",
        ),
    ], indirect=["input_bytes"])
    def test_read_from_non_empty_stream(self, byte_input_stream: ByteInputStream, expected_read_bytes: t.ByteString,
                                        input_bytes: io.BytesIO) -> None:
        actual_read_bytes = bytearray(byte_input_stream.read() for _ in range(len(expected_read_bytes)))

        assert actual_read_bytes == expected_read_bytes


class TestByteOutputStream:
    @pytest.mark.parametrize("expected_written_bytes, output_bytes", [
        pytest.param(
            b"",
            io.BytesIO(),
            id="Empty byte string",
        ),
        pytest.param(
            b"Hello, World!",
            io.BytesIO(),
            id="'Hello, World!'",
        ),
    ], indirect=["output_bytes"])
    def test_write(self, byte_output_stream: ByteOutputStream, expected_written_bytes: t.ByteString,
                   output_bytes: io.BytesIO) -> None:
        for byte in expected_written_bytes:
            byte_output_stream.write(byte)

        assert output_bytes.getvalue() == expected_written_bytes

    @pytest.mark.parametrize("non_byte, output_bytes", [
        pytest.param(
            -1,
            io.BytesIO(),
            id="Negative integer"
        ),
        pytest.param(
            256,
            io.BytesIO(),
            id="Integer which is greater than 255"
        ),
    ])
    def test_can_not_write_non_byte_integer(self, byte_output_stream: ByteOutputStream, non_byte: int,
                                            output_bytes: io.BytesIO) -> None:
        with pytest.raises(IoError) as exc_info:
            byte_output_stream.write(non_byte)

        assert str(exc_info.value) == "Byte should be in range [0, 255]"
        assert output_bytes.getvalue() == b""

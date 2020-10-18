import io
import typing as t

import pytest

from bfpy.core.io.stream import ByteInputStream, ByteOutputStream, IoError


class TestByteInputStream:
    _BYTES_EMPTY = b""
    _BYTES_HELLO_WORLD = b"Hello, World!"

    @pytest.mark.source_bytes(_BYTES_EMPTY)
    def test_read_from_empty_stream(self, byte_input_stream: ByteInputStream) -> None:
        with pytest.raises(IoError) as exc_info:
            byte_input_stream.read()

        assert str(exc_info.value) == "Can not read byte from empty byte input stream"

    @pytest.mark.source_bytes(_BYTES_HELLO_WORLD)
    def test_read_from_non_empty_stream(self, byte_input_stream: ByteInputStream) -> None:
        actual_read_bytes = bytearray(byte_input_stream.read() for _ in range(len(self._BYTES_HELLO_WORLD)))

        assert actual_read_bytes == self._BYTES_HELLO_WORLD


class TestByteOutputStream:
    @pytest.mark.parametrize("writing_bytes", [
        pytest.param(b"", id="Empty byte string"),
        pytest.param(b"Hello, World!", id="'Hello, World!'"),
    ])
    def test_write(self, byte_output_stream: ByteOutputStream, collected_written_bytes: io.BytesIO,
                   writing_bytes: t.ByteString) -> None:
        for byte in writing_bytes:
            byte_output_stream.write(byte)

        assert collected_written_bytes.getvalue() == writing_bytes

    @pytest.mark.parametrize("non_byte", [
        pytest.param(-1, id="Negative integer"),
        pytest.param(256, id="Integer which is greater than 255")
    ])
    def test_can_not_write_non_byte_integer(self, byte_output_stream: ByteOutputStream,
                                            collected_written_bytes: io.BytesIO, non_byte: int) -> None:
        with pytest.raises(IoError) as exc_info:
            byte_output_stream.write(non_byte)

        assert str(exc_info.value) == "Byte should be in range [0, 255]"
        assert collected_written_bytes.getvalue() == b""

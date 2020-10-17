import pytest

from bfpy.core.io.stream import ByteInputStream, IoError


class TestByteInputStream:
    _SOURCE_EMPTY = b""
    _SOURCE_HELLO_WORLD = b"Hello, World!"

    @pytest.mark.source_bytes(_SOURCE_EMPTY)
    def test_read_from_empty_stream(self, byte_input_stream: ByteInputStream) -> None:
        with pytest.raises(IoError) as exc_info:
            byte_input_stream.read()

        assert str(exc_info.value) == "Can not read byte from empty byte input stream"

    @pytest.mark.source_bytes(_SOURCE_HELLO_WORLD)
    def test_read_from_non_empty_stream(self, byte_input_stream: ByteInputStream) -> None:
        actual_read_bytes = bytearray(byte_input_stream.read() for _ in range(len(self._SOURCE_HELLO_WORLD)))

        assert actual_read_bytes == self._SOURCE_HELLO_WORLD

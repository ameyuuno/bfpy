import io
import typing as t

import pytest

from bfpy.repl.repl import Repl


class TestRepl:
    @pytest.mark.parametrize("expected_repl_output, expected_output_bytes, reader, writer, input_bytes, output_bytes", [
        pytest.param(
            "bfpy> ",
            b"",
            io.StringIO("\\q\n"),
            io.StringIO(),
            io.BytesIO(b""),
            io.BytesIO(),
            id="",
        ),
        pytest.param(
            "bfpy> \nbfpy> ",
            b"",
            io.StringIO("+\n\\q\n"),
            io.StringIO(),
            io.BytesIO(b""),
            io.BytesIO(),
            id="+",
        ),
        pytest.param(
            "bfpy> \nbfpy> ",
            b"\n",
            io.StringIO("++++++++++.\n\\q\n"),
            io.StringIO(),
            io.BytesIO(b""),
            io.BytesIO(),
            id="++++++++++.",
        ),
    ], indirect=["input_bytes", "output_bytes"])
    def test_run(self, expected_repl_output: t.Text, expected_output_bytes: t.ByteString,
                 repl: Repl, reader: io.StringIO, writer: io.StringIO,
                 input_bytes: io.BytesIO, output_bytes: io.BytesIO) -> None:
        repl.run(reader, writer)

        assert writer.getvalue() == expected_repl_output
        assert output_bytes.getvalue() == expected_output_bytes

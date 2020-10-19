import io
import typing as t

import pytest

from bfpy.core.machine.machine import Machine


class TestMachine:
    @pytest.mark.parametrize("code, expected_output, input_bytes, output_bytes", [
        pytest.param(
            "",
            b"",
            io.BytesIO(),
            io.BytesIO(),
        ),
        pytest.param(
            "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++"
            "..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.",
            b"Hello World!\n",
            io.BytesIO(),
            io.BytesIO(),
        ),
        pytest.param(
            ",[.,]",
            b"It is cat program.",
            io.BytesIO(b"It is cat program."),
            io.BytesIO(),
        ),
    ], indirect=["input_bytes", "output_bytes"])
    def test_execute(self, machine: Machine, code: t.Text, expected_output: t.ByteString,
                     input_bytes: io.BytesIO, output_bytes: io.BytesIO) -> None:
        machine.execute(code)

        assert output_bytes.getvalue() == expected_output

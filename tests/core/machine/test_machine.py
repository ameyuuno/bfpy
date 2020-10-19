import io
import typing as t

import pytest

from bfpy.core.machine.machine import Machine, MachineError


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

    @pytest.mark.parametrize("code, expected_error", [
        pytest.param(
            "++-.)",
            MachineError("Lexical error"),
        ),
        pytest.param(
            "++-.)",
            MachineError("Lexical error"),
        ),
        pytest.param(
            "--+=++[-]",
            MachineError("Lexical error"),
        ),
        pytest.param(
            "--+]++[-]",
            MachineError("Syntax error"),
        ),
        pytest.param(
            ".+>++[-",
            MachineError("Syntax error"),
        ),
        pytest.param(
            "<.+>++[-]",
            MachineError("Evaluation error"),
        ),
    ])
    def test_execute_invalid_code(self, machine: Machine, code: t.Text, expected_error: Exception) -> None:
        with pytest.raises(type(expected_error)) as exc_info:
            machine.execute(code)

        assert str(expected_error) in str(exc_info)

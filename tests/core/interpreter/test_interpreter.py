import io
import typing as t

import pytest

from bfpy.core.il.operation import Program, Addition, Subtraction, LeftShift, RightShift, WriteByte, Loop, ReadByte
from bfpy.core.interpreter.interpreter import Interpreter
from bfpy.core.io.stream import ByteInputStream, ByteOutputStream


class TestInterpreter:
    @pytest.mark.parametrize("program, input_bytes, output_bytes, expected_output", [
        pytest.param(
            Program([]),
            io.BytesIO(),
            io.BytesIO(),
            b"",
            id="Empty program"
        ),
        pytest.param(
            Program([
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                WriteByte(),
            ]),
            io.BytesIO(),
            io.BytesIO(),
            b"#",
            id="+++++++++++++++++++++++++++++++++++."
        ),
        pytest.param(
            Program([
                Addition(35),
                WriteByte(),
            ]),
            io.BytesIO(),
            io.BytesIO(),
            b"#",
            id="+(35)."
        ),
        pytest.param(
            Program([
                Subtraction(130),
                WriteByte(),
            ]),
            io.BytesIO(),
            io.BytesIO(),
            b"~",
            id="-(130)."
        ),
        pytest.param(
            Program([
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Loop([
                    RightShift(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    RightShift(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    RightShift(1),
                    Addition(1),
                    Addition(1),
                    Addition(1),
                    RightShift(1),
                    Addition(1),
                    LeftShift(1),
                    LeftShift(1),
                    LeftShift(1),
                    LeftShift(1),
                    Subtraction(1),
                ]),
                RightShift(1),
                Addition(1),
                Addition(1),
                WriteByte(),
                RightShift(1),
                Addition(1),
                WriteByte(),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                WriteByte(),
                WriteByte(),
                Addition(1),
                Addition(1),
                Addition(1),
                WriteByte(),
                RightShift(1),
                Addition(1),
                Addition(1),
                WriteByte(),
                LeftShift(1),
                LeftShift(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                Addition(1),
                WriteByte(),
                RightShift(1),
                WriteByte(),
                Addition(1),
                Addition(1),
                Addition(1),
                WriteByte(),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                WriteByte(),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                Subtraction(1),
                WriteByte(),
                RightShift(1),
                Addition(1),
                WriteByte(),
                RightShift(1),
                WriteByte(),
            ]),
            io.BytesIO(),
            io.BytesIO(),
            b"Hello World!\n",
            id="++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.------"
               "--.>+.>."
        ),
        pytest.param(
            Program([
                ReadByte(),
                WriteByte(),
            ]),
            io.BytesIO(b"1"),
            io.BytesIO(),
            b"1",
            id=",."
        ),
    ], indirect=["input_bytes", "output_bytes"])
    def test_evaluate(self, interpreter: Interpreter, program: Program, expected_output: t.ByteString,
                      input_stream: ByteInputStream, output_stream: ByteOutputStream,
                      input_bytes: io.BytesIO, output_bytes: io.BytesIO) -> None:
        interpreter.evaluate(input_stream, output_stream, program)

        assert output_bytes.getvalue() == expected_output

import io
import typing as t

import pytest

from bfpy.repl.repl import Repl


class TestRepl:
    @pytest.mark.parametrize("expected_repl_output, reader_byte_stream, writer_byte_stream", [
        pytest.param(
            "bfpy> ",
            io.BytesIO(b"\\q\n"),
            io.BytesIO(),
            id="(Quit ASAP)",
        ),
        pytest.param(
            ("bfpy> "
             "\n"
             "bfpy> "),
            io.BytesIO(b"+\n\\q\n"),
            io.BytesIO(),
            id="+",
        ),
        pytest.param(
            ("bfpy> "
             "\n"
             "\n"
             "bfpy> "),
            io.BytesIO(b"++++++++++.\n\\q\n"),
            io.BytesIO(),
            id="++++++++++.",
        ),
        pytest.param(
            ("bfpy> "
             "Hello World!\n"
             "\n"
             "bfpy> "),
            io.BytesIO("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++"
                       "..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
                       "\n\\q\n".encode()),
            io.BytesIO(),
            id="(Hello World!)",
        ),
        pytest.param(
            ("bfpy> "
             "bfpy| "
             "bfpy| "
             "Hello World!\n"
             "\n"
             "bfpy> "),
            io.BytesIO("++++++++++[>+++++++>++++++++++>\\\n"
                       "+++>+<<<<-]>++.>+.+++++++ \\\n"
                       "..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.\n"
                       "\\q\n".encode()),
            io.BytesIO(),
            id="(Hello World!) with line breakers",
        ),
        pytest.param(
            ("bfpy> "
             "a b c d e"
             "\n"
             "bfpy> "),
            io.BytesIO("+++++++++>,<[>.,<-]\n"
                       "a b c d e\n"
                       "\\q\n".encode()),
            io.BytesIO(),
            id="+++++++++>,<[>.,<-]",
        ),
    ], indirect=["reader_byte_stream", "writer_byte_stream"])
    def test_run(self, expected_repl_output: t.Text, repl: Repl, reader: t.TextIO, writer: t.TextIO,
                 reader_byte_stream: io.BytesIO, writer_byte_stream: io.BytesIO) -> None:
        repl.run(reader, writer)

        assert writer_byte_stream.getvalue().decode() == expected_repl_output

    @pytest.mark.parametrize("expected_error_in_repl, reader_byte_stream, writer_byte_stream", [
        pytest.param(
            "Lexical error",
            io.BytesIO(b"++-.)\n\\q\n"),
            io.BytesIO(),
            id="++-.) - Lexical error",
        ),
        pytest.param(
            "Lexical error",
            io.BytesIO(b"++-.)\n\\q\n"),
            io.BytesIO(),
            id="++-.) - Lexical error",
        ),
        pytest.param(
            "Lexical error",
            io.BytesIO(b"--+=++[-]\n\\q\n"),
            io.BytesIO(),
            id="--+=++[-] - Lexical error",
        ),
        pytest.param(
            "Syntax error",
            io.BytesIO(b"--+]++[-]\n\\q\n"),
            io.BytesIO(),
            id="--+]++[-] - Syntax error",
        ),
        pytest.param(
            "Syntax error",
            io.BytesIO(b".+>++[-\n\\q\n"),
            io.BytesIO(),
            id=".+>++[- - Syntax error",
        ),
        pytest.param(
            "Evaluation error",
            io.BytesIO(b"<.+>++[-]\n\\q\n"),
            io.BytesIO(),
            id="<.+>++[-] - Evaluation error",
        ),
    ], indirect=["reader_byte_stream", "writer_byte_stream"])
    def test_run_with_invalid_code(self, expected_error_in_repl: t.Text, repl: Repl, reader: t.TextIO, writer: t.TextIO,
                                   reader_byte_stream: io.BytesIO, writer_byte_stream: io.BytesIO) -> None:
        repl.run(reader, writer)

        assert expected_error_in_repl in writer_byte_stream.getvalue().decode()

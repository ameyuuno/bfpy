import typing as t

import pytest
from click import Command
from click.testing import CliRunner


CODE_HELLO_WORLD = """
++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++
..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.
""".strip()


CODE_CAT = """
,[.,]
""".strip()


CODE_FIBONACCI = """
+++++++++++
>+>>>>++++++++++++++++++++++++++++++++++++++++++++
>++++++++++++++++++++++++++++++++<<<<<<[>[>>>>>>+>
+<<<<<<<-]>>>>>>>[<<<<<<<+>>>>>>>-]<[>++++++++++[-
<-[>>+>+<<<-]>>>[<<<+>>>-]+<[>[-]<[-]]>[<<[>>>+<<<
-]>>[-]]<<]>>>[>>+>+<<<-]>>>[<<<+>>>-]+<[>[-]<[-]]
>[<<+>>[-]]<<<<<<<]>>>>>[+++++++++++++++++++++++++
+++++++++++++++++++++++.[-]]++++++++++<[->-<]>++++
++++++++++++++++++++++++++++++++++++++++++++.[-]<<
<<<<<<<<<<[>>>+>+<<<<-]>>>>[<<<<+>>>>-]<-[>>.>.<<<
[-]]<<[>>+>+<<<-]>>>[<<<+>>>-]<<[<+>-]>[<+>-]<<<-]
""".strip()


class TestCli:
    @pytest.mark.parametrize("code, input_, expected_output, expected_exit_code", [
        pytest.param(
            CODE_HELLO_WORLD,
            "",
            "Hello World!\n",
            0,
            id="Hello, World!",
        ),
        pytest.param(
            CODE_CAT,
            "It is a cat program!",
            "It is a cat program!",
            0,
            id="cat",
        ),
        pytest.param(
            CODE_FIBONACCI,
            "",
            "1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89",
            0,
            id="Fibonacci's numbers < 100",
        ),
    ])
    def test_run_code_as_option(self, code: t.Text, input_: t.Text, expected_output: t.Text, expected_exit_code: int,
                                cli: Command, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["run", "--code", code], input=input_)

        assert result.output == expected_output
        assert result.exit_code == 0

    def test_repl(self, cli: Command, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["repl"], input=",.\na\n\\q\n")

        assert result.output == ("bfpy> a\n"
                                 "bfpy> \n"
                                 "bfpy> ")
        assert result.exit_code == 0

__all__ = ["run"]

import contextlib
import pathlib as pth
import sys
import typing as t

import click
from click import UsageError

from bfpy.core.il.translator import TranslatorImpl
from bfpy.core.interpreter.interpreter import InterpreterImpl
from bfpy.core.interpreter.tape import FiniteTape
from bfpy.core.io.stream import BytesBidirectionalStreamOverTextIo
from bfpy.core.lexer.lexer import LexerImpl
from bfpy.core.machine.machine import Machine, MachineImpl
from bfpy.core.parser.parser import ParserImpl


# NOTE: Mark all `click`'s decorators as ignored for MyPy, because they use `Any` in type annotations.
@click.command()  # type: ignore
@click.argument("file", type=click.Path(), required=False)  # type: ignore
@click.option("--code", "program", type=str, required=False)  # type: ignore
@click.option("--input", "input_", type=click.Path(), required=False)  # type: ignore
@click.option('--output', type=click.Path(), required=False)  # type: ignore
def run(file: t.Optional[t.Text], program: t.Optional[t.Text],
        input_: t.Optional[t.Text], output: t.Optional[t.Text]) -> None:
    """Run brainfuck code."""
    if (file is None) == (program is None):
        raise UsageError("Define either file argument or code option! Run `bfpy run --help` for more information.")

    machine = _create_machine()

    with _open_if_presented(input_, "r", sys.stdin) as fin, _open_if_presented(output, "w", sys.stdout) as fout:
        input_stream = BytesBidirectionalStreamOverTextIo(fin)
        output_stream = BytesBidirectionalStreamOverTextIo(fout)

        # NOTE: Obviously in this section of function either file is defined or code which is passed via option,
        #   and it is impossible that this expression can be evaluated as `None`. But MyPy raises an error
        #   `Argument 3 to "execute" of "Machine" has incompatible type "Optional[str]"; expected "str"`.
        code = t.cast(t.Text, _read_code(file) if file is not None else program)

        machine.execute(input_stream, output_stream, code)


# NOTE: type annotation of context manager contains `Any`, but MyPy disallows dynamic typing.
@contextlib.contextmanager  # type: ignore
def _open_if_presented(file: t.Optional[t.Text], mode: t.Text, default: t.TextIO) -> t.Iterator[t.TextIO]:
    if file is None:
        yield default

    else:
        # NOTE: Add casting, because `open` returns `IO[Any]`, but MyPy disallows dynamic typing.
        with t.cast(t.TextIO, open(file, mode)) as f:
            yield f


def _read_code(file: t.Text) -> t.Text:
    with pth.Path(file).open() as fin:
        return "".join(line for line in fin)


def _create_machine() -> Machine:
    return MachineImpl(
        LexerImpl(),
        ParserImpl(),
        TranslatorImpl(),
        InterpreterImpl(FiniteTape()),
    )

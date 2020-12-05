__all__ = ["repl"]

import sys

import click

from bfpy.core.il.translator import TranslatorImpl
from bfpy.core.interpreter.interpreter import InterpreterImpl
from bfpy.core.interpreter.tape import FiniteTape
from bfpy.core.lexer.lexer import LexerImpl
from bfpy.core.machine.machine import MachineImpl
from bfpy.core.parser.parser import ParserImpl
from bfpy.repl.repl import ReplImpl


@click.command()  # type: ignore
def repl() -> None:
    """Run brainfuck REPL."""
    ReplImpl(
        MachineImpl(
            LexerImpl(),
            ParserImpl(),
            TranslatorImpl(),
            InterpreterImpl(FiniteTape()),
        )
    ).run(sys.stdin, sys.stdout)

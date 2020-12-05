__all__ = ["run_cli"]

import click

from bfpy.cli.repl import repl
from bfpy.cli.run import run


@click.group()  # type: ignore
def run_cli() -> None:
    pass


run_cli.add_command(run)
run_cli.add_command(repl)

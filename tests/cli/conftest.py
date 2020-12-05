import pytest
from click import Command
from click.testing import CliRunner

from bfpy.cli import run_cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def cli() -> Command:
    return run_cli

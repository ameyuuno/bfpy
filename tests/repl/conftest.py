import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.repl.repl import Repl


@pytest.fixture
def input_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def output_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def repl() -> Repl:
    raise NotImplementedError

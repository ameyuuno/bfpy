import io
import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.core.machine.machine import Machine


@pytest.fixture
def input_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def output_bytes(request: SubRequest) -> io.BytesIO:
    return t.cast(io.BytesIO, request.param)


@pytest.fixture
def machine() -> Machine:
    raise NotImplementedError

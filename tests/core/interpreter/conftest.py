import typing as t

import pytest
from _pytest.fixtures import SubRequest

from bfpy.core.interpreter.tape import Tape, FiniteTape


@pytest.fixture(params=[FiniteTape()])
def tape(request: SubRequest) -> Tape:
    return t.cast(Tape, request.param)

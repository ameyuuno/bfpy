import typing as t

import pytest
from _pytest.fixtures import SubRequest
from _pytest.mark import Mark

from bfpy.core.interpreter.tape import Tape, FiniteTape


@pytest.fixture
def finite_tape(request: SubRequest) -> Tape:
    marker: t.Optional[Mark] = request.node.get_closest_marker("finite_tape_length")
    finite_tape_length = marker.args[0] if marker is not None else None

    return FiniteTape(finite_tape_length)


@pytest.fixture(params=[FiniteTape()])
def tape(request: SubRequest) -> Tape:
    return t.cast(Tape, request.param)

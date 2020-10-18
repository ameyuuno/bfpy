import typing as t

import pytest

from bfpy.core.interpreter.tape import Tape


class TestTape:
    def test_get(self, tape: Tape) -> None:
        assert tape.get() == 0

    @pytest.mark.parametrize("call_number", [2, 5, 10, 50])
    def test_multiple_call_get(self, tape: Tape, call_number: int) -> None:
        for _ in range(call_number):
            assert tape.get() == 0

    def test_set(self, tape: Tape) -> None:
        tape.set(1)

        assert tape.get() == 1

    @pytest.mark.parametrize("args, expected_value", [
        pytest.param((1, 1), 1),
        pytest.param((1, 2, 3, 4), 4),
        pytest.param((1, 255, 8, 8, 0), 0),
    ])
    def test_multiple_call_set_on_the_same_cell(self, tape: Tape, args: t.Sequence[int], expected_value: int) -> None:
        for arg in args:
            tape.set(arg)

        actual_value = tape.get()

        assert actual_value == expected_value

    def test_shift_left(self, tape: Tape) -> None:
        tape.shift_right(1)
        tape.shift_left(1)

        assert tape.get() == 0

    @pytest.mark.parametrize("step_number", [1, 2, 5, 10, 50])
    def test_multiple_shifts_left_in_one_step(self, tape: Tape, step_number: int) -> None:
        tape.set(10)

        for _ in range(step_number):
            tape.shift_right(1)

        tape.shift_left(step_number)

        assert tape.get() == 10

    @pytest.mark.parametrize("step_number", [1, 2, 5, 10, 50])
    def test_multiple_shifts_right_in_one_step(self, tape: Tape, step_number: int) -> None:
        for _ in range(step_number):
            tape.shift_right(1)

        tape.set(10)

        tape.shift_left(step_number)
        tape.shift_right(step_number)

        assert tape.get() == 10

    def test_shift_right(self, tape: Tape) -> None:
        tape.shift_right(1)

        assert tape.get() == 0

    @pytest.mark.parametrize("scenario, expected_result", [
        pytest.param(
            (
                lambda tape: tape.set(9),
                lambda tape: tape.shift_right(1),
                lambda tape: tape.set(1),
                lambda tape: tape.shift_left(1),
            ),
            9
        ),
        pytest.param(
            (
                    lambda tape: tape.set(9),
                    lambda tape: tape.shift_right(1),
                    lambda tape: tape.shift_left(1),
                    lambda tape: tape.set(90),
                    lambda tape: tape.shift_right(3),
                    lambda tape: tape.shift_left(3),
                    lambda tape: tape.set(78),
                    lambda tape: tape.shift_right(1),
                    lambda tape: tape.shift_left(1),
            ),
            78
        ),
    ])
    def test_general_valid_scenarios(self, tape: Tape, scenario: t.Sequence[t.Callable[[Tape], None]],
                                     expected_result: int) -> None:
        for step in scenario:
            step(tape)

        actual_result = tape.get()

        assert actual_result == expected_result

    def test_set_all_valid_values(self, tape: Tape) -> None:
        for byte in range(0, 256):
            tape.set(byte)

            assert tape.get() == byte

    @pytest.mark.parametrize("invalid_value", [-10000, -1, 256, 1024])
    def test_can_not_set_invalid_value(self, tape: Tape, invalid_value: int) -> None:
        with pytest.raises(ValueError):
            tape.set(invalid_value)

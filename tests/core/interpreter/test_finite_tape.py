import pytest

from bfpy.core.interpreter.tape import FiniteTape, OutOfBoundsError


class TestFiniteTape:
    @pytest.mark.finite_tape_length(5)
    @pytest.mark.parametrize("steps", [1, 2, 5, 10])
    def test_out_of_left_bound(self, finite_tape: FiniteTape, steps: int) -> None:
        with pytest.raises(OutOfBoundsError) as exc_info:
            finite_tape.shift_left(steps)

        assert "Pointer is out of tape bounds" in str(exc_info.value)

    @pytest.mark.finite_tape_length(5)
    @pytest.mark.parametrize("extra_steps", [0, 1, 2, 5, 10])
    def test_out_of_right_bound(self, finite_tape: FiniteTape, extra_steps: int) -> None:
        with pytest.raises(OutOfBoundsError) as exc_info:
            finite_tape.shift_right(10 + extra_steps)

        assert "Pointer is out of tape bounds" in str(exc_info.value)

    def test_out_of_left_bound_error_do_not_change_tape_state(self, finite_tape: FiniteTape) -> None:
        finite_tape.set(1)

        with pytest.raises(OutOfBoundsError):
            finite_tape.shift_left(10)

        assert finite_tape.get() == 1

    @pytest.mark.finite_tape_length(5)
    def test_out_of_right_bound_error_do_not_change_tape_state(self, finite_tape: FiniteTape) -> None:
        finite_tape.set(1)

        with pytest.raises(OutOfBoundsError):
            finite_tape.shift_right(10)

        assert finite_tape.get() == 1

    def test_default_tape_length(self, finite_tape: FiniteTape) -> None:
        finite_tape.shift_right(29_999)

        with pytest.raises(OutOfBoundsError) as exc_info:
            finite_tape.shift_right(1)

        assert "Pointer is out of tape bounds" in str(exc_info.value)

    @pytest.mark.parametrize("tape_length", [0, -1, -10])
    def test_can_not_create_finite_tape_with_invalid_length(self, tape_length: int) -> None:
        with pytest.raises(ValueError) as exc_info:
            FiniteTape(tape_length)

        assert str(exc_info.value) == "Length of finite tape should be >= 0"

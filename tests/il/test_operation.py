import pytest

from bfpy.il.operation import Operation


class TestOperation:
    def test_can_not_create_instance_operation(self) -> None:
        with pytest.raises(TypeError) as exc_info:
            Operation()

        assert "Can not create an instance of class `Operation`" == str(exc_info.value)

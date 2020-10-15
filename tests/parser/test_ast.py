import pytest

from bfpy.parser.ast import AstNode


class TestAstNode:
    def test_ast_node(self) -> None:
        with pytest.raises(TypeError) as exc_info:
            AstNode()

        assert "Can not create an instance of class `AstNode`" == str(exc_info.value)

import pytest

from bfpy.parser.ast import AstNode


class TestAstNode:
    def test_ast_node(self):
        with pytest.raises(TypeError) as exc_info:
            AstNode()

        assert "Can not create an instance" in str(exc_info)

"""赋值解析器测试。"""

import pytest
from jass_runner.parser.parser import Parser


class TestParseCallArgs:
    """测试 _parse_call_args 方法。"""

    def test_parse_call_args_with_nested_call(self):
        """测试解析嵌套函数调用参数。"""
        code = '''
        function main takes nothing returns nothing
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
        endfunction
        '''
        parser = Parser(code)
        ast = parser.parse()

        # 获取 set 语句
        func = ast.functions[0]
        set_stmt = func.body[0]

        # 验证参数数量
        assert len(set_stmt.value.args) == 5

        # 验证第一个参数是嵌套调用
        from jass_runner.parser.ast_nodes import NativeCallNode
        assert isinstance(set_stmt.value.args[0], NativeCallNode)
        assert set_stmt.value.args[0].func_name == 'Player'
        assert set_stmt.value.args[0].args == ['0']

        # 验证其他参数
        assert set_stmt.value.args[1] == '1213484355'
        assert set_stmt.value.args[2] == '100.0'
        assert set_stmt.value.args[3] == '200.0'
        assert set_stmt.value.args[4] == '0.0'

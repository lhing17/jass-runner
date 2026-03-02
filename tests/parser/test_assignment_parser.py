"""赋值解析器测试。"""

import pytest
from jass_runner.parser.parser import Parser
from jass_runner.parser.ast_nodes import NativeCallNode


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
        assert isinstance(set_stmt.value.args[0], NativeCallNode)
        assert set_stmt.value.args[0].func_name == 'Player'
        assert set_stmt.value.args[0].args == ['0']

        # 验证其他参数
        assert set_stmt.value.args[1] == '1213484355'
        assert set_stmt.value.args[2] == '100.0'
        assert set_stmt.value.args[3] == '200.0'
        assert set_stmt.value.args[4] == '0.0'

    def test_parse_local_declaration_with_nested_call(self):
        """测试 local 声明支持嵌套函数调用。"""
        code = '''
        function main takes nothing returns nothing
            local unit u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
        endfunction
        '''
        parser = Parser(code)
        ast = parser.parse()

        # 获取 local 声明
        func = ast.functions[0]
        local_decl = func.body[0]

        # 验证参数数量
        assert len(local_decl.value.args) == 5

        # 验证第一个参数是嵌套调用
        assert isinstance(local_decl.value.args[0], NativeCallNode)
        assert local_decl.value.args[0].func_name == 'Player'

    def test_parse_empty_args(self):
        """测试空参数列表。"""
        code = '''
        function main takes nothing returns nothing
            call SomeFunc()
        endfunction
        '''
        parser = Parser(code)
        ast = parser.parse()

        func = ast.functions[0]
        call_stmt = func.body[0]

        assert len(call_stmt.args) == 0

    def test_parse_multiple_nested_calls(self):
        """测试多个嵌套调用。"""
        code = '''
        function main takes nothing returns nothing
            call FuncA(FuncB(1), FuncC(2))
        endfunction
        '''
        parser = Parser(code)
        ast = parser.parse()

        func = ast.functions[0]
        call_stmt = func.body[0]

        assert len(call_stmt.args) == 2
        assert isinstance(call_stmt.args[0], NativeCallNode)
        assert isinstance(call_stmt.args[1], NativeCallNode)

    def test_parse_mixed_args(self):
        """测试混合参数类型。"""
        code = '''
        function main takes nothing returns nothing
            call Func(1, Player(0), "string", 3.14)
        endfunction
        '''
        parser = Parser(code)
        ast = parser.parse()

        func = ast.functions[0]
        call_stmt = func.body[0]

        assert len(call_stmt.args) == 4
        assert call_stmt.args[0] == '1'
        assert call_stmt.args[2] == '"string"'
        assert call_stmt.args[3] == '3.14'

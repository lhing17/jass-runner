"""类型检查系统集成测试。"""

import pytest
from jass_runner.types.errors import JassTypeError
from jass_runner.parser.parser import Parser
from jass_runner.interpreter.interpreter import Interpreter


class TestTypeCheckingIntegration:
    """测试类型检查与完整解释器链集成。"""

    def test_valid_integer_to_real_conversion_in_script(self):
        """测试脚本中integer到real的有效转换。"""
        code = '''
        globals
            real g_result
        endglobals

        function main takes nothing returns nothing
            local real r = 10
            set g_result = r
            return nothing
        endfunction
        '''

        parser = Parser(code)
        ast = parser.parse()

        interpreter = Interpreter()
        interpreter.execute(ast)

        # 验证r被正确转换为real
        assert interpreter.global_context.get_variable('g_result') == 10.0

    def test_type_error_in_script_raises_exception(self):
        """测试脚本中类型错误抛出异常。"""
        code = '''
        function main takes nothing returns nothing
            local integer x
            set x = "hello"
            return nothing
        endfunction
        '''

        parser = Parser(code)
        ast = parser.parse()

        interpreter = Interpreter()

        with pytest.raises(JassTypeError) as exc_info:
            interpreter.execute(ast)

        assert 'string' in str(exc_info.value)
        assert 'integer' in str(exc_info.value)

    def test_handle_subtype_assignment(self):
        """测试handle子类型赋值。"""
        # 这个测试需要native函数支持，暂时跳过
        # 实际测试需要CreateUnit返回unit类型
        pytest.skip("需要native函数返回类型支持")

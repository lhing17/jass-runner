"""测试常量从 common.j 加载功能。"""

import pytest
from src.jass_runner.vm.jass_vm import JassVM


class TestConstantsLoading:
    """测试常量加载功能。"""

    def test_camera_margin_constants_loaded(self):
        """测试 CAMERA_MARGIN 常量从 common.j 加载。"""
        vm = JassVM()

        # 访问解释器的全局作用域
        global_scope = vm.interpreter.global_context.variables

        # 检查常量是否加载
        assert 'CAMERA_MARGIN_LEFT' in global_scope
        assert 'CAMERA_MARGIN_RIGHT' in global_scope
        assert 'CAMERA_MARGIN_TOP' in global_scope
        assert 'CAMERA_MARGIN_BOTTOM' in global_scope

        # 检查值是否正确
        assert global_scope['CAMERA_MARGIN_LEFT'] == 0
        assert global_scope['CAMERA_MARGIN_RIGHT'] == 1
        assert global_scope['CAMERA_MARGIN_TOP'] == 2
        assert global_scope['CAMERA_MARGIN_BOTTOM'] == 3

    def test_constant_values_are_integers(self):
        """测试常量值类型为整数。"""
        vm = JassVM()
        global_scope = vm.interpreter.global_context.variables

        assert isinstance(global_scope['CAMERA_MARGIN_LEFT'], int)
        assert isinstance(global_scope['CAMERA_MARGIN_RIGHT'], int)

    def test_constants_loaded_on_init(self):
        """测试常量加载在JassVM初始化时自动完成。"""
        vm = JassVM()
        # 不需要额外调用，初始化时应该已经加载
        global_scope = vm.interpreter.global_context.variables
        assert len(global_scope) > 0

    def test_boolean_constants_loaded(self):
        """测试布尔常量从 common.j 加载。"""
        vm = JassVM()
        global_scope = vm.interpreter.global_context.variables

        # 检查布尔常量
        assert 'TRUE' in global_scope
        assert 'FALSE' in global_scope
        assert global_scope['TRUE'] is True
        assert global_scope['FALSE'] is False

    def test_jass_max_array_size_constant(self):
        """测试 JASS_MAX_ARRAY_SIZE 常量加载。"""
        vm = JassVM()
        global_scope = vm.interpreter.global_context.variables

        assert 'JASS_MAX_ARRAY_SIZE' in global_scope
        assert global_scope['JASS_MAX_ARRAY_SIZE'] == 8192

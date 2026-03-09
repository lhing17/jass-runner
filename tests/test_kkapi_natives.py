"""KK对战平台扩展API native函数测试。"""

import unittest
from jass_runner.natives.kkapi_natives import DzUnlockOpCodeLimit
from jass_runner.natives.base import NativeFunction


class TestDzUnlockOpCodeLimit(unittest.TestCase):
    """测试DzUnlockOpCodeLimit native函数。"""

    def setUp(self):
        """设置测试环境。"""
        self.native = DzUnlockOpCodeLimit()

    def test_name(self):
        """测试函数名称。"""
        self.assertEqual(self.native.name, "DzUnlockOpCodeLimit")

    def test_source(self):
        """测试函数来源标识。"""
        self.assertEqual(self.native.source, "KKAPI.j")

    def test_inherits_from_native_function(self):
        """测试继承自NativeFunction基类。"""
        self.assertIsInstance(self.native, NativeFunction)

    def test_default_source_for_base_class(self):
        """测试基类默认source为common.j。"""
        # 创建一个没有覆盖source属性的测试类
        class TestNative(NativeFunction):
            @property
            def name(self):
                return "TestNative"

            def execute(self, state_context, *args, **kwargs):
                return None

        test_native = TestNative()
        self.assertEqual(test_native.source, "common.j")


class TestKKAPIIntegration(unittest.TestCase):
    """测试KKAPI在工厂中的集成。"""

    def test_factory_registers_kkapi_natives(self):
        """测试工厂正确注册KKAPI native函数。"""
        from jass_runner.natives.factory import NativeFactory

        factory = NativeFactory()
        registry = factory.create_default_registry()

        # 验证DzUnlockOpCodeLimit已被注册
        native = registry.get("DzUnlockOpCodeLimit")
        self.assertIsNotNone(native)
        self.assertEqual(native.source, "KKAPI.j")


if __name__ == "__main__":
    unittest.main()

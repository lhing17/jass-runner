"""布尔表达式 native 函数演示。

此脚本演示 Condition、Filter、And、Or、Not 等 native 函数的使用。
"""

import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from jass_runner.natives.factory import NativeFactory
from jass_runner.natives.manager import HandleManager


class MockStateContext:
    """模拟状态上下文。"""

    def __init__(self):
        self.handle_manager = HandleManager()


def test_condition():
    """测试 Condition native。"""
    print("=== 测试 Condition ===")

    ctx = MockStateContext()
    condition_native = NativeFactory().create_default_registry().get("Condition")

    # 定义条件函数
    def my_condition():
        return True

    # 创建 conditionfunc
    condition_id = condition_native.execute(ctx, my_condition)
    print(f"Created conditionfunc: {condition_id}")

    # 验证可以获取并执行
    condition = ctx.handle_manager.get_boolexpr(condition_id)
    result = condition.evaluate()
    print(f"Condition evaluate: {result}")

    # 销毁
    destroy_native = NativeFactory().create_default_registry().get("DestroyCondition")
    destroy_native.execute(ctx, condition_id)
    print(f"Destroyed conditionfunc: {condition_id}")


def test_filter():
    """测试 Filter native。"""
    print("\n=== 测试 Filter ===")

    ctx = MockStateContext()
    filter_native = NativeFactory().create_default_registry().get("Filter")

    # 定义过滤函数
    def my_filter(unit):
        return unit is not None

    # 创建 filterfunc
    filter_id = filter_native.execute(ctx, my_filter)
    print(f"Created filterfunc: {filter_id}")

    # 销毁
    destroy_native = NativeFactory().create_default_registry().get("DestroyFilter")
    destroy_native.execute(ctx, filter_id)
    print(f"Destroyed filterfunc: {filter_id}")


def test_and_or_not():
    """测试 And、Or、Not natives。"""
    print("\n=== 测试 And、Or、Not ===")

    ctx = MockStateContext()
    registry = NativeFactory().create_default_registry()

    condition_native = registry.get("Condition")
    and_native = registry.get("And")
    or_native = registry.get("Or")
    not_native = registry.get("Not")

    # 创建两个条件
    def condition_true():
        return True

    def condition_false():
        return False

    cond_true_id = condition_native.execute(ctx, condition_true)
    cond_false_id = condition_native.execute(ctx, condition_false)

    print(f"Created condition_true: {cond_true_id}")
    print(f"Created condition_false: {cond_false_id}")

    # 测试 And
    and_id = and_native.execute(ctx, cond_true_id, cond_false_id)
    and_expr = ctx.handle_manager.get_boolexpr(and_id)
    print(f"And(True, False) = {and_expr.evaluate()}")  # 应为 False

    # 测试 Or
    or_id = or_native.execute(ctx, cond_true_id, cond_false_id)
    or_expr = ctx.handle_manager.get_boolexpr(or_id)
    print(f"Or(True, False) = {or_expr.evaluate()}")  # 应为 True

    # 测试 Not
    not_id = not_native.execute(ctx, cond_true_id)
    not_expr = ctx.handle_manager.get_boolexpr(not_id)
    print(f"Not(True) = {not_expr.evaluate()}")  # 应为 False

    # 清理
    destroy_bool_expr = registry.get("DestroyBoolExpr")
    destroy_bool_expr.execute(ctx, and_id)
    destroy_bool_expr.execute(ctx, or_id)
    destroy_bool_expr.execute(ctx, not_id)
    print("Cleaned up boolexpr objects")


if __name__ == "__main__":
    test_condition()
    test_filter()
    test_and_or_not()
    print("\n=== 所有测试完成 ===")

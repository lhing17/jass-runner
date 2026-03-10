# RemoveUnit Native 函数设计文档

## 概述

为 JASS Runner 添加 `RemoveUnit` native 函数支持，用于立即移除单位而不触发死亡事件。

## 背景

- `KillUnit` - 杀死单位，会触发死亡事件，播放死亡动画
- `RemoveUnit` - 立即移除单位，不会触发死亡事件

## 设计方案

### 实现位置

`src/jass_runner/natives/basic.py` - 与 `KillUnit` 类并列

### 类设计

```python
class RemoveUnit(NativeFunction):
    """立即移除一个单位，不触发死亡事件。"""

    @property
    def name(self) -> str:
        return "RemoveUnit"

    def execute(self, state_context, unit: Unit):
        # 1. 检查单位是否为 None
        # 2. 通过 HandleManager 销毁单位句柄
        # 3. 输出移除日志（区别于 KillUnit 的日志）
        # 4. 返回是否成功
```

### 行为细节

1. **参数检查**: 如果 `unit` 为 `None`，输出警告日志 `[RemoveUnit] 尝试移除 None 单位` 并返回 `False`
2. **单位销毁**: 通过 `state_context.handle_manager.destroy_handle(unit.id)` 销毁单位
3. **成功日志**: `[RemoveUnit] 单位 {id} 已被移除`
4. **失败日志**: `[RemoveUnit] 单位 {id} 不存在或已被移除`
5. **返回值**: `bool` 表示操作是否成功

### 注册

在 `NativeFactory.create_default_registry()` 中注册 `RemoveUnit()` 函数

## 测试策略

### 单元测试

文件: `tests/unit/natives/test_basic_natives.py`

1. **成功移除存在的单位**: 创建单位后调用 RemoveUnit，验证返回 True，单位被销毁
2. **处理 None 单位**: 传入 None，验证返回 False，输出警告日志
3. **重复移除**: 对已移除的单位再次调用，验证返回 False

### 集成测试

文件: `tests/integration/test_removeunit.j`

编写 JASS 脚本测试 RemoveUnit 在实际脚本中的使用。

## 日志示例

```
[RemoveUnit] 单位 unit_123 已被移除
[RemoveUnit] 尝试移除 None 单位
[RemoveUnit] 单位 unit_123 不存在或已被移除
```

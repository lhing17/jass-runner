# TriggerExecute Native 函数设计文档

## 概述

实现 `TriggerExecute` native 函数，用于手动执行触发器中已添加的所有 action，不评估条件。

## JASS 函数定义

```jass
native TriggerExecute takes trigger whichTrigger returns nothing
```

## 设计决策

### 条件评估策略

**决策**：不评估条件，直接执行所有 actions（强制触发模式）

**理由**：
- 与 Warcraft III 的 `TriggerExecute` 行为一致
- 允许强制触发绕过条件检查
- 条件评估可使用单独的 `TriggerEvaluate` 函数

## 实现方法

采用**简单委托模式**：
- 在 `TriggerExecute` 中直接调用 `trigger.execute_actions(state_context)`
- 复用 Trigger 类现有的 `execute_actions` 方法
- 优点：代码简洁，无重复逻辑，易于测试，与现有代码风格一致

## 接口定义

```python
class TriggerExecute(NativeFunction):
    @property
    def name(self) -> str:
        return "TriggerExecute"

    def execute(self, state_context, trigger_id: str, *args, **kwargs) -> None:
        pass
```

### 参数说明

- `state_context`: 执行上下文，用于访问 trigger_manager
- `trigger_id`: 触发器句柄 ID（字符串）
- 返回 `None`（对应 JASS 的 `nothing`）

### 使用示例

```jass
call TriggerExecute(myTrigger)  // 直接执行，不评估条件
```

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| `state_context` 为 `None` 或缺少 `trigger_manager` | 记录 error 日志，静默返回 |
| `trigger_id` 对应的触发器不存在 | 记录 warning 日志，静默返回 |
| 单个 action 执行异常 | 由 `trigger.execute_actions` 处理，记录 warning 但继续执行后续 actions |

## 日志输出

使用 `logging` 模块，格式与现有 native 函数一致：

```
[INFO] [TriggerExecute] Executed trigger: trigger_abc123 with X actions
```

## 实现步骤

1. 在 `trigger_natives.py` 中创建 `TriggerExecute` 类
2. 在 `NativeFactory.create_default_registry()` 中注册
3. 编写单元测试：验证正常执行、错误处理、日志输出
4. 编写集成测试：与 `TriggerAddAction` 配合使用

## 测试策略

### 单元测试

- mock trigger_manager 和 trigger，验证调用关系
- 测试错误场景：state_context 为 None、触发器不存在

### 集成测试

- 完整流程测试：CreateTrigger → TriggerAddAction → TriggerExecute
- 验证 actions 是否按顺序执行
- 验证日志输出

## 相关文件

- `/Users/lianghao/Development/jass-runner/src/jass_runner/natives/trigger_natives.py` - native 函数实现
- `/Users/lianghao/Development/jass-runner/src/jass_runner/trigger/trigger.py` - Trigger 类
- `/Users/lianghao/Development/jass-runner/src/jass_runner/trigger/manager.py` - TriggerManager 类

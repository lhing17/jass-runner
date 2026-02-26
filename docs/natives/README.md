# Native函数框架

Native函数框架允许通过控制台输出模拟JASS native函数。

## 架构

- **NativeFunction**: 所有native函数的抽象基类
- **NativeRegistry**: 管理native函数的注册表
- **NativeFactory**: 创建预配置注册表的工厂

## 使用方法

```python
from jass_runner.natives.factory import NativeFactory

# 创建包含基础native函数的默认注册表
factory = NativeFactory()
registry = factory.create_default_registry()

# 获取并执行一个native函数
display_func = registry.get("DisplayTextToPlayer")
display_func.execute(0, 0, 0, "Hello World")
```

## 扩展

要添加新的native函数：

1. 创建继承自`NativeFunction`的类
2. 实现`name`属性和`execute`方法
3. 在工厂或注册表中注册

```python
from jass_runner.natives.base import NativeFunction

class MyNative(NativeFunction):
    @property
    def name(self) -> str:
        return "MyNative"

    def execute(self, *args):
        print(f"MyNative called with {args}")
        return None
```

## 已实现的Native函数

### DisplayTextToPlayer
向玩家显示文本（通过控制台输出模拟）。

```jass
call DisplayTextToPlayer(0, 0, 0, "Hello World")
```

**参数**:
- `player`: 玩家ID (整数)
- `x`: X坐标 (浮点数，游戏中未使用)
- `y`: Y坐标 (浮点数，游戏中未使用)
- `message`: 要显示的文本消息 (字符串)

**返回**: `None`

**日志输出**: `[DisplayTextToPlayer]玩家{player}: {message}`

### KillUnit
杀死一个单位（通过控制台输出模拟）。

```jass
call KillUnit("footman_001")
```

**参数**:
- `unit_identifier`: 单位标识符 (字符串)

**返回**: `True` (成功) 或 `False` (失败)

**日志输出**: `[KillUnit] 单位{unit_identifier}已被击杀`

### CreateUnit
创建一个单位（模拟）。

```jass
call CreateUnit(0, 'hfoo', 0.0, 0.0, 0.0)
```

**参数**:
- `player`: 玩家ID (整数)
- `unit_type`: 单位类型代码 (字符串，如'hfoo'代表步兵)
- `x`: X坐标 (浮点数)
- `y`: Y坐标 (浮点数)
- `facing`: 面向角度 (浮点数)

**返回**: 生成的单位标识符 (字符串，格式为`unit_{uuid}`)

**日志输出**: `[CreateUnit] 为玩家{player}在({x}, {y})创建{unit_type}，单位ID: {unit_id}`

### GetUnitState
获取单位状态（模拟）。

```jass
call GetUnitState("footman_001", "UNIT_STATE_LIFE")
```

**参数**:
- `unit_identifier`: 单位标识符 (字符串)
- `state_type`: 状态类型 (字符串，如"UNIT_STATE_LIFE"表示生命值)

**返回**: 单位状态值 (浮点数)

**支持的状态类型**:
- `"UNIT_STATE_LIFE"`: 返回100.0 (模拟生命值)
- `"UNIT_STATE_MANA"`: 返回50.0 (模拟魔法值)
- 其他类型: 返回0.0并输出警告日志

**日志输出**: 未知状态类型时输出警告`[GetUnitState] 未知状态类型: {state_type}`

## 与解释器集成

Native函数已集成到JASS解释器中，可以在JASS代码中直接调用：

```jass
function main takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "Hello from JASS!")
    call KillUnit("footman_001")

    local string unit_id = CreateUnit(0, 'hfoo', 0.0, 0.0, 0.0)
    local real health = GetUnitState(unit_id, "UNIT_STATE_LIFE")
endfunction
```

解释器会自动从注册表中查找并执行native函数，输出相应的日志信息。

## 设计原则

1. **插件式架构**: 每个native函数独立实现，易于扩展和维护
2. **模拟而非仿真**: 重点在于输出可观察的行为，而非完全精确模拟
3. **日志输出**: 所有操作通过logging模块输出，便于调试和测试
4. **类型安全**: 保持与JASS类型系统兼容，但适当简化
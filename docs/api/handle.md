# Handle 类体系

## Handle

所有JASS handle的基类。

### 类定义

```python
class Handle:
    def __init__(self, handle_id: str, type_name: str)
    def destroy(self) -> None
    def is_alive(self) -> bool
```

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `id` | str | 唯一标识符 |
| `type_name` | str | handle类型名称 |
| `alive` | bool | 是否存活 |

### 方法

#### `destroy()`

标记handle为销毁状态。

**返回**: None

#### `is_alive()` -> bool

检查handle是否存活。

**返回**: 如果handle存活返回True，否则返回False

---

## Unit

单位handle，继承自Handle。

### 类定义

```python
class Unit(Handle):
    def __init__(self, handle_id: str, unit_type: str, player_id: int,
                 x: float, y: float, facing: float)
```

### 属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `unit_type` | str | - | 单位类型代码（如'hfoo'） |
| `player_id` | int | - | 所属玩家ID |
| `x` | float | - | X坐标 |
| `y` | float | - | Y坐标 |
| `facing` | float | - | 面向角度 |
| `life` | float | 100.0 | 当前生命值 |
| `max_life` | float | 100.0 | 最大生命值 |
| `mana` | float | 50.0 | 当前魔法值 |
| `max_mana` | float | 50.0 | 最大魔法值 |

### 示例

```python
from jass_runner.natives.handle import Unit

unit = Unit("unit_001", "hfoo", 0, 100.0, 200.0, 270.0)
print(f"单位类型: {unit.unit_type}")
print(f"生命值: {unit.life}/{unit.max_life}")

# 销毁单位
unit.destroy()
assert not unit.is_alive()
```

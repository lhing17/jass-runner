# HandleManager

集中式handle生命周期管理器。

## 类定义

```python
class HandleManager:
    def __init__(self)
    def create_unit(self, unit_type: str, player_id: int,
                   x: float, y: float, facing: float) -> Unit
    def get_handle(self, handle_id: str) -> Optional[Handle]
    def get_unit(self, unit_id: str) -> Optional[Unit]
    def destroy_handle(self, handle_id: str) -> bool
    def get_unit_state(self, unit_id: str, state_type: str) -> float
    def set_unit_state(self, unit_id: str, state_type: str, value: float) -> bool
```

## 方法

### `create_unit(unit_type, player_id, x, y, facing)` -> Unit

创建一个单位并返回Unit对象。

**参数**:
- `unit_type` (str): 单位类型代码（如'hfoo'）
- `player_id` (int): 所属玩家ID
- `x` (float): X坐标
- `y` (float): Y坐标
- `facing` (float): 面向角度

**返回**: Unit对象

**示例**:
```python
manager = HandleManager()
unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)
print(f"创建单位: {unit.id}")  # 输出: 创建单位: unit_1
```

### `get_handle(handle_id)` -> Optional[Handle]

通过ID获取handle对象。

**参数**:
- `handle_id` (str): handle ID

**返回**: Handle对象，如果handle不存在或已销毁返回None

### `get_unit(unit_id)` -> Optional[Unit]

获取单位对象，进行类型检查。

**参数**:
- `unit_id` (str): 单位ID

**返回**: Unit对象，如果单位不存在、已销毁或类型不匹配返回None

### `destroy_handle(handle_id)` -> bool

销毁指定的handle。

**参数**:
- `handle_id` (str): handle ID

**返回**: 成功销毁返回True，否则返回False

### `get_unit_state(unit_id, state_type)` -> float

获取单位状态值。

**参数**:
- `unit_id` (str): 单位ID
- `state_type` (str): 状态类型（"UNIT_STATE_LIFE", "UNIT_STATE_MAX_LIFE", "UNIT_STATE_MANA", "UNIT_STATE_MAX_MANA"）

**返回**: 状态值，如果单位不存在返回0.0

### `set_unit_state(unit_id, state_type, value)` -> bool

设置单位状态值。

**参数**:
- `unit_id` (str): 单位ID
- `state_type` (str): 状态类型
- `value` (float): 新值

**返回**: 成功设置返回True，否则返回False

## 统计方法

### `get_total_handles()` -> int

获取总handle数量（包括已销毁的）。

### `get_alive_handles()` -> int

获取存活handle数量。

### `get_handle_type_count(type_name)` -> int

获取指定类型的handle数量。

## 完整示例

```python
from jass_runner.natives.manager import HandleManager

manager = HandleManager()

# 创建单位
unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

# 查询状态
life = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")
print(f"生命值: {life}")  # 输出: 生命值: 100.0

# 修改状态
manager.set_unit_state(unit.id, "UNIT_STATE_LIFE", 75.0)

# 销毁单位
manager.destroy_handle(unit.id)

# 统计
print(f"总handle数: {manager.get_total_handles()}")
print(f"存活handle数: {manager.get_alive_handles()}")
```

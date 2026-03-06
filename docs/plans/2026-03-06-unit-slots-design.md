# 技能格子槽位 Native 函数设计文档

## 概述

实现 `SetAllItemTypeSlots`, `SetAllUnitTypeSlots`, `SetItemTypeSlots`, `SetUnitTypeSlots` 四个 native 函数，用于设置单位技能格子中出售物品和单位的槽位数量。

## 背景

在魔兽争霸3中，这些函数用于配置商店和单位的技能格子（Ability Slots）库存容量：

```jass
native SetAllItemTypeSlots          takes integer slots returns nothing
native SetAllUnitTypeSlots          takes integer slots returns nothing
native SetItemTypeSlots             takes unit whichUnit, integer slots returns nothing
native SetUnitTypeSlots             takes unit whichUnit, integer slots returns nothing
```

- 技能格子出售物品/单位的默认最大槽位数为 11
- `SetAllXxx` 函数设置全局最大槽位数限制
- `SetXxx` 函数为单位设置具体槽位数，不能超过全局最大值

## 设计方案

### 1. 全局变量设计

在 `unit.py` 模块级别定义全局变量：
- `MAX_ITEM_TYPE_SLOTS` - 全局物品类型最大槽位数（默认11）
- `MAX_UNIT_TYPE_SLOTS` - 全局单位类型最大槽位数（默认11）

### 2. Unit 类扩展

添加以下属性和方法：
- `_item_type_slots` - 该单位技能格子中出售物品的槽位数（默认11）
- `_unit_type_slots` - 该单位技能格子中出售单位的槽位数（默认11）
- `set_item_type_slots(slots)` - 设置时截断到全局最大值，返回实际设置的值
- `set_unit_type_slots(slots)` - 设置时截断到全局最大值，返回实际设置的值

### 3. 截断逻辑

```python
def set_item_type_slots(self, slots):
    # 截断到 0-MAX_ITEM_TYPE_SLOTS 范围
    actual_slots = max(0, min(slots, MAX_ITEM_TYPE_SLOTS))
    self._item_type_slots = actual_slots
    return actual_slots
```

### 4. 新建 unit_slots_natives.py

实现四个 native 函数：

#### SetAllItemTypeSlots
- 设置全局物品类型最大槽位数
- 参数 `slots` 会被截断到 0-11 范围
- 返回实际设置的值

#### SetAllUnitTypeSlots
- 设置全局单位类型最大槽位数
- 参数 `slots` 会被截断到 0-11 范围
- 返回实际设置的值

#### SetItemTypeSlots
- 为单位设置物品类型槽位数
- 超过全局最大值时截断
- 返回实际设置的值

#### SetUnitTypeSlots
- 为单位设置单位类型槽位数
- 超过全局最大值时截断
- 返回实际设置的值

### 5. 工厂注册

在 `NativeFactory.create_default_registry()` 中注册四个新的 native 函数。

## 接口定义

```python
# 全局变量（在 unit.py 中）
MAX_ITEM_TYPE_SLOTS = 11
MAX_UNIT_TYPE_SLOTS = 11

# Unit 类方法
class Unit:
    def set_item_type_slots(self, slots: int) -> int: ...
    def set_unit_type_slots(self, slots: int) -> int: ...

# Native 函数
class SetAllItemTypeSlots(NativeFunction):
    def execute(self, state_context, slots: int) -> int: ...

class SetAllUnitTypeSlots(NativeFunction):
    def execute(self, state_context, slots: int) -> int: ...

class SetItemTypeSlots(NativeFunction):
    def execute(self, state_context, unit: Unit, slots: int) -> int: ...

class SetUnitTypeSlots(NativeFunction):
    def execute(self, state_context, unit: Unit, slots: int) -> int: ...
```

## 测试策略

1. 单元测试：测试四个 native 函数的基本功能
2. 单元测试：测试截断逻辑（超出范围时）
3. 单元测试：测试全局变量和单位属性的交互
4. 集成测试：测试完整的槽位设置流程

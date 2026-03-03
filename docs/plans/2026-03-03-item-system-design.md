# 物品系统设计方案

**日期**: 2026-03-03
**版本**: v0.6.0
**状态**: 待实现

---

## 1. 设计目标

扩展 JASS Runner 的物品系统，实现完整的单位背包（inventory）功能，支持：
- 6槽位物品背包管理
- 单位与物品的交互（添加、移除、查询）
- 符合原版魔兽争霸3行为的 Native 函数

---

## 2. 背景与现状

### 2.1 已实现基础
- `Item` 类：基础物品定义（item_type, x, y）
- `CreateItem` / `RemoveItem`：物品创建与销毁
- `HandleManager`：物品管理（create_item, get_item）

### 2.2 待实现功能
- 单位背包系统（6槽位）
- 物品与单位的交互 API
- 物品类型查询

---

## 3. 架构设计

### 3.1 数据模型

#### Unit 类扩展
```
location: src/jass_runner/natives/handle.py

新增属性:
    inventory: List[Optional[Item]]  # 6个槽位，None表示空
```

#### Item 类
保持现有简单设计，无修改。

### 3.2 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                     物 品 系 统                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────┐      ┌─────────────────────────┐  │
│  │   Item (物品)    │      │   Unit (单位)         │  │
│  │  - item_type    │      │  - id                 │  │
│  │  - x, y         │      │  - unit_type          │  │
│  │  - alive        │      │  - inventory[6]: Item │  │
│  └────────┬────────┘      └─────────────────────────┘  │
│           │                                              │
│  ┌────────▼──────────────────────────────────────────┐  │
│  │           Item Inventory Natives                    │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │ UnitAddItem(unit, item) -> bool             │  │  │
│  │  │ UnitAddItemById(unit, itemTypeId, slot?)    │  │  │
│  │  │ UnitRemoveItem(unit, item) -> bool          │  │  │
│  │  │ UnitRemoveItemFromSlot(unit, slot) -> bool  │  │  │
│  │  │ GetItemTypeId(item) -> int                  │  │  │
│  │  │ UnitItemInSlot(unit, slot) -> item          │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Native API 详细设计

### 4.1 函数列表

| 函数名 | 参数 | 返回值 | 行为描述 |
|--------|------|--------|----------|
| `UnitAddItem` | `(unit, item)` | `bool` | 将已有物品添加到单位第一个空槽位，成功返回 true |
| `UnitAddItemById` | `(unit, itemTypeId, slot=-1)` | `item` | 创建新物品并添加，slot=-1 自动找空槽，返回创建的 item |
| `UnitRemoveItem` | `(unit, item)` | `bool` | 从单位找到该物品并移除销毁，未找到返回 false |
| `UnitRemoveItemFromSlot` | `(unit, slot)` | `bool` | 移除指定槽位物品并销毁，槽位为空或越界返回 false |
| `GetItemTypeId` | `(item)` | `int` | 返回物品类型 ID（FourCC 整数）|
| `UnitItemInSlot` | `(unit, slot)` | `item/null` | 获取指定槽位物品，空槽返回 null |

### 4.2 行为规则

#### 槽位管理
- 固定 6 个槽位（索引 0-5），不可动态调整
- `UnitAddItem` 优先查找第一个 `None` 的槽位
- `UnitAddItemById` 可指定目标槽位（0-5），该槽位必须为空

#### 移除销毁
- 所有 `Remove` 操作会调用 `DestroyItem` 销毁 Item 对象
- 物品不在单位背包中时，`UnitRemoveItem` 返回 false
- 槽位越界时，`UnitRemoveItemFromSlot` 返回 false

#### 边界情况
- 单位已有 6 个物品时，`UnitAddItem` 返回 false
- 创建物品失败时，`UnitAddItemById` 返回 null
- 物品已在其他单位背包中时，不能添加到新单位

---

## 5. 实现细节

### 5.1 Unit 类扩展

```python
class Unit(Handle):
    """扩展 Unit 类支持物品背包。

    新增属性:
        inventory: 6个槽位的物品列表，None 表示空槽
    """

    def __init__(self, handle_id: str, unit_type: int, owner: Player, x: float, y: float):
        super().__init__(handle_id, "unit")
        # ... 现有属性
        self.inventory: List[Optional[Item]] = [None] * 6

    def add_item(self, item: Item, slot: int = -1) -> bool:
        """添加物品到背包，成功返回 True。"""
        if slot >= 0:
            if 0 <= slot < 6 and self.inventory[slot] is None:
                self.inventory[slot] = item
                return True
            return False
        # 自动找空槽
        for i in range(6):
            if self.inventory[i] is None:
                self.inventory[i] = item
                return True
        return False

    def remove_item(self, item: Item) -> bool:
        """从背包移除指定物品，成功返回 True。"""
        for i in range(6):
            if self.inventory[i] is item:
                self.inventory[i] = None
                return True
        return False

    def remove_item_from_slot(self, slot: int) -> bool:
        """从指定槽位移除物品，成功返回 True。"""
        if 0 <= slot < 6 and self.inventory[slot] is not None:
            self.inventory[slot] = None
            return True
        return False

    def get_item_in_slot(self, slot: int) -> Optional[Item]:
        """获取指定槽位的物品。"""
        if 0 <= slot < 6:
            return self.inventory[slot]
        return None

    def find_item(self, item: Item) -> int:
        """查找物品所在槽位，未找到返回 -1。"""
        for i in range(6):
            if self.inventory[i] is item:
                return i
        return -1
```

### 5.2 Native 函数实现（伪代码）

```python
class UnitAddItem(NativeFunction):
    """将物品添加到单位背包。"""

    def execute(self, state_context, unit: Unit, item: Item) -> bool:
        if unit.find_item(item) >= 0:
            # 物品已在此单位中
            return False
        result = unit.add_item(item)
        if result:
            logger.info(f"[UnitAddItem] 物品 {item.id} 添加到单位 {unit.id}")
        return result


class UnitAddItemById(NativeFunction):
    """创建物品并添加到单位背包。"""

    def execute(self, state_context, unit: Unit, item_type_id: int, slot: int = -1) -> Item:
        item_type_str = int_to_fourcc(item_type_id)
        handle_manager = state_context.handle_manager

        # 创建物品（位置用单位位置）
        item = handle_manager.create_item(item_type_str, unit.x, unit.y)

        # 添加到单位
        if unit.add_item(item, slot):
            logger.info(f"[UnitAddItemById] 创建并添加 {item_type_str} 到单位 {unit.id}")
            return item
        else:
            # 添加失败，销毁物品
            handle_manager.destroy_handle(item.id)
            return None


class UnitRemoveItem(NativeFunction):
    """从单位移除并销毁物品。"""

    def execute(self, state_context, unit: Unit, item: Item) -> bool:
        result = unit.remove_item(item)
        if result:
            handle_manager = state_context.handle_manager
            handle_manager.destroy_handle(item.id)
            logger.info(f"[UnitRemoveItem] 销毁物品 {item.id}")
        return result


class UnitRemoveItemFromSlot(NativeFunction):
    """从指定槽位移除并销毁物品。"""

    def execute(self, state_context, unit: Unit, slot: int) -> bool:
        item = unit.get_item_in_slot(slot)
        if item:
            unit.remove_item_from_slot(slot)
            handle_manager = state_context.handle_manager
            handle_manager.destroy_handle(item.id)
            logger.info(f"[UnitRemoveItemFromSlot] 槽位 {slot} 物品已销毁")
            return True
        return False


class GetItemTypeId(NativeFunction):
    """获取物品类型ID（FourCC整数）。"""

    def execute(self, state_context, item: Item) -> int:
        return string_to_fourcc(item.item_type)


class UnitItemInSlot(NativeFunction):
    """获取单位指定槽位的物品。"""

    def execute(self, state_context, unit: Unit, slot: int) -> Optional[Item]:
        return unit.get_item_in_slot(slot)
```

---

## 6. 错误处理

| 场景 | 预期行为 | 日志输出 |
|------|----------|----------|
| UnitAddItem 满槽 | 返回 False | `[UnitAddItem] 单位背包已满，无法添加物品` |
| UnitAddItemById 指定槽位非空 | 返回 None，销毁已创建物品 | `[UnitAddItemById] 槽位 X 已被占用` |
| UnitRemoveItem 物品不在背包中 | 返回 False | `[UnitRemoveItem] 物品不在单位背包中` |
| UnitRemoveItemFromSlot 越界 | 返回 False | `[UnitRemoveItemFromSlot] 无效槽位: X` |
| UnitItemInSlot 越界 | 返回 None | `[UnitItemInSlot] 无效槽位: X` |

---

## 7. 测试策略

### 7.1 单元测试（tests/natives/test_item_inventory_natives.py）

| 测试名 | 验证内容 |
|--------|----------|
| `test_unit_add_item_success` | 成功添加物品到空槽 |
| `test_unit_add_item_full_inventory` | 满槽时添加失败 |
| `test_unit_add_item_by_id_auto_slot` | 自动找空槽添加 |
| `test_unit_add_item_by_id_specific_slot` | 指定槽位添加 |
| `test_unit_add_item_by_id_occupied_slot` | 指定槽位被占时失败 |
| `test_unit_remove_item_success` | 成功移除并销毁物品 |
| `test_unit_remove_item_not_found` | 移除不在背包中的物品失败 |
| `test_unit_remove_item_from_slot_success` | 从指定槽位移除 |
| `test_unit_remove_item_from_slot_empty` | 空槽位移除失败 |
| `test_get_item_type_id` | 获取物品类型ID正确 |
| `test_unit_item_in_slot_exists` | 获取存在的物品 |
| `test_unit_item_in_slot_empty` | 空槽返回 None |

### 7.2 集成测试（tests/integration/test_item_inventory_integration.py）

| 测试名 | 场景描述 |
|--------|----------|
| `test_complete_item_lifecycle` | 创建→添加→查询→移除→销毁完整流程 |
| `test_fill_all_slots` | 填满6个槽位，逐个验证 |
| `test_swap_items_between_units` | 从单位A移除，添加到单位B |
| `test_inventory_persistence_in_vm` | 在完整 VM 运行中验证物品持久化 |

---

## 8. 文件变更清单

### 修改文件（2个）
1. `src/jass_runner/natives/handle.py` - 扩展 Unit 类（添加 inventory 和操作方法）
2. `src/jass_runner/natives/factory.py` - 注册 6 个新 Native 函数

### 新建文件（2个）
1. `src/jass_runner/natives/item_inventory_natives.py` - 6 个 Native 函数实现
2. `tests/natives/test_item_inventory_natives.py` - 单元测试
3. `tests/integration/test_item_inventory_integration.py` - 集成测试

---

## 9. 与现有系统的集成

### 9.1 与 HandleManager 的集成
- `Remove` 操作调用 `HandleManager.destroy_handle()` 销毁 Item
- `RemoveItemById` 失败时自动清理已创建的物品

### 9.2 与 TypeHierarchy 的集成
- Item 类型已在 `HANDLE_SUBTYPES` 中定义
- Native 函数参数类型检查通过 TypeChecker 完成

---

## 10. 验收标准

- [ ] 所有 6 个 Native 函数实现并通过单元测试
- [ ] Unit 类扩展包含完整的 inventory 管理方法
- [ ] 集成测试覆盖完整物品生命周期
- [ ] 测试覆盖率保持 95%+
- [ ] 文档（本文件）与实际实现一致

---

**设计者**: Claude Code
**审核状态**: 待用户确认

---

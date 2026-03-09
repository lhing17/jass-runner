# Hashtable 系统设计文档

**日期**: 2026-03-09
**主题**: JASS Hashtable 数据结构与 Native 函数实现

---

## 1. 需求概述

### 1.1 背景
JASS (Warcraft III 脚本语言) 中的 `hashtable` 是一种强大的数据结构，支持：
- 使用两层整数键 (`parentKey`, `childKey`) 存储数据
- 同一键组合下可同时存储不同类型的数据
- 支持基础类型（integer, real, boolean, string）和 handle 类型

### 1.2 目标
实现完整的 hashtable 支持，包括：
1. `Hashtable` 类 - 核心数据结构
2. `InitHashtable` native 函数
3. 核心 Save/Load 函数（基础类型 + 常用 handle 类型）
4. 辅助函数（HaveSaved*, RemoveSaved*, Flush*）

### 1.3 范围
**实现范围（选项B）**:
- 基础类型: integer, real, boolean, string
- 常用 handle: unit, item, player
- 辅助操作: HaveSaved*, RemoveSaved*, FlushChildHashtable, FlushParentHashtable

**暂不实现**:
- 不常用 handle: quest, multiboard, dialog 等（约40+个）
- gamecache 相关函数

---

## 2. 架构设计

### 2.1 核心组件

```
┌─────────────────────────────────────────────────────────────┐
│                      Native Functions                        │
├─────────────────────────────────────────────────────────────┤
│  InitHashtable                                               │
│  SaveInteger/SaveReal/SaveBoolean/SaveStr                   │
│  SaveUnitHandle/SaveItemHandle/SavePlayerHandle             │
│  LoadInteger/LoadReal/LoadBoolean/LoadStr                   │
│  LoadUnitHandle/LoadItemHandle/LoadPlayerHandle             │
│  HaveSavedInteger/HaveSavedReal/.../HaveSavedHandle         │
│  RemoveSavedInteger/RemoveSavedReal/.../RemoveSavedHandle   │
│  FlushChildHashtable/FlushParentHashtable                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Hashtable Class                         │
├─────────────────────────────────────────────────────────────┤
│  _data: Dict[parent, Dict[child, Dict[type, value]]]        │
├─────────────────────────────────────────────────────────────┤
│  save_integer(parent, child, value)                         │
│  load_integer(parent, child) -> int                         │
│  save_unit_handle(parent, child, unit) -> bool              │
│  load_unit_handle(parent, child) -> Optional[Unit]          │
│  have_saved_integer(parent, child) -> bool                  │
│  remove_saved_integer(parent, child)                        │
│  flush_child(parent)                                        │
│  flush_all()                                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Handle System                           │
├─────────────────────────────────────────────────────────────┤
│  HandleManager.create_hashtable()                           │
│  HandleManager.get_hashtable(handle_id)                     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 数据模型

**嵌套字典结构**:
```python
_data = {
    parent_key_1: {
        child_key_1: {
            "integer": 42,
            "real": 3.14,
            "unit": "unit_123",      # 存储 handle_id
        },
        child_key_2: {
            "string": "hello",
        }
    },
    parent_key_2: {
        child_key_1: {
            "boolean": True,
        }
    }
}
```

**类型存储键**:
- `"integer"` - 整数类型
- `"real"` - 实数类型
- `"boolean"` - 布尔类型
- `"string"` - 字符串类型
- `"unit"` - 单位 handle
- `"item"` - 物品 handle
- `"player"` - 玩家 handle

### 2.3 默认值策略

当读取不存在的键时，返回类型默认值：

| 类型 | 默认值 |
|------|--------|
| integer | 0 |
| real | 0.0 |
| boolean | False |
| string | null (None) |
| unit | null (None) |
| item | null (None) |
| player | null (None) |

---

## 3. API 设计

### 3.1 Hashtable 类

```python
class Hashtable(Handle):
    """JASS hashtable 实现"""

    # 类型到默认值的映射
    DEFAULT_VALUES: Dict[str, Any] = {
        "integer": 0,
        "real": 0.0,
        "boolean": False,
        "string": None,
        "unit": None,
        "item": None,
        "player": None,
    }

    def __init__(self, handle_id: str):
        """初始化 hashtable

        Args:
            handle_id: 唯一标识符
        """
        super().__init__(handle_id, "hashtable")
        self._data: Dict[int, Dict[int, Dict[str, Any]]] = {}

    # ========== Save 方法 ==========

    def save_integer(self, parent_key: int, child_key: int, value: int) -> None:
        """存储整数"""

    def save_real(self, parent_key: int, child_key: int, value: float) -> None:
        """存储实数"""

    def save_boolean(self, parent_key: int, child_key: int, value: bool) -> None:
        """存储布尔值"""

    def save_string(self, parent_key: int, child_key: int, value: str) -> bool:
        """存储字符串，返回是否成功"""

    def save_unit_handle(self, parent_key: int, child_key: int, unit: Unit) -> bool:
        """存储单位 handle"""

    def save_item_handle(self, parent_key: int, child_key: int, item: Item) -> bool:
        """存储物品 handle"""

    def save_player_handle(self, parent_key: int, child_key: int, player: Player) -> bool:
        """存储玩家 handle"""

    # ========== Load 方法 ==========

    def load_integer(self, parent_key: int, child_key: int) -> int:
        """加载整数，不存在返回 0"""

    def load_real(self, parent_key: int, child_key: int) -> float:
        """加载实数，不存在返回 0.0"""

    def load_boolean(self, parent_key: int, child_key: int) -> bool:
        """加载布尔值，不存在返回 False"""

    def load_string(self, parent_key: int, child_key: int) -> Optional[str]:
        """加载字符串，不存在返回 null"""

    def load_unit_handle(self, parent_key: int, child_key: int, handle_manager) -> Optional[Unit]:
        """加载单位 handle，不存在或已销毁返回 null"""

    def load_item_handle(self, parent_key: int, child_key: int, handle_manager) -> Optional[Item]:
        """加载物品 handle"""

    def load_player_handle(self, parent_key: int, child_key: int, handle_manager) -> Optional[Player]:
        """加载玩家 handle"""

    # ========== 存在性检查 ==========

    def have_saved_integer(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在整数"""

    def have_saved_real(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在实数"""

    def have_saved_boolean(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在布尔值"""

    def have_saved_string(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在字符串"""

    def have_saved_handle(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在任意 handle 类型"""

    # ========== 删除方法 ==========

    def remove_saved_integer(self, parent_key: int, child_key: int) -> None:
        """删除整数"""

    def remove_saved_real(self, parent_key: int, child_key: int) -> None:
        """删除实数"""

    def remove_saved_boolean(self, parent_key: int, child_key: int) -> None:
        """删除布尔值"""

    def remove_saved_string(self, parent_key: int, child_key: int) -> None:
        """删除字符串"""

    def remove_saved_handle(self, parent_key: int, child_key: int) -> None:
        """删除所有 handle 类型"""

    # ========== 清空方法 ==========

    def flush_child(self, parent_key: int) -> None:
        """删除指定 parentKey 下所有数据"""

    def flush_all(self) -> None:
        """清空整个 hashtable"""
```

### 3.2 Native 函数

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `InitHashtable` | nothing | hashtable | 创建 hashtable |
| `SaveInteger` | table, parentKey, childKey, value | nothing | 存储整数 |
| `SaveReal` | table, parentKey, childKey, value | nothing | 存储实数 |
| `SaveBoolean` | table, parentKey, childKey, value | nothing | 存储布尔 |
| `SaveStr` | table, parentKey, childKey, value | boolean | 存储字符串 |
| `SaveUnitHandle` | table, parentKey, childKey, whichUnit | boolean | 存储单位 |
| `SaveItemHandle` | table, parentKey, childKey, whichItem | boolean | 存储物品 |
| `SavePlayerHandle` | table, parentKey, childKey, whichPlayer | boolean | 存储玩家 |
| `LoadInteger` | table, parentKey, childKey | integer | 加载整数 |
| `LoadReal` | table, parentKey, childKey | real | 加载实数 |
| `LoadBoolean` | table, parentKey, childKey | boolean | 加载布尔 |
| `LoadStr` | table, parentKey, childKey | string | 加载字符串 |
| `LoadUnitHandle` | table, parentKey, childKey | unit | 加载单位 |
| `LoadItemHandle` | table, parentKey, childKey | item | 加载物品 |
| `LoadPlayerHandle` | table, parentKey, childKey | player | 加载玩家 |
| `HaveSavedInteger` | table, parentKey, childKey | boolean | 检查整数 |
| `HaveSavedReal` | table, parentKey, childKey | boolean | 检查实数 |
| `HaveSavedBoolean` | table, parentKey, childKey | boolean | 检查布尔 |
| `HaveSavedString` | table, parentKey, childKey | boolean | 检查字符串 |
| `HaveSavedHandle` | table, parentKey, childKey | boolean | 检查 handle |
| `RemoveSavedInteger` | table, parentKey, childKey | nothing | 删除整数 |
| `RemoveSavedReal` | table, parentKey, childKey | nothing | 删除实数 |
| `RemoveSavedBoolean` | table, parentKey, childKey | nothing | 删除布尔 |
| `RemoveSavedString` | table, parentKey, childKey | nothing | 删除字符串 |
| `RemoveSavedHandle` | table, parentKey, childKey | nothing | 删除 handle |
| `FlushChildHashtable` | table, parentKey | nothing | 清空 child |
| `FlushParentHashtable` | table | nothing | 清空整个 table |

---

## 4. 测试策略

### 4.1 单元测试

**Hashtable 类测试** (`test_hashtable.py`):
- 测试每种数据类型的 Save/Load
- 测试同一键下多类型存储
- 测试默认值返回
- 测试 HaveSaved* 方法
- 测试 RemoveSaved* 方法
- 测试 FlushChild/FlushAll

**Native 函数测试** (`test_hashtable_natives.py`):
- 测试 InitHashtable 创建和返回
- 测试每个 Save/Load 函数的参数传递
- 测试 handle 类型存储（存储 handle_id，加载时解析）
- 测试无效 hashtable 处理

### 4.2 集成测试

**完整工作流程** (`test_hashtable_integration.py`):
```jass
function testHashtable takes nothing returns nothing
    local hashtable ht = InitHashtable()
    local unit u = CreateUnit(Player(0), 'Hpal', 0, 0, 0)

    // 存储不同类型的数据
    call SaveInteger(ht, 0, 0, 42)
    call SaveReal(ht, 0, 0, 3.14)
    call SaveUnitHandle(ht, 0, 0, u)

    // 加载并验证
    call DisplayTextToPlayer(Player(0), 0, 0, I2S(LoadInteger(ht, 0, 0)))  // 42
    call DisplayTextToPlayer(Player(0), 0, 0, R2S(LoadReal(ht, 0, 0)))     // 3.14

    // 清理
    call FlushParentHashtable(ht)
endfunction
```

---

## 5. 实现细节

### 5.1 Handle 存储机制

当 SaveUnitHandle 时：
1. 接收 Unit 对象
2. 提取 unit.id (handle_id 字符串)
3. 存储 `"unit": "unit_123"`

当 LoadUnitHandle 时：
1. 从 _data 获取 `"unit"` 值
2. 如果是 None，返回 None
3. 调用 `handle_manager.get_unit(handle_id)`
4. 如果单位已销毁，返回 None

### 5.2 内存管理

- Hashtable 继承 Handle，生命周期由 HandleManager 管理
- 当 Hashtable 被销毁时，_data 字典被垃圾回收
- 存储的是 handle_id 而非对象引用，避免循环引用

### 5.3 错误处理

- **无效 hashtable**: 记录 warning，返回默认值
- **无效 handle**: Load 时返回 None
- **类型不存在**: Load 时返回类型默认值

---

## 6. 文件结构

```
src/jass_runner/natives/
├── hashtable.py              # Hashtable 类
├── hashtable_natives.py      # Native 函数
└── factory.py                # 注册新函数（修改）

tests/natives/
├── test_hashtable.py         # Hashtable 类测试
├── test_hashtable_natives.py # Native 函数测试
└── test_factory.py           # 更新函数计数（修改）

tests/integration/
└── test_hashtable_integration.py  # 集成测试
```

---

## 7. 下一步

调用 `writing-plans` 技能创建详细实施计划。

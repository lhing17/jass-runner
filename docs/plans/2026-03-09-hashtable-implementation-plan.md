# Hashtable Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 JASS Hashtable 数据结构和相关 Native 函数（InitHashtable, Save*/Load*, HaveSaved*, RemoveSaved*, Flush*）

**Architecture:** Hashtable 类继承 Handle 基类，使用嵌套字典存储数据（parent -> child -> type -> value），HandleManager 管理生命周期，Native 函数通过 state_context 访问 hashtable

**Tech Stack:** Python 3.8+, pytest, 现有 Handle 系统和 Native 函数框架

---

## 前置检查

**检查 HandleManager 是否支持 hashtable:**

查看 `src/jass_runner/natives/manager.py` 确认是否有 create_hashtable / get_hashtable 方法。

如果没有，需要在 Task 1 中添加。

---

### Task 1: Hashtable 类基础结构

**Files:**
- Create: `src/jass_runner/natives/hashtable.py`
- Test: `tests/natives/test_hashtable.py`

**Step 1: Write the failing test**

```python
# tests/natives/test_hashtable.py
"""Hashtable 类测试"""

import pytest
from jass_runner.natives.hashtable import Hashtable


class TestHashtableCreation:
    """测试 Hashtable 创建"""

    def test_hashtable_creation(self):
        """测试 Hashtable 创建和基本属性"""
        ht = Hashtable("hashtable_1")

        assert ht.id == "hashtable_1"
        assert ht.type_name == "hashtable"
        assert ht.is_alive()

    def test_hashtable_default_values(self):
        """测试 DEFAULT_VALUES 常量"""
        assert Hashtable.DEFAULT_VALUES["integer"] == 0
        assert Hashtable.DEFAULT_VALUES["real"] == 0.0
        assert Hashtable.DEFAULT_VALUES["boolean"] == False
        assert Hashtable.DEFAULT_VALUES["string"] is None
        assert Hashtable.DEFAULT_VALUES["unit"] is None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableCreation -v`
Expected: FAIL with "Hashtable not defined"

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/hashtable.py
"""JASS Hashtable 实现"""

from typing import Dict, Any, Optional
from .handle_base import Handle


class Hashtable(Handle):
    """JASS hashtable 实现

    支持两层整数键（parentKey, childKey）存储不同类型的数据。
    同一键组合下可同时存储多种类型（integer, real, boolean, string, unit等）。
    """

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
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableCreation -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_hashtable.py src/jass_runner/natives/hashtable.py
git commit -m "feat(hashtable): 添加Hashtable基础类结构"
```

---

### Task 2: 基础类型 Save/Load 方法

**Files:**
- Modify: `src/jass_runner/natives/hashtable.py`
- Test: `tests/natives/test_hashtable.py`

**Step 1: Write the failing test**

```python
# tests/natives/test_hashtable.py (添加)

class TestHashtableBasicTypes:
    """测试基础类型 Save/Load"""

    def test_save_and_load_integer(self):
        """测试整数存储和加载"""
        ht = Hashtable("ht_1")

        ht.save_integer(0, 0, 42)
        result = ht.load_integer(0, 0)

        assert result == 42

    def test_load_integer_default(self):
        """测试加载未设置的整数返回默认值"""
        ht = Hashtable("ht_1")

        result = ht.load_integer(0, 0)

        assert result == 0

    def test_save_and_load_real(self):
        """测试实数存储和加载"""
        ht = Hashtable("ht_1")

        ht.save_real(0, 0, 3.14)
        result = ht.load_real(0, 0)

        assert result == 3.14

    def test_save_and_load_boolean(self):
        """测试布尔值存储和加载"""
        ht = Hashtable("ht_1")

        ht.save_boolean(0, 0, True)
        result = ht.load_boolean(0, 0)

        assert result is True

    def test_save_and_load_string(self):
        """测试字符串存储和加载"""
        ht = Hashtable("ht_1")

        ht.save_string(0, 0, "hello")
        result = ht.load_string(0, 0)

        assert result == "hello"

    def test_multiple_types_same_key(self):
        """测试同一键下存储不同类型"""
        ht = Hashtable("ht_1")

        ht.save_integer(0, 0, 42)
        ht.save_real(0, 0, 3.14)
        ht.save_string(0, 0, "test")

        assert ht.load_integer(0, 0) == 42
        assert ht.load_real(0, 0) == 3.14
        assert ht.load_string(0, 0) == "test"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableBasicTypes -v`
Expected: FAIL with methods not defined

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/hashtable.py (添加方法)

    # ========== Save 方法 ==========

    def save_integer(self, parent_key: int, child_key: int, value: int) -> None:
        """存储整数"""
        if parent_key not in self._data:
            self._data[parent_key] = {}
        if child_key not in self._data[parent_key]:
            self._data[parent_key][child_key] = {}
        self._data[parent_key][child_key]["integer"] = value

    def save_real(self, parent_key: int, child_key: int, value: float) -> None:
        """存储实数"""
        if parent_key not in self._data:
            self._data[parent_key] = {}
        if child_key not in self._data[parent_key]:
            self._data[parent_key][child_key] = {}
        self._data[parent_key][child_key]["real"] = value

    def save_boolean(self, parent_key: int, child_key: int, value: bool) -> None:
        """存储布尔值"""
        if parent_key not in self._data:
            self._data[parent_key] = {}
        if child_key not in self._data[parent_key]:
            self._data[parent_key][child_key] = {}
        self._data[parent_key][child_key]["boolean"] = value

    def save_string(self, parent_key: int, child_key: int, value: str) -> bool:
        """存储字符串，返回是否成功（总是True）"""
        if parent_key not in self._data:
            self._data[parent_key] = {}
        if child_key not in self._data[parent_key]:
            self._data[parent_key][child_key] = {}
        self._data[parent_key][child_key]["string"] = value
        return True

    # ========== Load 方法 ==========

    def load_integer(self, parent_key: int, child_key: int) -> int:
        """加载整数，不存在返回 0"""
        return self._data.get(parent_key, {}).get(child_key, {}).get("integer", 0)

    def load_real(self, parent_key: int, child_key: int) -> float:
        """加载实数，不存在返回 0.0"""
        return self._data.get(parent_key, {}).get(child_key, {}).get("real", 0.0)

    def load_boolean(self, parent_key: int, child_key: int) -> bool:
        """加载布尔值，不存在返回 False"""
        return self._data.get(parent_key, {}).get(child_key, {}).get("boolean", False)

    def load_string(self, parent_key: int, child_key: int) -> Optional[str]:
        """加载字符串，不存在返回 null"""
        return self._data.get(parent_key, {}).get(child_key, {}).get("string", None)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableBasicTypes -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_hashtable.py src/jass_runner/natives/hashtable.py
git commit -m "feat(hashtable): 实现基础类型Save/Load方法"
```

---

### Task 3: Handle 类型 Save/Load 方法

**Files:**
- Modify: `src/jass_runner/natives/hashtable.py`
- Test: `tests/natives/test_hashtable.py`

**Step 1: Write the failing test**

```python
# tests/natives/test_hashtable.py (添加)

from unittest.mock import Mock

class TestHashtableHandleTypes:
    """测试 Handle 类型 Save/Load"""

    def test_save_and_load_unit_handle(self):
        """测试单位 handle 存储和加载"""
        ht = Hashtable("ht_1")
        mock_unit = Mock()
        mock_unit.id = "unit_123"

        ht.save_unit_handle(0, 0, mock_unit)

        # 验证存储的是 handle_id
        assert ht._data[0][0]["unit"] == "unit_123"

    def test_load_unit_handle(self):
        """测试加载单位 handle"""
        ht = Hashtable("ht_1")
        mock_manager = Mock()
        mock_unit = Mock()
        mock_manager.get_unit.return_value = mock_unit

        # 直接设置内部数据
        ht._data[0] = {0: {"unit": "unit_123"}}

        result = ht.load_unit_handle(0, 0, mock_manager)

        assert result == mock_unit
        mock_manager.get_unit.assert_called_once_with("unit_123")

    def test_load_unit_handle_not_found(self):
        """测试加载不存在的单位返回 None"""
        ht = Hashtable("ht_1")
        mock_manager = Mock()
        mock_manager.get_unit.return_value = None

        ht._data[0] = {0: {"unit": "unit_123"}}

        result = ht.load_unit_handle(0, 0, mock_manager)

        assert result is None

    def test_load_unit_handle_no_data(self):
        """测试加载未设置过的单位返回 None"""
        ht = Hashtable("ht_1")
        mock_manager = Mock()

        result = ht.load_unit_handle(0, 0, mock_manager)

        assert result is None
        mock_manager.get_unit.assert_not_called()

    def test_save_and_load_player_handle(self):
        """测试玩家 handle 存储和加载"""
        ht = Hashtable("ht_1")
        mock_player = Mock()
        mock_player.id = "player_0"

        ht.save_player_handle(0, 0, mock_player)

        assert ht._data[0][0]["player"] == "player_0"

    def test_save_and_load_item_handle(self):
        """测试物品 handle 存储和加载"""
        ht = Hashtable("ht_1")
        mock_item = Mock()
        mock_item.id = "item_456"

        ht.save_item_handle(0, 0, mock_item)

        assert ht._data[0][0]["item"] == "item_456"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableHandleTypes -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/hashtable.py (添加方法)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .manager import HandleManager

    # ========== Handle Save 方法 ==========

    def save_unit_handle(self, parent_key: int, child_key: int, unit) -> bool:
        """存储单位 handle，返回是否成功"""
        if parent_key not in self._data:
            self._data[parent_key] = {}
        if child_key not in self._data[parent_key]:
            self._data[parent_key][child_key] = {}
        self._data[parent_key][child_key]["unit"] = unit.id
        return True

    def save_item_handle(self, parent_key: int, child_key: int, item) -> bool:
        """存储物品 handle，返回是否成功"""
        if parent_key not in self._data:
            self._data[parent_key] = {}
        if child_key not in self._data[parent_key]:
            self._data[parent_key][child_key] = {}
        self._data[parent_key][child_key]["item"] = item.id
        return True

    def save_player_handle(self, parent_key: int, child_key: int, player) -> bool:
        """存储玩家 handle，返回是否成功"""
        if parent_key not in self._data:
            self._data[parent_key] = {}
        if child_key not in self._data[parent_key]:
            self._data[parent_key][child_key] = {}
        self._data[parent_key][child_key]["player"] = player.id
        return True

    # ========== Handle Load 方法 ==========

    def load_unit_handle(self, parent_key: int, child_key: int, handle_manager: "HandleManager"):
        """加载单位 handle，不存在或已销毁返回 null"""
        handle_id = self._data.get(parent_key, {}).get(child_key, {}).get("unit", None)
        if handle_id is None:
            return None
        return handle_manager.get_unit(handle_id)

    def load_item_handle(self, parent_key: int, child_key: int, handle_manager: "HandleManager"):
        """加载物品 handle"""
        handle_id = self._data.get(parent_key, {}).get(child_key, {}).get("item", None)
        if handle_id is None:
            return None
        return handle_manager.get_item(handle_id)

    def load_player_handle(self, parent_key: int, child_key: int, handle_manager: "HandleManager"):
        """加载玩家 handle"""
        handle_id = self._data.get(parent_key, {}).get(child_key, {}).get("player", None)
        if handle_id is None:
            return None
        # 玩家ID格式为 "player_N"，提取N
        if isinstance(handle_id, str) and handle_id.startswith("player_"):
            player_id = int(handle_id.split("_")[1])
            return handle_manager.get_player(player_id)
        return None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableHandleTypes -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_hashtable.py src/jass_runner/natives/hashtable.py
git commit -m "feat(hashtable): 实现Handle类型Save/Load方法"
```

---

### Task 4: HaveSaved 和 RemoveSaved 方法

**Files:**
- Modify: `src/jass_runner/natives/hashtable.py`
- Test: `tests/natives/test_hashtable.py`

**Step 1: Write the failing test**

```python
# tests/natives/test_hashtable.py (添加)

class TestHashtableExistenceAndRemoval:
    """测试存在性检查和删除方法"""

    def test_have_saved_integer_true(self):
        """测试检查存在的整数"""
        ht = Hashtable("ht_1")
        ht.save_integer(0, 0, 42)

        assert ht.have_saved_integer(0, 0) is True

    def test_have_saved_integer_false(self):
        """测试检查不存在的整数"""
        ht = Hashtable("ht_1")

        assert ht.have_saved_integer(0, 0) is False

    def test_have_saved_handle(self):
        """测试检查任意 handle 类型"""
        ht = Hashtable("ht_1")
        mock_unit = Mock()
        mock_unit.id = "unit_123"

        ht.save_unit_handle(0, 0, mock_unit)

        assert ht.have_saved_handle(0, 0) is True
        assert ht.have_saved_integer(0, 0) is False  # 整数不存在

    def test_remove_saved_integer(self):
        """测试删除整数"""
        ht = Hashtable("ht_1")
        ht.save_integer(0, 0, 42)

        ht.remove_saved_integer(0, 0)

        assert ht.have_saved_integer(0, 0) is False
        assert ht.load_integer(0, 0) == 0  # 返回默认值

    def test_remove_saved_handle(self):
        """测试删除所有 handle 类型"""
        ht = Hashtable("ht_1")
        mock_unit = Mock()
        mock_unit.id = "unit_123"
        mock_item = Mock()
        mock_item.id = "item_456"

        ht.save_unit_handle(0, 0, mock_unit)
        ht.save_item_handle(0, 0, mock_item)
        ht.save_integer(0, 0, 42)

        ht.remove_saved_handle(0, 0)

        assert ht.have_saved_handle(0, 0) is False
        assert ht.have_saved_integer(0, 0) is True  # 整数仍然存在
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableExistenceAndRemoval -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/hashtable.py (添加方法)

    # ========== 存在性检查 ==========

    def have_saved_integer(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在整数"""
        return "integer" in self._data.get(parent_key, {}).get(child_key, {})

    def have_saved_real(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在实数"""
        return "real" in self._data.get(parent_key, {}).get(child_key, {})

    def have_saved_boolean(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在布尔值"""
        return "boolean" in self._data.get(parent_key, {}).get(child_key, {})

    def have_saved_string(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在字符串"""
        return "string" in self._data.get(parent_key, {}).get(child_key, {})

    def have_saved_handle(self, parent_key: int, child_key: int) -> bool:
        """检查是否存在任意 handle 类型"""
        child_data = self._data.get(parent_key, {}).get(child_key, {})
        handle_types = ["unit", "item", "player"]
        return any(ht in child_data for ht in handle_types)

    # ========== 删除方法 ==========

    def remove_saved_integer(self, parent_key: int, child_key: int) -> None:
        """删除整数"""
        child_data = self._data.get(parent_key, {}).get(child_key, {})
        if "integer" in child_data:
            del child_data["integer"]

    def remove_saved_real(self, parent_key: int, child_key: int) -> None:
        """删除实数"""
        child_data = self._data.get(parent_key, {}).get(child_key, {})
        if "real" in child_data:
            del child_data["real"]

    def remove_saved_boolean(self, parent_key: int, child_key: int) -> None:
        """删除布尔值"""
        child_data = self._data.get(parent_key, {}).get(child_key, {})
        if "boolean" in child_data:
            del child_data["boolean"]

    def remove_saved_string(self, parent_key: int, child_key: int) -> None:
        """删除字符串"""
        child_data = self._data.get(parent_key, {}).get(child_key, {})
        if "string" in child_data:
            del child_data["string"]

    def remove_saved_handle(self, parent_key: int, child_key: int) -> None:
        """删除所有 handle 类型"""
        child_data = self._data.get(parent_key, {}).get(child_key, {})
        handle_types = ["unit", "item", "player"]
        for ht in handle_types:
            if ht in child_data:
                del child_data[ht]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableExistenceAndRemoval -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_hashtable.py src/jass_runner/natives/hashtable.py
git commit -m "feat(hashtable): 实现HaveSaved和RemoveSaved方法"
```

---

### Task 5: Flush 方法

**Files:**
- Modify: `src/jass_runner/natives/hashtable.py`
- Test: `tests/natives/test_hashtable.py`

**Step 1: Write the failing test**

```python
# tests/natives/test_hashtable.py (添加)

class TestHashtableFlush:
    """测试清空方法"""

    def test_flush_child(self):
        """测试清空指定 parentKey 下所有数据"""
        ht = Hashtable("ht_1")
        ht.save_integer(0, 0, 42)
        ht.save_integer(0, 1, 100)
        ht.save_integer(1, 0, 200)

        ht.flush_child(0)

        assert ht.load_integer(0, 0) == 0
        assert ht.load_integer(0, 1) == 0
        assert ht.load_integer(1, 0) == 200  # parentKey=1 的数据保留

    def test_flush_all(self):
        """测试清空整个 hashtable"""
        ht = Hashtable("ht_1")
        ht.save_integer(0, 0, 42)
        ht.save_real(1, 1, 3.14)

        ht.flush_all()

        assert ht.load_integer(0, 0) == 0
        assert ht.load_real(1, 1) == 0.0
        assert ht._data == {}
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableFlush -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/hashtable.py (添加方法)

    # ========== 清空方法 ==========

    def flush_child(self, parent_key: int) -> None:
        """删除指定 parentKey 下所有数据"""
        if parent_key in self._data:
            del self._data[parent_key]

    def flush_all(self) -> None:
        """清空整个 hashtable"""
        self._data.clear()
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_hashtable.py::TestHashtableFlush -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_hashtable.py src/jass_runner/natives/hashtable.py
git commit -m "feat(hashtable): 实现Flush方法"
```

---

### Task 6: HandleManager 支持 Hashtable

**Files:**
- Modify: `src/jass_runner/natives/manager.py`
- Test: `tests/natives/test_manager.py` (如果存在，否则创建)

**Step 1: 检查现有方法**

查看 `src/jass_runner/natives/manager.py` 是否已有 create_hashtable / get_hashtable 方法。

**Step 2: 如果需要，添加方法**

```python
# src/jass_runner/natives/manager.py

from .hashtable import Hashtable  # 添加导入

class HandleManager:
    # ... 现有代码 ...

    def create_hashtable(self) -> Hashtable:
        """创建 hashtable 并返回"""
        handle_id = f"hashtable_{self._generate_id()}"
        hashtable = Hashtable(handle_id)
        self._register_handle(hashtable)
        return hashtable

    def get_hashtable(self, handle_id: str) -> Optional[Hashtable]:
        """获取 hashtable 对象"""
        handle = self.get_handle(handle_id)
        if isinstance(handle, Hashtable):
            return handle
        return None
```

**Step 3: 添加测试**

```python
# tests/natives/test_manager.py (添加)

def test_create_hashtable(manager):
    """测试创建 hashtable"""
    from jass_runner.natives.hashtable import Hashtable

    ht = manager.create_hashtable()

    assert isinstance(ht, Hashtable)
    assert ht.id.startswith("hashtable_")
    assert manager.get_hashtable(ht.id) == ht

def test_get_hashtable_invalid(manager):
    """测试获取无效的 hashtable"""
    assert manager.get_hashtable("hashtable_invalid") is None
```

**Step 4: Run tests**

Run: `pytest tests/natives/test_manager.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_manager.py src/jass_runner/natives/manager.py
git commit -m "feat(hashtable): HandleManager支持hashtable创建和获取"
```

---

### Task 7: InitHashtable Native 函数

**Files:**
- Create: `src/jass_runner/natives/hashtable_natives.py`
- Test: `tests/natives/test_hashtable_natives.py`

**Step 1: Write the failing test**

```python
# tests/natives/test_hashtable_natives.py
"""Hashtable Native 函数测试"""

import pytest
from unittest.mock import MagicMock


class TestInitHashtable:
    """测试 InitHashtable native 函数"""

    def test_init_hashtable_returns_hashtable(self):
        """测试 InitHashtable 返回 hashtable"""
        from jass_runner.natives.hashtable_natives import InitHashtable

        mock_state = MagicMock()
        mock_state.handle_manager.create_hashtable.return_value = MagicMock(id="hashtable_1")

        native = InitHashtable()
        result = native.execute(mock_state)

        assert result is not None
        mock_state.handle_manager.create_hashtable.assert_called_once()

    def test_init_hashtable_without_handle_manager(self):
        """测试没有 handle_manager 时返回 None"""
        from jass_runner.natives.hashtable_natives import InitHashtable

        mock_state = MagicMock()
        delattr(mock_state, 'handle_manager')

        native = InitHashtable()
        result = native.execute(mock_state)

        assert result is None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_hashtable_natives.py::TestInitHashtable -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/hashtable_natives.py
"""Hashtable 相关 Native 函数"""

import logging
from typing import Any, Optional

from .base import NativeFunction


logger = logging.getLogger(__name__)


class InitHashtable(NativeFunction):
    """初始化 hashtable 的 native 函数"""

    @property
    def name(self) -> str:
        return "InitHashtable"

    def execute(self, state_context, *args, **kwargs) -> Any:
        """执行 InitHashtable native 函数

        Returns:
            hashtable 对象，如果失败返回 None
        """
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[InitHashtable] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.create_hashtable()
        logger.info(f"[InitHashtable] Created hashtable: {hashtable.id}")
        return hashtable
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_hashtable_natives.py::TestInitHashtable -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_hashtable_natives.py src/jass_runner/natives/hashtable_natives.py
git commit -m "feat(hashtable): 实现InitHashtable native函数"
```

---

### Task 8: Save* Native 函数

**Files:**
- Modify: `src/jass_runner/natives/hashtable_natives.py`
- Test: `tests/natives/test_hashtable_natives.py`

**Step 1: Write the failing test**

```python
# tests/natives/test_hashtable_natives.py (添加)

class TestSaveOperations:
    """测试 Save* native 函数"""

    def test_save_integer(self):
        """测试 SaveInteger"""
        from jass_runner.natives.hashtable_natives import SaveInteger

        mock_ht = MagicMock()
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = SaveInteger()
        native.execute(mock_state, "hashtable_1", 0, 0, 42)

        mock_state.handle_manager.get_hashtable.assert_called_once_with("hashtable_1")
        mock_ht.save_integer.assert_called_once_with(0, 0, 42)

    def test_save_real(self):
        """测试 SaveReal"""
        from jass_runner.natives.hashtable_natives import SaveReal

        mock_ht = MagicMock()
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = SaveReal()
        native.execute(mock_state, "hashtable_1", 0, 0, 3.14)

        mock_ht.save_real.assert_called_once_with(0, 0, 3.14)

    def test_save_str_returns_true(self):
        """测试 SaveStr 返回 True"""
        from jass_runner.natives.hashtable_natives import SaveStr

        mock_ht = MagicMock()
        mock_ht.save_string.return_value = True
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = SaveStr()
        result = native.execute(mock_state, "hashtable_1", 0, 0, "hello")

        assert result is True

    def test_save_unit_handle(self):
        """测试 SaveUnitHandle"""
        from jass_runner.natives.hashtable_natives import SaveUnitHandle

        mock_ht = MagicMock()
        mock_unit = MagicMock()
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = SaveUnitHandle()
        result = native.execute(mock_state, "hashtable_1", 0, 0, mock_unit)

        assert result is True
        mock_ht.save_unit_handle.assert_called_once_with(0, 0, mock_unit)

    def test_save_invalid_hashtable(self):
        """测试无效的 hashtable 记录警告"""
        from jass_runner.natives.hashtable_natives import SaveInteger

        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = None

        native = SaveInteger()
        result = native.execute(mock_state, "invalid_ht", 0, 0, 42)

        assert result is None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_hashtable_natives.py::TestSaveOperations -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/hashtable_natives.py (添加)

class SaveInteger(NativeFunction):
    """SaveInteger native 函数"""

    @property
    def name(self) -> str:
        return "SaveInteger"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, value: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveInteger] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveInteger] Hashtable not found: {hashtable_id}")
            return None

        hashtable.save_integer(parent_key, child_key, value)
        logger.debug(f"[SaveInteger] Saved integer {value} at ({parent_key}, {child_key})")
        return None


class SaveReal(NativeFunction):
    """SaveReal native 函数"""

    @property
    def name(self) -> str:
        return "SaveReal"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, value: float, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveReal] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveReal] Hashtable not found: {hashtable_id}")
            return None

        hashtable.save_real(parent_key, child_key, value)
        return None


class SaveBoolean(NativeFunction):
    """SaveBoolean native 函数"""

    @property
    def name(self) -> str:
        return "SaveBoolean"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, value: bool, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveBoolean] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveBoolean] Hashtable not found: {hashtable_id}")
            return None

        hashtable.save_boolean(parent_key, child_key, value)
        return None


class SaveStr(NativeFunction):
    """SaveStr native 函数"""

    @property
    def name(self) -> str:
        return "SaveStr"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, value: str, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveStr] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveStr] Hashtable not found: {hashtable_id}")
            return False

        result = hashtable.save_string(parent_key, child_key, value)
        return result


class SaveUnitHandle(NativeFunction):
    """SaveUnitHandle native 函数"""

    @property
    def name(self) -> str:
        return "SaveUnitHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, unit, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveUnitHandle] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveUnitHandle] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.save_unit_handle(parent_key, child_key, unit)


class SaveItemHandle(NativeFunction):
    """SaveItemHandle native 函数"""

    @property
    def name(self) -> str:
        return "SaveItemHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, item, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SaveItemHandle] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SaveItemHandle] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.save_item_handle(parent_key, child_key, item)


class SavePlayerHandle(NativeFunction):
    """SavePlayerHandle native 函数"""

    @property
    def name(self) -> str:
        return "SavePlayerHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, player, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[SavePlayerHandle] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[SavePlayerHandle] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.save_player_handle(parent_key, child_key, player)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_hashtable_natives.py::TestSaveOperations -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_hashtable_natives.py src/jass_runner/natives/hashtable_natives.py
git commit -m "feat(hashtable): 实现Save* native函数"
```

---

### Task 9: Load* Native 函数

**Files:**
- Modify: `src/jass_runner/natives/hashtable_natives.py`
- Test: `tests/natives/test_hashtable_natives.py`

**Step 1: Write the failing test**

```python
# tests/natives/test_hashtable_natives.py (添加)

class TestLoadOperations:
    """测试 Load* native 函数"""

    def test_load_integer(self):
        """测试 LoadInteger"""
        from jass_runner.natives.hashtable_natives import LoadInteger

        mock_ht = MagicMock()
        mock_ht.load_integer.return_value = 42
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = LoadInteger()
        result = native.execute(mock_state, "hashtable_1", 0, 0)

        assert result == 42
        mock_ht.load_integer.assert_called_once_with(0, 0)

    def test_load_real(self):
        """测试 LoadReal"""
        from jass_runner.natives.hashtable_natives import LoadReal

        mock_ht = MagicMock()
        mock_ht.load_real.return_value = 3.14
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = LoadReal()
        result = native.execute(mock_state, "hashtable_1", 0, 0)

        assert result == 3.14

    def test_load_unit_handle(self):
        """测试 LoadUnitHandle"""
        from jass_runner.natives.hashtable_natives import LoadUnitHandle

        mock_ht = MagicMock()
        mock_unit = MagicMock()
        mock_ht.load_unit_handle.return_value = mock_unit
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = LoadUnitHandle()
        result = native.execute(mock_state, "hashtable_1", 0, 0)

        assert result == mock_unit
        mock_ht.load_unit_handle.assert_called_once_with(0, 0, mock_state.handle_manager)

    def test_load_invalid_hashtable(self):
        """测试无效 hashtable 返回默认值"""
        from jass_runner.natives.hashtable_natives import LoadInteger

        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = None

        native = LoadInteger()
        result = native.execute(mock_state, "invalid_ht", 0, 0)

        assert result == 0  # 默认值
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_hashtable_natives.py::TestLoadOperations -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# src/jass_runner/natives/hashtable_natives.py (添加)

class LoadInteger(NativeFunction):
    """LoadInteger native 函数"""

    @property
    def name(self) -> str:
        return "LoadInteger"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> int:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadInteger] state_context or handle_manager not found")
            return 0

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadInteger] Hashtable not found: {hashtable_id}")
            return 0

        return hashtable.load_integer(parent_key, child_key)


class LoadReal(NativeFunction):
    """LoadReal native 函数"""

    @property
    def name(self) -> str:
        return "LoadReal"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> float:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadReal] state_context or handle_manager not found")
            return 0.0

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadReal] Hashtable not found: {hashtable_id}")
            return 0.0

        return hashtable.load_real(parent_key, child_key)


class LoadBoolean(NativeFunction):
    """LoadBoolean native 函数"""

    @property
    def name(self) -> str:
        return "LoadBoolean"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs) -> bool:
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadBoolean] state_context or handle_manager not found")
            return False

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadBoolean] Hashtable not found: {hashtable_id}")
            return False

        return hashtable.load_boolean(parent_key, child_key)


class LoadStr(NativeFunction):
    """LoadStr native 函数"""

    @property
    def name(self) -> str:
        return "LoadStr"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadStr] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadStr] Hashtable not found: {hashtable_id}")
            return None

        return hashtable.load_string(parent_key, child_key)


class LoadUnitHandle(NativeFunction):
    """LoadUnitHandle native 函数"""

    @property
    def name(self) -> str:
        return "LoadUnitHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadUnitHandle] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadUnitHandle] Hashtable not found: {hashtable_id}")
            return None

        return hashtable.load_unit_handle(parent_key, child_key, state_context.handle_manager)


class LoadItemHandle(NativeFunction):
    """LoadItemHandle native 函数"""

    @property
    def name(self) -> str:
        return "LoadItemHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadItemHandle] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadItemHandle] Hashtable not found: {hashtable_id}")
            return None

        return hashtable.load_item_handle(parent_key, child_key, state_context.handle_manager)


class LoadPlayerHandle(NativeFunction):
    """LoadPlayerHandle native 函数"""

    @property
    def name(self) -> str:
        return "LoadPlayerHandle"

    def execute(self, state_context, hashtable_id: str, parent_key: int,
                child_key: int, *args, **kwargs):
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[LoadPlayerHandle] state_context or handle_manager not found")
            return None

        hashtable = state_context.handle_manager.get_hashtable(hashtable_id)
        if hashtable is None:
            logger.warning(f"[LoadPlayerHandle] Hashtable not found: {hashtable_id}")
            return None

        return hashtable.load_player_handle(parent_key, child_key, state_context.handle_manager)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_hashtable_natives.py::TestLoadOperations -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_hashtable_natives.py src/jass_runner/natives/hashtable_natives.py
git commit -m "feat(hashtable): 实现Load* native函数"
```

---

### Task 10: HaveSaved* 和 RemoveSaved* Native 函数

**Files:**
- Modify: `src/jass_runner/natives/hashtable_natives.py`
- Test: `tests/natives/test_hashtable_natives.py`

**Step 1: Write tests and implementation**

参考 Task 8 和 Task 9 的模式，实现：
- HaveSavedInteger, HaveSavedReal, HaveSavedBoolean, HaveSavedString, HaveSavedHandle
- RemoveSavedInteger, RemoveSavedReal, RemoveSavedBoolean, RemoveSavedString, RemoveSavedHandle

每个函数遵循相同的模式：检查 state_context -> 获取 hashtable -> 调用对应方法

**Step 2: Commit**

```bash
git add tests/natives/test_hashtable_natives.py src/jass_runner/natives/hashtable_natives.py
git commit -m "feat(hashtable): 实现HaveSaved*和RemoveSaved* native函数"
```

---

### Task 11: Flush* Native 函数

**Files:**
- Modify: `src/jass_runner/natives/hashtable_natives.py`
- Test: `tests/natives/test_hashtable_natives.py`

**Step 1: Write tests and implementation**

实现：
- FlushChildHashtable - 调用 hashtable.flush_child(parent_key)
- FlushParentHashtable - 调用 hashtable.flush_all()

**Step 2: Commit**

```bash
git add tests/natives/test_hashtable_natives.py src/jass_runner/natives/hashtable_natives.py
git commit -m "feat(hashtable): 实现Flush* native函数"
```

---

### Task 12: NativeFactory 注册

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_factory.py`

**Step 1: 更新 factory.py**

```python
# src/jass_runner/natives/factory.py

# 添加导入
from .hashtable_natives import (
    InitHashtable,
    SaveInteger, SaveReal, SaveBoolean, SaveStr,
    SaveUnitHandle, SaveItemHandle, SavePlayerHandle,
    LoadInteger, LoadReal, LoadBoolean, LoadStr,
    LoadUnitHandle, LoadItemHandle, LoadPlayerHandle,
    HaveSavedInteger, HaveSavedReal, HaveSavedBoolean, HaveSavedString, HaveSavedHandle,
    RemoveSavedInteger, RemoveSavedReal, RemoveSavedBoolean, RemoveSavedString, RemoveSavedHandle,
    FlushChildHashtable, FlushParentHashtable,
)

# 在 create_default_registry 中添加注册
registry.register(InitHashtable())
registry.register(SaveInteger())
registry.register(SaveReal())
registry.register(SaveBoolean())
registry.register(SaveStr())
registry.register(SaveUnitHandle())
registry.register(SaveItemHandle())
registry.register(SavePlayerHandle())
registry.register(LoadInteger())
registry.register(LoadReal())
registry.register(LoadBoolean())
registry.register(LoadStr())
registry.register(LoadUnitHandle())
registry.register(LoadItemHandle())
registry.register(LoadPlayerHandle())
registry.register(HaveSavedInteger())
registry.register(HaveSavedReal())
registry.register(HaveSavedBoolean())
registry.register(HaveSavedString())
registry.register(HaveSavedHandle())
registry.register(RemoveSavedInteger())
registry.register(RemoveSavedReal())
registry.register(RemoveSavedBoolean())
registry.register(RemoveSavedString())
registry.register(RemoveSavedHandle())
registry.register(FlushChildHashtable())
registry.register(FlushParentHashtable())
```

**Step 2: 更新 test_factory.py 中的函数计数**

```python
# 更新测试中的函数数量
assert len(all_funcs) == 177 + 27  # 原有177个 + 新增27个hashtable函数
```

**Step 3: Run tests**

Run: `pytest tests/natives/test_factory.py -v`
Expected: PASS

**Step 4: Commit**

```bash
git add tests/natives/test_factory.py src/jass_runner/natives/factory.py
git commit -m "feat(hashtable): 在NativeFactory注册所有hashtable函数"
```

---

### Task 13: 集成测试

**Files:**
- Create: `tests/integration/test_hashtable_integration.py`

**Step 1: Write integration test**

```python
"""Hashtable 集成测试"""

import pytest
from jass_runner.vm.jass_vm import JassVM


class TestHashtableIntegration:
    """测试 Hashtable 完整工作流程"""

    def test_hashtable_basic_workflow(self):
        """测试 hashtable 基础工作流程"""
        script = '''
function testHashtable takes nothing returns nothing
    local hashtable ht = InitHashtable()

    call SaveInteger(ht, 0, 0, 42)
    call SaveReal(ht, 0, 0, 3.14)
    call SaveBoolean(ht, 0, 1, true)
    call SaveStr(ht, 0, 2, "hello")

    call DisplayTextToPlayer(Player(0), 0, 0, I2S(LoadInteger(ht, 0, 0)))
    call DisplayTextToPlayer(Player(0), 0, 0, R2S(LoadReal(ht, 0, 0)))
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)

    def test_hashtable_with_unit(self):
        """测试 hashtable 存储单位"""
        script = '''
function testHashtableWithUnit takes nothing returns nothing
    local hashtable ht = InitHashtable()
    local unit u = CreateUnit(Player(0), 'Hpal', 0, 0, 0)

    call SaveUnitHandle(ht, 0, 0, u)

    local unit loaded = LoadUnitHandle(ht, 0, 0)
    if loaded != null then
        call DisplayTextToPlayer(Player(0), 0, 0, "Unit loaded successfully")
    endif
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)

    def test_hashtable_flush(self):
        """测试 hashtable 清空"""
        script = '''
function testHashtableFlush takes nothing returns nothing
    local hashtable ht = InitHashtable()

    call SaveInteger(ht, 0, 0, 42)
    call FlushParentHashtable(ht)

    if LoadInteger(ht, 0, 0) == 0 then
        call DisplayTextToPlayer(Player(0), 0, 0, "Flush successful")
    endif
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)
```

**Step 2: Run tests**

Run: `pytest tests/integration/test_hashtable_integration.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/integration/test_hashtable_integration.py
git commit -m "test(hashtable): 添加集成测试"
```

---

### Task 14: 最终验证

**Step 1: Run all tests**

Run: `pytest tests/ -q`
Expected: All tests pass

**Step 2: Update PROJECT_NOTES.md**

添加新条目记录 hashtable 实现完成。

**Step 3: Final commit**

```bash
git add PROJECT_NOTES.md
git commit -m "docs: 记录hashtable实现完成"
```

---

## 总结

实施计划包含14个任务：
1. Hashtable 类基础结构
2. 基础类型 Save/Load 方法
3. Handle 类型 Save/Load 方法
4. HaveSaved 和 RemoveSaved 方法
5. Flush 方法
6. HandleManager 支持
7. InitHashtable Native 函数
8. Save* Native 函数
9. Load* Native 函数
10. HaveSaved* 和 RemoveSaved* Native 函数
11. Flush* Native 函数
12. NativeFactory 注册
13. 集成测试
14. 最终验证

**新增文件：**
- `src/jass_runner/natives/hashtable.py`
- `src/jass_runner/natives/hashtable_natives.py`
- `tests/natives/test_hashtable.py`
- `tests/natives/test_hashtable_natives.py`
- `tests/integration/test_hashtable_integration.py`

**修改文件：**
- `src/jass_runner/natives/manager.py`
- `src/jass_runner/natives/factory.py`
- `tests/natives/test_factory.py`
- `PROJECT_NOTES.md`

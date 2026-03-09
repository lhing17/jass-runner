"""JASS Hashtable 实现"""

from typing import Dict, Any, Optional, TYPE_CHECKING
from .handle_base import Handle

if TYPE_CHECKING:
    from .manager import HandleManager


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

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

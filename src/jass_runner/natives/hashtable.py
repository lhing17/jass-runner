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

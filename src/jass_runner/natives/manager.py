"""Handle管理器。

此模块包含HandleManager类，负责所有handle的生命周期管理。
"""

from typing import Dict, List, Optional
from .handle import Handle, Unit


class HandleManager:
    """集中式handle管理器。

    负责所有handle的生命周期管理。
    """

    def __init__(self):
        self._handles: Dict[str, Handle] = {}  # id -> handle对象
        self._type_index: Dict[str, List[str]] = {}  # 类型索引
        self._next_id = 1

    def _generate_id(self) -> int:
        """生成下一个ID。"""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def _register_handle(self, handle: Handle):
        """注册handle到管理器中。"""
        self._handles[handle.id] = handle

        # 更新类型索引
        if handle.type_name not in self._type_index:
            self._type_index[handle.type_name] = []
        self._type_index[handle.type_name].append(handle.id)

    def create_unit(self, unit_type: str, player_id: int,
                    x: float, y: float, facing: float) -> str:
        """创建一个单位并返回handle ID。"""
        handle_id = f"unit_{self._generate_id()}"
        unit = Unit(handle_id, unit_type, player_id, x, y, facing)
        self._register_handle(unit)
        return handle_id

    def get_handle(self, handle_id: str) -> Optional[Handle]:
        """通过ID获取handle对象。"""
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive():
            return handle
        return None

    def get_unit(self, unit_id: str) -> Optional[Unit]:
        """获取单位对象，进行类型检查。"""
        handle = self.get_handle(unit_id)
        if isinstance(handle, Unit):
            return handle
        return None

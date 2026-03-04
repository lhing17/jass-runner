"""JASS Effect特效类。

此模块包含JASS特效handle的实现。
"""

from typing import Optional, Union, Tuple

from .handle_base import Handle
from .unit import Unit
from .item import Item


class Effect(Handle):
    """特效句柄，用于标识一个已创建的特效。"""

    def __init__(self, effect_id: int, model_path: str,
                 target: Optional[Union[Unit, Item, Tuple[float, float, float]]] = None,
                 attach_point: Optional[str] = None):
        """初始化特效句柄。

        参数：
            effect_id: 特效唯一标识符
            model_path: 模型路径（原样保存）
            target: 绑定目标，可以是单位、物品或坐标三元组
            attach_point: 附着点名称（如 "hand", "origin"）
        """
        super().__init__(effect_id, "effect")
        self.model_path = model_path
        self.target = target
        self.attach_point = attach_point

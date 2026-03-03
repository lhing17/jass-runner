"""特效相关 native 函数实现。"""

import logging
from typing import TYPE_CHECKING, Union

from jass_runner.natives.base import NativeFunction
from jass_runner.natives.handle import Effect, Unit, Item

if TYPE_CHECKING:
    from jass_runner.natives.state import StateContext

logger = logging.getLogger(__name__)


class AddSpecialEffect(NativeFunction):
    """在指定坐标创建特效。"""

    @property
    def name(self) -> str:
        return "AddSpecialEffect"

    def execute(
        self,
        state_context: "StateContext",
        model_path: str,
        x: float,
        y: float
    ) -> Effect:
        """在指定坐标创建特效。

        参数：
            state_context: 状态上下文
            model_path: 特效模型路径
            x: X坐标
            y: Y坐标

        返回：
            创建的特效对象
        """
        handle_manager = state_context.handle_manager
        return handle_manager.create_effect(model_path, x, y, 0.0)


class AddSpecialEffectTarget(NativeFunction):
    """在目标对象指定附着点创建特效。"""

    @property
    def name(self) -> str:
        return "AddSpecialEffectTarget"

    def execute(
        self,
        state_context: "StateContext",
        model_path: str,
        target: Union[Unit, Item],
        attach_point: str
    ) -> Effect:
        """在目标对象指定附着点创建特效。

        参数：
            state_context: 状态上下文
            model_path: 特效模型路径
            target: 目标对象（单位或物品）
            attach_point: 附着点名称（如 "hand", "origin"）

        返回：
            创建的特效对象
        """
        handle_manager = state_context.handle_manager
        return handle_manager.create_effect_target(model_path, target, attach_point)


class DestroyEffect(NativeFunction):
    """销毁特效。"""

    @property
    def name(self) -> str:
        return "DestroyEffect"

    def execute(
        self,
        state_context: "StateContext",
        effect: Effect
    ) -> bool:
        """销毁特效。

        参数：
            state_context: 状态上下文
            effect: 要销毁的特效对象

        返回：
            销毁成功返回True，特效已死亡返回False
        """
        handle_manager = state_context.handle_manager
        return handle_manager.destroy_effect(effect)


class SetSpecialEffectScale(NativeFunction):
    """设置特效缩放。"""

    @property
    def name(self) -> str:
        return "SetSpecialEffectScale"

    def execute(
        self,
        state_context: "StateContext",
        effect: Effect,
        scale: float
    ) -> None:
        """设置特效缩放。

        参数：
            state_context: 状态上下文
            effect: 特效对象
            scale: 缩放比例
        """
        logger.info(f"[特效] 设置特效 (ID: {effect.id}) 缩放: {scale}")


class SetSpecialEffectColor(NativeFunction):
    """设置特效颜色。"""

    @property
    def name(self) -> str:
        return "SetSpecialEffectColor"

    def execute(
        self,
        state_context: "StateContext",
        effect: Effect,
        r: int,
        g: int,
        b: int,
        a: int
    ) -> None:
        """设置特效颜色。

        参数：
            state_context: 状态上下文
            effect: 特效对象
            r: 红色分量（0-255）
            g: 绿色分量（0-255）
            b: 蓝色分量（0-255）
            a: 透明度（0-255）
        """
        logger.info(f"[特效] 设置特效 (ID: {effect.id}) 颜色: RGBA({r}, {g}, {b}, {a})")

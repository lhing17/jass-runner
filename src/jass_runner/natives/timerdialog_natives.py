"""TimerDialog 相关的 native 函数。

此模块包含与 timerdialog 相关的 JASS native 函数实现。
"""

import logging
from ..natives.base import NativeFunction
from .timerdialog import TimerDialog


logger = logging.getLogger(__name__)


def _resolve_timerdialog(state_context, timerdialog):
    """解析 timerdialog，支持对象或字符串 ID。

    参数：
        state_context: 状态上下文
        timerdialog: TimerDialog 对象或 handle ID 字符串

    返回：
        TimerDialog 对象，如果无效返回 None
    """
    if isinstance(timerdialog, str):
        # 如果是字符串 ID，从 handle manager 获取对象
        return state_context.handle_manager.get_timerdialog(timerdialog)
    elif isinstance(timerdialog, TimerDialog):
        # 如果已经是对象，直接返回
        return timerdialog
    return None


class CreateTimerDialog(NativeFunction):
    """创建 timerdialog，关联指定 timer。"""

    @property
    def name(self) -> str:
        return "CreateTimerDialog"

    def execute(self, state_context, timer, *args):
        """执行 CreateTimerDialog native 函数。

        参数：
            state_context: 状态上下文
            timer: 关联的 timer 对象

        返回：
            创建的 TimerDialog 对象
        """
        timerdialog = state_context.handle_manager.create_timerdialog(timer)
        timer_id = timer.id if hasattr(timer, 'id') else str(timer)
        logger.info(f"[CreateTimerDialog] 创建 timerdialog: {timerdialog.id} (关联 timer: {timer_id})")
        return timerdialog


class DestroyTimerDialog(NativeFunction):
    """销毁 timerdialog。"""

    @property
    def name(self) -> str:
        return "DestroyTimerDialog"

    def execute(self, state_context, timerdialog, *args):
        """执行 DestroyTimerDialog native 函数。

        参数：
            state_context: 状态上下文
            timerdialog: TimerDialog 对象或 handle ID 字符串

        返回：
            bool: 是否成功销毁
        """
        td = _resolve_timerdialog(state_context, timerdialog)
        if not td:
            logger.warning("[DestroyTimerDialog] 无效的 timerdialog")
            return False

        handle_id = td.id
        success = state_context.handle_manager.destroy_handle(handle_id)
        if success:
            logger.info(f"[DestroyTimerDialog] 销毁 timerdialog: {handle_id}")
        else:
            logger.warning(f"[DestroyTimerDialog] 未找到 timerdialog: {handle_id}")
        return success


class TimerDialogSetTitle(NativeFunction):
    """设置 timerdialog 标题。"""

    @property
    def name(self) -> str:
        return "TimerDialogSetTitle"

    def execute(self, state_context, timerdialog, title, *args):
        """执行 TimerDialogSetTitle native 函数。

        参数：
            state_context: 状态上下文
            timerdialog: TimerDialog 对象或 handle ID 字符串
            title: 标题字符串

        返回：
            bool: 是否成功设置
        """
        td = _resolve_timerdialog(state_context, timerdialog)
        if not td:
            logger.warning("[TimerDialogSetTitle] 无效的 timerdialog")
            return False

        td.title = title
        logger.info(f'[TimerDialogSetTitle] 设置 timerdialog {td.id} 标题为: "{title}"')
        return True


class TimerDialogDisplay(NativeFunction):
    """设置 timerdialog 显示/隐藏。"""

    @property
    def name(self) -> str:
        return "TimerDialogDisplay"

    def execute(self, state_context, timerdialog, display, *args):
        """执行 TimerDialogDisplay native 函数。

        参数：
            state_context: 状态上下文
            timerdialog: TimerDialog 对象或 handle ID 字符串
            display: 是否显示（布尔值）

        返回：
            bool: 是否成功设置
        """
        td = _resolve_timerdialog(state_context, timerdialog)
        if not td:
            logger.warning("[TimerDialogDisplay] 无效的 timerdialog")
            return False

        td.displayed = display
        action = "显示" if display else "隐藏"
        logger.info(f"[TimerDialogDisplay] {action} timerdialog: {td.id}")
        return True


class IsTimerDialogDisplayed(NativeFunction):
    """检查 timerdialog 是否显示。"""

    @property
    def name(self) -> str:
        return "IsTimerDialogDisplayed"

    def execute(self, state_context, timerdialog, *args):
        """执行 IsTimerDialogDisplayed native 函数。

        参数：
            state_context: 状态上下文
            timerdialog: TimerDialog 对象或 handle ID 字符串

        返回：
            bool: 是否显示
        """
        td = _resolve_timerdialog(state_context, timerdialog)
        if not td:
            logger.warning("[IsTimerDialogDisplayed] 无效的 timerdialog")
            return False

        return td.displayed

"""TimerDialog 相关的 native 函数。

此模块包含与 timerdialog 相关的 JASS native 函数实现。
"""

import logging
from ..natives.base import NativeFunction


logger = logging.getLogger(__name__)


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
            timerdialog: TimerDialog 对象

        返回：
            bool: 是否成功销毁
        """
        if not timerdialog:
            logger.warning("[DestroyTimerDialog] 无效的 timerdialog")
            return False

        handle_id = timerdialog.id if hasattr(timerdialog, 'id') else str(timerdialog)
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
            timerdialog: TimerDialog 对象
            title: 标题字符串

        返回：
            bool: 是否成功设置
        """
        if not timerdialog:
            logger.warning("[TimerDialogSetTitle] 无效的 timerdialog")
            return False

        timerdialog.title = title
        handle_id = timerdialog.id if hasattr(timerdialog, 'id') else str(timerdialog)
        logger.info(f'[TimerDialogSetTitle] 设置 timerdialog {handle_id} 标题为: "{title}"')
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
            timerdialog: TimerDialog 对象
            display: 是否显示（布尔值）

        返回：
            bool: 是否成功设置
        """
        if not timerdialog:
            logger.warning("[TimerDialogDisplay] 无效的 timerdialog")
            return False

        timerdialog.displayed = display
        handle_id = timerdialog.id if hasattr(timerdialog, 'id') else str(timerdialog)
        action = "显示" if display else "隐藏"
        logger.info(f"[TimerDialogDisplay] {action} timerdialog: {handle_id}")
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
            timerdialog: TimerDialog 对象

        返回：
            bool: 是否显示
        """
        if not timerdialog:
            logger.warning("[IsTimerDialogDisplayed] 无效的 timerdialog")
            return False

        return timerdialog.displayed

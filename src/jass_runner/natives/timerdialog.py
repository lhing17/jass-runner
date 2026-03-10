"""TimerDialog handle 类。

此模块包含 TimerDialog 类，用于表示 JASS 中的 timerdialog 类型。
"""

from .handle_base import Handle


class TimerDialog(Handle):
    """计时器对话框 handle。

    属性：
        timer: 关联的 timer 对象
        title: 对话框标题
        displayed: 是否显示
    """

    def __init__(self, handle_id: str, timer):
        """初始化 TimerDialog。

        参数：
            handle_id: 唯一标识符
            timer: 关联的 timer 对象
        """
        super().__init__(handle_id, "timerdialog")
        self.timer = timer
        self.title = ""
        self.displayed = False

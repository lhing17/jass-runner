"""JASS 解释器协程实现。

此模块包含 JassCoroutine 类，用于包装 JASS 函数执行作为协程，
支持程序计数器（PC）驱动的语句逐步执行，以及 SleepInterrupt 和 ReturnSignal 的处理。
"""

from typing import Generator, Optional, Any, List
from ..coroutine import Coroutine, CoroutineStatus
from ..coroutine.signals import SleepSignal
from ..coroutine.exceptions import SleepInterrupt
from .control_flow import ReturnSignal


class JassCoroutine(Coroutine):
    """JASS 函数执行的协程包装。

    将 JASS 函数体转换为可暂停、可恢复的生成器执行，
    支持通过程序计数器（PC）实现语句级断点恢复。

    属性:
        interpreter: 解释器实例
        func: 函数定义（FunctionDecl）
        args: 调用参数列表
        _pc: 程序计数器，指向下一个要执行的语句索引
    """

    def __init__(self, interpreter, func, args: Optional[List] = None):
        """初始化 JassCoroutine。

        参数：
            interpreter: 解释器实例
            func: 函数定义节点（FunctionDecl）
            args: 函数参数值列表（可选）
        """
        super().__init__(interpreter, func, args)
        self._pc = 0  # 程序计数器
        self._func_context = None  # 函数执行上下文

    def _run(self) -> Generator:
        """执行函数体作为生成器。

        这是一个生成器函数，通过程序计数器控制语句执行流程，
        支持在 SleepInterrupt 时暂停并在指定时间后恢复。

        生成：
            SleepSignal: 当遇到 TriggerSleepAction 暂停时

        异常：
            ReturnSignal: 当执行 return 语句时，用于提前结束函数
        """
        self._setup_context()
        statements = self.func.body or []

        while self._pc < len(statements):
            statement = statements[self._pc]

            try:
                self.interpreter.execute_statement(statement)
                self._pc += 1

            except SleepInterrupt as e:
                # 遇到睡眠中断，增加PC并产生睡眠信号
                self._pc += 1
                yield SleepSignal(e.duration)

            except ReturnSignal:
                # 遇到return语句，结束函数执行
                break

        self._teardown_context()
        self.status = CoroutineStatus.FINISHED

    def _setup_context(self):
        """设置函数执行上下文。

        创建新的 ExecutionContext 作为函数的执行环境，
        绑定参数值到参数名，并更新解释器的当前上下文。
        """
        from .context import ExecutionContext

        # 创建函数级执行上下文
        func_context = ExecutionContext(
            parent=self.interpreter.global_context,
            native_registry=self.interpreter.global_context.native_registry,
            state_context=self.interpreter.state_context,
            interpreter=self.interpreter
        )

        # 绑定实参到形参
        if self.args:
            for param, arg_value in zip(self.func.parameters, self.args):
                func_context.set_variable(param.name, arg_value)

        # 更新解释器的当前上下文
        self.interpreter.current_context = func_context
        self.interpreter.evaluator.context = func_context
        self._func_context = func_context

    def _teardown_context(self):
        """清理函数执行上下文。

        将解释器的当前上下文恢复到全局上下文，
        结束当前函数的执行环境。
        """
        self.interpreter.current_context = self.interpreter.global_context
        self.interpreter.evaluator.context = self.interpreter.global_context
        self._func_context = None

    def resume(self):
        """恢复协程执行。

        从上次暂停的位置继续执行函数体。

        返回：
            SleepSignal 或 None: 如果遇到睡眠信号则返回 SleepSignal，
                               否则返回 None 表示正常继续执行
        """
        if self.status != CoroutineStatus.RUNNING or not self.generator:
            return None

        try:
            signal = next(self.generator)
            if isinstance(signal, SleepSignal):
                self.status = CoroutineStatus.SLEEPING
                return signal
        except StopIteration:
            self.status = CoroutineStatus.FINISHED

        return None

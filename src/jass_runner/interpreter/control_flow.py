"""控制流异常定义。

此模块定义用于控制流跳转的特殊异常类。
"""


class ReturnSignal(Exception):
    """函数返回信号，携带返回值。

    当执行return语句时抛出，用于从函数任意位置提前返回。

    属性:
        value: 返回值，对于return nothing为None
    """

    def __init__(self, value):
        self.value = value
        super().__init__(f"Return with value: {value}")


class ExitLoopSignal(Exception):
    """退出当前循环的信号。

    当执行exitwhen语句且条件为真时抛出，用于跳出loop循环。
    """
    pass

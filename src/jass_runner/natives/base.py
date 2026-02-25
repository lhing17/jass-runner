"""Native函数基类。

此模块定义了JASS native函数的抽象基类，所有native函数必须继承此类。
"""

from abc import ABC, abstractmethod


class NativeFunction(ABC):
    """JASS native函数的抽象基类。

    所有JASS native函数都必须继承此类，并实现name属性和execute方法。
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            native函数的名称字符串
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        """执行native函数。

        参数：
            *args: 位置参数
            **kwargs: 关键字参数

        返回：
            native函数的执行结果
        """
        pass
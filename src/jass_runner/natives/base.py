"""Native函数基类。

此模块定义了JASS native函数的抽象基类，所有native函数必须继承此类。
"""

from abc import ABC, abstractmethod
from typing import Optional


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

    @property
    def source(self) -> str:
        """获取native函数的来源。

        用于区分不同来源的native函数，如：
        - "common.j": 标准JASS native函数
        - "blizzard.j": Blizzard扩展函数
        - "KKAPI.j": KK对战平台扩展API
        - "DzAPI.j": 网易平台扩展API

        返回：
            native函数来源标识字符串，默认为"common.j"
        """
        return "common.j"

    @abstractmethod
    def execute(self, state_context, *args, **kwargs):
        """执行native函数。

        参数：
            state_context: 状态上下文，提供对HandleManager等的访问
            *args: 位置参数
            **kwargs: 关键字参数

        返回：
            native函数的执行结果
        """
        pass
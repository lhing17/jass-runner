"""GameState 类型定义。

此模块定义 JASS gamestate 类型和常量。
"""


class IGameState:
    """整数类型游戏状态。

    用于表示整数值的游戏状态。
    """

    DIVINE_INTERVENTION = 0
    DISCONNECTED = 1


class FGameState:
    """浮点类型游戏状态。

    用于表示浮点数值的游戏状态。
    """

    TIME_OF_DAY = 2

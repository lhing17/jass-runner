"""JASS handle类体系。

此模块包含所有JASS handle的基类和具体实现。
"""


class Handle:
    """所有JASS handle的基类。

    属性：
        id: 唯一标识符（字符串）
        type_name: handle类型名称
        alive: 是否存活
    """

    def __init__(self, handle_id: str, type_name: str):
        self.id = handle_id
        self.type_name = type_name
        self.alive = True

    def destroy(self):
        """标记handle为销毁状态。"""
        self.alive = False

    def is_alive(self) -> bool:
        """检查handle是否存活。"""
        return self.alive


class Unit(Handle):
    """单位handle。

    属性：
        unit_type: 单位类型代码（如'hfoo'）
        player_id: 所属玩家ID
        x, y: 位置坐标
        facing: 面向角度
        life: 当前生命值
        max_life: 最大生命值
        mana: 当前魔法值
        max_mana: 最大魔法值
    """

    def __init__(self, handle_id: str, unit_type: str, player_id: int,
                 x: float, y: float, facing: float):
        super().__init__(handle_id, "unit")
        self.unit_type = unit_type
        self.player_id = player_id
        self.x = x
        self.y = y
        self.z = 0.0  # Z轴高度，默认为0
        self.facing = facing
        self.life = 100.0
        self.max_life = 100.0
        self.mana = 50.0
        self.max_mana = 50.0

    def destroy(self):
        """销毁单位，将生命值设为0。"""
        self.life = 0
        super().destroy()


class Player(Handle):
    """玩家handle。

    属性：
        player_id: 玩家ID（0-15）
        name: 玩家名称
        race: 种族（如'human', 'orc', 'undead', 'nightelf'）
        color: 玩家颜色ID
        slot_state: 插槽状态（'empty', 'closed', 'player'）
        controller: 控制器类型（'user', 'computer', 'neutral', 'rescueable'）
    """

    def __init__(self, handle_id: str, player_id: int):
        super().__init__(handle_id, "player")
        self.player_id = player_id
        self.name = f"玩家{player_id}"
        self.race = "human"  # 默认人类
        self.color = player_id  # 默认颜色等于ID
        self.slot_state = "player" if player_id < 12 else "empty"  # 0-11为玩家，12-15为空
        self.controller = "user" if player_id < 8 else "computer" if player_id < 12 else "neutral"


class Item(Handle):
    """物品handle。

    属性：
        item_type: 物品类型代码（如'ratf'代表攻击之爪）
        x, y: 位置坐标
    """

    def __init__(self, handle_id: str, item_type: str, x: float, y: float):
        super().__init__(handle_id, "item")
        self.item_type = item_type
        self.x = x
        self.y = y

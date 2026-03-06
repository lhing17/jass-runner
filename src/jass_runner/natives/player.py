"""JASS Player玩家类。

此模块包含JASS玩家handle的实现。
"""

from typing import Dict, Set

from .handle_base import Handle


class Player(Handle):
    """玩家handle。

    属性：
        player_id: 玩家ID（0-15）
        name: 玩家名称
        race: 种族（如'human', 'orc', 'undead', 'nightelf'）
        color: 玩家颜色ID
        slot_state: 插槽状态（'empty', 'closed', 'player'）
        controller: 控制器类型（'user', 'computer', 'neutral', 'rescueable'）
        _gold, _lumber: 黄金和木材
        _food_cap, _food_used: 人口上限和已用人口
        _allies: 盟友玩家ID集合
        _enemies: 敌人玩家ID集合
    """

    # 玩家状态类型常量
    PLAYER_STATE_RESOURCE_GOLD = 1
    PLAYER_STATE_RESOURCE_LUMBER = 2
    PLAYER_STATE_RESOURCE_FOOD_CAP = 4
    PLAYER_STATE_RESOURCE_FOOD_USED = 5

    def __init__(self, handle_id: str, player_id: int):
        super().__init__(handle_id, "player")
        self.player_id = player_id
        self.name = f"玩家{player_id}"
        self.race = "human"  # 默认人类
        self.color = player_id  # 默认颜色等于ID
        self.slot_state = "player" if player_id < 12 else "empty"  # 0-11为玩家，12-15为空
        # MAP_CONTROL_USER=0, MAP_CONTROL_COMPUTER=1, MAP_CONTROL_NEUTRAL=3
        if player_id < 8:
            self.controller = 0  # MAP_CONTROL_USER
        elif player_id < 12:
            self.controller = 1  # MAP_CONTROL_COMPUTER
        else:
            self.controller = 3  # MAP_CONTROL_NEUTRAL
        self._allies: Set[int] = set()  # 盟友玩家ID集合
        self._enemies: Set[int] = set()  # 敌人玩家ID集合
        # 资源属性（最小集）
        self._gold: int = 500         # 黄金 0-1000000，初始500
        self._lumber: int = 0         # 木材 0-1000000，初始0
        self._food_cap: int = 100     # 人口上限 0-300，初始100
        self._food_used: int = 0      # 已用人口 0-food_cap，初始0
        # 通用状态存储字典（用于非资源类状态）
        self._state_data: Dict[int, int] = {}
        # 科技系统
        self._tech_max_allowed: Dict[int, int] = {}  # techid -> 最大允许等级
        self._tech_researched: Dict[int, int] = {}   # techid -> 当前研究等级

    def _clamp_resource(self, value: int, min_val: int, max_val: int) -> int:
        """将值截断到有效范围。

        参数：
            value: 要截断的值
            min_val: 最小值
            max_val: 最大值

        返回：
            截断后的值
        """
        return max(min_val, min(value, max_val))

    def get_state(self, state_type: int) -> int:
        """获取玩家状态值。

        参数：
            state_type: 状态类型（PLAYER_STATE_RESOURCE_*）

        返回：
            状态值

        异常：
            ValueError: 无效的状态类型
        """
        if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
            return self._gold
        elif state_type == Player.PLAYER_STATE_RESOURCE_LUMBER:
            return self._lumber
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_CAP:
            return self._food_cap
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_USED:
            return self._food_used
        else:
            # 其他状态从字典读取，默认为 0
            return self._state_data.get(state_type, 0)

    def set_state(self, state_type: int, value: int) -> int:
        """设置玩家状态值。

        参数：
            state_type: 状态类型（PLAYER_STATE_RESOURCE_*）
            value: 要设置的值

        返回：
            实际设置的值（超出范围时自动截断到边界）

        异常：
            ValueError: 无效的状态类型
        """
        if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
            self._gold = self._clamp_resource(value, 0, 1000000)
            return self._gold
        elif state_type == Player.PLAYER_STATE_RESOURCE_LUMBER:
            self._lumber = self._clamp_resource(value, 0, 1000000)
            return self._lumber
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_CAP:
            self._food_cap = self._clamp_resource(value, 0, 300)
            return self._food_cap
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_USED:
            # 已用人口不能超过人口上限
            max_food = self._food_cap
            self._food_used = self._clamp_resource(value, 0, max_food)
            return self._food_used
        else:
            # 其他状态存入字典
            self._state_data[state_type] = value
            return value

    def set_alliance(self, other_player_id: int, is_ally: bool) -> None:
        """设置与其他玩家的关系。

        参数：
            other_player_id: 其他玩家ID
            is_ally: True表示设为盟友，False表示设为敌人
        """
        if is_ally:
            self._allies.add(other_player_id)
            self._enemies.discard(other_player_id)
        else:
            self._enemies.add(other_player_id)
            self._allies.discard(other_player_id)

    def is_ally(self, other_player_id: int) -> bool:
        """检查是否是指定玩家的盟友。

        参数：
            other_player_id: 其他玩家ID

        返回：
            是盟友返回True，否则返回False
        """
        return other_player_id in self._allies

    def is_enemy(self, other_player_id: int) -> bool:
        """检查是否是指定玩家的敌人。

        参数：
            other_player_id: 其他玩家ID

        返回：
            是敌人返回True，否则返回False
        """
        return other_player_id in self._enemies

    def set_tech_max_allowed(self, techid: int, maximum: int) -> None:
        """设置科技最大允许等级。

        参数：
            techid: 科技ID（FourCC）
            maximum: 最大允许等级
        """
        self._tech_max_allowed[techid] = maximum

    def get_tech_max_allowed(self, techid: int) -> int:
        """获取科技最大允许等级。

        参数：
            techid: 科技ID（FourCC）

        返回：
            最大允许等级，未设置返回0
        """
        return self._tech_max_allowed.get(techid, 0)

    def add_tech_researched(self, techid: int, levels: int) -> None:
        """增加科技研究等级。

        参数：
            techid: 科技ID（FourCC）
            levels: 要增加的等级数
        """
        current = self._tech_researched.get(techid, 0)
        self._tech_researched[techid] = current + levels

    def set_tech_researched(self, techid: int, level: int) -> None:
        """设置科技研究等级。

        参数：
            techid: 科技ID（FourCC）
            level: 研究等级
        """
        self._tech_researched[techid] = level

    def get_tech_researched(self, techid: int, specificonly: bool) -> bool:
        """检查科技是否已研究。

        参数：
            techid: 科技ID（FourCC）
            specificonly: 是否只检查特定科技

        返回：
            已研究返回True，否则返回False
        """
        return self._tech_researched.get(techid, 0) > 0

    def get_tech_count(self, techid: int, specificonly: bool) -> int:
        """获取科技研究等级。

        参数：
            techid: 科技ID（FourCC）
            specificonly: 是否只检查特定科技

        返回：
            研究等级，未设置返回0
        """
        return self._tech_researched.get(techid, 0)


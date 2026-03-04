"""Native函数工厂。

此模块包含NativeFactory类，用于创建预配置的native函数注册表。
"""

from .registry import NativeRegistry
from .basic import DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState, CreateItem, RemoveItem, PlayerNative
from .math_core import SquareRoot, Pow, Cos, Sin, R2I, I2R
from .math_extended import Tan, ModuloInteger, ModuloReal, R2S, S2R, I2S, S2I, GetRandomInt, GetRandomReal
from .timer_natives import CreateTimer, TimerStart, TimerGetElapsed, DestroyTimer, PauseTimer, ResumeTimer
from .trigger_natives import (
    CreateTrigger,
    DestroyTrigger,
    EnableTrigger,
    DisableTrigger,
    IsTriggerEnabled,
    TriggerAddAction,
    TriggerRemoveAction,
    TriggerClearActions,
    TriggerAddCondition,
    TriggerRemoveCondition,
    TriggerClearConditions,
    TriggerEvaluate,
    TriggerClearEvents,
)
from .trigger_register_event_natives import (
    TriggerRegisterTimerEvent,
    TriggerRegisterTimerExpireEvent,
    TriggerRegisterPlayerUnitEvent,
    TriggerRegisterUnitEvent,
    TriggerRegisterPlayerEvent,
    TriggerRegisterGameEvent,
)
from .async_natives import TriggerSleepAction, ExecuteFunc
from .unit_property_natives import SetUnitState, GetUnitX, GetUnitY, GetUnitLoc, GetUnitTypeId, GetUnitName
from .unit_position_natives import SetUnitPosition, SetUnitPositionLoc, CreateUnitAtLoc, GetUnitFacing, SetUnitFacing, CreateUnitAtLocByName
from .location import LocationConstructor, RemoveLocation
from .group_natives import CreateGroup, DestroyGroup, GroupAddUnit, GroupRemoveUnit, GroupClear, FirstOfGroup, IsUnitInGroup, ForGroup, BlzGroupGetSize, BlzGroupUnitAt, GroupEnumUnitsOfPlayer, GroupEnumUnitsInRange, GroupEnumUnitsInRangeOfLoc, GroupEnumUnitsInRect
from .ability_natives import UnitAddAbility, UnitRemoveAbility, GetUnitAbilityLevel, SetUnitAbilityLevel, IncUnitAbilityLevel, DecUnitAbilityLevel, UnitMakeAbilityPermanent
from .unit_state_natives import GetWidgetLife, SetWidgetLife, UnitDamageTarget, GetUnitLevel, IsUnitType, IsUnitAlive, IsUnitDead
from .unit_ownership_natives import IsUnitOwnedByPlayer, SetUnitOwner, IsUnitAlly, IsUnitEnemy
from .unit_range_natives import IsUnitInRangeXY, IsUnitInRangeLoc, IsUnitInRange
from .item_inventory_natives import (
    UnitAddItem,
    UnitAddItemById,
    UnitRemoveItem,
    UnitRemoveItemFromSlot,
    GetItemTypeId,
    UnitItemInSlot,
)
from .player_state_natives import (
    GetPlayerState,
    SetPlayerState,
    ConvertPlayerState,
)
from .player_name_natives import (
    GetPlayerName,
    SetPlayerName,
)
from .alliance_natives import ConvertAllianceType, SetPlayerAlliance, GetPlayerAlliance
from .effect_natives import (
    AddSpecialEffect,
    AddSpecialEffectTarget,
    DestroyEffect,
    SetSpecialEffectScale,
    SetSpecialEffectColor,
)
from .camera import GetCameraMargin, SetCameraBounds, SetDayNightModels
from .sound_natives import NewSoundEnvironment, SetAmbientDaySound, SetAmbientNightSound, SetMapMusic
from .boolexpr_natives import (
    Condition,
    Filter,
    DestroyCondition,
    DestroyFilter,
    And,
    Or,
    Not,
    DestroyBoolExpr,
)
from .force_natives import (
    CreateForce,
    DestroyForce,
    ForceAddPlayer,
    ForceRemovePlayer,
    ForceClear,
    ForceEnumPlayers,
)
from .game_speed_natives import (
    ConvertGameSpeed,
    GetGameSpeed,
    SetGameSpeed,
)
from .fog_natives import FogState, FogMaskEnable, FogEnable, IsFogMaskEnabled, IsFogEnabled


class NativeFactory:
    """Native函数工厂。

    此类负责创建预配置的native函数注册表，简化注册过程。
    """

    def __init__(self, timer_system=None):
        """初始化工厂。

        参数：
            timer_system: 可选的计时器系统实例
        """
        self._timer_system = timer_system
        self._fog_state = FogState()  # 初始化迷雾状态

    def create_default_registry(self) -> NativeRegistry:
        """创建包含默认native函数的注册表。

        返回：
            NativeRegistry: 包含DisplayTextToPlayer、KillUnit、CreateUnit和GetUnitState的注册表
        """
        registry = NativeRegistry()

        # 注册基础native函数
        registry.register(DisplayTextToPlayer())
        registry.register(KillUnit())
        registry.register(CreateUnit())
        registry.register(GetUnitState())
        registry.register(CreateItem())
        registry.register(RemoveItem())
        registry.register(PlayerNative())

        # 注册触发器生命周期native函数
        registry.register(CreateTrigger())
        registry.register(DestroyTrigger())
        registry.register(EnableTrigger())
        registry.register(DisableTrigger())
        registry.register(IsTriggerEnabled())

        # 注册触发器动作管理native函数
        registry.register(TriggerAddAction())
        registry.register(TriggerRemoveAction())
        registry.register(TriggerClearActions())

        # 注册触发器条件管理native函数
        registry.register(TriggerAddCondition())
        registry.register(TriggerRemoveCondition())
        registry.register(TriggerClearConditions())
        registry.register(TriggerEvaluate())

        # 注册触发器事件管理native函数
        registry.register(TriggerClearEvents())

        # 注册触发器事件注册native函数
        registry.register(TriggerRegisterTimerEvent())
        registry.register(TriggerRegisterTimerExpireEvent())
        registry.register(TriggerRegisterPlayerUnitEvent())
        registry.register(TriggerRegisterUnitEvent())
        registry.register(TriggerRegisterPlayerEvent())
        registry.register(TriggerRegisterGameEvent())

        # 注册数学core native函数
        registry.register(SquareRoot())
        registry.register(Pow())
        registry.register(Cos())
        registry.register(Sin())
        registry.register(R2I())
        registry.register(I2R())

        # 注册数学extended native函数
        registry.register(Tan())
        registry.register(ModuloInteger())
        registry.register(ModuloReal())
        registry.register(R2S())
        registry.register(S2R())
        registry.register(I2S())
        registry.register(S2I())
        registry.register(GetRandomInt())
        registry.register(GetRandomReal())

        # 如果计时器系统可用，注册计时器原生函数
        if self._timer_system:
            registry.register(CreateTimer(self._timer_system))
            registry.register(TimerStart(self._timer_system))
            registry.register(TimerGetElapsed(self._timer_system))
            registry.register(DestroyTimer(self._timer_system))
            registry.register(PauseTimer(self._timer_system))
            registry.register(ResumeTimer(self._timer_system))

        # 注册异步原生函数
        registry.register(TriggerSleepAction())
        registry.register(ExecuteFunc())

        # 注册单位属性native函数
        registry.register(SetUnitState())
        registry.register(GetUnitX())
        registry.register(GetUnitY())
        registry.register(GetUnitLoc())
        registry.register(GetUnitTypeId())
        registry.register(GetUnitName())

        # 注册单位位置native函数
        registry.register(SetUnitPosition())
        registry.register(SetUnitPositionLoc())
        registry.register(CreateUnitAtLoc())
        registry.register(GetUnitFacing())
        registry.register(SetUnitFacing())
        registry.register(CreateUnitAtLocByName())

        # 注册 Location 相关 native 函数
        registry.register(LocationConstructor())
        registry.register(RemoveLocation())

        # 注册单位组native函数
        registry.register(CreateGroup())
        registry.register(DestroyGroup())
        registry.register(GroupAddUnit())
        registry.register(GroupRemoveUnit())
        registry.register(GroupClear())
        registry.register(FirstOfGroup())
        registry.register(IsUnitInGroup())
        registry.register(ForGroup())

        # 注册Blz单位组扩展函数
        registry.register(BlzGroupGetSize())
        registry.register(BlzGroupUnitAt())

        # 注册单位组枚举native函数
        registry.register(GroupEnumUnitsOfPlayer())
        registry.register(GroupEnumUnitsInRange())
        registry.register(GroupEnumUnitsInRangeOfLoc())
        registry.register(GroupEnumUnitsInRect())

        # 注册技能系统native函数
        registry.register(UnitAddAbility())
        registry.register(UnitRemoveAbility())
        registry.register(GetUnitAbilityLevel())
        registry.register(SetUnitAbilityLevel())
        registry.register(IncUnitAbilityLevel())
        registry.register(DecUnitAbilityLevel())
        registry.register(UnitMakeAbilityPermanent())

        # 注册单位状态native函数
        registry.register(GetWidgetLife())
        registry.register(SetWidgetLife())
        registry.register(UnitDamageTarget())
        registry.register(GetUnitLevel())
        registry.register(IsUnitType())
        registry.register(IsUnitAlive())
        registry.register(IsUnitDead())

        # 注册单位所有权native函数
        registry.register(IsUnitOwnedByPlayer())
        registry.register(SetUnitOwner())
        registry.register(IsUnitAlly())
        registry.register(IsUnitEnemy())

        # 注册单位范围检测native函数
        registry.register(IsUnitInRangeXY())
        registry.register(IsUnitInRangeLoc())
        registry.register(IsUnitInRange())

        # 注册物品背包native函数
        registry.register(UnitAddItem())
        registry.register(UnitAddItemById())
        registry.register(UnitRemoveItem())
        registry.register(UnitRemoveItemFromSlot())
        registry.register(GetItemTypeId())
        registry.register(UnitItemInSlot())

        # 注册特效native函数
        registry.register(AddSpecialEffect())
        registry.register(AddSpecialEffectTarget())
        registry.register(DestroyEffect())
        registry.register(SetSpecialEffectScale())
        registry.register(SetSpecialEffectColor())

        # 注册玩家资源native函数
        registry.register(GetPlayerState())
        registry.register(SetPlayerState())
        registry.register(ConvertPlayerState())

        # 注册玩家名称native函数
        registry.register(GetPlayerName())
        registry.register(SetPlayerName())

        # Camera natives
        registry.register(GetCameraMargin())
        registry.register(SetCameraBounds())
        registry.register(SetDayNightModels())

        # Sound natives
        registry.register(NewSoundEnvironment())
        registry.register(SetAmbientDaySound())
        registry.register(SetAmbientNightSound())
        registry.register(SetMapMusic())

        # 注册联盟相关 native 函数
        registry.register(ConvertAllianceType())
        registry.register(SetPlayerAlliance())
        registry.register(GetPlayerAlliance())

        # 注册布尔表达式相关 native 函数
        registry.register(Condition())
        registry.register(Filter())
        registry.register(DestroyCondition())
        registry.register(DestroyFilter())
        registry.register(And())
        registry.register(Or())
        registry.register(Not())
        registry.register(DestroyBoolExpr())

        # 注册玩家组(force)相关 native 函数
        registry.register(CreateForce())
        registry.register(DestroyForce())
        registry.register(ForceAddPlayer())
        registry.register(ForceRemovePlayer())
        registry.register(ForceClear())
        registry.register(ForceEnumPlayers())

        # 注册游戏速度相关 native 函数
        registry.register(ConvertGameSpeed())
        registry.register(GetGameSpeed())
        registry.register(SetGameSpeed())

        # 注册战争迷雾相关的 native 函数
        registry.register(FogMaskEnable(self._fog_state))
        registry.register(FogEnable(self._fog_state))
        registry.register(IsFogMaskEnabled(self._fog_state))
        registry.register(IsFogEnabled(self._fog_state))

        return registry
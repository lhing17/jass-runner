globals
//globals from AttackMonsterData:
constant boolean LIBRARY_AttackMonsterData=true
    // 怪物类型
constant integer MONSTER_TYPE_NORMAL= 1
constant integer MONSTER_TYPE_TANK= 2
constant integer MONSTER_TYPE_DPS= 3
constant integer MONSTER_TYPE_SPECIAL= 4

    // 怪物波次配置
constant integer MAX_WAVE_COUNT= 50
    // 怪物ID - 对应地图中的单位ID (使用四字符代码)
constant integer MONSTER_ID_NORMAL= 'n001'
constant integer MONSTER_ID_TANK= 'n002'
constant integer MONSTER_ID_DPS= 'n003'
constant integer MONSTER_ID_SPECIAL= 'n004'

    // 怪物生成点 (使用坐标)
constant real SPAWN_POINT_X= - 6000
constant real SPAWN_POINT_Y= 0
    // 怪物目标点 (移动攻击的位置)
constant real TARGET_POINT_X= 300
constant real TARGET_POINT_Y= - 150.0
    // 怪物生成间隔 (同波次怪物间的延迟，秒)
constant real MONSTER_SPAWN_INTERVAL= 1.0
    // 波次属性倍数，随波次增长
constant real WAVE_HP_MULTIPLIER= 1.15
constant real WAVE_DAMAGE_MULTIPLIER= 1.12
constant real WAVE_SPEED_MULTIPLIER= 1.02
    // 特殊怪物类型
constant integer SPECIAL_MONSTER_HEALER= 1
constant integer SPECIAL_MONSTER_SUMMONER= 2
constant integer SPECIAL_MONSTER_BOMBER= 3
    // 数组存储每波怪物信息 (转换为一维数组)
integer array udg_monster_types_per_wave
integer array udg_monster_count_per_wave
//endglobals from AttackMonsterData
//globals from BzAPI:
constant boolean LIBRARY_BzAPI=true
//endglobals from BzAPI
//globals from CultivationData:
constant boolean LIBRARY_CultivationData=true
        // ========================================================================
        // 历练等级常量定义
        // ========================================================================
constant integer CULTIVATION_LEVEL_MIN= 1
constant integer CULTIVATION_LEVEL_MAX= 7
        // 历练等级枚举
constant integer CULT_LEVEL_RUOJIANGHU= 1
constant integer CULT_LEVEL_CHUKUIJINGJING= 2
constant integer CULT_LEVEL_LOUYIXIAOCHENG= 3
constant integer CULT_LEVEL_RONGHUITONGGUAN= 4
constant integer CULT_LEVEL_LUHUOCHUNQING= 5
constant integer CULT_LEVEL_CHUSHENRUAHUA= 6
constant integer CULT_LEVEL_YIDAIZONGSHI= 7

        // ========================================================================
        // 历练等级阈值表
        // 每个等级需要的累计历练值（1-7级）
        // ========================================================================
integer array udg_cultivation_threshold
        // ========================================================================
        // 历练等级名称表
        // ========================================================================
string array udg_cultivation_name
        // ========================================================================
        // 历练伤害加成表
        // 每个等级对应的伤害加成百分比（存储为整数，如15表示15%）
        // ========================================================================
integer array udg_cultivation_bonus
        // ========================================================================
        // 玩家历练数据表
        // udg_cultivation_exp: 玩家当前历练值
        // udg_cultivation_level: 玩家当前等级（1-7）
        // ========================================================================
integer array udg_cultivation_exp
integer array udg_cultivation_level
        // ========================================================================
        // 解锁内容标记表
        // 用于记录玩家是否已解锁特定内容，避免重复提示
        // ========================================================================
boolean array udg_unlock_mid_dungeon
boolean array udg_unlock_graduation_skill
boolean array udg_unlock_high_dungeon
boolean array udg_unlock_elite_dungeon
boolean array udg_unlock_ultimate_dungeon
boolean array udg_unlock_b_encounter
boolean array udg_unlock_a_encounter

//endglobals from CultivationData
//globals from DungeonData:
constant boolean LIBRARY_DungeonData=true
        // ========================================================================
        // 副本ID常量定义
        // ========================================================================
constant integer DUNGEON_D001= 1
constant integer DUNGEON_D002= 2
constant integer DUNGEON_D003= 3
constant integer DUNGEON_D004= 4
constant integer DUNGEON_D005= 5
constant integer DUNGEON_D006= 6
constant integer DUNGEON_D007= 7
constant integer DUNGEON_D008= 8
constant integer DUNGEON_D009= 9
constant integer DUNGEON_D010= 10
constant integer DUNGEON_D011= 11
constant integer DUNGEON_D012= 12
constant integer DUNGEON_D013= 13
constant integer DUNGEON_D014= 14

        // ========================================================================
        // 副本进入物品ID (从I100开始，后续使用I10A, I10B等)
        // ========================================================================
constant integer ITEM_ID_D001= 'I100'
constant integer ITEM_ID_D002= 'I101'
constant integer ITEM_ID_D003= 'I102'
constant integer ITEM_ID_D004= 'I103'
constant integer ITEM_ID_D005= 'I104'
constant integer ITEM_ID_D006= 'I105'
constant integer ITEM_ID_D007= 'I106'
constant integer ITEM_ID_D008= 'I107'
constant integer ITEM_ID_D009= 'I108'
constant integer ITEM_ID_D010= 'I109'
constant integer ITEM_ID_D011= 'I10A'
constant integer ITEM_ID_D012= 'I10B'
constant integer ITEM_ID_D013= 'I10C'
constant integer ITEM_ID_D014= 'I10D'
        // ========================================================================
        // 神话碎片物品ID
        // ========================================================================
constant integer ITEM_ID_MYTH_FRAGMENT= 'I110'
        // ========================================================================
        // 副本类型常量定义
        // ========================================================================
constant integer DUNGEON_TYPE_SINGLE= 1
constant integer DUNGEON_TYPE_PARTY= 2
constant integer DUNGEON_TYPE_SECT= 3

        // ========================================================================
        // 副本品质常量定义
        // ========================================================================
constant integer DUNGEON_QUALITY_NORMAL= 1
constant integer DUNGEON_QUALITY_HARD= 2
constant integer DUNGEON_QUALITY_ELITE= 3
constant integer DUNGEON_QUALITY_MYTH= 4

        // ========================================================================
        // BOSS类型常量定义
        // 注意：这些常量应与怪物数据文件中的定义保持一致
        // ========================================================================
constant integer BOSS_TYPE_STRENGTH= 1
constant integer BOSS_TYPE_DEFENSE= 2
constant integer BOSS_TYPE_AGILITY= 3
constant integer BOSS_TYPE_CASTER= 4
constant integer BOSS_TYPE_SUMMONER= 5

        // ========================================================================
        // 副本状态常量定义
        // ========================================================================
constant integer DUNGEON_STATE_IDLE= 0
constant integer DUNGEON_STATE_ACTIVE= 1
constant integer DUNGEON_STATE_COMPLETE= 2
constant integer DUNGEON_STATE_FAILED= 3

        // ========================================================================
        // 掉落品质常量定义
        // ========================================================================
constant integer DROP_QUALITY_COMMON= 1
constant integer DROP_QUALITY_RARE= 2
constant integer DROP_QUALITY_EPIC= 3
constant integer DROP_QUALITY_LEGEND= 4
constant integer DROP_QUALITY_MYTH= 5

        // ========================================================================
        // 神话碎片相关常量
        // ========================================================================
constant integer FRAGMENT_DROP_MIN= 1
constant integer FRAGMENT_DROP_MAX= 3
constant integer FRAGMENT_EXCLUSIVE_WEAPON= 100
constant integer FRAGMENT_EXCLUSIVE_ARMOR= 150
constant integer FRAGMENT_EXCLUSIVE_ACCESSORY= 200
constant integer FRAGMENT_RANDOM_EQUIP= 300
constant integer FRAGMENT_MATERIAL_PACK= 200
        // ========================================================================
        // 历练等级相关常量
        // ========================================================================
constant integer UNLOCK_COUNT_PER_LEVEL= 2
        // ========================================================================
        // 副本入口区域中心坐标（主世界）
        // ========================================================================
constant real DUNGEON_AREA_CENTER_X= - 4500.00
constant real DUNGEON_AREA_CENTER_Y= - 5000.00
        // ========================================================================
        // 副本基础数据表 - 使用snake_case命名
        // ========================================================================
string array dungeon_name
integer array dungeon_item_id
integer array dungeon_type
integer array dungeon_recommend_level_min
integer array dungeon_recommend_level_max
real array dungeon_entrance_x
real array dungeon_entrance_y
real array dungeon_exit_x
real array dungeon_exit_y
integer array dungeon_boss_unit_id
integer array dungeon_boss_type
integer array dungeon_quality
integer array dungeon_state
integer array dungeon_player_count
integer array dungeon_complete_count
boolean array dungeon_can_revive

        // ========================================================================
        // 武学书籍掉落配置
        // ========================================================================
integer array dungeon_martial_book_id

//endglobals from DungeonData
//globals from DzAPI:
constant boolean LIBRARY_DzAPI=true
//endglobals from DzAPI
//globals from EquipmentData:
constant boolean LIBRARY_EquipmentData=true
        // ========================================================================
        // 装备槽位常量定义
        // ========================================================================
constant integer EQUIP_SLOT_WEAPON= 1
constant integer EQUIP_SLOT_ARMOR= 2
constant integer EQUIP_SLOT_HELMET= 3
constant integer EQUIP_SLOT_LEG= 4
constant integer EQUIP_SLOT_ACCESSORY= 5
constant integer EQUIP_SLOT_NECKLACE= 6

        // ========================================================================
        // 装备品质常量定义
        // ========================================================================
constant integer EQUIP_QUALITY_COMMON= 1
constant integer EQUIP_QUALITY_RARE= 2
constant integer EQUIP_QUALITY_EPIC= 3
constant integer EQUIP_QUALITY_LEGENDARY= 4
constant integer EQUIP_QUALITY_MYTHIC= 5

        // ========================================================================
        // 元素类型常量定义
        // ========================================================================
constant integer ELEMENT_NONE= 0
constant integer ELEMENT_FIRE= 1
constant integer ELEMENT_ICE= 2
constant integer ELEMENT_THUNDER= 3
constant integer ELEMENT_POISON= 4

        // ========================================================================
        // 元素前缀配置
        // ========================================================================
string array ELEMENT_PREFIX
string array ELEMENT_NAME
        // ========================================================================
        // 装备槽位名称
        // ========================================================================
string array EQUIP_SLOT_NAME
        // ========================================================================
        // 装备品质名称
        // ========================================================================
string array EQUIP_QUALITY_NAME
        // ========================================================================
        // 装备数据表 - 使用二维数组模拟 [装备ID]
        // ========================================================================
        // 装备基础属性
integer array udg_equip_id
integer array udg_equip_item_type_id
string array udg_equip_name
integer array udg_equip_slot
integer array udg_equip_quality
integer array udg_equip_icon

        // 装备主属性
integer array udg_equip_attack
integer array udg_equip_spell_power
integer array udg_equip_health
integer array udg_equip_armor
integer array udg_equip_resistance
integer array udg_equip_move_speed

        // 装备副属性
integer array udg_equip_crit_rate
integer array udg_equip_crit_damage
integer array udg_equip_cooldown
integer array udg_equip_range
integer array udg_equip_cost
integer array udg_equip_haste

        // 元素属性
integer array udg_equip_element
integer array udg_equip_element_value

        // 特殊效果
integer array udg_equip_special_type
integer array udg_equip_special_value

        // ========================================================================
        // 装备掉落来源表
        // ========================================================================
integer array udg_equip_drop_dungeon
integer array udg_equip_drop_chance

        // ========================================================================
        // 打造消耗表
        // ========================================================================
integer array udg_equip_craft_material_type
integer array udg_equip_craft_amount

        // ========================================================================
        // 套装关联表
        // ========================================================================
integer array udg_equip_set_id

        // ========================================================================
        // 装备数量计数
        // ========================================================================
integer udg_equip_count= 0
        // ========================================================================
        // 套装数据表
        // ========================================================================
integer array udg_set_id
string array udg_set_name
integer array udg_set_quality
integer array udg_set_bonus_2
integer array udg_set_bonus_4
integer array udg_set_bonus_6
integer array udg_set_count
        // ========================================================================
        // 装备查询缓存
        // ========================================================================
integer array udg_equip_cache_item_type
integer array udg_equip_cache_equip_id
integer udg_equip_cache_size= 0

//endglobals from EquipmentData
//globals from GameTimeSystem:
constant boolean LIBRARY_GameTimeSystem=true
    // 游戏时间（秒）
real udg_game_time= 0
    // 游戏主计时器
timer udg_game_timer= null
//endglobals from GameTimeSystem
//globals from LBKKAPI:
constant boolean LIBRARY_LBKKAPI=true
string MOVE_TYPE_NONE= "none"
string MOVE_TYPE_FOOT= "foot"
string MOVE_TYPE_HORSE= "horse"
string MOVE_TYPE_FLY= "fly"
string MOVE_TYPE_HOVER= "hover"
string MOVE_TYPE_FLOAT= "float"
string MOVE_TYPE_AMPH= "amph"
string MOVE_TYPE_UNBUILD= "unbuild"
constant integer DEFENSE_TYPE_SMALL= 0
constant integer DEFENSE_TYPE_MEDIUM= 1
constant integer DEFENSE_TYPE_LARGE= 2
constant integer DEFENSE_TYPE_FORT= 3
constant integer DEFENSE_TYPE_NORMAL= 4
constant integer DEFENSE_TYPE_HERO= 5
constant integer DEFENSE_TYPE_DIVINE= 6
constant integer DEFENSE_TYPE_NONE= 7
integer array LBKKAPI___MonthDay
hashtable LBKKAPI___Hash=InitHashtable()
//endglobals from LBKKAPI
//globals from SectData:
constant boolean LIBRARY_SectData=true
        // ========================================================================
        // 门派类型常量定义
        // ========================================================================
constant integer SECT_TYPE_RIGHTEOUS= 1
constant integer SECT_TYPE_EVIL= 2
constant integer SECT_TYPE_BEGGAR= 3
constant integer SECT_TYPE_HIDDEN= 4
constant integer SECT_TYPE_BLADE= 5
constant integer SECT_TYPE_SWORD= 6

        // ========================================================================
        // 门派定位常量定义
        // ========================================================================
constant integer SECT_ROLE_BALANCED= 1
constant integer SECT_ROLE_CONTROL= 2
constant integer SECT_ROLE_SUPPORT= 3
constant integer SECT_ROLE_BURST= 4
constant integer SECT_ROLE_DOT= 5
constant integer SECT_ROLE_MOBILE= 6
constant integer SECT_ROLE_SUSTAIN= 7
constant integer SECT_ROLE_FORMATION= 8
constant integer SECT_ROLE_TECHNIQUE= 9
constant integer SECT_ROLE_COMBO= 10
constant integer SECT_ROLE_ICE= 11
constant integer SECT_ROLE_PHYSICAL= 12
constant integer SECT_ROLE_ARMOR_BREAK= 13
constant integer SECT_ROLE_SPELL= 14
constant integer SECT_ROLE_ELEMENTAL= 15

        // ========================================================================
        // 门派ID常量定义
        // ========================================================================
constant integer SECT_SHAOLIN= 1
constant integer SECT_WUDANG= 2
constant integer SECT_EMEI= 3
constant integer SECT_MINGJIAO= 4
constant integer SECT_XINGXIU= 5
constant integer SECT_XIAOYAO= 6
constant integer SECT_GAIBANG= 7
constant integer SECT_QUANZHEN= 8
constant integer SECT_HUASHAN= 9
constant integer SECT_DIANCANG= 10
constant integer SECT_KUNLUN= 11
constant integer SECT_JINDAOMEN= 12
constant integer SECT_TIEJIANMEN= 13
constant integer SECT_SHUSHAN= 14
constant integer SECT_KONGTONG= 15

        // ========================================================================
        // 技能槽位常量定义
        // ========================================================================
constant integer SKILL_SLOT_FIRST= 1
constant integer SKILL_SLOT_SECOND= 2
constant integer SKILL_SLOT_THIRD= 3
constant integer SKILL_SLOT_GRADUATION_A= 4
constant integer SKILL_SLOT_GRADUATION_B= 5

        // ========================================================================
        // 主城坐标常量
        // ========================================================================
constant real MAIN_CITY_X= 0.0
constant real MAIN_CITY_Y= 0.0
        // ========================================================================
        // 门派基础数据表 - 使用snake_case命名
        // ========================================================================
string array sect_name
integer array sect_type_id
integer array sect_role_id
real array sect_coefficient

        // ========================================================================
        // 门派技能数据表 - 使用二维数组模拟 [门派ID * 20 + 槽位]
        // ========================================================================
integer array sect_skill_id
string array sect_skill_name
integer array sect_skill_unlock_level

        // ========================================================================
        // 门派道具物品ID表 - 用于门派选择
        // 玩家购买并拾取门派道具后触发加入门派
        // ========================================================================
integer array sect_join_item_id
        // ========================================================================
        // 玩家门派选择状态表
        // 0 = 未选择门派, >0 = 已选择的门派ID
        // ========================================================================
integer array udg_player_sect_selected
//endglobals from SectData
//globals from SkillLibary:
constant boolean LIBRARY_SkillLibary=true
        
constant integer SKILL_TYPE_ACTIVE= 1
        
constant integer SKILL_TYPE_PASSIVE= 2
        
constant integer SKILL_TARGET_TYPE_NONE= 0
        
constant integer SKILL_TARGET_TYPE_UNIT= 1
        
constant integer SKILL_TARGET_TYPE_POINT= 2
        
constant integer SKILL_TARGET_TYPE_UNIT_OR_POINT= 3
        
constant integer SKILL_ATTRIBUTE_TYPE_STR= 1
        
constant integer SKILL_ATTRIBUTE_TYPE_AGI= 2
        
constant integer SKILL_ATTRIBUTE_TYPE_INT= 3
        
constant integer SKILL_ATTRIBUTE_TYPE_ALL= 4
        
constant integer SKILL_ELEMENT_TYPE_FIRE= 1
        
constant integer SKILL_ELEMENT_TYPE_ICE= 2
        
constant integer SKILL_ELEMENT_TYPE_LIGHTNING= 3
        
constant integer SKILL_ELEMENT_TYPE_POISON= 4
        
constant integer SKILL_ELEMENT_TYPE_ALL= 5
        
constant integer SKILL_DAMAGE_TYPE_PHYSICAL= 1
        
constant integer SKILL_DAMAGE_TYPE_MAGICAL= 2
integer array udg_skills
integer udg_skill_count= 0
hashtable udg_skill_table= InitHashtable()
//endglobals from SkillLibary
//globals from TestEquipmentGenerate:
constant boolean LIBRARY_TestEquipmentGenerate=true
trigger gg_trg_TestEquipGenerate
//endglobals from TestEquipmentGenerate
//globals from YDWEBase:
constant boolean LIBRARY_YDWEBase=true
//ȫ�ֹ�ϣ�� 
hashtable YDHT= null
string bj_AllString=".................................!.#$%&'()*+,-./0123456789:;<=>.@ABCDEFGHIJKLMNOPQRSTUVWXYZ[.]^_`abcdefghijklmnopqrstuvwxyz{|}~................................................................................................................................"
//全局系统变量
unit bj_lastAbilityCastingUnit=null
unit bj_lastAbilityTargetUnit=null
unit bj_lastPoolAbstractedUnit=null
unitpool bj_lastCreatedUnitPool=null
item bj_lastPoolAbstractedItem=null
itempool bj_lastCreatedItemPool=null
attacktype bj_lastSetAttackType= ATTACK_TYPE_NORMAL
damagetype bj_lastSetDamageType= DAMAGE_TYPE_NORMAL
weapontype bj_lastSetWeaponType= WEAPON_TYPE_WHOKNOWS
real yd_MapMaxX= 0
real yd_MapMinX= 0
real yd_MapMaxY= 0
real yd_MapMinY= 0
string array YDWEBase___yd_PlayerColor
trigger array YDWEBase___AbilityCastingOverEventQueue
integer array YDWEBase___AbilityCastingOverEventType
integer YDWEBase___AbilityCastingOverEventNumber= 0
//endglobals from YDWEBase
//globals from YDWEWakePlayerUnitsNull:
constant boolean LIBRARY_YDWEWakePlayerUnitsNull=true
//endglobals from YDWEWakePlayerUnitsNull
//globals from AttackMonsterSystem:
constant boolean LIBRARY_AttackMonsterSystem=true
    // 当前波次信息
integer udg_current_wave= 0
integer udg_monsters_remaining= 0
integer udg_total_monsters_spawned= 0
    // 怪物数组追踪生成单位
unit array udg_spawned_monsters
integer udg_spawned_monster_count= 0
    // 控制波次生成的计时器
timer udg_wave_spawn_timer= CreateTimer()
timerdialog udg_wave_spawn_timer_dialog= CreateTimerDialog(udg_wave_spawn_timer)
timer udg_next_wave_timer= CreateTimer()
timerdialog udg_next_wave_timer_dialog= CreateTimerDialog(udg_next_wave_timer)
    // 波次完成回调
    // 由主防守系统设置
    // 防守系统是否激活
boolean udg_defense_system_active= false
    // 用于延迟生成怪物的临时变量
integer udg_temp_monster_type= 0
integer udg_temp_wave_number= 0
    // 魔教玩家ID (8号玩家，从0开始计数)
constant integer PLAYER_EVIL= 7
constant integer FIRST_WAVE_DELAY= 5
constant integer EVERY_WAVE_DELAY= 150
//endglobals from AttackMonsterSystem
//globals from CommonFunction:
constant boolean LIBRARY_CommonFunction=true
//endglobals from CommonFunction
//globals from DungeonMonsterData:
constant boolean LIBRARY_DungeonMonsterData=true
    // ========================================================================
    // 小怪角色类型常量定义
    // ========================================================================
constant integer ROLE_TYPE_MELEE_DPS= 1
constant integer ROLE_TYPE_RANGER= 2
constant integer ROLE_TYPE_TANK= 3
constant integer ROLE_TYPE_CASTER_CONTROL= 4
constant integer ROLE_TYPE_HEALER_SUPPORT= 5
constant integer ROLE_TYPE_SUMMONER= 6

    // ========================================================================
    // 副本主题类型常量定义
    // ========================================================================
constant integer THEME_TYPE_HEIFENG= 1
constant integer THEME_TYPE_BANDIT= 2
constant integer THEME_TYPE_SHAOLIN= 3
constant integer THEME_TYPE_MING= 4
constant integer THEME_TYPE_DARK= 5
constant integer THEME_TYPE_BAMBOO= 6
constant integer THEME_TYPE_XIAOYAO= 7
constant integer THEME_TYPE_PLUM= 8
constant integer THEME_TYPE_KONGTONG= 9
constant integer THEME_TYPE_WATER_MOON= 10
constant integer THEME_TYPE_SWORD= 11
constant integer THEME_TYPE_MARSH= 12
constant integer THEME_TYPE_SACRED= 13
constant integer THEME_TYPE_FINAL= 14

    // ========================================================================
    // 技能类型常量定义
    // ========================================================================
constant integer SKILL_TYPE_ATTACK= 1
constant integer SKILL_TYPE_DEFENSE= 2
constant integer SKILL_TYPE_HEAL= 3
constant integer SKILL_TYPE_SUMMON= 4
constant integer SKILL_TYPE_CONTROL= 5
constant integer SKILL_TYPE_BUFF= 6
constant integer SKILL_TYPE_DEBUFF= 7
constant integer SKILL_TYPE_AOE= 8

    // ========================================================================
    // 技能ID范围常量定义
    // ========================================================================
constant integer SKILL_ID_MIN= 91001
constant integer SKILL_ID_MAX= 91014

    // ========================================================================
    // 小怪配置数组
    // 使用公式: role_type * 100 + theme_type 作为索引
    // ========================================================================
integer array udg_monster_unit_id
integer array udg_monster_base_hp
integer array udg_monster_base_attack
integer array udg_monster_base_defense
integer array udg_monster_move_speed
integer array udg_monster_attack_range
integer array udg_monster_skill_id
integer array udg_monster_skill_type

    // ========================================================================
    // BOSS配置数组
    // 使用公式: boss_type * 100 + theme_type 作为索引
    // ========================================================================
integer array udg_boss_unit_id
integer array udg_boss_base_hp
integer array udg_boss_base_attack
integer array udg_boss_base_defense
integer array udg_boss_move_speed
integer array udg_boss_attack_range
integer array udg_boss_attribute_bonus

    // ========================================================================
    // 标记变量
    // ========================================================================
boolean udg_monster_data_initialized= false

//endglobals from DungeonMonsterData
//globals from GeneralBonusSystem:
constant boolean LIBRARY_GeneralBonusSystem=true
integer array GeneralBonusSystem___ABILITY_COUNT
integer array GeneralBonusSystem___ABILITY_NUM
integer array GeneralBonusSystem___BonusAbilitys
integer array GeneralBonusSystem___PowersOf2
integer GeneralBonusSystem___PRELOAD_DUMMY_UNIT= 'hpea'
integer array GeneralBonusSystem___YDWEBONUS_MyChar
boolean GeneralBonusSystem___PRELOAD_ABILITYS= true
constant integer GeneralBonusSystem___BONUS_TYPES= 4
integer array GeneralBonusSystem___MaxBonus
integer array GeneralBonusSystem___MinBonus
unit array GeneralBonusSystem___Units
integer GeneralBonusSystem___UnitCount= 0
//endglobals from GeneralBonusSystem
//globals from SectSystem:
constant boolean LIBRARY_SectSystem=true
        // ========================================================================
        // 系统初始化标记 - 全局变量加udg_前缀
        // ========================================================================
boolean udg_sect_system_initialized
        // ========================================================================
        // 玩家门派任务完成状态
        // true = 已完成门派入门任务, false = 未完成
        // ========================================================================
boolean array udg_player_sect_completed
        // ========================================================================
        // 玩家拾取物品触发器
        // 用于监听玩家拾取门派道具
        // ========================================================================
trigger array pick_item_trigger
        // ========================================================================
        // 玩家升级事件触发器
        // 用于监听玩家升级并解锁门派技能
        // ========================================================================
trigger array level_up_trigger
        // ========================================================================
        // 玩家已解锁技能状态表
        // [玩家ID][技能槽位] = true/false
        // 用于记录哪些技能已经解锁，避免重复解锁
        // ========================================================================
boolean array udg_skill_unlocked
//endglobals from SectSystem
//globals from YDWEEnableCreepSleepBJNull:
constant boolean LIBRARY_YDWEEnableCreepSleepBJNull=true
//endglobals from YDWEEnableCreepSleepBJNull
//globals from BossSkillSystem:
constant boolean LIBRARY_BossSkillSystem=true
    // ========================================================================
    // 常量定义
    // ========================================================================
constant integer BOSS_SKILL_SLOT_COUNT= 4
constant integer BOSS_PHASE_1= 1
constant integer BOSS_PHASE_2= 2
constant real BOSS_AI_UPDATE_INTERVAL= 2.0

    // ========================================================================
    // 索引计算常量
    // ========================================================================
constant integer INDEX_MULTIPLIER= 100

    // ========================================================================
    // 技能冷却时间数组 [boss_type][技能槽]
    // ========================================================================
real array udg_boss_skill_cooldown
    // ========================================================================
    // 技能最后使用时间数组 [boss_unit_handle_id][技能槽]
    // ========================================================================
real array udg_boss_skill_last_used
    // ========================================================================
    // BOSS阶段追踪数组 [boss_unit_handle_id]
    // ========================================================================
integer array udg_boss_phase
    // ========================================================================
    // BOSS生命值百分比数组 [boss_unit_handle_id]
    // ========================================================================
real array udg_boss_hp_percent
    // ========================================================================
    // BOSS AI计时器数组 [boss_unit_handle_id]
    // ========================================================================
timer array udg_boss_ai_timer
    // ========================================================================
    // BOSS单位引用数组 [boss_unit_handle_id]
    // ========================================================================
unit array udg_boss_unit_ref
    // ========================================================================
    // BOSS类型数组 [boss_unit_handle_id]
    // ========================================================================
integer array udg_boss_type
    // ========================================================================
    // BOSS副本ID数组 [boss_unit_handle_id]
    // ========================================================================
integer array udg_boss_dungeon_id
    // ========================================================================
    // 技能槽是否可用数组 [boss_unit_handle_id][技能槽]
    // ========================================================================
boolean array udg_boss_skill_available
    // ========================================================================
    // 技能ID数组 [boss_unit_handle_id][技能槽]
    // ========================================================================
integer array udg_boss_skill_id
    // ========================================================================
    // 技能类型数组 [boss_unit_handle_id][技能槽]
    // ========================================================================
integer array udg_boss_skill_type
    // ========================================================================
    // 标记
    // ========================================================================
boolean array udg_boss_skill_system_initialized
//endglobals from BossSkillSystem
//globals from CultivationSystem:
constant boolean LIBRARY_CultivationSystem=true
        // ========================================================================
        // 系统初始化标记
        // ========================================================================
boolean array udg_cultivation_initialized
        // ========================================================================
        // 升级事件触发器数组
        // 每个玩家一个，用于监听升级事件
        // ========================================================================
trigger array udg_cultivation_levelup_trigger
//endglobals from CultivationSystem
//globals from HeroAttributeSystem:
constant boolean LIBRARY_HeroAttributeSystem=true
        // ==========================================
        // 常量定义 - 25个局内属性枚举
        // ==========================================
        // 核心属性（6个）
constant integer ATTR_HEALTH= 1
constant integer ATTR_MANA= 2
constant integer ATTR_CONSTITUTION= 3
constant integer ATTR_INTELLIGENCE= 4
constant integer ATTR_AGILITY= 5
constant integer ATTR_TECHNIQUE= 6

        // 战斗属性（10个）
constant integer ATTR_ATTACK= 7
constant integer ATTR_SPELL_POWER= 8
constant integer ATTR_CRIT_RATE= 9
constant integer ATTR_CRIT_DAMAGE= 10
constant integer ATTR_FIRE_POWER= 11
constant integer ATTR_ICE_POWER= 12
constant integer ATTR_THUNDER_POWER= 13
constant integer ATTR_POISON_POWER= 14
constant integer ATTR_ARMOR= 15
constant integer ATTR_RESISTANCE= 16

        // 技能属性（4个）
constant integer ATTR_COOLDOWN= 17
constant integer ATTR_RANGE= 18
constant integer ATTR_COST= 19
constant integer ATTR_HASTE= 20

        // 特殊属性（3个）
constant integer ATTR_BERSERK= 21
constant integer ATTR_NIRVANA= 22
constant integer ATTR_PENETRATION= 23

        // 扩展属性（2个，v1.1）
constant integer ATTR_DODGE= 24
constant integer ATTR_LIFESTEAL= 25

        // 区分最大属性和当前属性
constant integer ATTR_MAX_HEALTH= 26
constant integer ATTR_MAX_MANA= 27

        // ========================================================================
        // 扩展属性常量定义（用于特殊效果）
        // ========================================================================
        // 注意：这些常量在HeroAttributeSystem中可能不存在，但在这里定义以便使用
constant integer ATTR_DAMAGE_REDUCTION= 28
constant integer ATTR_HEAL_BONUS= 29
constant integer ATTR_DODGE_BONUS= 30
constant integer ATTR_ALL_ATTR_BONUS= 31
constant integer ATTR_ATTACK_BONUS= 32
constant integer ATTR_SPELL_POWER_BONUS= 33
constant integer ATTR_MOVE_SPEED_BONUS= 34
constant integer ATTR_MANA_REGEN_BONUS= 35
constant integer ATTR_RANGE_BONUS= 36
constant integer ATTR_COOLDOWN_BONUS= 37
constant integer ATTR_SLOW_IMMUNE= 38
constant integer ATTR_REBIRTH= 39

        // ==========================================
        // 常量定义 - 10位英雄ID
        // ==========================================
constant integer HERO_RUODIE= 1
constant integer HERO_XIAOXIA= 2
constant integer HERO_ZHANHEN= 3
constant integer HERO_JINXUAN= 4
constant integer HERO_KONGYAO= 5
constant integer HERO_JIANDAO= 6
constant integer HERO_SHENXING= 7
constant integer HERO_CANGLANG= 8
constant integer HERO_HONGLING= 9
constant integer HERO_YUEHUA= 10

        // ==========================================
        // 常量定义 - 属性上限
        // ==========================================
constant real MAX_CRIT_RATE= 100.0
constant real MAX_CRIT_DAMAGE= 300.0
constant real MAX_COOLDOWN_REDUCTION= 40.0
constant real MAX_DODGE_RATE= 80.0
constant real MAX_LIFESTEAL= 50.0

        // 以下常量用于YDWE万能属性系统
constant integer MODE_ADD= 0
constant integer MODE_SUB= 1
constant integer MODE_SET= 2

constant integer BONUS_TYPE_MAX_LIFE= 0
constant integer BONUS_TYPE_MAX_MANA= 1
constant integer BONUS_TYPE_ARMOR= 2
constant integer BONUS_TYPE_ATTACK= 3
constant integer BONUS_TYPE_ATTACK_SPEED= 4

        // ==========================================
        // 全局变量
        // ==========================================
        // 主哈希表 - 存储所有英雄属性
hashtable udg_hero_attribute_ht
        // 玩家英雄映射
unit array udg_player_hero
integer array udg_player_hero_id

        // 标记
boolean array HeroSystemInitialized
//endglobals from HeroAttributeSystem
//globals from DungeonSystem:
constant boolean LIBRARY_DungeonSystem=true
        // ========================================================================
        // 玩家状态数据
        // ========================================================================
integer array udg_player_current_dungeon
integer array udg_player_dungeon_completed_today
real udg_fragment_drop_rate

        // ========================================================================
        // 副本状态数据
        // ========================================================================
boolean array udg_dungeon_boss_alive
//endglobals from DungeonSystem
//globals from EnemySkill:
constant boolean LIBRARY_EnemySkill=true
integer udg_enemy_skill_count= 0
integer array udg_enemy_skills
group udg_temp_group= CreateGroup()
        // 敌人技能ID常量
constant integer ENEMY_SKILL_NORMAL_ATTACK= 91001
constant integer ENEMY_SKILL_HEAVY_STRIKE= 91002
constant integer ENEMY_SKILL_COMBO_STRIKE= 91003
constant integer ENEMY_SKILL_RANGE_SHOT= 91004
constant integer ENEMY_SKILL_PRECISION_SHOT= 91005
constant integer ENEMY_SKILL_DEFENSIVE_STANCE= 91006
constant integer ENEMY_SKILL_TAUNT= 91007
constant integer ENEMY_SKILL_FIREBALL= 91008
constant integer ENEMY_SKILL_FREEZE= 91009
constant integer ENEMY_SKILL_HEAL= 91010
constant integer ENEMY_SKILL_SUMMON_MINIONS= 91011
constant integer ENEMY_SKILL_BERSERK= 91012
constant integer ENEMY_SKILL_WEAKEN_CURSE= 91013
constant integer ENEMY_SKILL_FLAME_STORM= 91014
//endglobals from EnemySkill
//globals from EquipmentSystem:
constant boolean LIBRARY_EquipmentSystem=true
        // ========================================================================
        // 玩家装备状态存储
        // ========================================================================
        // 玩家当前装备状态（按槽位存储装备ID）
        // JASS不支持二维数组，使用一维数组模拟：player_id * 6 + slot_index
integer array udg_player_equipped_item_id

        // 玩家当前装备属性总加成（缓存）
real array udg_player_equip_attack_bonus
real array udg_player_equip_spell_power_bonus
real array udg_player_equip_health_bonus
real array udg_player_equip_armor_bonus
real array udg_player_equip_resistance_bonus
real array udg_player_equip_move_speed_bonus
real array udg_player_equip_crit_rate_bonus
real array udg_player_equip_crit_damage_bonus
real array udg_player_equip_cooldown_bonus
real array udg_player_equip_range_bonus
real array udg_player_equip_cost_bonus
real array udg_player_equip_haste_bonus

        // 特殊效果加成
real array udg_player_equip_damage_reduction_bonus
real array udg_player_equip_heal_bonus
real array udg_player_equip_attack_bonus_percent
real array udg_player_equip_move_speed_bonus_percent
real array udg_player_equip_dodge_bonus
real array udg_player_equip_all_attr_bonus

        // 元素属性加成
real array udg_player_equip_fire_power_bonus
real array udg_player_equip_ice_power_bonus
real array udg_player_equip_thunder_power_bonus
real array udg_player_equip_poison_power_bonus

        // 属性缓存机制
boolean array udg_player_equip_cache_valid
real array udg_player_equip_cache_time

        // 系统状态
boolean array udg_equipment_system_initialized
boolean udg_equipment_system_enabled= true
//endglobals from EquipmentSystem
//globals from HeroSelectionSystem:
constant boolean LIBRARY_HeroSelectionSystem=true
    // 常量配置
constant real HERO_DOUBLE_CLICK_TIME= 1.5
constant real HERO_SPAWN_X= 5800
constant real HERO_SPAWN_Y= - 3000

    // 玩家选择状态记录
unit array g_last_select_unit
real array g_last_select_time
boolean array g_hero_selected

//endglobals from HeroSelectionSystem
//globals from DungeonMonsterSystem:
constant boolean LIBRARY_DungeonMonsterSystem=true
    // ========================================================================
    // 波次生成控制数组
    // ========================================================================
integer array udg_current_wave_number
integer array udg_monsters_per_wave

    // ========================================================================
    // 生成位置相关数组
    // ========================================================================
real array udg_spawn_center_x
real array udg_spawn_center_y
real array udg_spawn_radius

    // ========================================================================
    // 小怪实例追踪数组
    // ========================================================================
unit array udg_active_monsters
integer array udg_active_monster_count
integer array udg_max_active_monsters

    // ========================================================================
    // 难度系数常量
    // ========================================================================
constant real DIFFICULTY_COEFFICIENT_NORMAL= 1.0
constant real DIFFICULTY_COEFFICIENT_HARD= 1.3
constant real DIFFICULTY_COEFFICIENT_ELITE= 1.6
constant real DIFFICULTY_COEFFICIENT_MYTH= 2.0

    // ========================================================================
    // 波次配置常量
    // ========================================================================
constant integer MAX_WAVES= 5
constant integer MIN_MONSTERS_PER_WAVE= 3
constant integer MAX_MONSTERS_PER_WAVE= 8
constant real WAVE_SPAWN_INTERVAL= 30.0
constant integer MAX_ACTIVE_MONSTERS= 25

    // ========================================================================
    // 生成位置常量
    // ========================================================================
constant real DEFAULT_SPAWN_RADIUS= 300.0
constant real MIN_SPAWN_RADIUS= 200.0
constant real MAX_SPAWN_RADIUS= 400.0
constant real SPAWN_OFFSET_X= 400.0
constant real SPAWN_OFFSET_Y= 0.0

    // ========================================================================
    // 数组索引常量
    // ========================================================================
constant integer MONSTER_ARRAY_MULTIPLIER= 100

    // ========================================================================
    // 角色类型权重常量
    // ========================================================================
constant integer WEIGHT_MELEE_DPS= 60
constant integer WEIGHT_RANGER= 30
constant integer WEIGHT_TANK= 10
constant integer WEIGHT_HEALER_SUPPORT= 50
constant integer WEIGHT_CASTER= 40
constant integer WEIGHT_ASSASSIN= 20

    // ========================================================================
    // 波次怪物数量常量
    // ========================================================================
constant integer MONSTERS_NORMAL= 4
constant integer MONSTERS_HARD= 5
constant integer MONSTERS_ELITE= 6
constant integer MONSTERS_MYTH= 7

    // ========================================================================
    // 标记变量
    // ========================================================================
boolean udg_monster_system_initialized= false
real udg_temp_spawn_x= 0.0
real udg_temp_spawn_y= 0.0
//endglobals from DungeonMonsterSystem
//globals from EquipmentTriggers:
constant boolean LIBRARY_EquipmentTriggers=true
        // 装备拾取触发器
trigger gg_trg_EquipmentPickup= null
        // 装备扔下触发器
trigger gg_trg_EquipmentDrop= null
        // 装备测试触发器
trigger gg_trg_EquipmentTest= null
//endglobals from EquipmentTriggers
//globals from TestEquipmentDebug:
constant boolean LIBRARY_TestEquipmentDebug=true
trigger gg_trg_TestEquipDebug
//endglobals from TestEquipmentDebug
//globals from MonsterAISystem:
constant boolean LIBRARY_MonsterAISystem=true
        // AI更新计时器
timer array udg_monster_ai_timers
timer array udg_boss_ai_timers
        // 怪物目标追踪 [monster_unit_handle_id]
unit array udg_monster_targets
real array udg_monster_last_attack_time
        // 怪物角色类型映射 [monster_unit_handle_id]
integer array udg_monster_role_type
        // 怪物主题类型映射 [monster_unit_handle_id]
integer array udg_monster_theme_type
        // 活动怪物数量
integer udg_all_active_monster_count= 0
        // 标记变量
boolean udg_monster_ai_system_initialized= false
//endglobals from MonsterAISystem
//globals from GameInit:
constant boolean LIBRARY_GameInit=true
        // 游戏版本
constant integer GAME_VERSION_MAJOR= 1
constant integer GAME_VERSION_MINOR= 0
constant integer GAME_VERSION_PATCH= 0
        // 游戏状态
        // 状态: 0=未开始, 1=进行中, 2=暂停, 3=结束
integer array udg_game_status
        // 当前难度
integer array udg_current_difficulty
        // 游戏开始时间
real array udg_game_start_time
        // 玩家数据
        // 玩家门派
integer array udg_player_sect
        // 玩家历练
integer array udg_player_cultivation
        // 标记
boolean array udg_game_initialized
        // 测试模式
boolean TEST_MODE= true
//endglobals from GameInit
    // Generated
trigger gg_trg_firstOccur= null
trigger gg_trg_fisrtOccur_2= null
trigger gg_trg_init= null
trigger gg_trg_firstSecond= null
unit gg_unit_O000_0001= null
unit gg_unit_O007_0002= null
unit gg_unit_O008_0003= null
unit gg_unit_O005_0004= null
unit gg_unit_O003_0005= null
unit gg_unit_O004_0006= null
unit gg_unit_O006_0007= null
unit gg_unit_O001_0008= null
unit gg_unit_O009_0009= null
unit gg_unit_O002_0010= null

trigger l__library_init

//JASSHelper struct globals:
constant integer si__Skill=1
integer si__Skill_F=0
integer si__Skill_I=0
integer array si__Skill_V
integer array s__Skill_skill_id
string array s__Skill_skill_name
string array s__Skill_skill_desc
integer array s__Skill_skill_type
integer array s__Skill_skill_target_type
integer array s__Skill_skill_template_id
real array s__Skill_skill_cooldown
integer array s__Skill_skill_magic_cost
real array s__Skill_skill_cast_range
real array s__Skill_skill_damage_coefficient
integer array s__Skill_skill_attribute_type
integer array s__Skill_skill_element_type
integer array s__Skill_skill_damage_type
trigger st__Skill_onDestroy
integer f__arg_this

endglobals
    native DzGetMouseTerrainX takes nothing returns real
    native DzGetMouseTerrainY takes nothing returns real
    native DzGetMouseTerrainZ takes nothing returns real
    native DzIsMouseOverUI takes nothing returns boolean
    native DzGetMouseX takes nothing returns integer
    native DzGetMouseY takes nothing returns integer
    native DzGetMouseXRelative takes nothing returns integer
    native DzGetMouseYRelative takes nothing returns integer
    native DzSetMousePos takes integer x, integer y returns nothing
    native DzTriggerRegisterMouseEvent takes trigger trig, integer btn, integer status, boolean sync, string func returns nothing
    native DzTriggerRegisterMouseEventByCode takes trigger trig, integer btn, integer status, boolean sync, code funcHandle returns nothing
    native DzTriggerRegisterKeyEvent takes trigger trig, integer key, integer status, boolean sync, string func returns nothing
    native DzTriggerRegisterKeyEventByCode takes trigger trig, integer key, integer status, boolean sync, code funcHandle returns nothing
    native DzTriggerRegisterMouseWheelEvent takes trigger trig, boolean sync, string func returns nothing
    native DzTriggerRegisterMouseWheelEventByCode takes trigger trig, boolean sync, code funcHandle returns nothing
    native DzTriggerRegisterMouseMoveEvent takes trigger trig, boolean sync, string func returns nothing
    native DzTriggerRegisterMouseMoveEventByCode takes trigger trig, boolean sync, code funcHandle returns nothing
    native DzGetTriggerKey takes nothing returns integer
    native DzGetWheelDelta takes nothing returns integer
    native DzIsKeyDown takes integer iKey returns boolean
    native DzGetTriggerKeyPlayer takes nothing returns player
    native DzGetWindowWidth takes nothing returns integer
    native DzGetWindowHeight takes nothing returns integer
    native DzGetWindowX takes nothing returns integer
    native DzGetWindowY takes nothing returns integer
    native DzTriggerRegisterWindowResizeEvent takes trigger trig, boolean sync, string func returns nothing
    native DzTriggerRegisterWindowResizeEventByCode takes trigger trig, boolean sync, code funcHandle returns nothing
    native DzIsWindowActive takes nothing returns boolean
    native DzDestructablePosition takes destructable d, real x, real y returns nothing
    native DzSetUnitPosition takes unit whichUnit, real x, real y returns nothing
    native DzExecuteFunc takes string funcName returns nothing
    native DzGetUnitUnderMouse takes nothing returns unit
    native DzSetUnitTexture takes unit whichUnit, string path, integer texId returns nothing
    native DzSetMemory takes integer address, real value returns nothing
    native DzSetUnitID takes unit whichUnit, integer id returns nothing
    native DzSetUnitModel takes unit whichUnit, string path returns nothing
    native DzSetWar3MapMap takes string map returns nothing
    native DzGetLocale takes nothing returns string
    native DzGetUnitNeededXP takes unit whichUnit, integer level returns integer
    native DzTriggerRegisterSyncData takes trigger trig, string prefix, boolean server returns nothing
    native DzSyncData takes string prefix, string data returns nothing
    native DzGetTriggerSyncPrefix takes nothing returns string
    native DzGetTriggerSyncData takes nothing returns string
    native DzGetTriggerSyncPlayer takes nothing returns player
    native DzSyncBuffer takes string prefix, string data, integer dataLen returns nothing
    native DzSyncDataImmediately takes string prefix, string data returns nothing 
    native DzFrameHideInterface takes nothing returns nothing
    native DzFrameEditBlackBorders takes real upperHeight, real bottomHeight returns nothing
    native DzFrameGetPortrait takes nothing returns integer
    native DzFrameGetMinimap takes nothing returns integer
    native DzFrameGetCommandBarButton takes integer row, integer column returns integer
    native DzFrameGetHeroBarButton takes integer buttonId returns integer
    native DzFrameGetHeroHPBar takes integer buttonId returns integer
    native DzFrameGetHeroManaBar takes integer buttonId returns integer
    native DzFrameGetItemBarButton takes integer buttonId returns integer
    native DzFrameGetMinimapButton takes integer buttonId returns integer
    native DzFrameGetUpperButtonBarButton takes integer buttonId returns integer
    native DzFrameGetTooltip takes nothing returns integer
    native DzFrameGetChatMessage takes nothing returns integer
    native DzFrameGetUnitMessage takes nothing returns integer
    native DzFrameGetTopMessage takes nothing returns integer
    native DzGetColor takes integer r, integer g, integer b, integer a returns integer
    native DzFrameSetUpdateCallback takes string func returns nothing
    native DzFrameSetUpdateCallbackByCode takes code funcHandle returns nothing
    native DzFrameShow takes integer frame, boolean enable returns nothing
    native DzCreateFrame takes string frame, integer parent, integer id returns integer
    native DzCreateSimpleFrame takes string frame, integer parent, integer id returns integer
    native DzDestroyFrame takes integer frame returns nothing
    native DzLoadToc takes string fileName returns nothing
    native DzFrameSetPoint takes integer frame, integer point, integer relativeFrame, integer relativePoint, real x, real y returns nothing
    native DzFrameSetAbsolutePoint takes integer frame, integer point, real x, real y returns nothing
    native DzFrameClearAllPoints takes integer frame returns nothing
    native DzFrameSetEnable takes integer name, boolean enable returns nothing
    native DzFrameSetScript takes integer frame, integer eventId, string func, boolean sync returns nothing
    native DzFrameSetScriptByCode takes integer frame, integer eventId, code funcHandle, boolean sync returns nothing
    native DzFrameSetScriptBlock takes integer frame, integer eventId, code funcHandle, boolean sync returns nothing
    native DzFrameSetScriptAsync takes integer frame, integer eventId, string funcName returns nothing
    native DzFrameSetScriptByCodeAsync takes integer frame, integer eventId, code func returns nothing
    native DzFrameSetScriptBlockAsync takes integer frame, integer eventId, code func returns nothing
    native DzGetTriggerUIEventPlayer takes nothing returns player
    native DzGetTriggerUIEventFrame takes nothing returns integer
    native DzFrameFindByName takes string name, integer id returns integer
    native DzSimpleFrameFindByName takes string name, integer id returns integer
    native DzSimpleFontStringFindByName takes string name, integer id returns integer
    native DzSimpleTextureFindByName takes string name, integer id returns integer
    native DzGetGameUI takes nothing returns integer
    native DzClickFrame takes integer frame returns nothing
    native DzSetCustomFovFix takes real value returns nothing
    native DzEnableWideScreen takes boolean enable returns nothing
    native DzFrameSetText takes integer frame, string text returns nothing
    native DzFrameGetText takes integer frame returns string
    native DzFrameSetTextSizeLimit takes integer frame, integer size returns nothing
    native DzFrameGetTextSizeLimit takes integer frame returns integer
    native DzFrameSetTextColor takes integer frame, integer color returns nothing
    native DzGetMouseFocus takes nothing returns integer
    native DzFrameSetAllPoints takes integer frame, integer relativeFrame returns boolean
    native DzFrameSetFocus takes integer frame, boolean enable returns boolean
    native DzFrameSetModel takes integer frame, string modelFile, integer modelType, integer flag returns nothing
    native DzFrameGetEnable takes integer frame returns boolean
    native DzFrameSetAlpha takes integer frame, integer alpha returns nothing
    native DzFrameGetAlpha takes integer frame returns integer
    native DzFrameSetAnimate takes integer frame, integer animId, boolean autocast returns nothing
    native DzFrameSetAnimateOffset takes integer frame, real offset returns nothing
    native DzFrameSetTexture takes integer frame, string texture, integer flag returns nothing
    native DzFrameSetScale takes integer frame, real scale returns nothing
    native DzFrameSetTooltip takes integer frame, integer tooltip returns nothing
    native DzFrameCageMouse takes integer frame, boolean enable returns nothing
    native DzFrameGetValue takes integer frame returns real
    native DzFrameSetMinMaxValue takes integer frame, real minValue, real maxValue returns nothing
    native DzFrameSetStepValue takes integer frame, real step returns nothing
    native DzFrameSetValue takes integer frame, real value returns nothing
    native DzFrameSetSize takes integer frame, real w, real h returns nothing
    native DzCreateFrameByTagName takes string frameType, string name, integer parent, string template, integer id returns integer
    native DzFrameSetVertexColor takes integer frame, integer color returns nothing
    native DzOriginalUIAutoResetPoint takes boolean enable returns nothing
    native DzFrameSetPriority takes integer frame, integer priority returns nothing
    native DzFrameSetParent takes integer frame, integer parent returns nothing
    native DzFrameGetHeight takes integer frame returns real
    native DzFrameSetFont takes integer frame, string fileName, real height, integer flag returns nothing
    native DzFrameGetParent takes integer frame returns integer
    native DzFrameSetTextAlignment takes integer frame, integer align returns nothing
    native DzFrameGetName takes integer frame returns string
    native DzGetClientWidth takes nothing returns integer
    native DzGetClientHeight takes nothing returns integer
    native DzFrameIsVisible takes integer frame returns boolean
    native DzSimpleFrameShow takes integer frame, boolean enable returns nothing
    native DzFrameAddText takes integer frame, string text returns nothing
    native DzUnitSilence takes unit whichUnit, boolean disable returns nothing
    native DzUnitDisableAttack takes unit whichUnit, boolean disable returns nothing
    native DzUnitDisableInventory takes unit whichUnit, boolean disable returns nothing
    native DzUpdateMinimap takes nothing returns nothing
    native DzUnitChangeAlpha takes unit whichUnit, integer alpha, boolean forceUpdate returns nothing
    native DzUnitSetCanSelect takes unit whichUnit, boolean state returns nothing
    native DzUnitSetTargetable takes unit whichUnit, boolean state returns nothing
    native DzSaveMemoryCache takes string cache returns nothing
    native DzGetMemoryCache takes nothing returns string
    native DzSetSpeed takes real ratio returns nothing
    native DzConvertWorldPosition takes real x, real y, real z, code callback returns boolean
    native DzGetConvertWorldPositionX takes nothing returns real
    native DzGetConvertWorldPositionY takes nothing returns real
    native DzCreateCommandButton takes integer parent, string icon, string name, string desc returns integer
    native DzAPI_Map_HasMallItem takes player whichPlayer, string key returns boolean
    native DzAPI_Map_GetMapLevel takes player whichPlayer returns integer
    native RequestExtraIntegerData takes integer dataType, player whichPlayer, string param1, string param2, boolean param3, integer param4, integer param5, integer param6 returns integer
    native RequestExtraBooleanData takes integer dataType, player whichPlayer, string param1, string param2, boolean param3, integer param4, integer param5, integer param6 returns boolean
    native RequestExtraStringData takes integer dataType, player whichPlayer, string param1, string param2, boolean param3, integer param4, integer param5, integer param6 returns string
    native RequestExtraRealData takes integer dataType, player whichPlayer, string param1, string param2, boolean param3, integer param4, integer param5, integer param6 returns real
        native DzGetSelectedLeaderUnit takes nothing returns unit 
        native DzIsChatBoxOpen takes nothing returns boolean 
        native DzSetUnitPreselectUIVisible takes unit whichUnit, boolean visible returns nothing 
        native DzSetEffectAnimation takes effect whichEffect, integer index, integer flag returns nothing 
        native DzSetEffectPos takes effect whichEffect, real x, real y, real z returns nothing 
        native DzSetEffectVertexColor takes effect whichEffect, integer color returns nothing 
        native DzSetEffectVertexAlpha takes effect whichEffect, integer alpha returns nothing 
        native DzSetEffectModel takes effect whichEffect, string model returns nothing
        native DzSetEffectTeamColor takes effect whichHandle, integer playerId returns nothing
        native DzFrameSetClip takes integer whichframe, boolean enable returns nothing 
        native DzChangeWindowSize takes integer width, integer height returns boolean 
        native DzPlayEffectAnimation takes effect whichEffect, string anim, string link returns nothing 
        native DzBindEffect takes widget parent, string attachPoint, effect whichEffect returns nothing 
        native DzUnbindEffect takes effect whichEffect returns nothing 
        native DzSetWidgetSpriteScale takes widget whichUnit, real scale returns nothing 
        native DzSetEffectScale takes effect whichHandle, real scale returns nothing 
        native DzGetEffectVertexColor takes effect whichEffect returns integer 
        native DzGetEffectVertexAlpha takes effect whichEffect returns integer 
        native DzGetItemAbility takes item whichEffect, integer index returns ability 
        native DzFrameGetChildrenCount takes integer whichframe returns integer 
        native DzFrameGetChild takes integer whichframe, integer index returns integer 
        native DzUnlockBlpSizeLimit takes boolean enable returns nothing 
        native DzGetActivePatron takes unit store, player p returns unit 
        native DzGetLocalSelectUnitCount takes nothing returns integer 
        native DzGetLocalSelectUnit takes integer index returns unit 
        native DzGetJassStringTableCount takes nothing returns integer 
        native DzModelRemoveFromCache takes string path returns nothing 
        native DzModelRemoveAllFromCache takes nothing returns nothing 
        native DzFrameGetInfoPanelSelectButton takes integer index returns integer 
        native DzFrameGetInfoPanelBuffButton takes integer index returns integer 
        native DzFrameGetPeonBar takes nothing returns integer 
        native DzFrameGetCommandBarButtonNumberText takes integer whichframe returns integer 
        native DzFrameGetCommandBarButtonNumberOverlay takes integer whichframe returns integer 
        native DzFrameGetCommandBarButtonCooldownIndicator takes integer whichframe returns integer 
        native DzFrameGetCommandBarButtonAutoCastIndicator takes integer whichframe returns integer 
        native DzToggleFPS takes boolean show returns nothing 
        native DzGetFPS takes nothing returns integer 
        native DzFrameWorldToMinimapPosX takes real x, real y returns real 
        native DzFrameWorldToMinimapPosY takes real x, real y returns real 
        native DzWidgetSetMinimapIcon takes unit whichunit, string path returns nothing 
        native DzWidgetSetMinimapIconEnable takes unit whichunit, boolean enable returns nothing 
        native DzFrameGetWorldFrameMessage takes nothing returns integer 
        native DzSimpleMessageFrameAddMessage takes integer whichframe, string text, integer color, real duration, boolean permanent returns nothing 
        native DzSimpleMessageFrameClear takes integer whichframe returns nothing 
        native DzConvertScreenPositionX takes real x, real y returns real 
        native DzConvertScreenPositionY takes real x, real y returns real 
        native DzRegisterOnBuildLocal takes code func returns nothing 
        native DzGetOnBuildOrderId takes nothing returns integer 
        native DzGetOnBuildOrderType takes nothing returns integer 
        native DzGetOnBuildAgent takes nothing returns widget 
        native DzRegisterOnTargetLocal takes code func returns nothing 
        native DzGetOnTargetAbilId takes nothing returns integer 
        native DzGetOnTargetOrderId takes nothing returns integer 
        native DzGetOnTargetOrderType takes nothing returns integer 
        native DzGetOnTargetAgent takes nothing returns widget 
        native DzGetOnTargetInstantTarget takes nothing returns widget 
        native DzOpenQQGroupUrl takes string url returns boolean 
        native DzFrameEnableClipRect takes boolean enable returns nothing 
        native DzSetUnitName takes unit whichUnit, string name returns nothing 
        native DzSetUnitPortrait takes unit whichUnit, string modelFile returns nothing 
        native DzSetUnitDescription takes unit whichUnit, string value returns nothing 
        native DzSetUnitMissileArc takes unit whichUnit, real arc returns nothing 
        native DzSetUnitMissileModel takes unit whichUnit, string modelFile returns nothing 
        native DzSetUnitProperName takes unit whichUnit, string name returns nothing 
        native DzSetUnitMissileHoming takes unit whichUnit, boolean enable returns nothing 
        native DzSetUnitMissileSpeed takes unit whichUnit, real speed returns nothing 
        native DzSetEffectVisible takes effect whichHandle, boolean enable returns nothing 
        native DzReviveUnit takes unit whichUnit, player whichPlayer, real hp, real mp, real x, real y returns nothing 
        native DzGetAttackAbility takes unit whichUnit returns ability 
        native DzAttackAbilityEndCooldown takes ability whichHandle returns nothing 
        native EXSetUnitArrayString takes integer uid, integer id, integer n, string name returns boolean 
        native EXSetUnitInteger takes integer uid, integer id, integer n returns boolean 
        native DzDoodadCreate takes integer id, integer var, real x, real y, real z, real rotate, real scale returns integer 
        native DzDoodadGetTypeId takes integer doodad returns integer 
        native DzDoodadSetModel takes integer doodad, string modelFile returns nothing 
        native DzDoodadSetTeamColor takes integer doodad, integer color returns nothing 
        native DzDoodadSetColor takes integer doodad, integer color returns nothing 
        native DzDoodadGetX takes integer doodad returns real 
        native DzDoodadGetY takes integer doodad returns real 
        native DzDoodadGetZ takes integer doodad returns real 
        native DzDoodadSetPosition takes integer doodad, real x, real y, real z returns nothing 
        native DzDoodadSetOrientMatrixRotate takes integer doodad, real angle, real axisX, real axisY, real axisZ returns nothing 
        native DzDoodadSetOrientMatrixScale takes integer doodad, real x, real y, real z returns nothing 
        native DzDoodadSetOrientMatrixResize takes integer doodad returns nothing 
        native DzDoodadSetVisible takes integer doodad, boolean enable returns nothing 
        native DzDoodadSetAnimation takes integer doodad, string animName, boolean animRandom returns nothing 
        native DzDoodadSetTimeScale takes integer doodad, real scale returns nothing 
        native DzDoodadGetTimeScale takes integer doodad returns real 
        native DzDoodadGetCurrentAnimationIndex takes integer doodad returns integer 
        native DzDoodadGetAnimationCount takes integer doodad returns integer 
        native DzDoodadGetAnimationName takes integer doodad, integer index returns string 
        native DzDoodadGetAnimationTime takes integer doodad, integer index returns integer 
        native DzUnlockOpCodeLimit takes boolean enable returns nothing
        native DzSetClipboard takes string content returns boolean
        native DzDoodadRemove takes integer doodad returns nothing
        native DzRemovePlayerTechResearched takes player whichPlayer, integer techid, integer removelevels returns nothing
        native DzUnitFindAbility takes unit whichUnit, integer abilcode returns ability
        native DzAbilitySetStringData takes ability whichAbility, string key, string value returns nothing
        native DzAbilitySetEnable takes ability whichAbility, boolean enable, boolean hideUI returns nothing
        native DzUnitSetMoveType takes unit whichUnit, string moveType returns nothing
        native DzFrameGetWidth takes integer frame returns real
        native DzFrameSetAnimateByIndex takes integer frame, integer index, integer flag returns nothing
        native DzSetUnitDataCacheInteger takes integer uid, integer id,integer index,integer v returns nothing
        native DzUnitUIAddLevelArrayInteger takes integer uid, integer id,integer lv,integer v returns nothing
        native DzItemSetModel takes item whichItem, string file returns nothing
        native DzItemSetVertexColor takes item whichItem, integer color returns nothing
        native DzItemSetAlpha takes item whichItem, integer color returns nothing
        native DzItemSetPortrait takes item whichItem, string modelPath returns nothing
	native DzFrameHookHpBar takes code func returns nothing
	native DzFrameGetTriggerHpBarUnit takes nothing returns unit
	native DzFrameGetTriggerHpBar takes nothing returns integer
	native DzFrameGetUnitHpBar takes unit whichUnit returns integer
        native DzGetCursorFrame takes nothing returns integer
        native DzFrameGetPointValid takes integer frame, integer anchor returns boolean
        native DzFrameGetPointRelative takes integer frame, integer anchor returns integer
        native DzFrameGetPointRelativePoint takes integer frame, integer anchor returns integer
        native DzFrameGetPointX takes integer frame, integer anchor returns real
        native DzFrameGetPointY takes integer frame, integer anchor returns real
        native DzWriteLog takes string msg returns nothing
        native DzTextTagGetFont takes nothing returns string
        native DzTextTagSetFont takes string fileName returns nothing
        native DzTextTagSetStartAlpha takes texttag t, integer alpha returns nothing
        native DzTextTagGetShadowColor takes texttag t returns integer
        native DzTextTagSetShadowColor takes texttag t, integer color returns nothing
        native DzGroupGetCount takes group g returns integer
        native DzGroupGetUnitAt takes group g, integer index returns unit
        native DzUnitCreateIllusion takes player p, integer unitId, real x, real y, real face returns unit
        native DzUnitCreateIllusionFromUnit takes unit u returns unit
        native DzStringContains takes string s, string whichString, boolean caseSensitive returns boolean
        native DzStringFind takes string s, string whichString, integer off, boolean caseSensitive returns integer
        native DzStringFindFirstOf takes string s, string whichString, integer off, boolean caseSensitive returns integer
        native DzStringFindFirstNotOf takes string s, string whichString, integer off, boolean caseSensitive returns integer
        native DzStringFindLastOf takes string s, string whichString, integer off, boolean caseSensitive returns integer
        native DzStringFindLastNotOf takes string s, string whichString, integer off, boolean caseSensitive returns integer
        native DzStringTrimLeft takes string s returns string
        native DzStringTrimRight takes string s returns string
        native DzStringTrim takes string s returns string
        native DzStringReverse takes string s returns string
        native DzStringReplace takes string s, string whichString, string replaceWith, boolean caseSensitive returns string
        native DzStringInsert takes string s, integer whichPosition, string whichString returns string
        native DzBitGet takes integer i, integer byteIndex returns integer
        native DzBitSet takes integer i, integer byteIndex, integer byteValue returns integer
        native DzBitGetByte takes integer i, integer byteIndex returns integer
        native DzBitSetByte takes integer i, integer byteIndex, integer byteValue returns integer
        native DzBitNot takes integer i returns integer
        native DzBitAnd takes integer a, integer b returns integer
        native DzBitOr takes integer a, integer b returns integer
        native DzBitXor takes integer a, integer b returns integer
        native DzBitShiftLeft takes integer i, integer bitsToShift returns integer
        native DzBitShiftRight takes integer i, integer bitsToShift returns integer
        native DzBitToInt takes integer b1, integer b2, integer b3, integer b4 returns integer
        native DzQueueGroupImmediateOrderById takes group whichGroup, integer order returns boolean
        native DzQueueGroupPointOrderById takes group whichGroup, integer order, real x, real y returns boolean
        native DzQueueGroupTargetOrderById takes group whichGroup, integer order, widget targetWidget returns boolean
        native DzQueueIssueImmediateOrderById takes unit whichUnit, integer order returns boolean
        native DzQueueIssuePointOrderById takes unit whichUnit, integer order, real x, real y returns boolean
        native DzQueueIssueTargetOrderById takes unit whichUnit, integer order, widget targetWidget returns boolean
        native DzQueueIssueInstantPointOrderById takes unit whichUnit, integer order, real x, real y, widget instantTargetWidget returns boolean
        native DzQueueIssueInstantTargetOrderById takes unit whichUnit, integer order, widget targetWidget, widget instantTargetWidget returns boolean
        native DzQueueIssueBuildOrderById takes unit whichPeon, integer unitId, real x, real y returns boolean
        native DzQueueIssueNeutralImmediateOrderById takes player forWhichPlayer,unit neutralStructure, integer unitId returns boolean
        native DzQueueIssueNeutralPointOrderById takes player forWhichPlayer,unit neutralStructure, integer unitId, real x, real y returns boolean
        native DzQueueIssueNeutralTargetOrderById takes player forWhichPlayer,unit neutralStructure, integer unitId, widget target returns boolean
        native DzUnitOrdersCount takes unit u returns integer
        native DzUnitOrdersClear takes unit u, boolean onlyQueued returns nothing
        native DzUnitOrdersExec takes unit u returns nothing
        native DzUnitOrdersForceStop takes unit u, boolean clearQueue returns nothing
        native DzUnitOrdersReverse takes unit u returns nothing
        native DzXlsxOpen takes string filePath returns integer
        native DzXlsxClose takes integer docHandle returns boolean
        native DzXlsxWorksheetGetRowCount takes integer docHandle, string sheetName returns integer
        native DzXlsxWorksheetGetColumnCount takes integer docHandle, string sheetName returns integer
        native DzXlsxWorksheetGetCellType takes integer docHandle, string sheetName, integer row, integer column returns integer
        native DzXlsxWorksheetGetCellString takes integer docHandle, string sheetName, integer row, integer column returns string
        native DzXlsxWorksheetGetCellInteger takes integer docHandle, string sheetName, integer row, integer column returns integer
        native DzXlsxWorksheetGetCellBoolean takes integer docHandle, string sheetName, integer row, integer column returns boolean
        native DzXlsxWorksheetGetCellFloat takes integer docHandle, string sheetName, integer row, integer column returns real
        native DzFrameSetTexCoord takes integer frame, real left, real top, real right, real bottom returns nothing
        native DzSetUnitAbilityRange takes unit Unit, integer abil_code, real value returns boolean
        native DzGetUnitAbilityRange takes unit Unit, integer abil_code returns real
        native DzSetUnitAbilityArea takes unit Unit, integer abil_code, real value returns boolean
        native DzGetUnitAbilityArea takes unit Unit, integer abil_code returns real
        native DzSetUnitAbilityCool takes unit Unit, integer abil_code, real cool, real max_cool returns boolean
        native DzGetUnitAbilityCool takes unit Unit, integer abil_code returns real
        native DzGetUnitAbilityMaxCool takes unit Unit, integer abil_code returns real
        native DzSetUnitAbilityDataA takes unit Unit, integer abil_code, real value returns boolean
        native DzGetUnitAbilityDataA takes unit Unit, integer abil_code returns real
        native DzSetUnitAbilityDataB takes unit Unit, integer abil_code, real value returns boolean
        native DzGetUnitAbilityDataB takes unit Unit, integer abil_code returns real
        native DzSetUnitAbilityDataC takes unit Unit, integer abil_code, real value returns boolean
        native DzGetUnitAbilityDataC takes unit Unit, integer abil_code returns real
        native DzSetUnitAbilityDataD takes unit Unit, integer abil_code, real value returns boolean
        native DzGetUnitAbilityDataD takes unit Unit, integer abil_code returns real
        native DzSetUnitAbilityDataE takes unit Unit, integer abil_code, real value returns boolean
        native DzGetUnitAbilityDataE takes unit Unit, integer abil_code returns real
        native DzSetUnitAbilityButtonPos takes unit Unit, integer abil_code, integer x, integer y returns boolean
        native DzSetUnitAbilityHotkey takes unit Unit, integer abil_code, string key returns boolean
        native DzConvertTargs2Str takes integer targs returns string 
        native DzConvertStr2Targs takes string targs returns integer 
        native DzSetUnitAbilityTargs takes unit Unit, integer abil_code, integer value returns boolean
        native DzGetUnitAbilityTargs takes unit Unit, integer abil_code returns integer
        native DzSetUnitAbilityCost takes unit Unit, integer abil_code, integer value returns boolean
        native DzGetUnitAbilityCost takes unit Unit, integer abil_code returns integer
        native DzSetUnitAbilityReqLevel takes unit Unit, integer abil_code, integer value returns boolean
        native DzGetUnitAbilityReqLevel takes unit Unit, integer abil_code returns integer
        native DzSetUnitAbilityUnitId takes unit Unit, integer abil_code, integer value returns boolean
        native DzGetUnitAbilityUnitId takes unit Unit, integer abil_code returns integer
        native DzSetUnitAbilityBuildOrderId takes unit Unit, integer abil_code, integer value returns boolean
        native DzGetUnitAbilityBuildOrderId takes unit Unit, integer abil_code returns integer
        native DzSetUnitAbilityBuildModel takes unit Unit, integer abil_code, string model_path, real model_scale returns boolean 
        native DzUnitHasAbility takes unit Unit, integer abil_code returns boolean 
        native KKCreateCommandButton takes nothing returns integer 
        native KKDestroyCommandButton takes integer btn returns nothing 
        native KKCommandButtonClick takes integer btn, integer mouse_type returns nothing
        native KKCommandTargetClick takes integer mouse_type, widget target returns boolean 
        native KKCommandTerrainClick takes integer mouse_type, real x, real y, real z returns boolean 
        native KKSetCommandUnitAbility takes integer btn, unit Unit, integer abil_code returns nothing 
        native DzItemGetVertexColor takes item Item returns integer 
        native DzItemSetSize takes item Item, real size returns nothing 
        native DzItemGetSize takes item Item returns real 
        native DzItemMatRotateX takes item Item, real x returns nothing
        native DzItemMatRotateY takes item Item, real y returns nothing
        native DzItemMatRotateZ takes item Item, real z returns nothing
        native DzItemMatScale takes item Item, real x, real y, real z returns nothing
        native DzItemMatReset takes item Item returns nothing 
        native DzGetLastSelectedItem takes nothing returns item 
        native DzSetPariticle2Size takes agent Widget, real scale returns nothing 
        native DzSetUnitCollisionSize takes unit Unit, real size returns nothing 
        native DzGetUnitCollisionSize takes unit Unit returns real 
        native DzSetWidgetTexture takes agent Handle, string TexturePath, integer ReplaceId returns nothing 
        native DzSetUnitSelectScale takes unit Unit, real scale returns nothing 
        native DzSetUnitHitIgnore takes unit Unit, boolean ignore returns nothing 
        native DzEffectBindEffect takes agent Handle, string AttachName, effect eff returns nothing
        native DzFrameSetIgnoreTrackEvents takes integer frame, boolean ignore returns nothing 
        native DzFrameAddModel takes integer parent_frame returns integer 
        native DzFrameSetModel2 takes integer model_frame, string model_file, integer team_color_id returns nothing 
        native DzFrameAddModelEffect takes integer model_frame, string attach_point, string model_file returns integer 
        native DzFrameRemoveModelEffect takes integer model_frame, integer effect_frame returns nothing 
        native DzFrameSetModelAnimationByIndex takes integer model_frame, integer anim_index returns nothing 
        native DzFrameSetModelAnimation takes integer model_frame, string animation returns nothing 
        native DzFrameSetModelCameraSource takes integer model_frame, real x, real y, real z returns nothing 
        native DzFrameSetModelCameraTarget takes integer model_frame, real x, real y, real z returns nothing 
        native DzFrameSetModelSize takes integer model_frame, real size returns nothing 
        native DzFrameGetModelSize takes integer model_frame returns real 
        native DzFrameSetModelPosition takes integer model_frame, real x, real y, real z returns nothing
        native DzFrameSetModelX takes integer model_frame, real x returns nothing 
        native DzFrameGetModelX takes integer model_frame returns real 
        native DzFrameSetModelY takes integer model_frame, real y returns nothing 
        native DzFrameGetModelY takes integer model_frame returns real 
        native DzFrameSetModelZ takes integer model_frame, real z returns nothing 
        native DzFrameGetModelZ takes integer model_frame returns real 
        native DzFrameSetModelSpeed takes integer model_frame, real speed returns nothing 
        native DzFrameGetModelSpeed takes integer model_frame returns real 
        native DzFrameSetModelScale takes integer model_frame, real x, real y, real z returns nothing 
        native DzFrameSetModelMatReset takes integer model_frame returns nothing 
        native DzFrameSetModelRotateX takes integer model_frame, real x returns nothing 
        native DzFrameSetModelRotateY takes integer model_frame, real y returns nothing 
        native DzFrameSetModelRotateZ takes integer model_frame, real z returns nothing 
        native DzFrameSetModelColor takes integer model_frame, integer color returns nothing 
        native DzFrameGetModelColor takes integer model_frame returns integer
        native DzFrameSetModelTexture takes integer model_frame, string texture_file, integer replace_texutre_id returns nothing 
        native DzFrameSetModelParticle2Size takes integer model_frame, real scale returns nothing 
        native DzGetGlueUI takes nothing returns integer 
        native DzFrameGetMouse takes nothing returns integer 
        native DzFrameGetContext takes integer frame returns integer 
        native DzFrameSetNameContext takes integer frame, string name, integer context returns nothing 
        native DzFrameSetTextFontSpacing takes integer text_frame, real spacing returns nothing 
        native KKCommandGetCooldownModel takes integer cmd_btn returns integer 
        native KKCommandSetCooldownModelSize takes integer cmd_btn, real size returns nothing 
        native KKCommandSetCooldownModelSize2 takes integer cmd_btn, real width, real height returns nothing 
        native DzGetPlayerLastSelectedItem takes player p returns item 
        native DzGetCacheModelCount takes nothing returns integer 
        native DzSetMaxFps takes integer max_fps returns nothing 
        native DzEnableDrawSkillPanel takes unit u, boolean is_enable returns nothing 
        native DzEnableDrawSkillPanelByPlayer takes player p, boolean is_enable returns nothing 
        native DzSetEffectFogVisible takes effect eff, boolean is_visible returns nothing 
        native DzSetEffectMaskVisible takes effect eff, boolean is_visible returns nothing 
        native DzFrameBindWidget takes integer frame, widget u, real world_x, real world_y, real world_z, real screen_x, real screen_y, boolean fog_visible, boolean unit_visible, boolean dead_visible returns nothing 
        native DzFrameBindWorldPos takes integer frame, real world_x, real world_y, real world_z, real screen_x, real screen_y, boolean fog_visible returns nothing
        native DzFrameUnBind takes integer frame returns nothing 
        native DzDisableUnitPreselectUi takes nothing returns nothing
        native DzDisableItemPreselectUi takes nothing returns nothing
        native DzFrameGetLowerLevelFrame takes nothing returns integer 
        native DzFrameSetCheckBoxState takes integer check_box_frame, boolean checked returns nothing
        native DzFrameGetCheckBoxState takes integer check_box_frame returns boolean
        native DzFrameIsFocus takes integer frame returns boolean 
        native DzFrameSetEditBoxActive takes integer frame, boolean is_active returns nothing 
        native DzFrameSetEditBoxDisableIme takes integer frame, boolean is_disable returns nothing 
        native DzIsWindowMode takes nothing returns boolean 
        native DzWindowSetPoint takes integer x, integer y returns nothing 
        native DzWindowSetSize takes integer width, integer height returns nothing 
        native DzGetSystemMetricsWidth takes nothing returns integer 
        native DzGetSystemMetricsHeight takes nothing returns integer 
        native DzGetDoodadsCount takes nothing returns integer 
        native DzSetDoodadsMatScale takes integer doodads_index, real x, real y, real z returns nothing 
        native DzSetDoodadsMatRotateX takes integer doodads_index, real x returns nothing 
        native DzSetDoodadsMatRotateY takes integer doodads_index, real y returns nothing 
        native DzSetDoodadsMatRotateZ takes integer doodads_index, real z returns nothing 
        native DzSetDoodadsMatReset takes integer doodads_index returns nothing 
        native DzSetUnitAbilityArt takes unit u, integer abil_id, string art_path returns boolean
        native DzGetUnitAbilityArt takes unit u, integer abil_id returns string
        native DzSetUnitAbilityTip takes unit u, integer abil_id, string tip returns boolean
        native DzGetUnitAbilityTip takes unit u, integer abil_id returns string
        native DzSetUnitAbilityUberTip takes unit u, integer abil_id, string ubertip returns boolean
        native DzGetUnitAbilityUberTip takes unit u, integer abil_id returns string
        native DzSetUnitAbilityUpdate takes unit u, integer abil_id returns boolean 
        native DzSetUnitAbilityOrderId takes unit u, integer abil_id, integer order_id returns boolean
        native DzGetUnitAbilityOrderId takes unit u, integer abil_id returns integer
        native DzSetUnitAbilitySpellBookList takes unit u, integer abil_id, string abil_list, boolean save_cooldown returns boolean 
        native DzGetUnitAbilitySpellBookList takes unit u, integer abil_id returns string 
        native DzSetUnitAbilityMissileArt takes unit u, integer abil_id, string missile_art returns boolean
        native DzGetUnitAbilityMissileArt takes unit u, integer abil_id returns string
        native DzSetUnitAbilityMissileSpeed takes unit u, integer abil_id, real missile_speed returns boolean
        native DzGetUnitAbilityMissileSpeed takes unit u, integer abil_id returns real
        native DzSetUnitAbilityMissileArc takes unit u, integer abil_id, real missile_arc returns boolean
        native DzGetUnitAbilityMissileArc takes unit u, integer abil_id returns real
        native DzSetUnitAbilityMissileHoming takes unit u, integer abil_id, boolean missile_homing returns boolean
        native DzGetUnitAbilityMissileHoming takes unit u, integer abil_id returns boolean
        native DzSetUnitAbilityMissileCount takes unit u, integer abil_id, integer missile_count returns boolean
        native DzGetUnitAbilityMissileCount takes unit u, integer abil_id returns integer
        native DzSetUnitAbilityMissileDamage takes unit u, integer abil_id, real damage, real max_damage, attacktype atktp, damagetype dmgtp returns boolean
        native DzGetUnitAbilityMissileDamage takes unit u, integer abil_id returns real
        native DzGetUnitAbilityMissileMaxDamage takes unit u, integer abil_id returns real


//Generated method caller for Skill.onDestroy
function sc__Skill_onDestroy takes integer this returns nothing
            set s__Skill_skill_id[this]=0
            set s__Skill_skill_name[this]=""
            set s__Skill_skill_desc[this]=""
            set s__Skill_skill_type[this]=0
            set s__Skill_skill_target_type[this]=0
            set s__Skill_skill_template_id[this]=0
            set s__Skill_skill_cooldown[this]=0.0
            set s__Skill_skill_magic_cost[this]=0
            set s__Skill_skill_cast_range[this]=0.0
            set s__Skill_skill_damage_coefficient[this]=0.0
            set s__Skill_skill_attribute_type[this]=0
            set s__Skill_skill_element_type[this]=0
            set s__Skill_skill_damage_type[this]=0
endfunction

//Generated allocator of Skill
function s__Skill__allocate takes nothing returns integer
 local integer this=si__Skill_F
    if (this!=0) then
        set si__Skill_F=si__Skill_V[this]
    else
        set si__Skill_I=si__Skill_I+1
        set this=si__Skill_I
    endif
    if (this>8190) then
        return 0
    endif

    set si__Skill_V[this]=-1
 return this
endfunction

//Generated destructor of Skill
function sc__Skill_deallocate takes integer this returns nothing
    if this==null then
        return
    elseif (si__Skill_V[this]!=-1) then
        return
    endif
    set f__arg_this=this
    call TriggerEvaluate(st__Skill_onDestroy)
    set si__Skill_V[this]=si__Skill_F
    set si__Skill_F=this
endfunction

//library AttackMonsterData:
    // 将二维数组转换为一维数组的辅助函数
    function GetMonsterIndex takes integer wave,integer monsterIdx returns integer
        return ( wave * MAX_MONSTERS_PER_WAVE ) + monsterIdx
    endfunction
    // 初始化每波怪物组成
    // 此函数确定每波出现的怪物类型
    function InitializeMonsterWaves takes nothing returns nothing
        local integer wave= 1
        local integer monster_idx= 1
        local integer monster_array_index= 0
        // 波次1-10: 主要是普通怪物，偶尔出现坦克
        loop
            exitwhen wave > 10
            set udg_monster_count_per_wave[wave]=10 + wave // 从10开始，每波增加1个

            set monster_idx=1
            loop
                exitwhen monster_idx > udg_monster_count_per_wave[wave]
                set monster_array_index=GetMonsterIndex(wave , monster_idx)
                if monster_idx == udg_monster_count_per_wave[wave] and udg_monster_count_per_wave[wave] > 3 then
                    // 波次最后一个怪物有几率是坦克
                    if GetRandomInt(1, 100) <= 30 then
                        set udg_monster_types_per_wave[monster_array_index]=MONSTER_TYPE_TANK
                    else
                        set udg_monster_types_per_wave[monster_array_index]=MONSTER_TYPE_NORMAL
                    endif
                else
                    set udg_monster_types_per_wave[monster_array_index]=MONSTER_TYPE_NORMAL
                endif
                set monster_idx=monster_idx + 1
            endloop
            set wave=wave + 1
        endloop
        // 波次11-20: 普通和输出怪物混合，更多坦克
        loop
            exitwhen wave > 20
            set udg_monster_count_per_wave[wave]=10 + wave * 2 // 从10开始，每波增加2个

            set monster_idx=1
            loop
                exitwhen monster_idx > udg_monster_count_per_wave[wave]
                set monster_array_index=GetMonsterIndex(wave , monster_idx)
                set udg_monster_types_per_wave[monster_array_index]=GetRandomInt(MONSTER_TYPE_NORMAL, MONSTER_TYPE_DPS)
                // 坦克怪物出现几率 (随波次增加)
                if GetRandomInt(1, 100) <= ( 10 + ( wave - 10 ) * 2 ) then
                    set udg_monster_types_per_wave[monster_array_index]=MONSTER_TYPE_TANK
                endif
                set monster_idx=monster_idx + 1
            endloop
            set wave=wave + 1
        endloop
        // 波次21-30: 所有类型混合，引入特殊怪物
        loop
            exitwhen wave > 30
            set udg_monster_count_per_wave[wave]=7 + ( wave - 20 ) // 从7开始，每波增加1个

            set monster_idx=1
            loop
                exitwhen monster_idx > udg_monster_count_per_wave[wave]
                set monster_array_index=GetMonsterIndex(wave , monster_idx)
                set udg_monster_types_per_wave[monster_array_index]=GetRandomInt(MONSTER_TYPE_NORMAL, MONSTER_TYPE_SPECIAL)
                // 特殊怪物几率调整
                if GetRandomInt(1, 100) <= ( 5 + ( wave - 20 ) * 2 ) then
                    set udg_monster_types_per_wave[monster_array_index]=MONSTER_TYPE_SPECIAL
                elseif GetRandomInt(1, 100) <= ( 15 + ( wave - 20 ) ) then
                    set udg_monster_types_per_wave[monster_array_index]=MONSTER_TYPE_TANK
                endif
                set monster_idx=monster_idx + 1
            endloop
            set wave=wave + 1
        endloop
        // 波次31+: 高难度混合，更多特殊怪物
        loop
            exitwhen wave > MAX_WAVE_COUNT
            set udg_monster_count_per_wave[wave]=10 + ( ( wave - 30 ) * 2 ) // 30波后每波增加2个

            set monster_idx=1
            loop
                exitwhen monster_idx > udg_monster_count_per_wave[wave]
                set monster_array_index=GetMonsterIndex(wave , monster_idx)
                set udg_monster_types_per_wave[monster_array_index]=GetRandomInt(MONSTER_TYPE_NORMAL, MONSTER_TYPE_SPECIAL)
                // 后期特殊和坦克怪物几率更高
                if GetRandomInt(1, 100) <= ( 15 + ( wave - 30 ) * 3 ) then
                    set udg_monster_types_per_wave[monster_array_index]=MONSTER_TYPE_SPECIAL
                elseif GetRandomInt(1, 100) <= ( 20 + ( wave - 30 ) * 2 ) then
                    set udg_monster_types_per_wave[monster_array_index]=MONSTER_TYPE_TANK
                elseif GetRandomInt(1, 100) <= ( 10 + ( wave - 30 ) ) then
                    set udg_monster_types_per_wave[monster_array_index]=MONSTER_TYPE_DPS
                endif
                set monster_idx=monster_idx + 1
            endloop
            set wave=wave + 1
        endloop
        // 重置局部变量以节省内存
        set wave=0
        set monster_idx=0
        set monster_array_index=0
    endfunction

//library AttackMonsterData ends
//library BzAPI:
    //hardware




























    //plus











    //sync






    //native DzGetPushContext takes nothing returns string

    //gui















































































    //显示/隐藏SimpleFrame

    // 追加文字（支持TextArea）

    // 沉默单位-禁用技能

    // 禁用攻击

    // 禁用道具

    // 刷新小地图

    // 修改单位alpha

    // 设置单位是否可以选中

    // 修改单位是否可以被设置为目标

    // 保存内存数据

    // 读取内存数据

    // 设置加速倍率

    // 转换世界坐标为屏幕坐标-异步

    // 转换世界坐标为屏幕坐标-获取转换后的X坐标

    // 转换世界坐标为屏幕坐标-获取转换后的Y坐标

    // 创建command button

    function DzTriggerRegisterMouseEventTrg takes trigger trg,integer status,integer btn returns nothing
        if trg == null then
            return
        endif
        call DzTriggerRegisterMouseEvent(trg, btn, status, true, null)
    endfunction
    function DzTriggerRegisterKeyEventTrg takes trigger trg,integer status,integer btn returns nothing
        if trg == null then
            return
        endif
        call DzTriggerRegisterKeyEvent(trg, btn, status, true, null)
    endfunction
    function DzTriggerRegisterMouseMoveEventTrg takes trigger trg returns nothing
        if trg == null then
            return
        endif
        call DzTriggerRegisterMouseMoveEvent(trg, true, null)
    endfunction
    function DzTriggerRegisterMouseWheelEventTrg takes trigger trg returns nothing
        if trg == null then
            return
        endif
        call DzTriggerRegisterMouseWheelEvent(trg, true, null)
    endfunction
    function DzTriggerRegisterWindowResizeEventTrg takes trigger trg returns nothing
        if trg == null then
            return
        endif
        call DzTriggerRegisterWindowResizeEvent(trg, true, null)
    endfunction
    function DzF2I takes integer i returns integer
        return i
    endfunction
    function DzI2F takes integer i returns integer
        return i
    endfunction
    function DzK2I takes integer i returns integer
        return i
    endfunction
    function DzI2K takes integer i returns integer
        return i
    endfunction
    function DzTriggerRegisterMallItemSyncData takes trigger trig returns nothing
        call DzTriggerRegisterSyncData(trig, "DZMIA", true)
    endfunction
    //玩家消耗/使用商城道具事件
    function DzTriggerRegisterMallItemConsumeEvent takes trigger trig returns nothing
        call DzTriggerRegisterSyncData(trig, "DZMIC", true)
    endfunction
    //玩家删除商城道具事件
    function DzTriggerRegisterMallItemRemoveEvent takes trigger trig returns nothing
        call DzTriggerRegisterSyncData(trig, "DZMID", true)
    endfunction
    function DzGetTriggerMallItemPlayer takes nothing returns player
        return DzGetTriggerSyncPlayer()
    endfunction
    function DzGetTriggerMallItem takes nothing returns string
        return DzGetTriggerSyncData()
    endfunction
    

//library BzAPI ends
//library CultivationData:
    // ============================================================================
    // 数据初始化函数
    // 初始化历练阈值、名称、加成表，以及玩家数据
    // ============================================================================
    function InitCultivationData takes nothing returns nothing
        local integer i
        // ========================================================================
        // 初始化历练等级阈值表 (1-7级)
        // ========================================================================
        set udg_cultivation_threshold[1]=0
        set udg_cultivation_threshold[2]=500
        set udg_cultivation_threshold[3]=1500
        set udg_cultivation_threshold[4]=3000
        set udg_cultivation_threshold[5]=5000
        set udg_cultivation_threshold[6]=8000
        set udg_cultivation_threshold[7]=12000
        // ========================================================================
        // 初始化历练等级名称表
        // ========================================================================
        set udg_cultivation_name[1]="初入江湖"
        set udg_cultivation_name[2]="初窥门径"
        set udg_cultivation_name[3]="略有小成"
        set udg_cultivation_name[4]="融会贯通"
        set udg_cultivation_name[5]="炉火纯青"
        set udg_cultivation_name[6]="出神入化"
        set udg_cultivation_name[7]="一代宗师"
        // ========================================================================
        // 初始化历练伤害加成表（百分比）
        // ========================================================================
        set udg_cultivation_bonus[1]=0
        set udg_cultivation_bonus[2]=15
        set udg_cultivation_bonus[3]=35
        set udg_cultivation_bonus[4]=60
        set udg_cultivation_bonus[5]=90
        set udg_cultivation_bonus[6]=130
        set udg_cultivation_bonus[7]=180
        // ========================================================================
        // 初始化所有玩家的历练数据
        // ========================================================================
        set i=0
        loop
            exitwhen i > 11
            set udg_cultivation_exp[i]=0
            set udg_cultivation_level[i]=1
            set udg_unlock_mid_dungeon[i]=false
            set udg_unlock_graduation_skill[i]=false
            set udg_unlock_high_dungeon[i]=false
            set udg_unlock_elite_dungeon[i]=false
            set udg_unlock_ultimate_dungeon[i]=false
            set udg_unlock_b_encounter[i]=false
            set udg_unlock_a_encounter[i]=false
            set i=i + 1
        endloop
    endfunction
    // ============================================================================
    // 获取历练等级阈值
    // ============================================================================
    function CultivationData_GetThreshold takes integer level returns integer
        if level < 1 or level > 7 then
            return 0
        endif
        return udg_cultivation_threshold[level]
    endfunction
    // ============================================================================
    // 获取历练等级名称
    // ============================================================================
    function CultivationData_GetName takes integer level returns string
        if level < 1 or level > 7 then
            return "未知境界"
        endif
        return udg_cultivation_name[level]
    endfunction
    // ============================================================================
    // 获取历练伤害加成（百分比）
    // ============================================================================
    function CultivationData_GetBonus takes integer level returns integer
        if level < 1 or level > 7 then
            return 0
        endif
        return udg_cultivation_bonus[level]
    endfunction
    // ============================================================================
    // 根据历练值获取当前等级
    // ============================================================================
    function CultivationData_GetLevelByExp takes integer exp returns integer
        local integer level= 1
        loop
            exitwhen level >= 7
            if exp >= udg_cultivation_threshold[level + 1] then
                set level=level + 1
            else
                exitwhen true
            endif
        endloop
        return level
    endfunction
    // ============================================================================
    // 获取历练等级名称对应的解锁内容
    // ============================================================================
    function CultivationData_GetUnlockInfo takes integer level returns string
        if level == 2 then
            return "中阶副本、门派毕业技能选择"
        elseif level == 3 then
            return "高阶副本"
        elseif level == 4 then
            return "精英副本"
        elseif level == 5 then
            return "终极副本"
        elseif level == 6 then
            return "B级奇遇触发"
        elseif level == 7 then
            return "A级奇遇触发"
        endif
        return ""
    endfunction

//library CultivationData ends
//library DungeonData:
    // ============================================================================
    // 副本数据初始化函数
    // 初始化所有副本的基础数据配置
    // ============================================================================
    function InitDungeonData takes nothing returns nothing
        local integer dungeon_id
        // ========================================================================
        // D001 黑风寨
        // 品质：普通，BOSS：力量型
        // ========================================================================
        set dungeon_id=DUNGEON_D001
        set dungeon_name[dungeon_id]="黑风寨"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D001
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=1
        set dungeon_recommend_level_max[dungeon_id]=10
        set dungeon_entrance_x[dungeon_id]=0.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=- 500.00
        set dungeon_exit_y[dungeon_id]=0.00
        set dungeon_boss_unit_id[dungeon_id]='n001'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_STRENGTH
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_NORMAL
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D002 山贼据点
        // 品质：普通，BOSS：力量型
        // ========================================================================
        set dungeon_id=DUNGEON_D002
        set dungeon_name[dungeon_id]="山贼据点"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D002
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=5
        set dungeon_recommend_level_max[dungeon_id]=10
        set dungeon_entrance_x[dungeon_id]=500.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=0.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n002'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_STRENGTH
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_NORMAL
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D003 藏经阁
        // 品质：困难，BOSS：防御型
        // ========================================================================
        set dungeon_id=DUNGEON_D003
        set dungeon_name[dungeon_id]="藏经阁"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D003
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SECT
        set dungeon_recommend_level_min[dungeon_id]=11
        set dungeon_recommend_level_max[dungeon_id]=18
        set dungeon_entrance_x[dungeon_id]=1000.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=500.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n003'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_DEFENSE
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_HARD
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D004 隐世洞窟
        // 品质：困难，BOSS：法师型
        // ========================================================================
        set dungeon_id=DUNGEON_D004
        set dungeon_name[dungeon_id]="隐世洞窟"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D004
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=15
        set dungeon_recommend_level_max[dungeon_id]=22
        set dungeon_entrance_x[dungeon_id]=1500.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=1000.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n004'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_CASTER
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_HARD
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]='I201' // 侠客刀法

        // ========================================================================
        // D005 明教密窟
        // 品质：困难，BOSS：召唤型
        // ========================================================================
        set dungeon_id=DUNGEON_D005
        set dungeon_name[dungeon_id]="明教密窟"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D005
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=28
        set dungeon_recommend_level_max[dungeon_id]=35
        set dungeon_entrance_x[dungeon_id]=2000.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=1500.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n005'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_SUMMONER
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_HARD
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D006 竹林秘境
        // 品质：精英，BOSS：敏捷型
        // ========================================================================
        set dungeon_id=DUNGEON_D006
        set dungeon_name[dungeon_id]="竹林秘境"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D006
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=30
        set dungeon_recommend_level_max[dungeon_id]=38
        set dungeon_entrance_x[dungeon_id]=2500.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=2000.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n006'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_AGILITY
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_ELITE
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]='I202' // 丐帮棍法

        // ========================================================================
        // D007 逍遥山庄
        // 品质：精英，BOSS：法师型，可组队
        // ========================================================================
        set dungeon_id=DUNGEON_D007
        set dungeon_name[dungeon_id]="逍遥山庄"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D007
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_PARTY
        set dungeon_recommend_level_min[dungeon_id]=33
        set dungeon_recommend_level_max[dungeon_id]=38
        set dungeon_entrance_x[dungeon_id]=3000.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=2500.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n007'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_CASTER
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_ELITE
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D008 梅花坞
        // 品质：精英，BOSS：敏捷型
        // ========================================================================
        set dungeon_id=DUNGEON_D008
        set dungeon_name[dungeon_id]="梅花坞"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D008
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=36
        set dungeon_recommend_level_max[dungeon_id]=40
        set dungeon_entrance_x[dungeon_id]=3500.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=3000.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n008'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_AGILITY
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_ELITE
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]='I203' // 梅花暗器

        // ========================================================================
        // D009 五行峰
        // 品质：精英，BOSS：防御型
        // ========================================================================
        set dungeon_id=DUNGEON_D009
        set dungeon_name[dungeon_id]="五行峰"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D009
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=41
        set dungeon_recommend_level_max[dungeon_id]=47
        set dungeon_entrance_x[dungeon_id]=4000.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=3500.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n009'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_DEFENSE
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_ELITE
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D010 水月洞
        // 品质：精英，BOSS：法师型
        // ========================================================================
        set dungeon_id=DUNGEON_D010
        set dungeon_name[dungeon_id]="水月洞"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D010
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=45
        set dungeon_recommend_level_max[dungeon_id]=50
        set dungeon_entrance_x[dungeon_id]=4500.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=4000.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n010'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_CASTER
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_ELITE
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D011 剑圣谷
        // 品质：神级，BOSS：力量型
        // ========================================================================
        set dungeon_id=DUNGEON_D011
        set dungeon_name[dungeon_id]="剑圣谷"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D011
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=56
        set dungeon_recommend_level_max[dungeon_id]=63
        set dungeon_entrance_x[dungeon_id]=5000.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=4500.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n011'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_STRENGTH
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_MYTH
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D012 云梦泽
        // 品质：神级，BOSS：法师型
        // ========================================================================
        set dungeon_id=DUNGEON_D012
        set dungeon_name[dungeon_id]="云梦泽"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D012
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=60
        set dungeon_recommend_level_max[dungeon_id]=67
        set dungeon_entrance_x[dungeon_id]=5500.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=5000.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n012'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_CASTER
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_MYTH
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D013 武林圣地
        // 品质：神级，BOSS：召唤型，掉落神话碎片
        // ========================================================================
        set dungeon_id=DUNGEON_D013
        set dungeon_name[dungeon_id]="武林圣地"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D013
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=71
        set dungeon_recommend_level_max[dungeon_id]=85
        set dungeon_entrance_x[dungeon_id]=6000.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=5500.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n013'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_SUMMONER
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_MYTH
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
        // ========================================================================
        // D014 决战台
        // 品质：神级，BOSS：力量型，掉落神话碎片
        // ========================================================================
        set dungeon_id=DUNGEON_D014
        set dungeon_name[dungeon_id]="决战台"
        set dungeon_item_id[dungeon_id]=ITEM_ID_D014
        set dungeon_type[dungeon_id]=DUNGEON_TYPE_SINGLE
        set dungeon_recommend_level_min[dungeon_id]=80
        set dungeon_recommend_level_max[dungeon_id]=85
        set dungeon_entrance_x[dungeon_id]=6500.00
        set dungeon_entrance_y[dungeon_id]=0.00
        set dungeon_exit_x[dungeon_id]=6000.00
        set dungeon_exit_y[dungeon_id]=500.00
        set dungeon_boss_unit_id[dungeon_id]='n014'
        set dungeon_boss_type[dungeon_id]=BOSS_TYPE_STRENGTH
        set dungeon_quality[dungeon_id]=DUNGEON_QUALITY_MYTH
        set dungeon_can_revive[dungeon_id]=true
        set dungeon_state[dungeon_id]=DUNGEON_STATE_IDLE
        set dungeon_player_count[dungeon_id]=0
        set dungeon_complete_count[dungeon_id]=0
        set dungeon_martial_book_id[dungeon_id]=0
    endfunction
    // ============================================================================
    // 获取副本名称
    // ============================================================================
    function DungeonData_GetName takes integer dungeon_id returns string
        return dungeon_name[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本物品ID
    // ============================================================================
    function DungeonData_GetItemId takes integer dungeon_id returns integer
        return dungeon_item_id[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本类型
    // ============================================================================
    function DungeonData_GetType takes integer dungeon_id returns integer
        return dungeon_type[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本推荐等级最小值
    // ============================================================================
    function DungeonData_GetMinLevel takes integer dungeon_id returns integer
        return dungeon_recommend_level_min[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本推荐等级最大值
    // ============================================================================
    function DungeonData_GetMaxLevel takes integer dungeon_id returns integer
        return dungeon_recommend_level_max[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本入口坐标
    // ============================================================================
    function DungeonData_GetEntranceX takes integer dungeon_id returns real
        return dungeon_entrance_x[dungeon_id]
    endfunction
    function DungeonData_GetEntranceY takes integer dungeon_id returns real
        return dungeon_entrance_y[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本出口坐标
    // ============================================================================
    function DungeonData_GetExitX takes integer dungeon_id returns real
        return dungeon_exit_x[dungeon_id]
    endfunction
    function DungeonData_GetExitY takes integer dungeon_id returns real
        return dungeon_exit_y[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本BOSS单位ID
    // ============================================================================
    function DungeonData_GetBossUnitId takes integer dungeon_id returns integer
        return dungeon_boss_unit_id[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本BOSS类型
    // ============================================================================
    function DungeonData_GetBossType takes integer dungeon_id returns integer
        return dungeon_boss_type[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本品质
    // ============================================================================
    function DungeonData_GetQuality takes integer dungeon_id returns integer
        return dungeon_quality[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本状态
    // ============================================================================
    function DungeonData_GetState takes integer dungeon_id returns integer
        return dungeon_state[dungeon_id]
    endfunction
    // ============================================================================
    // 设置副本状态
    // ============================================================================
    function DungeonData_SetState takes integer dungeon_id,integer state returns nothing
        set dungeon_state[dungeon_id]=state
    endfunction
    // ============================================================================
    // 获取副本内玩家数量
    // ============================================================================
    function DungeonData_GetPlayerCount takes integer dungeon_id returns integer
        return dungeon_player_count[dungeon_id]
    endfunction
    // ============================================================================
    // 设置副本内玩家数量
    // ============================================================================
    function DungeonData_SetPlayerCount takes integer dungeon_id,integer count returns nothing
        set dungeon_player_count[dungeon_id]=count
    endfunction
    // ============================================================================
    // 增加副本内玩家数量
    // ============================================================================
    function DungeonData_AddPlayerCount takes integer dungeon_id returns nothing
        set dungeon_player_count[dungeon_id]=dungeon_player_count[dungeon_id] + 1
    endfunction
    // ============================================================================
    // 减少副本内玩家数量
    // ============================================================================
    function DungeonData_RemovePlayerCount takes integer dungeon_id returns nothing
        set dungeon_player_count[dungeon_id]=dungeon_player_count[dungeon_id] - 1
    endfunction
    // ============================================================================
    // 获取副本完成次数
    // ============================================================================
    function DungeonData_GetCompleteCount takes integer dungeon_id returns integer
        return dungeon_complete_count[dungeon_id]
    endfunction
    // ============================================================================
    // 增加副本完成次数
    // ============================================================================
    function DungeonData_AddCompleteCount takes integer dungeon_id returns nothing
        set dungeon_complete_count[dungeon_id]=dungeon_complete_count[dungeon_id] + 1
    endfunction
    // ============================================================================
    // 检查副本是否允许复活
    // ============================================================================
    function DungeonData_CanRevive takes integer dungeon_id returns boolean
        return dungeon_can_revive[dungeon_id]
    endfunction
    // ============================================================================
    // 获取副本武学书籍ID
    // ============================================================================
    function DungeonData_GetMartialBookId takes integer dungeon_id returns integer
        return dungeon_martial_book_id[dungeon_id]
    endfunction
    // ============================================================================
    // 根据物品ID获取副本ID
    // ============================================================================
    function DungeonData_GetDungeonIdByItemId takes integer item_id returns integer
        local integer dungeon_id
        set dungeon_id=1
        loop
            exitwhen dungeon_id > 14
            if item_id == dungeon_item_id[dungeon_id] then
                return dungeon_id
            endif
            set dungeon_id=dungeon_id + 1
        endloop
        return 0
    endfunction

//library DungeonData ends
//library DzAPI:


    // native DzAPI_Map_GetGuildName takes player whichPlayer returns string




    // SaveServerValue,               //保存服务器存档
    function DzAPI_Map_SaveServerValue takes player whichPlayer,string key,string value returns boolean
        return RequestExtraBooleanData(4, whichPlayer, key, value, false, 0, 0, 0)
    endfunction
    // GetServerValue,                //读取服务器存档
    function DzAPI_Map_GetServerValue takes player whichPlayer,string key returns string
        return RequestExtraStringData(5, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // GetGameStartTime,              //取游戏开始时间
    function DzAPI_Map_GetGameStartTime takes nothing returns integer
        return RequestExtraIntegerData(11, null, null, null, false, 0, 0, 0)
    endfunction
    // IsRPGLadder,                   //判断当前是否rpg天梯
    function DzAPI_Map_IsRPGLadder takes nothing returns boolean
        return RequestExtraBooleanData(12, null, null, null, false, 0, 0, 0)
    endfunction
    // GetMatchType,                  //获取匹配类型
    function DzAPI_Map_GetMatchType takes nothing returns integer
        return RequestExtraIntegerData(13, null, null, null, false, 0, 0, 0)
    endfunction
        // SetStat,                       //统计-提交地图数据
    function DzAPI_Map_Stat_SetStat takes player whichPlayer,string key,string value returns nothing
        call RequestExtraIntegerData(7, whichPlayer, key, value, false, 0, 0, 0)
    endfunction
    // SetLadderStat,                 //天梯-统计数据
    function DzAPI_Map_Ladder_SetStat takes player whichPlayer,string key,string value returns nothing
        call RequestExtraIntegerData(8, whichPlayer, key, value, false, 0, 0, 0)
    endfunction
    // SetLadderPlayerStat,           //天梯-统计数据
    function DzAPI_Map_Ladder_SetPlayerStat takes player whichPlayer,string key,string value returns nothing
        call RequestExtraIntegerData(9, whichPlayer, key, value, false, 0, 0, 0)
    endfunction
        // GetServerValueErrorCode,       //读取加载服务器存档时的错误码
    function DzAPI_Map_GetServerValueErrorCode takes player whichPlayer returns integer
        return RequestExtraIntegerData(6, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // GetLadderLevel,                //提供给地图的接口，用与取天梯等级
    function DzAPI_Map_GetLadderLevel takes player whichPlayer returns integer
        return RequestExtraIntegerData(14, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // PlayerIdentityType, // 获取玩家身份类型
    function KKApiPlayerIdentityType takes player whichPlayer,integer id returns boolean
        return RequestExtraBooleanData(92, whichPlayer, null, null, false, id, 0, 0)
    endfunction
    // IsRedVIP,                      //提供给地图的接口，用与判断是否红V
    function DzAPI_Map_IsRedVIP takes player whichPlayer returns boolean
        return KKApiPlayerIdentityType(whichPlayer , 4)
    endfunction
    // IsBlueVIP,                     //提供给地图的接口，用与判断是否蓝V
    function DzAPI_Map_IsBlueVIP takes player whichPlayer returns boolean
        return KKApiPlayerIdentityType(whichPlayer , 3)
    endfunction
    // GetLadderRank,                 //提供给地图的接口，用与取天梯排名
    function DzAPI_Map_GetLadderRank takes player whichPlayer returns integer
        return RequestExtraIntegerData(17, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // GetMapLevelRank,               //提供给地图的接口，用与取地图等级排名
    function DzAPI_Map_GetMapLevelRank takes player whichPlayer returns integer
        return RequestExtraIntegerData(18, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // GetGuildRole,                  //获取公会职责 Member=10 Admin=20 Leader=30
    function DzAPI_Map_GetGuildRole takes player whichPlayer returns integer
        return RequestExtraIntegerData(20, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // IsRPGLobby,                    //检查是否大厅地图
    function DzAPI_Map_IsRPGLobby takes nothing returns boolean
        return RequestExtraBooleanData(10, null, null, null, false, 0, 0, 0)
    endfunction
    // MissionComplete,               //用作完成某个任务，发奖励
    function DzAPI_Map_MissionComplete takes player whichPlayer,string key,string value returns nothing
        call RequestExtraIntegerData(1, whichPlayer, key, value, false, 0, 0, 0)
    endfunction
    // GetActivityData,               //提供给地图的接口，用作取服务器上的活动数据
    function DzAPI_Map_GetActivityData takes nothing returns string
        return RequestExtraStringData(2, null, null, null, false, 0, 0, 0)
    endfunction
    // GetMapConfig,                  //获取地图配置
    function DzAPI_Map_GetMapConfig takes string key returns string
        return RequestExtraStringData(21, null, key, null, false, 0, 0, 0)
    endfunction
    // SavePublicArchive,             //保存服务器存档组
    function DzAPI_Map_SavePublicArchive takes player whichPlayer,string key,string value returns boolean
        return RequestExtraBooleanData(31, whichPlayer, key, value, false, 0, 0, 0)
    endfunction
    // GetPublicArchive,              //读取服务器存档组
    function DzAPI_Map_GetPublicArchive takes player whichPlayer,string key returns string
        return RequestExtraStringData(32, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_UseConsumablesItem takes player whichPlayer,string key returns nothing
        call RequestExtraIntegerData(33, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // OrpgTrigger,                   //触发boss击杀
    function DzAPI_Map_OrpgTrigger takes player whichPlayer,string key returns nothing
        call RequestExtraIntegerData(28, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // GetServerArchiveDrop,          //读取服务器掉落数据
    function DzAPI_Map_GetServerArchiveDrop takes player whichPlayer,string key returns string
        return RequestExtraStringData(27, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // GetServerArchiveEquip,         //读取服务器装备数据
    function DzAPI_Map_GetServerArchiveEquip takes player whichPlayer,string key returns integer
        return RequestExtraIntegerData(26, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_GetPlatformVIP takes player whichPlayer returns integer
        return RequestExtraIntegerData(30, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_IsPlatformVIP takes player whichPlayer returns boolean
        return DzAPI_Map_GetPlatformVIP(whichPlayer) > 0
    endfunction
    function DzAPI_Map_Global_GetStoreString takes string key returns string
        return RequestExtraStringData(36, GetLocalPlayer(), key, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_Global_StoreString takes string key,string value returns nothing
        call RequestExtraBooleanData(37, GetLocalPlayer(), key, value, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_Global_ChangeMsg takes trigger trig returns nothing
        call DzTriggerRegisterSyncData(trig, "DZGAU", true)
    endfunction
    function DzAPI_Map_ServerArchive takes player whichPlayer,string key returns string
        return RequestExtraStringData(38, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_SaveServerArchive takes player whichPlayer,string key,string value returns nothing
        call RequestExtraBooleanData(39, whichPlayer, key, value, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_IsRPGQuickMatch takes nothing returns boolean
        return RequestExtraBooleanData(40, null, null, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_GetMallItemCount takes player whichPlayer,string key returns integer
        return RequestExtraIntegerData(41, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_ConsumeMallItem takes player whichPlayer,string key,integer count returns boolean
        return RequestExtraBooleanData(42, whichPlayer, key, null, false, count, 0, 0)
    endfunction
    function DzAPI_Map_EnablePlatformSettings takes player whichPlayer,integer option,boolean enable returns boolean
        return RequestExtraBooleanData(43, whichPlayer, null, null, enable, option, 0, 0)
    endfunction
    function GetPlayerServerValueSuccess takes player whichPlayer returns boolean
        if ( DzAPI_Map_GetServerValueErrorCode(whichPlayer) == 0 ) then
            return true
        else
            return false
        endif
    endfunction
    function DzAPI_Map_StoreIntegerEX takes player whichPlayer,string key,integer value returns nothing
        set key="I" + key
        call RequestExtraBooleanData(39, whichPlayer, key, I2S(value), false, 0, 0, 0)
        set key=null
        set whichPlayer=null
    endfunction
    function DzAPI_Map_GetStoredIntegerEX takes player whichPlayer,string key returns integer
        local integer value
        set key="I" + key
        set value=S2I(RequestExtraStringData(38, whichPlayer, key, null, false, 0, 0, 0))
        set key=null
        set whichPlayer=null
        return value
    endfunction
    function DzAPI_Map_StoreInteger takes player whichPlayer,string key,integer value returns nothing
        set key="I" + key
        call DzAPI_Map_SaveServerValue(whichPlayer , key , I2S(value))
        set key=null
        set whichPlayer=null
    endfunction
    function DzAPI_Map_GetStoredInteger takes player whichPlayer,string key returns integer
        local integer value
        set key="I" + key
        set value=S2I(DzAPI_Map_GetServerValue(whichPlayer , key))
        set key=null
        set whichPlayer=null
        return value
    endfunction
    function DzAPI_Map_CommentTotalCount1 takes player whichPlayer,integer id returns integer
            return RequestExtraIntegerData(52, whichPlayer, null, null, false, id, 0, 0)
    endfunction
    function DzAPI_Map_StoreReal takes player whichPlayer,string key,real value returns nothing
        set key="R" + key
        call DzAPI_Map_SaveServerValue(whichPlayer , key , R2S(value))
        set key=null
        set whichPlayer=null
    endfunction
    function DzAPI_Map_GetStoredReal takes player whichPlayer,string key returns real
        local real value
        set key="R" + key
        set value=S2R(DzAPI_Map_GetServerValue(whichPlayer , key))
        set key=null
        set whichPlayer=null
        return value
    endfunction
    function DzAPI_Map_StoreBoolean takes player whichPlayer,string key,boolean value returns nothing
        set key="B" + key
        if ( value ) then
            call DzAPI_Map_SaveServerValue(whichPlayer , key , "1")
        else
            call DzAPI_Map_SaveServerValue(whichPlayer , key , "0")
        endif
        set key=null
        set whichPlayer=null
    endfunction
    function DzAPI_Map_GetStoredBoolean takes player whichPlayer,string key returns boolean
        local boolean value
        set key="B" + key
        set key=DzAPI_Map_GetServerValue(whichPlayer , key)
        if ( key == "1" ) then
            set value=true
        else
            set value=false
        endif
        set key=null
        set whichPlayer=null
        return value
    endfunction
    function DzAPI_Map_StoreString takes player whichPlayer,string key,string value returns nothing
        set key="S" + key
        call DzAPI_Map_SaveServerValue(whichPlayer , key , value)
        set key=null
        set whichPlayer=null
    endfunction
    function DzAPI_Map_GetStoredString takes player whichPlayer,string key returns string
        return DzAPI_Map_GetServerValue(whichPlayer , "S" + key)
    endfunction
    function DzAPI_Map_StoreStringEX takes player whichPlayer,string key,string value returns nothing
        set key="S" + key
        call RequestExtraBooleanData(39, whichPlayer, key, value, false, 0, 0, 0)
        set key=null
        set whichPlayer=null
    endfunction
    function DzAPI_Map_GetStoredStringEX takes player whichPlayer,string key returns string
        return RequestExtraStringData(38, whichPlayer, "S" + key, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_GetStoredUnitType takes player whichPlayer,string key returns integer
        local integer value
        set key="I" + key
        set value=S2I(DzAPI_Map_GetServerValue(whichPlayer , key))
        set key=null
        set whichPlayer=null
        return value
    endfunction
    function DzAPI_Map_GetStoredAbilityId takes player whichPlayer,string key returns integer
        local integer value
        set key="I" + key
        set value=S2I(DzAPI_Map_GetServerValue(whichPlayer , key))
        set key=null
        set whichPlayer=null
        return value
    endfunction
    function DzAPI_Map_FlushStoredMission takes player whichPlayer,string key returns nothing
        call DzAPI_Map_SaveServerValue(whichPlayer , key , null)
        set key=null
        set whichPlayer=null
    endfunction
    function DzAPI_Map_Ladder_SubmitIntegerData takes player whichPlayer,string key,integer value returns nothing
        call DzAPI_Map_Ladder_SetStat(whichPlayer , key , I2S(value))
    endfunction
    function DzAPI_Map_Stat_SubmitUnitIdData takes player whichPlayer,string key,integer value returns nothing
        if ( value == 0 ) then
            //call DzAPI_Map_Ladder_SetStat(whichPlayer,key,"0")
        else
            call DzAPI_Map_Ladder_SetStat(whichPlayer , key , I2S(value))
        endif
    endfunction
    function DzAPI_Map_Stat_SubmitUnitData takes player whichPlayer,string key,unit value returns nothing
        call DzAPI_Map_Stat_SubmitUnitIdData(whichPlayer , key , GetUnitTypeId(value))
    endfunction
    function DzAPI_Map_Ladder_SubmitAblityIdData takes player whichPlayer,string key,integer value returns nothing
        if ( value == 0 ) then
            //call DzAPI_Map_Ladder_SetStat(whichPlayer,key,"0")
        else
            call DzAPI_Map_Ladder_SetStat(whichPlayer , key , I2S(value))
        endif
    endfunction
    function DzAPI_Map_Ladder_SubmitItemIdData takes player whichPlayer,string key,integer value returns nothing
        local string S
        if ( value == 0 ) then
            set S="0"
        else
            set S=I2S(value)
            call DzAPI_Map_Ladder_SetStat(whichPlayer , key , S)
        endif
        //call DzAPI_Map_Ladder_SetStat(whichPlayer,key,S)
        set S=null
        set whichPlayer=null
    endfunction
    function DzAPI_Map_Ladder_SubmitItemData takes player whichPlayer,string key,item value returns nothing
        call DzAPI_Map_Ladder_SubmitItemIdData(whichPlayer , key , GetItemTypeId(value))
    endfunction
    function DzAPI_Map_Ladder_SubmitBooleanData takes player whichPlayer,string key,boolean value returns nothing
        if ( value ) then
            call DzAPI_Map_Ladder_SetStat(whichPlayer , key , "1")
        else
            call DzAPI_Map_Ladder_SetStat(whichPlayer , key , "0")
        endif
    endfunction
    function DzAPI_Map_Ladder_SubmitTitle takes player whichPlayer,string value returns nothing
        call DzAPI_Map_Ladder_SetStat(whichPlayer , value , "1")
    endfunction
    function DzAPI_Map_Ladder_SubmitPlayerRank takes player whichPlayer,integer value returns nothing
        call DzAPI_Map_Ladder_SetPlayerStat(whichPlayer , "RankIndex" , I2S(value))
    endfunction
    function DzAPI_Map_Ladder_SubmitPlayerExtraExp takes player whichPlayer,integer value returns nothing
        call DzAPI_Map_Ladder_SetStat(whichPlayer , "ExtraExp" , I2S(value))
    endfunction
    function DzAPI_Map_PlayedGames takes player whichPlayer returns integer
        return RequestExtraIntegerData(45, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_CommentCount takes player whichPlayer returns integer
        return RequestExtraIntegerData(46, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_FriendCount takes player whichPlayer returns integer
        return RequestExtraIntegerData(47, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_IsConnoisseur takes player whichPlayer returns boolean
        return RequestExtraBooleanData(48, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_IsAuthor takes player whichPlayer returns boolean
        return RequestExtraBooleanData(50, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_CommentTotalCount takes nothing returns integer
        return RequestExtraIntegerData(51, null, null, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_Statistics takes player whichPlayer,string eventKey,string eventType,integer value returns nothing
        call RequestExtraBooleanData(34, whichPlayer, eventKey, eventType, false, value, 0, 0)
    endfunction
    function DzAPI_Map_Returns takes player whichPlayer,integer label returns boolean
        return RequestExtraBooleanData(53, whichPlayer, null, null, false, label, 0, 0)
    endfunction
    function DzAPI_Map_ContinuousCount takes player whichPlayer,integer id returns integer
        return RequestExtraIntegerData(54, whichPlayer, null, null, false, id, 0, 0)
    endfunction
    // IsPlayer,                      //是否为玩家
    function DzAPI_Map_IsPlayer takes player whichPlayer returns boolean
        return RequestExtraBooleanData(55, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // MapsTotalPlayed,               //所有地图的总游戏时长
    function DzAPI_Map_MapsTotalPlayed takes player whichPlayer returns integer
        return RequestExtraIntegerData(56, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // MapsLevel,                    //指定地图的地图等级
    function DzAPI_Map_MapsLevel takes player whichPlayer,integer mapId returns integer
        return RequestExtraIntegerData(57, whichPlayer, null, null, false, mapId, 0, 0)
    endfunction
    // MapsConsumeGold,              //所有地图的金币消耗
    function DzAPI_Map_MapsConsumeGold takes player whichPlayer,integer mapId returns integer
        return RequestExtraIntegerData(58, whichPlayer, null, null, false, mapId, 0, 0)
    endfunction
    // MapsConsumeLumber,            //所有地图的木材消耗
    function DzAPI_Map_MapsConsumeLumber takes player whichPlayer,integer mapId returns integer
        return RequestExtraIntegerData(59, whichPlayer, null, null, false, mapId, 0, 0)
    endfunction
    // MapsConsumeLv1,               //消费 1-199
    function DzAPI_Map_MapsConsumeLv1 takes player whichPlayer,integer mapId returns boolean
        return RequestExtraBooleanData(60, whichPlayer, null, null, false, mapId, 0, 0)
    endfunction
    // MapsConsumeLv2,               //消费 200-499
    function DzAPI_Map_MapsConsumeLv2 takes player whichPlayer,integer mapId returns boolean
        return RequestExtraBooleanData(61, whichPlayer, null, null, false, mapId, 0, 0)
    endfunction
    // MapsConsumeLv3,               //消费 500~999
    function DzAPI_Map_MapsConsumeLv3 takes player whichPlayer,integer mapId returns boolean
        return RequestExtraBooleanData(62, whichPlayer, null, null, false, mapId, 0, 0)
    endfunction
    // MapsConsumeLv4,               //消费 1000+
    function DzAPI_Map_MapsConsumeLv4 takes player whichPlayer,integer mapId returns boolean
        return RequestExtraBooleanData(63, whichPlayer, null, null, false, mapId, 0, 0)
    endfunction
    // IsPlayerUsingSkin,            //检查是否装备着皮肤（skinType：头像=1、边框=2、称号=3、底纹=4）
    function DzAPI_Map_IsPlayerUsingSkin takes player whichPlayer,integer skinType,integer id returns boolean
        return RequestExtraBooleanData(64, whichPlayer, null, null, false, skinType, id, 0)
    endfunction
    //获取论坛数据（0=累计获得赞数，1=精华帖数量，2=发表回复次数，3=收到的欢乐数，4=是否发过贴子，5=是否版主，6=主题数量）
    function DzAPI_Map_GetForumData takes player whichPlayer,integer whichData returns integer
        return RequestExtraIntegerData(65, whichPlayer, null, null, false, whichData, 0, 0)
    endfunction
    // PlayerFlags,                   //玩家标记 label（1=曾经是平台回流用户，2=当前是平台回流用户，4=曾经是地图回流用户，8=当前是地图回流用户，16=地图是否被玩家收藏）
    function DzAPI_Map_PlayerFlags takes player whichPlayer,integer label returns boolean
        return RequestExtraBooleanData(53, whichPlayer, null, null, false, label, 0, 0)
    endfunction
    // GetLotteryUsedCount, // 获取宝箱抽取次数
    function DzAPI_Map_GetLotteryUsedCountEx takes player whichPlayer,integer index returns integer
        return RequestExtraIntegerData(68, whichPlayer, null, null, false, index, 0, 0)
    endfunction
    function DzAPI_Map_GetLotteryUsedCount takes player whichPlayer returns integer
        return DzAPI_Map_GetLotteryUsedCountEx(whichPlayer , 0) + DzAPI_Map_GetLotteryUsedCountEx(whichPlayer , 1) + DzAPI_Map_GetLotteryUsedCountEx(whichPlayer , 2)
    endfunction
    function DzAPI_Map_OpenMall takes player whichPlayer,string whichkey returns boolean
        return RequestExtraBooleanData(66, whichPlayer, whichkey, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_GameResult_CommitData takes player whichPlayer,string key,string value returns nothing
        call RequestExtraIntegerData(69, whichPlayer, key, value, false, 0, 0, 0)
    endfunction
    //游戏结算
    function DzAPI_Map_GameResult_CommitTitle takes player whichPlayer,string value returns nothing
        call DzAPI_Map_GameResult_CommitData(whichPlayer , value , "1")
        set whichPlayer=null
        set value=null
    endfunction
    function DzAPI_Map_GameResult_CommitPlayerRank takes player whichPlayer,integer value returns nothing
        call DzAPI_Map_GameResult_CommitData(whichPlayer , "RankIndex" , I2S(value))
        set whichPlayer=null
        set value=0
    endfunction
    function DzAPI_Map_GameResult_CommitGameMode takes string value returns nothing
        call DzAPI_Map_GameResult_CommitData(GetLocalPlayer() , "InnerGameMode" , value)
        set value=null
    endfunction
    function DzAPI_Map_GameResult_CommitGameResult takes player whichPlayer,integer value returns nothing
        call DzAPI_Map_GameResult_CommitData(whichPlayer , "GameResult" , I2S(value))
        set whichPlayer=null
    endfunction
    function DzAPI_Map_GameResult_CommitGameResultNoEnd takes player whichPlayer,integer value returns nothing
        call DzAPI_Map_GameResult_CommitData(whichPlayer , "GameResultNoEnd" , I2S(value))
        set whichPlayer=null
    endfunction
    // GetSinceLastPlayedSeconds, // 获取距最后一次游戏的秒数
    function DzAPI_Map_GetSinceLastPlayedSeconds takes player whichPlayer returns integer
        return RequestExtraIntegerData(70, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    //游戏内快速购买
    function DzAPI_Map_QuickBuy takes player whichPlayer,string key,integer count,integer seconds returns boolean
        return RequestExtraBooleanData(72, whichPlayer, key, null, false, count, seconds, 0)
    endfunction
    //取消快速购买
    function DzAPI_Map_CancelQuickBuy takes player whichPlayer returns boolean
        return RequestExtraBooleanData(73, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // 是否地图测试服
    function DzAPI_Map_IsMapTest takes nothing returns boolean
        return RequestExtraBooleanData(74, null, null, null, false, 0, 0, 0)
    endfunction
    //判断是加载成功某个玩家的道具
    function DzAPI_Map_PlayerLoadedItems takes player whichPlayer returns boolean
        return RequestExtraBooleanData(77, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    function DzAPI_Map_CustomRankCount takes integer id returns integer
        return RequestExtraIntegerData(78, null, null, null, false, id, 0, 0)
    endfunction
    // CustomRankPlayerName            // 获取排行榜上指定排名的用户名称
    function DzAPI_Map_CustomRankPlayerName takes integer id,integer ranking returns string
        return RequestExtraStringData(79, null, null, null, false, id, ranking, 0)
    endfunction
    // CustomRankPlayerValue           // 获取排行榜上指定排名的值
    function DzAPI_Map_CustomRankValue takes integer id,integer ranking returns integer
        return RequestExtraIntegerData(80, null, null, null, false, id, ranking, 0)
    endfunction
    //获取玩家在KK平台的完整昵称（基础昵称#编号）
    function DzAPI_Map_GetPlayerUserName takes player whichPlayer returns string
        return RequestExtraStringData(81, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // GetServerValueLimitLeft,   // 获取服务器存档限制余额
    function KKApiGetServerValueLimitLeft takes player whichPlayer,string key returns integer
        return RequestExtraIntegerData(82, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // RequestBackendLogic,       //请求后端逻辑生成
    function KKApiRequestBackendLogic takes player whichPlayer,string key,string groupkey returns boolean
        return RequestExtraBooleanData(83, whichPlayer, key, groupkey, false, 0, 0, 0)
    endfunction
    // CheckBackendLogicExists,   // 获取后端逻辑生成结果 是否存在
    function KKApiCheckBackendLogicExists takes player whichPlayer,string key returns boolean
        return RequestExtraBooleanData(84, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // GetBackendLogicIntResult,  // 获取后端逻辑生成结果 整型
    function KKApiGetBackendLogicIntResult takes player whichPlayer,string key returns integer
        return RequestExtraIntegerData(85, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // GetBackendLogicStrResult,  // 获取后端逻辑生成结果 字符串
    function KKApiGetBackendLogicStrResult takes player whichPlayer,string key returns string
        return RequestExtraStringData(86, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // GetBackendLogicUpdateTime, // 获取后端逻辑生成时间
    function KKApiGetBackendLogicUpdateTime takes player whichPlayer,string key returns integer
        return RequestExtraIntegerData(87, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // GetBackendLogicGroup,      // 获取后端逻辑生成组
    function KKApiGetBackendLogicGroup takes player whichPlayer,string key returns string
        return RequestExtraStringData(88, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // RemoveBackendLogicResult,  // 删除后端逻辑生成结果
    function KKApiRemoveBackendLogicResult takes player whichPlayer,string key returns boolean
        return RequestExtraBooleanData(89, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // 获取随机存档剩余次数
    function KKApiRandomSaveGameCount takes player whichPlayer,string groupkey returns integer
        return RequestExtraIntegerData(101, whichPlayer, groupkey, null, false, 0, 0, 0)
    endfunction
    function KKApiTriggerRegisterBackendLogicUpdata takes trigger trig returns nothing
        call DzTriggerRegisterSyncData(trig, "DZBLU", true)
    endfunction
    function KKApiTriggerRegisterBackendLogicDelete takes trigger trig returns nothing
        call DzTriggerRegisterSyncData(trig, "DZBLD", true)
    endfunction
    function KKApiGetSyncBackendLogic takes nothing returns string
        return DzGetTriggerSyncData()
    endfunction
    function KKApiIsGameMode takes nothing returns boolean
        return RequestExtraBooleanData(90, null, null, null, false, 0, 0, 0)
    endfunction
    function KKApiInitializeGameKey takes player whichPlayer,integer setIndex,string k,string data returns boolean
        return RequestExtraBooleanData(91, whichPlayer, "[{\"name\":\"" + data + "\",\"key\":\"" + k + "\"}]", null, false, setIndex, 0, 0)
    endfunction
    function KKApiPlayerGUID takes player whichPlayer returns string
        return RequestExtraStringData(93, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    function KKApiIsTaskInProgress takes player whichPlayer,integer setIndex,integer taskstat returns boolean
        return RequestExtraIntegerData(94, whichPlayer, null, null, false, setIndex, 0, 0) == taskstat
    endfunction
    function KKApiQueryTaskCurrentProgress takes player whichPlayer,integer setIndex returns integer
        return RequestExtraIntegerData(95, whichPlayer, null, null, false, setIndex, 0, 0)
    endfunction
    function KKApiQueryTaskTotalProgress takes player whichPlayer,integer setIndex returns integer
        return RequestExtraIntegerData(96, whichPlayer, null, null, false, setIndex, 0, 0)
    endfunction
    // IsAchievementCompleted,  // 获取玩家成就是否完成
    function KKApiIsAchievementCompleted takes player whichPlayer,string id returns boolean
        return RequestExtraBooleanData(98, whichPlayer, id, null, false, 0, 0, 0)
    endfunction
    // AchievementPoints,  // 获取玩家地图成就点数
    function KKApiAchievementPoints takes player whichPlayer returns integer
        return RequestExtraIntegerData(99, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // 判断游戏时长是否满足条件 minHours: 最小小时数，maxHours: 最大小时数，0表示不限制
    function KKApiPlayedTime takes player whichPlayer,integer minHours,integer maxHours returns boolean
        return RequestExtraBooleanData(100, whichPlayer, null, null, false, minHours, maxHours, 0)
    endfunction
    // BeginBatchSaveArchive,  // 开始批量保存存档
    function KKApiBeginBatchSaveArchive takes player whichPlayer returns boolean
        return RequestExtraBooleanData(102, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // AddBatchSaveArchive,    // 添加批量保存存档条目
    function KKApiAddBatchSaveArchive takes player whichPlayer,string key,string value,boolean caseInsensitive returns boolean
        return RequestExtraBooleanData(103, whichPlayer, key, value, caseInsensitive, 0, 0, 0)
    endfunction
    // EndBatchSaveArchive,    // 结束批量保存存档
    function KKApiEndBatchSaveArchive takes player whichPlayer,boolean abandon returns boolean
        return RequestExtraBooleanData(104, whichPlayer, null, null, abandon, 0, 0, 0)
    endfunction
    
    function KKApiAddBatchSaveArchiveInteger takes player whichPlayer,string key,integer value returns nothing
        set key="I" + key
        call KKApiAddBatchSaveArchive(whichPlayer , key , I2S(value) , false)
        set key=null
        set whichPlayer=null
    endfunction
    function KKApiAddBatchSaveArchiveReal takes player whichPlayer,string key,real value returns nothing
        set key="R" + key
        call KKApiAddBatchSaveArchive(whichPlayer , key , R2S(value) , false)
        set key=null
        set whichPlayer=null
    endfunction
    function KKApiAddBatchSaveArchiveBoolean takes player whichPlayer,string key,boolean value returns nothing
        set key="B" + key
        if ( value ) then
            call KKApiAddBatchSaveArchive(whichPlayer , key , "1" , false)
        else
            call KKApiAddBatchSaveArchive(whichPlayer , key , "0" , false)
        endif
        set key=null
        set whichPlayer=null
    endfunction
    function KKApiAddBatchSaveArchiveString takes player whichPlayer,string key,string value returns nothing
        set key="S" + key
        call KKApiAddBatchSaveArchive(whichPlayer , key , value , false)
        set key=null
        set whichPlayer=null
    endfunction
    //天梯投降
    function KKApiTriggerRegisterLadderSurrender takes trigger trig returns nothing
        call DzTriggerRegisterSyncData(trig, "DZSR", true)
    endfunction
    function KKApiGetLadderSurrenderTeamId takes nothing returns integer
        return S2I(DzGetTriggerSyncData())
    endfunction
    // GetGuildLevel,          // 获取公会等级
    function KKApiGetGuildLevel takes player whichPlayer returns integer
        return RequestExtraIntegerData(106, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    //宠物探险次数
    function KKApiMapExplorationNum takes player whichPlayer returns integer
        return RequestExtraIntegerData(107, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    //宠物探险时间
    function KKApiMapExplorationTime takes player whichPlayer returns integer
        return RequestExtraIntegerData(108, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    //测试大厅预约人数
    function KKApiMapOrderNum takes nothing returns integer
        return RequestExtraIntegerData(109, null, null, null, false, 0, 0, 0)
    endfunction
    // 发送云脚本数据
    function KKApiMlScriptEvent takes player whichPlayer,string eventName,string payload returns boolean
        return RequestExtraBooleanData(1009, whichPlayer, eventName, payload, false, 0, 0, 0)
    endfunction
    // 获取商城道具最后变动的数量（新增/删除）
    function KKApiGetMallItemUpdateCount takes player whichPlayer,string key returns integer
        return RequestExtraIntegerData(110, whichPlayer, key, null, false, 0, 0, 0)
    endfunction
    // GetMapVersion,          // 获取地图版本号
    function KKApiGetMapVersion takes nothing returns string
        return RequestExtraStringData(111, null, null, null, false, 0, 0, 0)
    endfunction
    // 获取赛事RPG地图游戏模式
    function KKApiGetCompetitionGameMode takes nothing returns string
        return RequestExtraStringData(112, null, null, null, false, 0, 0, 0)
    endfunction
    // DayRounds,              // 获取当天游戏局数
    function KKApiDayRounds takes player whichPlayer returns integer
        return RequestExtraIntegerData(113, whichPlayer, null, null, false, 0, 0, 0)
    endfunction
    // ConsumeLevel
    function KKApiConsumeLevel takes player whichPlayer,integer mapId returns integer
        return RequestExtraIntegerData(115, whichPlayer, null, null, false, mapId, 0, 0)
    endfunction
    //  IsPinned, // 获取是否已经置顶
    function KKApiIsPinned takes player whichPlayer returns boolean
        return RequestExtraBooleanData(117, whichPlayer, null, null, false, 0, 0, 0)
    endfunction

//library DzAPI ends
//library EquipmentData:
    // ============================================================================
    // 辅助函数：添加装备
    // ============================================================================
    function AddEquipment takes integer item_type_id,string name,integer slot,integer quality,integer attack,integer spell_power,integer health,integer armor,integer resistance,integer move_speed,integer crit_rate,integer crit_damage,integer cooldown,integer range_val,integer cost,integer haste,integer element,integer element_value,integer special_type,integer special_value,integer dungeon,integer chance,integer material_type,integer material_amount,integer set_id returns nothing
        local integer id
        set id=udg_equip_count + 1
        set udg_equip_count=id
        set udg_equip_item_type_id[id]=item_type_id
        set udg_equip_name[id]=name
        set udg_equip_slot[id]=slot
        set udg_equip_quality[id]=quality
        set udg_equip_attack[id]=attack
        set udg_equip_spell_power[id]=spell_power
        set udg_equip_health[id]=health
        set udg_equip_armor[id]=armor
        set udg_equip_resistance[id]=resistance
        set udg_equip_move_speed[id]=move_speed
        set udg_equip_crit_rate[id]=crit_rate
        set udg_equip_crit_damage[id]=crit_damage
        set udg_equip_cooldown[id]=cooldown
        set udg_equip_range[id]=range_val
        set udg_equip_cost[id]=cost
        set udg_equip_haste[id]=haste
        set udg_equip_element[id]=element
        set udg_equip_element_value[id]=element_value
        set udg_equip_special_type[id]=special_type
        set udg_equip_special_value[id]=special_value
        set udg_equip_drop_dungeon[id]=dungeon
        set udg_equip_drop_chance[id]=chance
        set udg_equip_craft_material_type[id]=material_type
        set udg_equip_craft_amount[id]=material_amount
        set udg_equip_set_id[id]=set_id
    endfunction
    // ============================================================================
    // 验证装备数据完整性
    // ============================================================================
    function EquipmentData_Validate takes nothing returns boolean
        local integer i= 1
        local boolean valid= true
        call DisplayTextToPlayer(Player(0), 0, 0, "装备数据开始验证！")
        loop
            exitwhen i > udg_equip_count
            if udg_equip_item_type_id[i] == 0 then
                call DisplayTextToPlayer(Player(0), 0, 0, "装备ID " + I2S(i) + " 缺少物品类型ID")
                set valid=false
            else
                call DisplayTextToPlayer(Player(0), 0, 0, "装备ID " + I2S(i) + " 物品类型ID: " + I2S(udg_equip_item_type_id[i]))
            endif
            set i=i + 1
        endloop
        if valid then
            call DisplayTextToPlayer(Player(0), 0, 0, "装备数据验证通过1")
        else
            call DisplayTextToPlayer(Player(0), 0, 0, "装备数据验证失败1")
        endif
        return valid
    endfunction
    // ============================================================================
    // 数据初始化函数
    // ============================================================================
    function InitEquipmentData takes nothing returns nothing
        local integer i
        // 初始化缓存
        set udg_equip_cache_size=0
        // ========================================================================
        // 初始化元素前缀
        // ========================================================================
        set ELEMENT_PREFIX[ELEMENT_NONE]=""
        set ELEMENT_PREFIX[ELEMENT_FIRE]="烈火"
        set ELEMENT_PREFIX[ELEMENT_ICE]="寒冰"
        set ELEMENT_PREFIX[ELEMENT_THUNDER]="奔雷"
        set ELEMENT_PREFIX[ELEMENT_POISON]="剧毒"
        set ELEMENT_NAME[ELEMENT_NONE]="无"
        set ELEMENT_NAME[ELEMENT_FIRE]="火"
        set ELEMENT_NAME[ELEMENT_ICE]="冰"
        set ELEMENT_NAME[ELEMENT_THUNDER]="雷"
        set ELEMENT_NAME[ELEMENT_POISON]="毒"
        // ========================================================================
        // 初始化槽位名称
        // ========================================================================
        set EQUIP_SLOT_NAME[1]="武器"
        set EQUIP_SLOT_NAME[2]="盔甲"
        set EQUIP_SLOT_NAME[3]="头盔"
        set EQUIP_SLOT_NAME[4]="护腿"
        set EQUIP_SLOT_NAME[5]="饰品"
        set EQUIP_SLOT_NAME[6]="项链"
        // ========================================================================
        // 初始化品质名称
        // ========================================================================
        set EQUIP_QUALITY_NAME[1]="凡品"
        set EQUIP_QUALITY_NAME[2]="利器"
        set EQUIP_QUALITY_NAME[3]="宝刃"
        set EQUIP_QUALITY_NAME[4]="神兵"
        set EQUIP_QUALITY_NAME[5]="传说神兵"
        // ========================================================================
        // 添加主武器数据（槽位1）- 20件
        // ========================================================================
        // 凡品武器（1-4）
        // 铁剑: 武力18
        call AddEquipment('I200' , "铁剑" , 1 , 1 , 18 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 朴刀: 武力18
        call AddEquipment('I201' , "朴刀" , 1 , 1 , 18 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 木棍: 武力15
        call AddEquipment('I202' , "木棍" , 1 , 1 , 15 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 竹杖: 法强15
        call AddEquipment('I203' , "竹杖" , 1 , 1 , 0 , 15 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 利器武器（5-8）
        // 青锋剑: 武力30
        call AddEquipment('I204' , "青锋剑" , 1 , 2 , 30 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 雪花镗: 武力30
        call AddEquipment('I205' , "雪花镗" , 1 , 2 , 30 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 紫金棍: 武力27
        call AddEquipment('I206' , "紫金棍" , 1 , 2 , 27 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 八卦杖: 法强27
        call AddEquipment('I207' , "八卦杖" , 1 , 2 , 0 , 27 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 宝刃武器（9-12）
        // 碧水剑: 武力52
        call AddEquipment('I208' , "碧水剑" , 1 , 3 , 52 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 鬼头刀: 武力52
        call AddEquipment('I209' , "鬼头刀" , 1 , 3 , 52 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 风雷棍: 武力48
        call AddEquipment('I20A' , "风雷棍" , 1 , 3 , 48 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 玄铁杖: 法强48
        call AddEquipment('I20B' , "玄铁杖" , 1 , 3 , 0 , 48 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 神兵武器（13-16）
        // 倚天剑: 武力90, 会心5%
        call AddEquipment('I20C' , "倚天剑" , 1 , 4 , 90 , 0 , 0 , 0 , 0 , 0 , 5 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 4 , 4 , 4)
        // 屠龙刀: 武力90, 要害10%
        call AddEquipment('I20D' , "屠龙刀" , 1 , 4 , 90 , 0 , 0 , 0 , 0 , 0 , 0 , 10 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 4 , 4 , 4)
        // 打狗棒: 武力85
        call AddEquipment('I20E' , "打狗棒" , 1 , 4 , 85 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 4 , 4 , 4)
        // 圣火令: 法强85, 火30
        call AddEquipment('I20F' , "圣火令" , 1 , 4 , 0 , 85 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 30 , 0 , 0 , 0 , 0 , 4 , 4 , 4)
        // 传说神兵武器（17-20）
        // 轩辕剑: 武力135, 会心10%, 雷50
        call AddEquipment('I20G' , "轩辕剑" , 1 , 5 , 135 , 0 , 0 , 0 , 0 , 0 , 10 , 0 , 0 , 0 , 0 , 0 , 3 , 50 , 0 , 0 , 0 , 0 , 5 , 5 , 5)
        // 屠龙宝刀: 武力135, 要害15%, 火50
        call AddEquipment('I20H' , "屠龙宝刀" , 1 , 5 , 135 , 0 , 0 , 0 , 0 , 0 , 0 , 15 , 0 , 0 , 0 , 0 , 1 , 50 , 0 , 0 , 0 , 0 , 5 , 5 , 5)
        // 如意金箍棒: 武力145, 雷40, 攻击+20%(Type 16)
        call AddEquipment('I20I' , "如意金箍棒" , 1 , 5 , 145 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 40 , 16 , 20 , 0 , 0 , 5 , 5 , 5)
        // 乾坤袋: 法强135, 冰50, 范围+15%
        call AddEquipment('I20J' , "乾坤袋" , 1 , 5 , 0 , 135 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 15 , 0 , 0 , 2 , 50 , 0 , 0 , 0 , 0 , 5 , 5 , 5)
        // ========================================================================
        // 添加盔甲数据（槽位2）- 20件
        // ========================================================================
        // 凡品盔甲（21-24）
        // 布衣: 气血60, 护体18
        call AddEquipment('I20K' , "布衣" , 2 , 1 , 0 , 0 , 60 , 18 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 皮甲: 气血70, 护体22
        call AddEquipment('I20L' , "皮甲" , 2 , 1 , 0 , 0 , 70 , 22 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 短衫: 气血55, 护体15
        call AddEquipment('I20M' , "短衫" , 2 , 1 , 0 , 0 , 55 , 15 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 麻袍: 气血60, 护体17
        call AddEquipment('I20N' , "麻袍" , 2 , 1 , 0 , 0 , 60 , 17 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 利器盔甲（25-28）
        // 铁甲: 气血140, 护体42
        call AddEquipment('I20O' , "铁甲" , 2 , 2 , 0 , 0 , 140 , 42 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 战袍: 气血120, 护体38
        call AddEquipment('I20P' , "战袍" , 2 , 2 , 0 , 0 , 120 , 38 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 皮袍: 气血112, 护体35
        call AddEquipment('I20Q' , "皮袍" , 2 , 2 , 0 , 0 , 112 , 35 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 锦衣: 气血125, 护体40
        call AddEquipment('I20R' , "锦衣" , 2 , 2 , 0 , 0 , 125 , 40 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 宝刃盔甲（29-32）
        // 锁子甲: 气血250, 护体88
        call AddEquipment('I20S' , "锁子甲" , 2 , 3 , 0 , 0 , 250 , 88 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 金丝甲: 气血225, 护体98
        call AddEquipment('I20T' , "金丝甲" , 2 , 3 , 0 , 0 , 225 , 98 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 鳞甲: 气血240, 护体92
        call AddEquipment('I20U' , "鳞甲" , 2 , 3 , 0 , 0 , 240 , 92 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 龙吟甲: 气血258, 护体95
        call AddEquipment('I20V' , "龙吟甲" , 2 , 3 , 0 , 0 , 258 , 95 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 神兵盔甲（33-36）
        // 龙鳞甲: 气血400, 护体135, 减伤10%(Type 1)
        call AddEquipment('I20W' , "龙鳞甲" , 2 , 4 , 0 , 0 , 400 , 135 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 10 , 0 , 0 , 4 , 4 , 4)
        // 天蚕宝甲: 气血430, 护体125, 恢复5%(Type 2)
        call AddEquipment('I20X' , "天蚕宝甲" , 2 , 4 , 0 , 0 , 430 , 125 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 5 , 0 , 0 , 4 , 4 , 4)
        // 紫霞甲: 气血400, 护体130, 内力30(Type 3)
        call AddEquipment('I20Y' , "紫霞甲" , 2 , 4 , 0 , 0 , 400 , 130 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 30 , 0 , 0 , 4 , 4 , 4)
        // 金钟罩: 气血380, 护体145, 减伤8%(Type 1)
        call AddEquipment('I20Z' , "金钟罩" , 2 , 4 , 0 , 0 , 380 , 145 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 8 , 0 , 0 , 4 , 4 , 4)
        // 传说神兵盔甲（37-40）
        // 凤凰神甲: 气血625, 护体200, 火40, 浴火重生(Type 99)
        call AddEquipment('I210' , "凤凰神甲" , 2 , 5 , 0 , 0 , 625 , 200 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 40 , 99 , 1 , 0 , 0 , 5 , 5 , 5)
        // 玄武圣甲: 气血675, 护体225, 冰40, 减伤15%(Type 1)
        call AddEquipment('I211' , "玄武圣甲" , 2 , 5 , 0 , 0 , 675 , 225 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 40 , 1 , 15 , 0 , 0 , 5 , 5 , 5)
        // 白虎战甲: 气血650, 护体210, 雷35, 攻击+12%(Type 16)
        call AddEquipment('I212' , "白虎战甲" , 2 , 5 , 0 , 0 , 650 , 210 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 35 , 16 , 12 , 0 , 0 , 5 , 5 , 5)
        // 朱雀羽衣: 气血620, 护体195, 火50, 移动+10%(Type 11)
        call AddEquipment('I213' , "朱雀羽衣" , 2 , 5 , 0 , 0 , 620 , 195 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 50 , 11 , 10 , 0 , 0 , 5 , 5 , 5)
        // ========================================================================
        // 添加头盔数据（槽位3）- 20件
        // ========================================================================
        // 凡品头盔（41-44）
        // 布巾: 气血40, 抗性12
        call AddEquipment('I214' , "布巾" , 3 , 1 , 0 , 0 , 40 , 0 , 12 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 皮帽: 气血45, 抗性15
        call AddEquipment('I215' , "皮帽" , 3 , 1 , 0 , 0 , 45 , 0 , 15 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 斗笠: 气血36, 抗性12
        call AddEquipment('I216' , "斗笠" , 3 , 1 , 0 , 0 , 36 , 0 , 12 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 纶巾: 气血40, 抗性13
        call AddEquipment('I217' , "纶巾" , 3 , 1 , 0 , 0 , 40 , 0 , 13 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 利器头盔（45-48）
        // 铁盔: 气血102, 抗性42
        call AddEquipment('I218' , "铁盔" , 3 , 2 , 0 , 0 , 102 , 0 , 42 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 道冠: 气血88, 抗性48
        call AddEquipment('I219' , "道冠" , 3 , 2 , 0 , 0 , 88 , 0 , 48 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 皮盔: 气血95, 抗性40
        call AddEquipment('I21A' , "皮盔" , 3 , 2 , 0 , 0 , 95 , 0 , 40 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 银冠: 气血92, 抗性45
        call AddEquipment('I21B' , "银冠" , 3 , 2 , 0 , 0 , 92 , 0 , 45 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 宝刃头盔（49-52）
        // 银冠(史诗): 气血175, 抗性95
        call AddEquipment('I21C' , "银冠" , 3 , 3 , 0 , 0 , 175 , 0 , 95 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 金盔: 气血185, 抗性102
        call AddEquipment('I21D' , "金盔" , 3 , 3 , 0 , 0 , 185 , 0 , 102 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 铜翅冠: 气血168, 抗性90
        call AddEquipment('I21E' , "铜翅冠" , 3 , 3 , 0 , 0 , 168 , 0 , 90 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 紫金冠(史诗): 气血180, 抗性98
        call AddEquipment('I21F' , "紫金冠" , 3 , 3 , 0 , 0 , 180 , 0 , 98 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 神兵头盔（53-56）
        // 紫金冠(传说): 气血285, 抗性135, 法强20
        call AddEquipment('I21G' , "紫金冠" , 3 , 4 , 0 , 20 , 285 , 0 , 135 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 4 , 4 , 4)
        // 虎头帽: 气血315, 抗性125, 护体15(Type 4)
        call AddEquipment('I21H' , "虎头帽" , 3 , 4 , 0 , 0 , 315 , 0 , 125 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 4 , 15 , 0 , 0 , 4 , 4 , 4)
        // 麒麟冠: 气血300, 抗性140, 法强18
        call AddEquipment('I21I' , "麒麟冠" , 3 , 4 , 0 , 18 , 300 , 0 , 140 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 4 , 4 , 4)
        // 八卦巾: 气血290, 抗性133, 冷却-5%(Type 5)
        call AddEquipment('I21J' , "八卦巾" , 3 , 4 , 0 , 0 , 290 , 0 , 133 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 5 , 5 , 0 , 0 , 4 , 4 , 4)
        // 传说神兵头盔（57-60）
        // 凤冠霞帔: 气血450, 抗性225, 冰30, 治疗+10%(Type 6)
        call AddEquipment('I21K' , "凤冠霞帔" , 3 , 5 , 0 , 0 , 450 , 0 , 225 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 30 , 6 , 10 , 0 , 0 , 5 , 5 , 5)
        // 雷神之盔: 气血470, 抗性240, 雷50, 急速+10%(Type 7)
        call AddEquipment('I21L' , "雷神之盔" , 3 , 5 , 0 , 0 , 470 , 0 , 240 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 50 , 7 , 10 , 0 , 0 , 5 , 5 , 5)
        // 火神冠: 气血435, 抗性218, 火55, 法强25(Type 8)
        call AddEquipment('I21M' , "火神冠" , 3 , 5 , 0 , 0 , 435 , 0 , 218 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 55 , 8 , 25 , 0 , 0 , 5 , 5 , 5)
        // 冰魄头环: 气血455, 抗性230, 冰50, 抗性+20(Type 9)
        call AddEquipment('I21N' , "冰魄头环" , 3 , 5 , 0 , 0 , 455 , 0 , 230 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 50 , 9 , 20 , 0 , 0 , 5 , 5 , 5)
        // ========================================================================
        // 添加护腿数据（槽位4）- 20件
        // ========================================================================
        // 凡品护腿（61-64）
        // 布裤: 气血40, 移动60
        call AddEquipment('I21O' , "布裤" , 4 , 1 , 0 , 0 , 40 , 0 , 0 , 60 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 草鞋: 气血35, 移动70
        call AddEquipment('I21P' , "草鞋" , 4 , 1 , 0 , 0 , 35 , 0 , 0 , 70 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 布绑腿: 气血36, 移动65
        call AddEquipment('I21Q' , "布绑腿" , 4 , 1 , 0 , 0 , 36 , 0 , 0 , 65 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 草履: 气血31, 移动75
        call AddEquipment('I21R' , "草履" , 4 , 1 , 0 , 0 , 31 , 0 , 0 , 75 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 利器护腿（65-68）
        // 皮绑腿: 气血80, 移动120
        call AddEquipment('I21S' , "皮绑腿" , 4 , 2 , 0 , 0 , 80 , 0 , 0 , 120 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 布靴: 气血70, 移动130
        call AddEquipment('I21T' , "布靴" , 4 , 2 , 0 , 0 , 70 , 0 , 0 , 130 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 皮靴: 气血75, 移动125
        call AddEquipment('I21U' , "皮靴" , 4 , 2 , 0 , 0 , 75 , 0 , 0 , 125 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 快靴: 气血67, 移动135
        call AddEquipment('I21V' , "快靴" , 4 , 2 , 0 , 0 , 67 , 0 , 0 , 135 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 宝刃护腿（69-72）
        // 铁护腿: 气血140, 移动230
        call AddEquipment('I21W' , "铁护腿" , 4 , 3 , 0 , 0 , 140 , 0 , 0 , 230 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 快靴(史诗): 气血120, 移动250
        call AddEquipment('I21X' , "快靴" , 4 , 3 , 0 , 0 , 120 , 0 , 0 , 250 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 铜护腿: 气血130, 移动235
        call AddEquipment('I21Y' , "铜护腿" , 4 , 3 , 0 , 0 , 130 , 0 , 0 , 235 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 疾风靴: 气血115, 移动260
        call AddEquipment('I21Z' , "疾风靴" , 4 , 3 , 0 , 0 , 115 , 0 , 0 , 260 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 神兵护腿（73-76）
        // 凌波靴: 气血210, 移动360, 闪避5%(Type 10)
        call AddEquipment('I220' , "凌波靴" , 4 , 4 , 0 , 0 , 210 , 0 , 0 , 360 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 10 , 5 , 0 , 0 , 4 , 4 , 4)
        // 风火轮: 气血190, 移动385, 速度+10%(Type 11)
        call AddEquipment('I221' , "风火轮" , 4 , 4 , 0 , 0 , 190 , 0 , 0 , 385 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 11 , 10 , 0 , 0 , 4 , 4 , 4)
        // 奔雷靴: 气血200, 移动375, 雷20
        call AddEquipment('I222' , "奔雷靴" , 4 , 4 , 0 , 0 , 200 , 0 , 0 , 375 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 20 , 0 , 0 , 0 , 0 , 4 , 4 , 4)
        // 追星履: 气血195, 移动395, 闪避4%(Type 10)
        call AddEquipment('I223' , "追星履" , 4 , 4 , 0 , 0 , 195 , 0 , 0 , 395 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 10 , 4 , 0 , 0 , 4 , 4 , 4)
        // 传说神兵护腿（77-80）
        // 追风履: 气血350, 移动550, 闪避10%(Type 10)
        call AddEquipment('I224' , "追风履" , 4 , 5 , 0 , 0 , 350 , 0 , 0 , 550 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 10 , 10 , 0 , 0 , 5 , 5 , 5)
        // 登云靴: 气血370, 移动600, 免疫减速(Type 12)
        call AddEquipment('I225' , "登云靴" , 4 , 5 , 0 , 0 , 370 , 0 , 0 , 600 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 12 , 1 , 0 , 0 , 5 , 5 , 5)
        // 逐日靴: 气血355, 移动575, 速度+12%(Type 11)
        call AddEquipment('I226' , "逐日靴" , 4 , 5 , 0 , 0 , 355 , 0 , 0 , 575 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 11 , 12 , 0 , 0 , 5 , 5 , 5)
        // 缩地靴: 气血348, 移动565, 冷却-8%(Type 5)
        call AddEquipment('I227' , "缩地靴" , 4 , 5 , 0 , 0 , 348 , 0 , 0 , 565 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 5 , 8 , 0 , 0 , 5 , 5 , 5)
        // ========================================================================
        // 添加饰品数据（槽位5）- 20件
        // ========================================================================
        // 凡品饰品（81-84）
        // 铜戒: 冷却4%
        call AddEquipment('I228' , "铜戒" , 5 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 4 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 布囊: 消耗4%
        call AddEquipment('I229' , "布囊" , 5 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 4 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 绳结: 范围3%
        call AddEquipment('I22A' , "绳结" , 5 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 木珠: 急速3%
        call AddEquipment('I22B' , "木珠" , 5 , 1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 利器饰品（85-88）
        // 银戒: 冷却7%
        call AddEquipment('I22C' , "银戒" , 5 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 7 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 玉佩: 范围6%, 急速6%
        call AddEquipment('I22D' , "玉佩" , 5 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 6 , 0 , 6 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 皮囊: 冷却7%, 消耗5%
        call AddEquipment('I22E' , "皮囊" , 5 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 7 , 0 , 5 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 铜佩: 冷却6%, 急速7%
        call AddEquipment('I22F' , "铜佩" , 5 , 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 6 , 0 , 0 , 7 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 宝刃饰品（89-92）
        // 金戒: 冷却14%, 消耗12%
        call AddEquipment('I22G' , "金戒" , 5 , 3 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 14 , 0 , 12 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 宝囊: 范围14%, 急速14%
        call AddEquipment('I22H' , "宝囊" , 5 , 3 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 14 , 0 , 14 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 玉环: 冷却13%, 消耗12%
        call AddEquipment('I22I' , "玉环" , 5 , 3 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 13 , 0 , 12 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 丝绦: 范围13%, 急速13%
        call AddEquipment('I22J' , "丝绦" , 5 , 3 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 13 , 0 , 13 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 神兵饰品（93-96）
        // 乾坤戒: 冷却25%, 消耗22%, 法力+30(Type 3)
        call AddEquipment('I22K' , "乾坤戒" , 5 , 4 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 25 , 0 , 22 , 0 , 0 , 0 , 3 , 30 , 0 , 0 , 4 , 4 , 4)
        // 太极佩: 范围25%, 急速25%, 冷却-10%(Type 5)
        call AddEquipment('I22L' , "太极佩" , 5 , 4 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 25 , 0 , 25 , 0 , 0 , 5 , 10 , 0 , 0 , 4 , 4 , 4)
        // 玄元囊: 冷却22%, 消耗20%, 内力+25(Type 3)
        call AddEquipment('I22M' , "玄元囊" , 5 , 4 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22 , 0 , 20 , 0 , 0 , 0 , 3 , 25 , 0 , 0 , 4 , 4 , 4)
        // 天星坠: 冷却22%, 急速24%, 法强+22%(Type 17)
        call AddEquipment('I22N' , "天星坠" , 5 , 4 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 22 , 0 , 0 , 24 , 0 , 0 , 17 , 22 , 0 , 0 , 4 , 4 , 4)
        // 传说神兵饰品（97-100）
        // 时空之戒: 冷却40%, 消耗36%, 技能冷却-15%(Type 5)
        call AddEquipment('I22O' , "时空之戒" , 5 , 5 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 40 , 0 , 36 , 0 , 0 , 0 , 5 , 15 , 0 , 0 , 5 , 5 , 5)
        // 永恒宝玉: 范围40%, 急速40%, 法力恢复+20%(Type 13)
        call AddEquipment('I22P' , "永恒宝玉" , 5 , 5 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 40 , 0 , 40 , 0 , 0 , 13 , 20 , 0 , 0 , 5 , 5 , 5)
        // 紫霄云符: 冷却37%, 消耗34%, 技能范围+12%(Type 14)
        call AddEquipment('I22Q' , "紫霄云符" , 5 , 5 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 37 , 0 , 34 , 0 , 0 , 0 , 14 , 12 , 0 , 0 , 5 , 5 , 5)
        // 太初灵珠: 范围36%, 急速38%, 全属性+8%(Type 15)
        call AddEquipment('I22R' , "太初灵珠" , 5 , 5 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 36 , 0 , 38 , 0 , 0 , 15 , 8 , 0 , 0 , 5 , 5 , 5)
        // ========================================================================
        // 添加项链数据（槽位6）- 20件
        // ========================================================================
        // 凡品项链（101-104）
        // 皮绳: 法强25, 抗性15
        call AddEquipment('I22S' , "皮绳" , 6 , 1 , 0 , 25 , 0 , 0 , 15 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 铜链: 法强27, 抗性17
        call AddEquipment('I22T' , "铜链" , 6 , 1 , 0 , 27 , 0 , 0 , 17 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 麻绳: 法强23, 抗性13
        call AddEquipment('I22U' , "麻绳" , 6 , 1 , 0 , 23 , 0 , 0 , 13 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 骨链: 法强25, 抗性15
        call AddEquipment('I22V' , "骨链" , 6 , 1 , 0 , 25 , 0 , 0 , 15 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1)
        // 利器项链（105-108）
        // 银链: 法强52, 抗性42
        call AddEquipment('I22W' , "银链" , 6 , 2 , 0 , 52 , 0 , 0 , 42 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 玉珠: 法强48, 抗性48
        call AddEquipment('I22X' , "玉珠" , 6 , 2 , 0 , 48 , 0 , 0 , 48 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 铁链: 法强46, 抗性40
        call AddEquipment('I22Y' , "铁链" , 6 , 2 , 0 , 46 , 0 , 0 , 40 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 珠链: 法强51, 抗性45
        call AddEquipment('I22Z' , "珠链" , 6 , 2 , 0 , 51 , 0 , 0 , 45 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 2 , 2)
        // 宝刃项链（109-112）
        // 金链: 法强98, 抗性75, 火18
        call AddEquipment('I230' , "金链" , 6 , 3 , 0 , 98 , 0 , 0 , 75 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 18 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 宝珠: 法强92, 抗性80, 冰20
        call AddEquipment('I231' , "宝珠" , 6 , 3 , 0 , 92 , 0 , 0 , 80 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 20 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 玉牌: 法强95, 抗性78, 火18
        call AddEquipment('I232' , "玉牌" , 6 , 3 , 0 , 95 , 0 , 0 , 78 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 18 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 银坠: 法强90, 抗性76, 雷16
        call AddEquipment('I233' , "银坠" , 6 , 3 , 0 , 90 , 0 , 0 , 76 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 3 , 16 , 0 , 0 , 0 , 0 , 3 , 3 , 3)
        // 神兵项链（113-116）
        // 龙凤链: 法强175, 抗性125, 冰30, 会心8%
        call AddEquipment('I234' , "龙凤链" , 6 , 4 , 0 , 175 , 0 , 0 , 125 , 0 , 8 , 0 , 0 , 0 , 0 , 0 , 2 , 30 , 0 , 0 , 0 , 0 , 4 , 4 , 4)
        // 太极珠: 法强185, 抗性135, 冰35, 法强+25(Type 8)
        call AddEquipment('I235' , "太极珠" , 6 , 4 , 0 , 185 , 0 , 0 , 135 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 , 35 , 8 , 25 , 0 , 0 , 4 , 4 , 4)
        // 五行佩: 法强180, 抗性130, 全元素25(Type 5), 法强+20(Type 8)
        // 注意：元素字段只能存一个类型，全元素用Type 5表示，Type 8法强加成用Special Type字段
        call AddEquipment('I236' , "五行佩" , 6 , 4 , 0 , 180 , 0 , 0 , 130 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 5 , 25 , 8 , 20 , 0 , 0 , 4 , 4 , 4)
        // 麒麟坠: 法强173, 抗性123, 雷28, 会心7%
        call AddEquipment('I237' , "麒麟坠" , 6 , 4 , 0 , 173 , 0 , 0 , 123 , 0 , 7 , 0 , 0 , 0 , 0 , 0 , 3 , 28 , 0 , 0 , 0 , 0 , 4 , 4 , 4)
        // 传说神兵项链（117-120）
        // 星辰之链: 法强285, 抗性225, 全元素50, 会心15%
        call AddEquipment('I238' , "星辰之链" , 6 , 5 , 0 , 285 , 0 , 0 , 225 , 0 , 15 , 0 , 0 , 0 , 0 , 0 , 5 , 50 , 0 , 0 , 0 , 0 , 5 , 5 , 5)
        // 命运之牌: 法强315, 抗性250, 全元素60, 要害20%
        call AddEquipment('I239' , "命运之牌" , 6 , 5 , 0 , 315 , 0 , 0 , 250 , 0 , 0 , 20 , 0 , 0 , 0 , 0 , 5 , 60 , 0 , 0 , 0 , 0 , 5 , 5 , 5)
        // 太极昆仑: 法强302, 抗性240, 全元素55, 冷却-12%(Type 5)
        call AddEquipment('I23A' , "太极昆仑" , 6 , 5 , 0 , 302 , 0 , 0 , 240 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 5 , 55 , 5 , 12 , 0 , 0 , 5 , 5 , 5)
        // 四象神链: 法强292, 抗性230, 全元素52, 伤害+15%(Type 16)
        call AddEquipment('I23B' , "四象神链" , 6 , 5 , 0 , 292 , 0 , 0 , 230 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 5 , 52 , 16 , 15 , 0 , 0 , 5 , 5 , 5)
                // ========================================================================
        // 初始化套装数据
        // ========================================================================
        // 套装ID: 1=凡品, 2=利器, 3=宝刃, 4=神兵, 5=传说神兵
        set udg_set_id[1]=1
        set udg_set_name[1]="江湖套装"
        set udg_set_quality[1]=1
        set udg_set_bonus_2[1]=10
        set udg_set_bonus_4[1]=25
        set udg_set_bonus_6[1]=50
        set udg_set_count[1]=6
        set udg_set_id[2]=2
        set udg_set_name[2]="武林套装"
        set udg_set_quality[2]=2
        set udg_set_bonus_2[2]=10
        set udg_set_bonus_4[2]=25
        set udg_set_bonus_6[2]=50
        set udg_set_count[2]=6
        set udg_set_id[3]=3
        set udg_set_name[3]="英雄套装"
        set udg_set_quality[3]=3
        set udg_set_bonus_2[3]=10
        set udg_set_bonus_4[3]=25
        set udg_set_bonus_6[3]=50
        set udg_set_count[3]=6
        set udg_set_id[4]=4
        set udg_set_name[4]="神话套装"
        set udg_set_quality[4]=4
        set udg_set_bonus_2[4]=10
        set udg_set_bonus_4[4]=25
        set udg_set_bonus_6[4]=50
        set udg_set_count[4]=6
        set udg_set_id[5]=5
        set udg_set_name[5]="乾坤套装"
        set udg_set_quality[5]=5
        set udg_set_bonus_2[5]=10
        set udg_set_bonus_4[5]=25
        set udg_set_bonus_6[5]=50
        set udg_set_count[5]=6
         call DisplayTextToPlayer(Player(0), 0, 0, "装备数据加载完成！")
        // 验证数据完整性
        if not EquipmentData_Validate() then
            call DisplayTextToPlayer(Player(0), 0, 0, "装备数据验证失败！")
        endif
    endfunction
    // ============================================================================
    // 获取装备名称
    // ============================================================================
    function EquipmentData_GetName takes integer equip_id returns string
        if equip_id < 1 or equip_id > udg_equip_count then
            return "未知装备"
        endif
        return udg_equip_name[equip_id]
    endfunction
    // ============================================================================
    // 获取装备槽位
    // ============================================================================
    function EquipmentData_GetSlot takes integer equip_id returns integer
        if equip_id < 1 or equip_id > udg_equip_count then
            return 0
        endif
        return udg_equip_slot[equip_id]
    endfunction
    // ============================================================================
    // 获取装备品质
    // ============================================================================
    function EquipmentData_GetQuality takes integer equip_id returns integer
        if equip_id < 1 or equip_id > udg_equip_count then
            return 0
        endif
        return udg_equip_quality[equip_id]
    endfunction
    // ============================================================================
    // 根据槽位和品质随机获取装备ID
    // ============================================================================
    function EquipmentData_GetRandom takes integer slot,integer quality returns integer
        local integer i
        local integer count= 0
        local integer result= 0
        // 统计符合条件的装备数量
        set i=1
        loop
            exitwhen i > udg_equip_count
            if udg_equip_slot[i] == slot and udg_equip_quality[i] == quality then
                set count=count + 1
            endif
            set i=i + 1
        endloop
        if count == 0 then
            return 0
        endif
        // 随机选择一个
        set count=GetRandomInt(1, count)
        set i=1
        loop
            exitwhen i > udg_equip_count
            if udg_equip_slot[i] == slot and udg_equip_quality[i] == quality then
                set count=count - 1
                if count == 0 then
                    set result=i
                    exitwhen true
                endif
            endif
            set i=i + 1
        endloop
        return result
    endfunction
    // ============================================================================
    // 根据物品类型ID获取装备ID
    // ============================================================================
    function EquipmentData_GetEquipIdByItemType takes integer item_type_id returns integer
        local integer i= 1
        // 检查缓存
        set i=1
        loop
            exitwhen i > udg_equip_cache_size
            if udg_equip_cache_item_type[i] == item_type_id then
                return udg_equip_cache_equip_id[i]
            endif
            set i=i + 1
        endloop
        // 缓存未命中，执行查询
        set i=1
        loop
            exitwhen i > udg_equip_count
            if udg_equip_item_type_id[i] == item_type_id then
                // 添加到缓存（简单实现，最多缓存20个）
                if udg_equip_cache_size < 20 then
                    set udg_equip_cache_size=udg_equip_cache_size + 1
                    set udg_equip_cache_item_type[udg_equip_cache_size]=item_type_id
                    set udg_equip_cache_equip_id[udg_equip_cache_size]=i
                endif
                return i
            endif
            set i=i + 1
        endloop
        return 0
    endfunction
    // ============================================================================
    // 获取装备的物品类型ID
    // ============================================================================
    function EquipmentData_GetItemTypeId takes integer equip_id returns integer
        if equip_id < 1 or equip_id > udg_equip_count then
            return 0
        endif
        return udg_equip_item_type_id[equip_id]
    endfunction
    // ============================================================================
    // 根据槽位和品质获取物品类型ID
    // ============================================================================
    function EquipmentData_GetItemTypeBySlotQuality takes integer slot,integer quality returns integer
        local integer equip_id= EquipmentData_GetRandom(slot , quality)
        if equip_id == 0 then
            return 0
        endif
        return EquipmentData_GetItemTypeId(equip_id)
    endfunction
    

//library EquipmentData ends
//library GameTimeSystem:
// ============================================================================
// Timer Callback
// ============================================================================
// 计时器回调函数 - 每0.5秒执行一次
// ============================================================================
function GameTimerCallback takes nothing returns nothing
    // 游戏时间递增
    set udg_game_time=udg_game_time + 0.5
endfunction
// ============================================================================
// System Initialization
// ============================================================================
// 系统初始化
// ============================================================================
function InitGameTimeSystem takes nothing returns nothing
    // 创建计时器
    set udg_game_timer=CreateTimer()
    
    // 启动循环计时器，周期为0.5秒
    call TimerStart(udg_game_timer, 0.5, true, function GameTimerCallback)
    
    // 初始化时间为0
    set udg_game_time=0
endfunction

//library GameTimeSystem ends
//library LBKKAPI:












































        //转换屏幕坐标到世界坐标  


        //监听建筑选位置  

        //等于0时是结束事件  



        //监听技能选目标  

        //等于0时是结束事件  





        // 打开QQ群链接  
















        function DzSetHeroTypeProperName takes integer uid,string name returns nothing
                call EXSetUnitArrayString(uid, 61, 0, name)
                call EXSetUnitInteger(uid, 61, 1)
        endfunction 
        function DzSetUnitTypeName takes integer uid,string name returns nothing
                call EXSetUnitArrayString(uid, 10, 0, name)
                call EXSetUnitInteger(uid, 10, 1)
        endfunction 
        function DzIsUnitAttackType takes unit whichUnit,integer index,attacktype attackType returns boolean
                return ConvertAttackType(R2I(GetUnitState(whichUnit, ConvertUnitState(16 + 19 * index)))) == attackType
        endfunction 
        function DzSetUnitAttackType takes unit whichUnit,integer index,attacktype attackType returns nothing
                call SetUnitState(whichUnit, ConvertUnitState(16 + 19 * index), GetHandleId(attackType))
        endfunction 
        function DzIsUnitDefenseType takes unit whichUnit,integer defenseType returns boolean
                return R2I(GetUnitState(whichUnit, ConvertUnitState(0x50))) == defenseType
        endfunction 
        function DzSetUnitDefenseType takes unit whichUnit,integer defenseType returns nothing
                call SetUnitState(whichUnit, ConvertUnitState(0x50), defenseType)
        endfunction 
        // 地形装饰物




















        // 解锁JASS字节码限制

        // 设置剪切板内容

        //删除装饰物

        //移除科技等级

        
        // 查找单位技能

        // 修改技能数据-字符串

                
        // 启用/禁用技能

        // 设置单位移动类型

        // 获取控件宽度




        function KKWESetUnitDataCacheInteger takes integer uid,integer id,integer v returns nothing
                call DzSetUnitDataCacheInteger(uid, id, 0, v)
        endfunction
        function KKWEUnitUIAddUpgradesIds takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 94, id, v)
        endfunction
        function KKWEUnitUIAddBuildsIds takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 100, id, v)
        endfunction
        function KKWEUnitUIAddResearchesIds takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 112, id, v)
        endfunction
        function KKWEUnitUIAddTrainsIds takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 106, id, v)
        endfunction
        function KKWEUnitUIAddSellsUnitIds takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 118, id, v)
        endfunction
        function KKWEUnitUIAddSellsItemIds takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 124, id, v)
        endfunction
        function KKWEUnitUIAddMakesItemIds takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 130, id, v)
        endfunction
        function KKWEUnitUIAddRequiresUnitCode takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 166, id, v)
        endfunction
        function KKWEUnitUIAddRequiresTechcode takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 166, id, v)
        endfunction
        function KKWEUnitUIAddRequiresAmounts takes integer uid,integer id,integer v returns nothing
                call DzUnitUIAddLevelArrayInteger(uid, 172, id, v)
        endfunction
         // 设置道具模型

        // 设置道具颜色

        // 设置道具透明度

        // 设置道具头像











                
        function DzIsLeapYear takes integer year returns boolean
                return ( ModuloInteger(year, 4) == 0 and ModuloInteger(year, 100) != 0 ) or ( ModuloInteger(year, 400) == 0 )
        endfunction
        function DzGetTimeDateFromTimestamp takes integer timestamp returns string
                local integer totalSeconds= timestamp + 28800
                local integer days= 0
                local integer day= 0
                local integer secondsInDay= 86400
                local integer remainingSeconds= ModuloInteger(totalSeconds, secondsInDay)
                local integer year= 1970
                local integer totalDays= ( totalSeconds + 86399 ) / ( secondsInDay )
                local integer num= 0
                local integer month=0
                local integer hour
                local integer minute
                local integer second
                local string str
                loop
                if DzIsLeapYear(year) then
                        set num=num + 366
                else
                        set num=num + 365
                endif
                if num > totalDays then
                        set totalDays=totalDays - days
                        exitwhen true
                else
                        set days=num
                endif
                set year=year + 1
                endloop
                set month=1
                set num=0
                set days=0
                if ( DzIsLeapYear(year) ) then
                loop
                        set num=num + LBKKAPI___MonthDay[100 + month]
                        if num >= totalDays then
                        set day=totalDays - days
                        exitwhen true
                        else
                        set days=num
                        endif
                        set month=month + 1
                endloop
                else
                loop
                        set num=num + LBKKAPI___MonthDay[month]
                        if num >= totalDays then
                        set day=totalDays - days
                        exitwhen true
                        else
                        set days=num
                        endif
                        set month=month + 1
                endloop
                endif
                if ( day == 0 ) then
                set day=1
                endif
                set hour=remainingSeconds / 3600
                set remainingSeconds=ModuloInteger(remainingSeconds, 3600)
                set minute=remainingSeconds / 60
                set second=ModuloInteger(remainingSeconds, 60)
                set str=I2S(year) + "-" + I2S(month) + "-" + I2S(day) + " " + I2S(hour) + ":" + I2S(minute) + ":" + I2S(second)
                call SaveInteger(LBKKAPI___Hash, timestamp, 1, year)
                call SaveInteger(LBKKAPI___Hash, timestamp, 2, month)
                call SaveInteger(LBKKAPI___Hash, timestamp, 3, day)
                call SaveStr(LBKKAPI___Hash, timestamp, 4, str)
                return str
        endfunction
        function KKAPIGetTimeDateFromTimestamp takes integer timestamp returns string
                set timestamp=IMaxBJ(timestamp, 0)
                if ( HaveSavedString(LBKKAPI___Hash, timestamp, 4) ) then
                        return LoadStr(LBKKAPI___Hash, timestamp, 4)
                else
                        return DzGetTimeDateFromTimestamp(timestamp)
                endif
        endfunction
        function KKAPIGetTimestampYear takes integer timestamp returns integer
                set timestamp=IMaxBJ(timestamp, 0)
                if ( HaveSavedInteger(LBKKAPI___Hash, timestamp, 1) == false ) then
                        call DzGetTimeDateFromTimestamp(timestamp)
                endif
                 return LoadInteger(LBKKAPI___Hash, timestamp, 1)
        endfunction
        function KKAPIGetTimestampMonth takes integer timestamp returns integer
                set timestamp=IMaxBJ(timestamp, 0)
                if ( HaveSavedInteger(LBKKAPI___Hash, timestamp, 2) == false ) then
                        call DzGetTimeDateFromTimestamp(timestamp)
                endif
                 return LoadInteger(LBKKAPI___Hash, timestamp, 2)
        endfunction
        function KKAPIGetTimestampDay takes integer timestamp returns integer
                set timestamp=IMaxBJ(timestamp, 0)
                if ( HaveSavedInteger(LBKKAPI___Hash, timestamp, 3) == false ) then
                        call DzGetTimeDateFromTimestamp(timestamp)
                endif
                 return LoadInteger(LBKKAPI___Hash, timestamp, 3)
        endfunction
        function LBKKAPI___Init takes nothing returns nothing
                set LBKKAPI___MonthDay[1]=31
                set LBKKAPI___MonthDay[2]=28
                set LBKKAPI___MonthDay[3]=31
                set LBKKAPI___MonthDay[4]=30
                set LBKKAPI___MonthDay[5]=31
                set LBKKAPI___MonthDay[6]=30
                set LBKKAPI___MonthDay[7]=31
                set LBKKAPI___MonthDay[8]=31
                set LBKKAPI___MonthDay[9]=30
                set LBKKAPI___MonthDay[10]=31
                set LBKKAPI___MonthDay[11]=30
                set LBKKAPI___MonthDay[12]=31
                set LBKKAPI___MonthDay[101]=31
                set LBKKAPI___MonthDay[102]=29
                set LBKKAPI___MonthDay[103]=31
                set LBKKAPI___MonthDay[104]=30
                set LBKKAPI___MonthDay[105]=31
                set LBKKAPI___MonthDay[106]=30
                set LBKKAPI___MonthDay[107]=31
                set LBKKAPI___MonthDay[108]=31
                set LBKKAPI___MonthDay[109]=30
                set LBKKAPI___MonthDay[110]=31
                set LBKKAPI___MonthDay[111]=30
                set LBKKAPI___MonthDay[112]=31
        endfunction

        // texttag





    
        // group


    
        // unit


    
        // string












    
        // bit











    
        // issue

















        // xlsx









    




























        




        


        
        















        







        function KKConvertInt2AbilId takes integer i returns integer
                return i
        endfunction
        function KKConvertAbilId2Int takes integer i returns integer
                return i
        endfunction
        function KKConvertInt2Color takes integer i returns integer
                return i
        endfunction
        function KKConvertColor2Int takes integer i returns integer
                return i
        endfunction









































        
                







        function KKFrameBindItem takes integer frame,widget u,real world_x,real world_y,real world_z,real screen_x,real screen_y,boolean fog_visible,boolean item_visible returns nothing
                call DzFrameBindWidget(frame, u, world_x, world_y, world_z, screen_x, screen_y, fog_visible, item_visible, false)
        endfunction




















           
























        

//library LBKKAPI ends
//library SectData:
    // ============================================================================
    // 门派数据初始化函数
    // 初始化所有门派的基础数据和技能配置
    // ============================================================================
    function InitSectData takes nothing returns nothing
        local integer sect_id
        // ========================================================================
        // 少林门派数据配置
        // 定位：均衡型，坦克/输出双修，技能全面
        // ========================================================================
        set sect_id=SECT_SHAOLIN
        set sect_name[sect_id]="少林"
        set sect_type_id[sect_id]=SECT_TYPE_RIGHTEOUS
        set sect_role_id[sect_id]=SECT_ROLE_BALANCED
        set sect_coefficient[sect_id]=1.0
        // 第一技能 - 大力金刚掌
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_FIRST]=10101
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_FIRST]="大力金刚掌"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_FIRST]=1
        // 第二技能 - 般若掌
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_SECOND]=10102
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_SECOND]="般若掌"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_SECOND]=6
        // 第三技能 - 金刚伏魔神功
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_THIRD]=10103
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_THIRD]="金刚伏魔神功"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_THIRD]=12
        // 毕业技能A - 金刚不坏身
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_GRADUATION_A]=10104
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_GRADUATION_A]="金刚不坏身"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_GRADUATION_A]=0
        // 毕业技能B - 狮子吼
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_GRADUATION_B]=10105
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_GRADUATION_B]="狮子吼"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_GRADUATION_B]=0
        // ========================================================================
        // 武当门派数据配置
        // 定位：控制型，剑气伤人，附带减速/眩晕
        // ========================================================================
        set sect_id=SECT_WUDANG
        set sect_name[sect_id]="武当"
        set sect_type_id[sect_id]=SECT_TYPE_RIGHTEOUS
        set sect_role_id[sect_id]=SECT_ROLE_CONTROL
        set sect_coefficient[sect_id]=1.0
        // 第一技能 - 太极剑法
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_FIRST]=10201
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_FIRST]="太极剑法"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_FIRST]=1
        // 第二技能 - 梯云纵
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_SECOND]=10202
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_SECOND]="梯云纵"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_SECOND]=6
        // 第三技能 - 绵掌
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_THIRD]=10203
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_THIRD]="绵掌"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_THIRD]=12
        // 毕业技能A - 纯阳无极功
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_GRADUATION_A]=10204
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_GRADUATION_A]="纯阳无极功"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_GRADUATION_A]=0
        // 毕业技能B - 太极阵法
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_GRADUATION_B]=10205
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_GRADUATION_B]="太极阵法"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_GRADUATION_B]=0
        // ========================================================================
        // 峨眉门派数据配置
        // 定位：辅助型，治疗与增益并重
        // ========================================================================
        set sect_id=SECT_EMEI
        set sect_name[sect_id]="峨眉"
        set sect_type_id[sect_id]=SECT_TYPE_RIGHTEOUS
        set sect_role_id[sect_id]=SECT_ROLE_SUPPORT
        set sect_coefficient[sect_id]=0.7
        // 第一技能 - 峨眉剑法
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_FIRST]=10301
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_FIRST]="峨眉剑法"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_FIRST]=1
        // 第二技能 - 倚天剑意
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_SECOND]=10302
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_SECOND]="倚天剑意"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_SECOND]=6
        // 第三技能 - 九阳神功
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_THIRD]=10303
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_THIRD]="峨眉九阳功"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_THIRD]=12
        // 毕业技能A - 金顶绵掌
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_GRADUATION_A]=10304
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_GRADUATION_A]="金顶绵掌"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_GRADUATION_A]=0
        // 毕业技能B - 佛光普照
        set sect_skill_id[sect_id * 10 + SKILL_SLOT_GRADUATION_B]=10305
        set sect_skill_name[sect_id * 10 + SKILL_SLOT_GRADUATION_B]="佛光普照"
        set sect_skill_unlock_level[sect_id * 10 + SKILL_SLOT_GRADUATION_B]=0
        // ========================================================================
        // 初始化所有玩家的门派选择状态
        // ========================================================================
        set udg_player_sect_selected[0]=0
        set udg_player_sect_selected[1]=0
        set udg_player_sect_selected[2]=0
        set udg_player_sect_selected[3]=0
        set udg_player_sect_selected[4]=0
        set udg_player_sect_selected[5]=0
        set udg_player_sect_selected[6]=0
        set udg_player_sect_selected[7]=0
        set udg_player_sect_selected[8]=0
        set udg_player_sect_selected[9]=0
        set udg_player_sect_selected[10]=0
        set udg_player_sect_selected[11]=0
        // ========================================================================
        // 配置门派道具物品ID
        // ========================================================================
        set sect_join_item_id[SECT_SHAOLIN]='I000' // 少林信物
set sect_join_item_id[SECT_WUDANG]='I001' // 武当信物
set sect_join_item_id[SECT_EMEI]='I002' // 峨眉信物
set sect_join_item_id[SECT_MINGJIAO]='I003' // 明教信物
set sect_join_item_id[SECT_XINGXIU]='I004' // 星宿信物
set sect_join_item_id[SECT_XIAOYAO]='I005' // 逍遥信物
set sect_join_item_id[SECT_GAIBANG]='I006' // 丐帮信物
set sect_join_item_id[SECT_QUANZHEN]='I007' // 全真信物
set sect_join_item_id[SECT_HUASHAN]='I008' // 华山信物
set sect_join_item_id[SECT_DIANCANG]='I009' // 点苍信物
set sect_join_item_id[SECT_KUNLUN]='I00A' // 昆仑信物
set sect_join_item_id[SECT_JINDAOMEN]='I00B' // 金刀门信物
set sect_join_item_id[SECT_TIEJIANMEN]='I00C' // 铁剑门信物
set sect_join_item_id[SECT_SHUSHAN]='I00D' // 蜀山信物
set sect_join_item_id[SECT_KONGTONG]='I00E' // 崆峒信物

    endfunction
    // ============================================================================
    // 获取门派名称
    // ============================================================================
    function SectData_GetName takes integer sect_id returns string
        return sect_name[sect_id]
    endfunction
    // ============================================================================
    // 获取门派类型ID
    // ============================================================================
    function SectData_GetTypeId takes integer sect_id returns integer
        return sect_type_id[sect_id]
    endfunction
    // ============================================================================
    // 获取门派定位ID
    // ============================================================================
    function SectData_GetRoleId takes integer sect_id returns integer
        return sect_role_id[sect_id]
    endfunction
    // ============================================================================
    // 获取指定门派指定槽位的技能ID
    // ============================================================================
    function SectData_GetSkillId takes integer sect_id,integer slot returns integer
        return sect_skill_id[sect_id * 10 + slot]
    endfunction
    // ============================================================================
    // 获取指定门派指定槽位的技能名称
    // ============================================================================
    function SectData_GetSkillName takes integer sect_id,integer slot returns string
        return sect_skill_name[sect_id * 10 + slot]
    endfunction
    // ============================================================================
    // 获取指定门派指定槽位的技能解锁等级
    // ============================================================================
    function SectData_GetSkillUnlockLevel takes integer sect_id,integer slot returns integer
        return sect_skill_unlock_level[sect_id * 10 + slot]
    endfunction
    // ============================================================================
    // 获取指定门派对应的加入道具ID
    // ============================================================================
    function SectData_GetJoinItemId takes integer sect_id returns integer
        return sect_join_item_id[sect_id]
    endfunction
    // ============================================================================
    // 根据物品ID获取对应的门派ID
    // 返回0表示无效的门派道具
    // ============================================================================
    function SectData_GetSectByItemId takes integer item_id returns integer
        if item_id == sect_join_item_id[SECT_SHAOLIN] then
            return SECT_SHAOLIN
        elseif item_id == sect_join_item_id[SECT_WUDANG] then
            return SECT_WUDANG
        elseif item_id == sect_join_item_id[SECT_EMEI] then
            return SECT_EMEI
        elseif item_id == sect_join_item_id[SECT_MINGJIAO] then
            return SECT_MINGJIAO
        elseif item_id == sect_join_item_id[SECT_XINGXIU] then
            return SECT_XINGXIU
        elseif item_id == sect_join_item_id[SECT_XIAOYAO] then
            return SECT_XIAOYAO
        elseif item_id == sect_join_item_id[SECT_GAIBANG] then
            return SECT_GAIBANG
        elseif item_id == sect_join_item_id[SECT_QUANZHEN] then
            return SECT_QUANZHEN
        elseif item_id == sect_join_item_id[SECT_HUASHAN] then
            return SECT_HUASHAN
        elseif item_id == sect_join_item_id[SECT_DIANCANG] then
            return SECT_DIANCANG
        elseif item_id == sect_join_item_id[SECT_KUNLUN] then
            return SECT_KUNLUN
        elseif item_id == sect_join_item_id[SECT_JINDAOMEN] then
            return SECT_JINDAOMEN
        elseif item_id == sect_join_item_id[SECT_TIEJIANMEN] then
            return SECT_TIEJIANMEN
        elseif item_id == sect_join_item_id[SECT_SHUSHAN] then
            return SECT_SHUSHAN
        elseif item_id == sect_join_item_id[SECT_KONGTONG] then
            return SECT_KONGTONG
        endif
        return 0
    endfunction

//library SectData ends
//library SkillLibary:
        
        // 技能名称
        // 技能描述
        // 技能类型 1-主动 2-被动
        // 技能目标类型 0-无目标 1-单位目标 2-点目标 3-单位或点目标
        // 技能模板ID 从A000~A00B 共12个技能 快捷键分别为Q、W、E、R、S、D、F、G、Z、X、C、V
        // 技能CD
        // 技能魔法消耗
        // 技能施法范围
        // 技能伤害系数
        // 技能属性类型 1-根骨 2-身法 3-悟性 4-全部
        // 技能元素类型 1-火 2-冰 3-雷 4-毒 5-全部
        // 技能伤害类型 1-物理伤害 2-魔法伤害
        function s__Skill_create takes integer skill_id,string skill_name,string skill_desc,integer skill_type,integer skill_target_type,integer skill_template_id,real skill_cooldown,integer skill_magic_cost,real skill_cast_range,real skill_damage_coefficient,integer skill_attribute_type,integer skill_element_type,integer skill_damage_type returns integer
            local integer s= s__Skill__allocate()
            set s__Skill_skill_id[s]=skill_id
            set s__Skill_skill_name[s]=skill_name
            set s__Skill_skill_desc[s]=skill_desc
            set s__Skill_skill_type[s]=skill_type
            set s__Skill_skill_damage_type[s]=skill_damage_type
            set s__Skill_skill_target_type[s]=skill_target_type
            set s__Skill_skill_template_id[s]=skill_template_id
            set s__Skill_skill_cooldown[s]=skill_cooldown
            set s__Skill_skill_magic_cost[s]=skill_magic_cost
            set s__Skill_skill_cast_range[s]=skill_cast_range
            set s__Skill_skill_damage_coefficient[s]=skill_damage_coefficient
            set s__Skill_skill_attribute_type[s]=skill_attribute_type
            set s__Skill_skill_element_type[s]=skill_element_type
            return s
        endfunction
        function s__Skill_onDestroy takes integer this returns nothing
            set s__Skill_skill_id[this]=0
            set s__Skill_skill_name[this]=""
            set s__Skill_skill_desc[this]=""
            set s__Skill_skill_type[this]=0
            set s__Skill_skill_target_type[this]=0
            set s__Skill_skill_template_id[this]=0
            set s__Skill_skill_cooldown[this]=0.0
            set s__Skill_skill_magic_cost[this]=0
            set s__Skill_skill_cast_range[this]=0.0
            set s__Skill_skill_damage_coefficient[this]=0.0
            set s__Skill_skill_attribute_type[this]=0
            set s__Skill_skill_element_type[this]=0
            set s__Skill_skill_damage_type[this]=0
        endfunction

//Generated destructor of Skill
function s__Skill_deallocate takes integer this returns nothing
    if this==null then
        return
    elseif (si__Skill_V[this]!=-1) then
        return
    endif
    call s__Skill_onDestroy(this)
    set si__Skill_V[this]=si__Skill_F
    set si__Skill_F=this
endfunction
        function s__Skill_addToUnit takes integer this,unit u returns nothing
            if GetUnitAbilityLevel(u, s__Skill_skill_template_id[this]) > 0 then
                call DisplayTextToPlayer(GetOwningPlayer(u), 0, 0, "|cffff0000[系统]|r请先遗忘对应位置的技能")
            else
                call UnitAddAbility(u, s__Skill_skill_template_id[this])
                // 通过japi/kkapi设置技能的各项属性
                call DzSetUnitAbilityTip(u, s__Skill_skill_template_id[this], s__Skill_skill_name[this])
                call DzSetUnitAbilityUberTip(u, s__Skill_skill_template_id[this], s__Skill_skill_desc[this])
                call DzSetUnitAbilityDataB(u, s__Skill_skill_template_id[this], s__Skill_skill_target_type[this])
                call DzSetUnitAbilityCool(u, s__Skill_skill_template_id[this], 0, s__Skill_skill_cooldown[this])
                call DzSetUnitAbilityCost(u, s__Skill_skill_template_id[this], s__Skill_skill_magic_cost[this])
                call DzSetUnitAbilityRange(u, s__Skill_skill_template_id[this], s__Skill_skill_cast_range[this])
                call SaveInteger(udg_skill_table, GetHandleId(u), s__Skill_skill_template_id[this], s__Skill_skill_id[this])
            endif
        endfunction
    function GetSkillById takes integer skill_id returns integer
        local integer i= 1
        loop
            exitwhen i > udg_skill_count
            if s__Skill_skill_id[udg_skills[i]] == skill_id then
                return udg_skills[i]
            endif
            set i=i + 1
        endloop
        
        set i=1
        loop
            exitwhen i > udg_enemy_skill_count
            if s__Skill_skill_id[udg_enemy_skills[i]] == skill_id then
                return udg_enemy_skills[i]
            endif
            set i=i + 1
        endloop
        return 0
    endfunction
    function GetSkillByUnitAndTemplateId takes unit u,integer skill_template_id returns integer
        local integer skill_id= LoadInteger(udg_skill_table, GetHandleId(u), skill_template_id)
        return GetSkillById(skill_id)
    endfunction

//library SkillLibary ends
//library TestEquipmentGenerate:
    // ============================================================================
    // 生成测试装备
    // ============================================================================
    function GenerateTestEquipment takes player p,integer slot,integer quality returns nothing
        local unit hero= udg_player_hero[GetPlayerId(p)]
        local integer item_type_id
        local item test_item
        if hero == null then
            call DisplayTextToPlayer(p, 0, 0, "没有英雄单位")
            return
        endif
        // 获取物品类型ID
        set item_type_id=EquipmentData_GetItemTypeBySlotQuality(slot , quality)
        if item_type_id == 0 then
            call DisplayTextToPlayer(p, 0, 0, "未找到符合条件的装备")
            return
        endif
        // 创建测试物品
        set test_item=CreateItem(item_type_id, GetUnitX(hero), GetUnitY(hero))
        // 自动拾取
        call UnitAddItem(hero, test_item)
        call DisplayTextToPlayer(p, 0, 0, "生成测试装备: 槽位" + I2S(slot) + " 品质" + I2S(quality))
        // 排泄局部handle变量
        set test_item=null
    endfunction
    // ============================================================================
    // 测试装备生成事件处理
    // ============================================================================
    function Trig_TestEquipGenerate_Actions takes nothing returns nothing
        local player p= GetTriggerPlayer()
        local string cmd= GetEventPlayerChatString()
        local integer slot
        local integer quality
        // 解析命令: -testequip [slot] [quality]
        if SubString(cmd, 0, 9) == "-testequip" then
            set slot=S2I(SubString(cmd, 10, 11))
            set quality=S2I(SubString(cmd, 12, 13))
            if slot < 1 or slot > 6 then
                call DisplayTextToPlayer(p, 0, 0, "槽位无效 (1-6)")
                return
            endif
            if quality < 1 or quality > 5 then
                call DisplayTextToPlayer(p, 0, 0, "品质无效 (1-5)")
                return
            endif
            call GenerateTestEquipment(p , slot , quality)
        endif
        // 排泄局部handle变量
        set p=null
    endfunction
    // ============================================================================
    // 初始化测试装备生成
    // ============================================================================
    function InitTestEquipmentGenerate takes nothing returns nothing
        local integer i= 0
        set gg_trg_TestEquipGenerate=CreateTrigger()
        // 为所有玩家注册聊天事件
        loop
            exitwhen i >= 12
            call TriggerRegisterPlayerChatEvent(gg_trg_TestEquipGenerate, Player(i), "-testequip", false)
            set i=i + 1
        endloop
        // 添加触发动作
        call TriggerAddAction(gg_trg_TestEquipGenerate, function Trig_TestEquipGenerate_Actions)
        call DisplayTextToPlayer(Player(0), 0, 0, "装备测试生成系统初始化完成")
    endfunction

//library TestEquipmentGenerate ends
//library YDWEBase:
//===========================================================================
//HashTable
//===========================================================================
//===========================================================================
//Return bug
//===========================================================================
function YDWEH2I takes handle h returns integer
    return GetHandleId(h)
endfunction
//����
function YDWEFlushAllData takes nothing returns nothing
    call FlushParentHashtable(YDHT)
endfunction
function YDWEFlushMissionByInteger takes integer i returns nothing
    call FlushChildHashtable(YDHT, i)
endfunction
function YDWEFlushMissionByString takes string s returns nothing
    call FlushChildHashtable(YDHT, StringHash(s))
endfunction
function YDWEFlushStoredIntegerByInteger takes integer i,integer j returns nothing
    call RemoveSavedInteger(YDHT, i, j)
endfunction
function YDWEFlushStoredIntegerByString takes string s1,string s2 returns nothing
    call RemoveSavedInteger(YDHT, StringHash(s1), StringHash(s2))
endfunction
function YDWEHaveSavedIntegerByInteger takes integer i,integer j returns boolean
    return HaveSavedInteger(YDHT, i, j)
endfunction
function YDWEHaveSavedIntegerByString takes string s1,string s2 returns boolean
    return HaveSavedInteger(YDHT, StringHash(s1), StringHash(s2))
endfunction
//store and get integer
function YDWESaveIntegerByInteger takes integer pTable,integer pKey,integer i returns nothing
    call SaveInteger(YDHT, pTable, pKey, i)
endfunction
function YDWESaveIntegerByString takes string pTable,string pKey,integer i returns nothing
    call SaveInteger(YDHT, StringHash(pTable), StringHash(pKey), i)
endfunction
function YDWEGetIntegerByInteger takes integer pTable,integer pKey returns integer
    return LoadInteger(YDHT, pTable, pKey)
endfunction
function YDWEGetIntegerByString takes string pTable,string pKey returns integer
    return LoadInteger(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//store and get real
function YDWESaveRealByInteger takes integer pTable,integer pKey,real r returns nothing
    call SaveReal(YDHT, pTable, pKey, r)
endfunction
function YDWESaveRealByString takes string pTable,string pKey,real r returns nothing
    call SaveReal(YDHT, StringHash(pTable), StringHash(pKey), r)
endfunction
function YDWEGetRealByInteger takes integer pTable,integer pKey returns real
    return LoadReal(YDHT, pTable, pKey)
endfunction
function YDWEGetRealByString takes string pTable,string pKey returns real
    return LoadReal(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//store and get string
function YDWESaveStringByInteger takes integer pTable,integer pKey,string s returns nothing
    call SaveStr(YDHT, pTable, pKey, s)
endfunction
function YDWESaveStringByString takes string pTable,string pKey,string s returns nothing
    call SaveStr(YDHT, StringHash(pTable), StringHash(pKey), s)
endfunction
function YDWEGetStringByInteger takes integer pTable,integer pKey returns string
    return LoadStr(YDHT, pTable, pKey)
endfunction
function YDWEGetStringByString takes string pTable,string pKey returns string
    return LoadStr(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//store and get boolean
function YDWESaveBooleanByInteger takes integer pTable,integer pKey,boolean b returns nothing
    call SaveBoolean(YDHT, pTable, pKey, b)
endfunction
function YDWESaveBooleanByString takes string pTable,string pKey,boolean b returns nothing
    call SaveBoolean(YDHT, StringHash(pTable), StringHash(pKey), b)
endfunction
function YDWEGetBooleanByInteger takes integer pTable,integer pKey returns boolean
    return LoadBoolean(YDHT, pTable, pKey)
endfunction
function YDWEGetBooleanByString takes string pTable,string pKey returns boolean
    return LoadBoolean(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Unit
function YDWESaveUnitByInteger takes integer pTable,integer pKey,unit u returns nothing
    call SaveUnitHandle(YDHT, pTable, pKey, u)
endfunction
function YDWESaveUnitByString takes string pTable,string pKey,unit u returns nothing
    call SaveUnitHandle(YDHT, StringHash(pTable), StringHash(pKey), u)
endfunction
function YDWEGetUnitByInteger takes integer pTable,integer pKey returns unit
    return LoadUnitHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetUnitByString takes string pTable,string pKey returns unit
    return LoadUnitHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert UnitID
function YDWESaveUnitIDByInteger takes integer pTable,integer pKey,integer uid returns nothing
    call SaveInteger(YDHT, pTable, pKey, uid)
endfunction
function YDWESaveUnitIDByString takes string pTable,string pKey,integer uid returns nothing
    call SaveInteger(YDHT, StringHash(pTable), StringHash(pKey), uid)
endfunction
function YDWEGetUnitIDByInteger takes integer pTable,integer pKey returns integer
    return LoadInteger(YDHT, pTable, pKey)
endfunction
function YDWEGetUnitIDByString takes string pTable,string pKey returns integer
    return LoadInteger(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert AbilityID
function YDWESaveAbilityIDByInteger takes integer pTable,integer pKey,integer abid returns nothing
    call SaveInteger(YDHT, pTable, pKey, abid)
endfunction
function YDWESaveAbilityIDByString takes string pTable,string pKey,integer abid returns nothing
    call SaveInteger(YDHT, StringHash(pTable), StringHash(pKey), abid)
endfunction
function YDWEGetAbilityIDByInteger takes integer pTable,integer pKey returns integer
    return LoadInteger(YDHT, pTable, pKey)
endfunction
function YDWEGetAbilityIDByString takes string pTable,string pKey returns integer
    return LoadInteger(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Player
function YDWESavePlayerByInteger takes integer pTable,integer pKey,player p returns nothing
    call SavePlayerHandle(YDHT, pTable, pKey, p)
endfunction
function YDWESavePlayerByString takes string pTable,string pKey,player p returns nothing
    call SavePlayerHandle(YDHT, StringHash(pTable), StringHash(pKey), p)
endfunction
function YDWEGetPlayerByInteger takes integer pTable,integer pKey returns player
    return LoadPlayerHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetPlayerByString takes string pTable,string pKey returns player
    return LoadPlayerHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Item
function YDWESaveItemByInteger takes integer pTable,integer pKey,item it returns nothing
    call SaveItemHandle(YDHT, pTable, pKey, it)
endfunction
function YDWESaveItemByString takes string pTable,string pKey,item it returns nothing
    call SaveItemHandle(YDHT, StringHash(pTable), StringHash(pKey), it)
endfunction
function YDWEGetItemByInteger takes integer pTable,integer pKey returns item
    return LoadItemHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetItemByString takes string pTable,string pKey returns item
    return LoadItemHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert ItemID
function YDWESaveItemIDByInteger takes integer pTable,integer pKey,integer itid returns nothing
    call SaveInteger(YDHT, pTable, pKey, itid)
endfunction
function YDWESaveItemIDByString takes string pTable,string pKey,integer itid returns nothing
    call SaveInteger(YDHT, StringHash(pTable), StringHash(pKey), itid)
endfunction
function YDWEGetItemIDByInteger takes integer pTable,integer pKey returns integer
    return LoadInteger(YDHT, pTable, pKey)
endfunction
function YDWEGetItemIDByString takes string pTable,string pKey returns integer
    return LoadInteger(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Timer
function YDWESaveTimerByInteger takes integer pTable,integer pKey,timer t returns nothing
    call SaveTimerHandle(YDHT, pTable, pKey, t)
endfunction
function YDWESaveTimerByString takes string pTable,string pKey,timer t returns nothing
    call SaveTimerHandle(YDHT, StringHash(pTable), StringHash(pKey), t)
endfunction
function YDWEGetTimerByInteger takes integer pTable,integer pKey returns timer
    return LoadTimerHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetTimerByString takes string pTable,string pKey returns timer
    return LoadTimerHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Trigger
function YDWESaveTriggerByInteger takes integer pTable,integer pKey,trigger trg returns nothing
    call SaveTriggerHandle(YDHT, pTable, pKey, trg)
endfunction
function YDWESaveTriggerByString takes string pTable,string pKey,trigger trg returns nothing
    call SaveTriggerHandle(YDHT, StringHash(pTable), StringHash(pKey), trg)
endfunction
function YDWEGetTriggerByInteger takes integer pTable,integer pKey returns trigger
    return LoadTriggerHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetTriggerByString takes string pTable,string pKey returns trigger
    return LoadTriggerHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Location
function YDWESaveLocationByInteger takes integer pTable,integer pKey,location pt returns nothing
    call SaveLocationHandle(YDHT, pTable, pKey, pt)
endfunction
function YDWESaveLocationByString takes string pTable,string pKey,location pt returns nothing
    call SaveLocationHandle(YDHT, StringHash(pTable), StringHash(pKey), pt)
endfunction
function YDWEGetLocationByInteger takes integer pTable,integer pKey returns location
    return LoadLocationHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetLocationByString takes string pTable,string pKey returns location
    return LoadLocationHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Group
function YDWESaveGroupByInteger takes integer pTable,integer pKey,group g returns nothing
    call SaveGroupHandle(YDHT, pTable, pKey, g)
endfunction
function YDWESaveGroupByString takes string pTable,string pKey,group g returns nothing
    call SaveGroupHandle(YDHT, StringHash(pTable), StringHash(pKey), g)
endfunction
function YDWEGetGroupByInteger takes integer pTable,integer pKey returns group
    return LoadGroupHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetGroupByString takes string pTable,string pKey returns group
    return LoadGroupHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Multiboard
function YDWESaveMultiboardByInteger takes integer pTable,integer pKey,multiboard m returns nothing
    call SaveMultiboardHandle(YDHT, pTable, pKey, m)
endfunction
function YDWESaveMultiboardByString takes string pTable,string pKey,multiboard m returns nothing
    call SaveMultiboardHandle(YDHT, StringHash(pTable), StringHash(pKey), m)
endfunction
function YDWEGetMultiboardByInteger takes integer pTable,integer pKey returns multiboard
    return LoadMultiboardHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetMultiboardByString takes string pTable,string pKey returns multiboard
    return LoadMultiboardHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert MultiboardItem
function YDWESaveMultiboardItemByInteger takes integer pTable,integer pKey,multiboarditem mt returns nothing
    call SaveMultiboardItemHandle(YDHT, pTable, pKey, mt)
endfunction
function YDWESaveMultiboardItemByString takes string pTable,string pKey,multiboarditem mt returns nothing
    call SaveMultiboardItemHandle(YDHT, StringHash(pTable), StringHash(pKey), mt)
endfunction
function YDWEGetMultiboardItemByInteger takes integer pTable,integer pKey returns multiboarditem
    return LoadMultiboardItemHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetMultiboardItemByString takes string pTable,string pKey returns multiboarditem
    return LoadMultiboardItemHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert TextTag
function YDWESaveTextTagByInteger takes integer pTable,integer pKey,texttag tt returns nothing
    call SaveTextTagHandle(YDHT, pTable, pKey, tt)
endfunction
function YDWESaveTextTagByString takes string pTable,string pKey,texttag tt returns nothing
    call SaveTextTagHandle(YDHT, StringHash(pTable), StringHash(pKey), tt)
endfunction
function YDWEGetTextTagByInteger takes integer pTable,integer pKey returns texttag
    return LoadTextTagHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetTextTagByString takes string pTable,string pKey returns texttag
    return LoadTextTagHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Lightning
function YDWESaveLightningByInteger takes integer pTable,integer pKey,lightning ln returns nothing
    call SaveLightningHandle(YDHT, pTable, pKey, ln)
endfunction
function YDWESaveLightningByString takes string pTable,string pKey,lightning ln returns nothing
    call SaveLightningHandle(YDHT, StringHash(pTable), StringHash(pKey), ln)
endfunction
function YDWEGetLightningByInteger takes integer pTable,integer pKey returns lightning
    return LoadLightningHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetLightningByString takes string pTable,string pKey returns lightning
    return LoadLightningHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Region
function YDWESaveRegionByInteger takes integer pTable,integer pKey,region rn returns nothing
    call SaveRegionHandle(YDHT, pTable, pKey, rn)
endfunction
function YDWESaveRegionByString takes string pTable,string pKey,region rt returns nothing
    call SaveRegionHandle(YDHT, StringHash(pTable), StringHash(pKey), rt)
endfunction
function YDWEGetRegionByInteger takes integer pTable,integer pKey returns region
    return LoadRegionHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetRegionByString takes string pTable,string pKey returns region
    return LoadRegionHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Rect
function YDWESaveRectByInteger takes integer pTable,integer pKey,rect rn returns nothing
    call SaveRectHandle(YDHT, pTable, pKey, rn)
endfunction
function YDWESaveRectByString takes string pTable,string pKey,rect rt returns nothing
    call SaveRectHandle(YDHT, StringHash(pTable), StringHash(pKey), rt)
endfunction
function YDWEGetRectByInteger takes integer pTable,integer pKey returns rect
    return LoadRectHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetRectByString takes string pTable,string pKey returns rect
    return LoadRectHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Leaderboard
function YDWESaveLeaderboardByInteger takes integer pTable,integer pKey,leaderboard lb returns nothing
    call SaveLeaderboardHandle(YDHT, pTable, pKey, lb)
endfunction
function YDWESaveLeaderboardByString takes string pTable,string pKey,leaderboard lb returns nothing
    call SaveLeaderboardHandle(YDHT, StringHash(pTable), StringHash(pKey), lb)
endfunction
function YDWEGetLeaderboardByInteger takes integer pTable,integer pKey returns leaderboard
    return LoadLeaderboardHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetLeaderboardByString takes string pTable,string pKey returns leaderboard
    return LoadLeaderboardHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Effect
function YDWESaveEffectByInteger takes integer pTable,integer pKey,effect e returns nothing
    call SaveEffectHandle(YDHT, pTable, pKey, e)
endfunction
function YDWESaveEffectByString takes string pTable,string pKey,effect e returns nothing
    call SaveEffectHandle(YDHT, StringHash(pTable), StringHash(pKey), e)
endfunction
function YDWEGetEffectByInteger takes integer pTable,integer pKey returns effect
    return LoadEffectHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetEffectByString takes string pTable,string pKey returns effect
    return LoadEffectHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert Destructable
function YDWESaveDestructableByInteger takes integer pTable,integer pKey,destructable da returns nothing
    call SaveDestructableHandle(YDHT, pTable, pKey, da)
endfunction
function YDWESaveDestructableByString takes string pTable,string pKey,destructable da returns nothing
    call SaveDestructableHandle(YDHT, StringHash(pTable), StringHash(pKey), da)
endfunction
function YDWEGetDestructableByInteger takes integer pTable,integer pKey returns destructable
    return LoadDestructableHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetDestructableByString takes string pTable,string pKey returns destructable
    return LoadDestructableHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert triggercondition
function YDWESaveTriggerConditionByInteger takes integer pTable,integer pKey,triggercondition tc returns nothing
    call SaveTriggerConditionHandle(YDHT, pTable, pKey, tc)
endfunction
function YDWESaveTriggerConditionByString takes string pTable,string pKey,triggercondition tc returns nothing
    call SaveTriggerConditionHandle(YDHT, StringHash(pTable), StringHash(pKey), tc)
endfunction
function YDWEGetTriggerConditionByInteger takes integer pTable,integer pKey returns triggercondition
    return LoadTriggerConditionHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetTriggerConditionByString takes string pTable,string pKey returns triggercondition
    return LoadTriggerConditionHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert triggeraction
function YDWESaveTriggerActionByInteger takes integer pTable,integer pKey,triggeraction ta returns nothing
    call SaveTriggerActionHandle(YDHT, pTable, pKey, ta)
endfunction
function YDWESaveTriggerActionByString takes string pTable,string pKey,triggeraction ta returns nothing
    call SaveTriggerActionHandle(YDHT, StringHash(pTable), StringHash(pKey), ta)
endfunction
function YDWEGetTriggerActionByInteger takes integer pTable,integer pKey returns triggeraction
    return LoadTriggerActionHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetTriggerActionByString takes string pTable,string pKey returns triggeraction
    return LoadTriggerActionHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert event
function YDWESaveTriggerEventByInteger takes integer pTable,integer pKey,event et returns nothing
    call SaveTriggerEventHandle(YDHT, pTable, pKey, et)
endfunction
function YDWESaveTriggerEventByString takes string pTable,string pKey,event et returns nothing
    call SaveTriggerEventHandle(YDHT, StringHash(pTable), StringHash(pKey), et)
endfunction
function YDWEGetTriggerEventByInteger takes integer pTable,integer pKey returns event
    return LoadTriggerEventHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetTriggerEventByString takes string pTable,string pKey returns event
    return LoadTriggerEventHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert force
function YDWESaveForceByInteger takes integer pTable,integer pKey,force fc returns nothing
    call SaveForceHandle(YDHT, pTable, pKey, fc)
endfunction
function YDWESaveForceByString takes string pTable,string pKey,force fc returns nothing
    call SaveForceHandle(YDHT, StringHash(pTable), StringHash(pKey), fc)
endfunction
function YDWEGetForceByInteger takes integer pTable,integer pKey returns force
    return LoadForceHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetForceByString takes string pTable,string pKey returns force
    return LoadForceHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert boolexpr
function YDWESaveBoolexprByInteger takes integer pTable,integer pKey,boolexpr be returns nothing
    call SaveBooleanExprHandle(YDHT, pTable, pKey, be)
endfunction
function YDWESaveBoolexprByString takes string pTable,string pKey,boolexpr be returns nothing
    call SaveBooleanExprHandle(YDHT, StringHash(pTable), StringHash(pKey), be)
endfunction
function YDWEGetBoolexprByInteger takes integer pTable,integer pKey returns boolexpr
    return LoadBooleanExprHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetBoolexprByString takes string pTable,string pKey returns boolexpr
    return LoadBooleanExprHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert sound
function YDWESaveSoundByInteger takes integer pTable,integer pKey,sound sd returns nothing
    call SaveSoundHandle(YDHT, pTable, pKey, sd)
endfunction
function YDWESaveSoundByString takes string pTable,string pKey,sound sd returns nothing
    call SaveSoundHandle(YDHT, StringHash(pTable), StringHash(pKey), sd)
endfunction
function YDWEGetSoundByInteger takes integer pTable,integer pKey returns sound
    return LoadSoundHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetSoundByString takes string pTable,string pKey returns sound
    return LoadSoundHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert timerdialog
function YDWESaveTimerDialogByInteger takes integer pTable,integer pKey,timerdialog td returns nothing
    call SaveTimerDialogHandle(YDHT, pTable, pKey, td)
endfunction
function YDWESaveTimerDialogByString takes string pTable,string pKey,timerdialog td returns nothing
    call SaveTimerDialogHandle(YDHT, StringHash(pTable), StringHash(pKey), td)
endfunction
function YDWEGetTimerDialogByInteger takes integer pTable,integer pKey returns timerdialog
    return LoadTimerDialogHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetTimerDialogByString takes string pTable,string pKey returns timerdialog
    return LoadTimerDialogHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert trackable
function YDWESaveTrackableByInteger takes integer pTable,integer pKey,trackable ta returns nothing
    call SaveTrackableHandle(YDHT, pTable, pKey, ta)
endfunction
function YDWESaveTrackableByString takes string pTable,string pKey,trackable ta returns nothing
    call SaveTrackableHandle(YDHT, StringHash(pTable), StringHash(pKey), ta)
endfunction
function YDWEGetTrackableByInteger takes integer pTable,integer pKey returns trackable
    return LoadTrackableHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetTrackableByString takes string pTable,string pKey returns trackable
    return LoadTrackableHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert dialog
function YDWESaveDialogByInteger takes integer pTable,integer pKey,dialog d returns nothing
    call SaveDialogHandle(YDHT, pTable, pKey, d)
endfunction
function YDWESaveDialogByString takes string pTable,string pKey,dialog d returns nothing
    call SaveDialogHandle(YDHT, StringHash(pTable), StringHash(pKey), d)
endfunction
function YDWEGetDialogByInteger takes integer pTable,integer pKey returns dialog
    return LoadDialogHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetDialogByString takes string pTable,string pKey returns dialog
    return LoadDialogHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert button
function YDWESaveButtonByInteger takes integer pTable,integer pKey,button bt returns nothing
    call SaveButtonHandle(YDHT, pTable, pKey, bt)
endfunction
function YDWESaveButtonByString takes string pTable,string pKey,button bt returns nothing
    call SaveButtonHandle(YDHT, StringHash(pTable), StringHash(pKey), bt)
endfunction
function YDWEGetButtonByInteger takes integer pTable,integer pKey returns button
    return LoadButtonHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetButtonByString takes string pTable,string pKey returns button
    return LoadButtonHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert quest
function YDWESaveQuestByInteger takes integer pTable,integer pKey,quest qt returns nothing
    call SaveQuestHandle(YDHT, pTable, pKey, qt)
endfunction
function YDWESaveQuestByString takes string pTable,string pKey,quest qt returns nothing
    call SaveQuestHandle(YDHT, StringHash(pTable), StringHash(pKey), qt)
endfunction
function YDWEGetQuestByInteger takes integer pTable,integer pKey returns quest
    return LoadQuestHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetQuestByString takes string pTable,string pKey returns quest
    return LoadQuestHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
//Covert questitem
function YDWESaveQuestItemByInteger takes integer pTable,integer pKey,questitem qi returns nothing
    call SaveQuestItemHandle(YDHT, pTable, pKey, qi)
endfunction
function YDWESaveQuestItemByString takes string pTable,string pKey,questitem qi returns nothing
    call SaveQuestItemHandle(YDHT, StringHash(pTable), StringHash(pKey), qi)
endfunction
function YDWEGetQuestItemByInteger takes integer pTable,integer pKey returns questitem
    return LoadQuestItemHandle(YDHT, pTable, pKey)
endfunction
function YDWEGetQuestItemByString takes string pTable,string pKey returns questitem
    return LoadQuestItemHandle(YDHT, StringHash(pTable), StringHash(pKey))
endfunction
function YDWES2I takes string s returns integer
    return StringHash(s)
endfunction
function YDWESaveAbilityHandleBJ takes integer AbilityID,integer key,integer missionKey,hashtable table returns nothing
    call SaveInteger(table, missionKey, key, AbilityID)
endfunction
function YDWESaveAbilityHandle takes hashtable table,integer parentKey,integer childKey,integer AbilityID returns nothing
    call SaveInteger(table, parentKey, childKey, AbilityID)
endfunction
function YDWELoadAbilityHandleBJ takes integer key,integer missionKey,hashtable table returns integer
    return LoadInteger(table, missionKey, key)
endfunction
function YDWELoadAbilityHandle takes hashtable table,integer parentKey,integer childKey returns integer
    return LoadInteger(table, parentKey, childKey)
endfunction
//===========================================================================
//返回参数
//===========================================================================
//地图边界判断
function YDWECoordinateX takes real x returns real
    return RMinBJ(RMaxBJ(x, yd_MapMinX), yd_MapMaxX)
endfunction
function YDWECoordinateY takes real y returns real
    return RMinBJ(RMaxBJ(y, yd_MapMinY), yd_MapMaxY)
endfunction
//两个单位之间的距离
function YDWEDistanceBetweenUnits takes unit a,unit b returns real
    return SquareRoot(( GetUnitX(a) - GetUnitX(b) ) * ( GetUnitX(a) - GetUnitX(b) ) + ( GetUnitY(a) - GetUnitY(b) ) * ( GetUnitY(a) - GetUnitY(b) ))
endfunction
//两个单位之间的角度
function YDWEAngleBetweenUnits takes unit fromUnit,unit toUnit returns real
    return bj_RADTODEG * Atan2(GetUnitY(toUnit) - GetUnitY(fromUnit), GetUnitX(toUnit) - GetUnitX(fromUnit))
endfunction
//生成区域
function YDWEGetRect takes real x,real y,real width,real height returns rect
    return Rect(x - width * 0.5, y - height * 0.5, x + width * 0.5, y + height * 0.5)
endfunction
//===========================================================================
//设置单位可以飞行
//===========================================================================
function YDWEFlyEnable takes unit u returns nothing
    call UnitAddAbility(u, 'Amrf')
    call UnitRemoveAbility(u, 'Amrf')
endfunction
//===========================================================================
//字符窜与ID转换
//===========================================================================
function YDWEId2S takes integer value returns string
    local string charMap=bj_AllString
    local string result= ""
    local integer remainingValue= value
    local integer charValue
    local integer byteno
    set byteno=0
    loop
        set charValue=ModuloInteger(remainingValue, 256)
        set remainingValue=remainingValue / 256
        set result=SubString(charMap, charValue, charValue + 1) + result
        set byteno=byteno + 1
        exitwhen byteno == 4
    endloop
    return result
endfunction
function YDWES2Id takes string targetstr returns integer
    local string originstr=bj_AllString
    local integer strlength=StringLength(targetstr)
    local integer a=0
local integer b=0
local integer numx=1
local integer result=0
    loop
    exitwhen b > strlength - 1
        set numx=R2I(Pow(256, strlength - 1 - b))
        set a=1
        loop
            exitwhen a > 255
            if SubString(targetstr, b, b + 1) == SubString(originstr, a, a + 1) then
                set result=result + a * numx
                set a=256
            endif
            set a=a + 1
        endloop
        set b=b + 1
    endloop
    return result
endfunction
function YDWES2UnitId takes string targetstr returns integer
    return YDWES2Id(targetstr)
endfunction
function YDWES2ItemId takes string targetstr returns integer
    return YDWES2Id(targetstr)
endfunction
function GetLastAbilityCastingUnit takes nothing returns unit
    return bj_lastAbilityCastingUnit
endfunction
function GetLastAbilityTargetUnit takes nothing returns unit
    return bj_lastAbilityTargetUnit
endfunction
function YDWESetMapLimitCoordinate takes real MinX,real MaxX,real MinY,real MaxY returns nothing
    set yd_MapMaxX=MaxX
    set yd_MapMinX=MinX
    set yd_MapMaxY=MaxY
    set yd_MapMinY=MinY
endfunction
//===========================================================================
//===========================================================================
//地图初始化
//===========================================================================
//YDWE特殊技能结束事件 
function YDWESyStemAbilityCastingOverTriggerAction takes unit hero,integer index returns nothing
 local integer i= 0
    loop
        exitwhen i >= YDWEBase___AbilityCastingOverEventNumber
        if YDWEBase___AbilityCastingOverEventType[i] == index then
            set bj_lastAbilityCastingUnit=hero
			if YDWEBase___AbilityCastingOverEventQueue[i] != null and TriggerEvaluate(YDWEBase___AbilityCastingOverEventQueue[i]) and IsTriggerEnabled(YDWEBase___AbilityCastingOverEventQueue[i]) then
				call TriggerExecute(YDWEBase___AbilityCastingOverEventQueue[i])
			endif
		endif
        set i=i + 1
    endloop
endfunction
//===========================================================================  
//YDWE技能捕捉事件 
//===========================================================================  
function YDWESyStemAbilityCastingOverRegistTrigger takes trigger trg,integer index returns nothing
	set YDWEBase___AbilityCastingOverEventQueue[YDWEBase___AbilityCastingOverEventNumber]=trg
	set YDWEBase___AbilityCastingOverEventType[YDWEBase___AbilityCastingOverEventNumber]=index
	set YDWEBase___AbilityCastingOverEventNumber=YDWEBase___AbilityCastingOverEventNumber + 1
endfunction 
//===========================================================================
//系统函数完善
//===========================================================================
function YDWECreateUnitPool takes nothing returns nothing
    set bj_lastCreatedUnitPool=CreateUnitPool()
endfunction
function YDWEPlaceRandomUnit takes unitpool up,player p,real x,real y,real face returns nothing
set bj_lastPoolAbstractedUnit=PlaceRandomUnit(up, p, x, y, face)
endfunction
function YDWEGetLastUnitPool takes nothing returns unitpool
    return bj_lastCreatedUnitPool
endfunction
function YDWEGetLastPoolAbstractedUnit takes nothing returns unit
    return bj_lastPoolAbstractedUnit
endfunction
function YDWECreateItemPool takes nothing returns nothing
    set bj_lastCreatedItemPool=CreateItemPool()
endfunction
function YDWEPlaceRandomItem takes itempool ip,real x,real y returns nothing
set bj_lastPoolAbstractedItem=PlaceRandomItem(ip, x, y)
endfunction
function YDWEGetLastItemPool takes nothing returns itempool
    return bj_lastCreatedItemPool
endfunction
function YDWEGetLastPoolAbstractedItem takes nothing returns item
    return bj_lastPoolAbstractedItem
endfunction
function YDWESetAttackDamageWeaponType takes attacktype at,damagetype dt,weapontype wt returns nothing
    set bj_lastSetAttackType=at
    set bj_lastSetDamageType=dt
    set bj_lastSetWeaponType=wt
endfunction
//unitpool bj_lastCreatedPool=null
//unit bj_lastPoolAbstractedUnit=null
function YDWEGetPlayerColorString takes player p,string s returns string
    return YDWEBase___yd_PlayerColor[GetHandleId(GetPlayerColor(p))] + s + "|r"
endfunction
//===========================================================================
//===========================================================================
//系统函数补充
//===========================================================================
//===========================================================================
function YDWEGetUnitItemSoftId takes unit hero,item it returns integer
    local integer i= 0
    loop
         exitwhen i > 5
         if UnitItemInSlot(hero, i) == it then
            return i + 1
         endif
         set i=i + 1
    endloop
    return 0
endfunction
//===========================================================================
//===========================================================================
//地图初始化
//===========================================================================
//===========================================================================
//显示版本
function YDWEVersion_Display takes nothing returns boolean
    call DisplayTimedTextToPlayer(GetTriggerPlayer(), 0, 0, 30, "|cFF1E90FF当前编辑器版本为： |r|cFF00FF00KKWE 1.1.0.2372")
    return false
endfunction
function YDWEVersion_Init takes nothing returns nothing
    local trigger t= CreateTrigger()
    local integer i= 0
    loop
        exitwhen i == 12
        call TriggerRegisterPlayerChatEvent(t, Player(i), "KKWE Version", true)
        set i=i + 1
    endloop
    call TriggerAddCondition(t, Condition(function YDWEVersion_Display))
    set t=null
endfunction
function InitializeYD takes nothing returns nothing
     set YDHT=InitHashtable()
	//=================设置变量=====================
	set yd_MapMinX=GetCameraBoundMinX() - GetCameraMargin(CAMERA_MARGIN_LEFT)
	set yd_MapMinY=GetCameraBoundMinY() - GetCameraMargin(CAMERA_MARGIN_BOTTOM)
	set yd_MapMaxX=GetCameraBoundMaxX() + GetCameraMargin(CAMERA_MARGIN_RIGHT)
	set yd_MapMaxY=GetCameraBoundMaxY() + GetCameraMargin(CAMERA_MARGIN_TOP)
	
    set YDWEBase___yd_PlayerColor[0]="|cFFFF0303"
    set YDWEBase___yd_PlayerColor[1]="|cFF0042FF"
    set YDWEBase___yd_PlayerColor[2]="|cFF1CE6B9"
    set YDWEBase___yd_PlayerColor[3]="|cFF540081"
    set YDWEBase___yd_PlayerColor[4]="|cFFFFFC01"
    set YDWEBase___yd_PlayerColor[5]="|cFFFE8A0E"
    set YDWEBase___yd_PlayerColor[6]="|cFF20C000"
    set YDWEBase___yd_PlayerColor[7]="|cFFE55BB0"
    set YDWEBase___yd_PlayerColor[8]="|cFF959697"
    set YDWEBase___yd_PlayerColor[9]="|cFF7EBFF1"
    set YDWEBase___yd_PlayerColor[10]="|cFF106246"
    set YDWEBase___yd_PlayerColor[11]="|cFF4E2A04"
    set YDWEBase___yd_PlayerColor[12]="|cFF282828"
    set YDWEBase___yd_PlayerColor[13]="|cFF282828"
    set YDWEBase___yd_PlayerColor[14]="|cFF282828"
    set YDWEBase___yd_PlayerColor[15]="|cFF282828"
    //=================显示版本=====================
    call YDWEVersion_Init()
endfunction

//library YDWEBase ends
//library YDWEWakePlayerUnitsNull:
function YDWEWakePlayerUnitsNull takes player whichPlayer returns nothing
    local group g= CreateGroup()
    call GroupEnumUnitsOfPlayer(g, whichPlayer, null)
    call ForGroup(g, function WakePlayerUnitsEnum)
    call DestroyGroup(g)
    set g=null
endfunction

//library YDWEWakePlayerUnitsNull ends
//library AttackMonsterSystem:
// 临时变量用于延迟创建怪物
// ============================================================================
// 怪物创建函数
// ============================================================================
// 根据类型和当前波次创建怪物
function CreateMonsterOfType takes integer monsterType,integer wave returns unit
    local unit newMonster= null
    local integer monsterId= 0
    local real scaledHp= 0
    local real scaledDamage= 0
    local real scaledSpeed= 0
    local integer playerId= PLAYER_EVIL

    // 根据类型选择怪物ID
    if monsterType == MONSTER_TYPE_NORMAL then
        set monsterId=MONSTER_ID_NORMAL
        set scaledHp=100 * Pow(WAVE_HP_MULTIPLIER, wave)
        set scaledDamage=20 * Pow(WAVE_DAMAGE_MULTIPLIER, wave)
        set scaledSpeed=300 * Pow(WAVE_SPEED_MULTIPLIER, wave)
    elseif monsterType == MONSTER_TYPE_TANK then
        set monsterId=MONSTER_ID_TANK
        set scaledHp=300 * Pow(WAVE_HP_MULTIPLIER, wave)
        set scaledDamage=15 * Pow(WAVE_DAMAGE_MULTIPLIER, wave)
        set scaledSpeed=250 * Pow(WAVE_SPEED_MULTIPLIER, wave)
    elseif monsterType == MONSTER_TYPE_DPS then
        set monsterId=MONSTER_ID_DPS
        set scaledHp=75 * Pow(WAVE_HP_MULTIPLIER, wave)
        set scaledDamage=40 * Pow(WAVE_DAMAGE_MULTIPLIER, wave)
        set scaledSpeed=270 * Pow(WAVE_SPEED_MULTIPLIER, wave)
    elseif monsterType == MONSTER_TYPE_SPECIAL then
        set monsterId=MONSTER_ID_SPECIAL
        set scaledHp=150 * Pow(WAVE_HP_MULTIPLIER, wave)
        set scaledDamage=25 * Pow(WAVE_DAMAGE_MULTIPLIER, wave)
        set scaledSpeed=280 * Pow(WAVE_SPEED_MULTIPLIER, wave)
    endif
    // 在指定坐标创建怪物单位
    set newMonster=CreateUnit(Player(playerId), monsterId, SPAWN_POINT_X, SPAWN_POINT_Y, 0)
    // 应用缩放后的属性
    if newMonster != null then
        // 设置基于当前波次的血量
        call SetUnitState(newMonster, UNIT_STATE_LIFE, scaledHp)
        // 注意: 魔兽争霸3的JASS不支持直接修改伤害
        // 我们需依靠编辑器中的单位配置设置基础伤害
        // 设置移动速度
        call SetUnitMoveSpeed(newMonster, R2I(scaledSpeed))
        // 在追踪数组中存储怪物
        set udg_spawned_monsters[udg_spawned_monster_count]=newMonster
        set udg_spawned_monster_count=udg_spawned_monster_count + 1
    endif
    return newMonster
endfunction
// ============================================================================
// 怪物AI函数
// ============================================================================
// 为怪物应用基本AI行为
function ApplyMonsterBehavior takes unit monster returns nothing
    if monster == null then
        return
    endif
    // 命令怪物移动到目标坐标
    call IssuePointOrder(monster, "attack", TARGET_POINT_X, TARGET_POINT_Y)
endfunction
// 用于延迟生成怪物的辅助函数
function DelayedMonsterSpawn takes nothing returns nothing
    local unit delayedMonster= CreateMonsterOfType(udg_temp_monster_type , udg_temp_wave_number)
    if delayedMonster != null then
        call ApplyMonsterBehavior(delayedMonster)
        set udg_total_monsters_spawned=udg_total_monsters_spawned + 1
    endif
endfunction
// ============================================================================
// 波次管理函数
// ============================================================================
// 主要函数 - 生成一波怪物
function SpawnWaveOfMonsters takes integer waveNumber returns nothing
    local integer monsterIdx= 1
    local unit newMonster= null
    local real spawnDelay= 0.0
    local integer monster_array_index= 0
    local timer tempTimer= null
    if waveNumber > MAX_WAVE_COUNT then
        // 达到最大波次，可能需要处理胜利条件
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "所有波次完成！防守成功！")
        set udg_defense_system_active=false
        return
    endif
    // 初始化此波次的怪物数量
    set udg_monsters_remaining=udg_monster_count_per_wave[waveNumber]
    set udg_total_monsters_spawned=0
    // 显示波次通知
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "第 " + I2S(waveNumber) + " 波来袭！ " + I2S(udg_monsters_remaining) + " 个怪物接近！")
    // 延迟生成波次中的每个怪物
    loop
        exitwhen monsterIdx > udg_monster_count_per_wave[waveNumber]
        // 计算生成延迟以错开怪物生成
        set spawnDelay=( monsterIdx - 1 ) * MONSTER_SPAWN_INTERVAL
        // 获取正确的怪物类型索引
        set monster_array_index=GetMonsterIndex(waveNumber , monsterIdx)
        // 设置临时变量用于延迟函数
        set udg_temp_monster_type=udg_monster_types_per_wave[monster_array_index]
        set udg_temp_wave_number=waveNumber
        // 创建临时计时器延迟每个怪物生成
        set tempTimer=CreateTimer()
        call TimerStart(tempTimer, spawnDelay, false, function DelayedMonsterSpawn)
        set monsterIdx=monsterIdx + 1
    endloop
    // 重置局部变量释放内存
    set tempTimer=null
    set monster_array_index=0
endfunction
// 开始下一波
function SpawnNextWave takes nothing returns nothing
    if udg_defense_system_active then
        call SpawnWaveOfMonsters(udg_current_wave)
    endif
    call TimerDialogDisplay(udg_next_wave_timer_dialog, false)
endfunction
// 进入下一波
function AdvanceToNextWave takes nothing returns nothing
    set udg_current_wave=udg_current_wave + 1
    // 打印调试信息 (将替换为适当的UI通知)
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "第 " + I2S(udg_current_wave) + " 波完成！准备下一波...")
    // 延迟后开始下一波
    call TimerStart(udg_next_wave_timer, EVERY_WAVE_DELAY, false, function SpawnNextWave)
    call TimerDialogDisplay(udg_next_wave_timer_dialog, true)
endfunction
// 怪物死亡时的回调函数
function OnMonsterDeath takes nothing returns nothing
    local unit dyingMonster= GetDyingUnit()
    local integer i= 0
    // 检查此单位是否是我们生成的怪物之一
    loop
        exitwhen i >= udg_spawned_monster_count
        if udg_spawned_monsters[i] == dyingMonster then
            // 从追踪数组中移除此怪物
            set udg_spawned_monsters[i]=udg_spawned_monsters[udg_spawned_monster_count - 1]
            set udg_spawned_monster_count=udg_spawned_monster_count - 1
            set udg_monsters_remaining=udg_monsters_remaining - 1
            // 检查波次是否完成
            if udg_monsters_remaining <= 10 then
                call AdvanceToNextWave()
            endif
            return
        endif
        set i=i + 1
    endloop
endfunction
// 开始第一波
function StartFirstWave takes nothing returns nothing
    if udg_defense_system_active and udg_current_wave == 0 then
        set udg_current_wave=1
        call SpawnWaveOfMonsters(1)
    endif
    if TEST_MODE then
        call BJDebugMsg("StartFirstWave!!!")
    endif
    call TimerDialogDisplay(udg_wave_spawn_timer_dialog, false)
endfunction
// 初始化防守系统
function InitDefenseSystem takes nothing returns nothing
    local trigger monsterDeathTrigger= null
    // 重置波次计数器
    set udg_current_wave=0
    set udg_monsters_remaining=0
    set udg_spawned_monster_count=0
    set udg_total_monsters_spawned=0
    set udg_defense_system_active=true
    // 创建触发器检测怪物死亡
    set monsterDeathTrigger=CreateTrigger()
    // 注册中立敌对单位的死亡事件
    call TriggerRegisterAnyUnitEventBJ(monsterDeathTrigger, EVENT_PLAYER_UNIT_DEATH)
    call TriggerAddAction(monsterDeathTrigger, function OnMonsterDeath)
    // 如果尚未初始化则初始化波次数据
    call InitializeMonsterWaves()
    // 显示开始消息
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "防守系统激活！准备第1波！")
    call TimerStart(udg_wave_spawn_timer, I2R(FIRST_WAVE_DELAY), false, function StartFirstWave)
    
    call TimerDialogSetTitle(udg_wave_spawn_timer_dialog, "距离第1波：")
    call TimerDialogDisplay(udg_wave_spawn_timer_dialog, true)
endfunction
// 清理所有生成的怪物
function ClearAllMonsters takes nothing returns nothing
    local integer i= 0
    local unit currentUnit= null
    loop
        exitwhen i >= udg_spawned_monster_count
        set currentUnit=udg_spawned_monsters[i]
        if currentUnit != null then
            call RemoveUnit(currentUnit)
            set udg_spawned_monsters[i]=null // 清除引用
endif
        set i=i + 1
    endloop
    set udg_spawned_monster_count=0
    set udg_monsters_remaining=0
endfunction
// 停用防守系统
function DeactivateDefenseSystem takes nothing returns nothing
    set udg_defense_system_active=false
    call ClearAllMonsters()
    call PauseTimer(udg_wave_spawn_timer)
    call PauseTimer(udg_next_wave_timer)
    call DestroyTimer(udg_wave_spawn_timer) // 释放计时器资源
call DestroyTimer(udg_next_wave_timer) // 释放计时器资源
endfunction

//library AttackMonsterSystem ends
//library CommonFunction:
    // ==========================================
    // 辅助函数
    // ==========================================
    // 获取玩家英雄单位
    function Hero_GetPlayerHero takes integer player_id returns unit
        return udg_player_hero[player_id]
    endfunction
    // 获取玩家英雄ID
    function Hero_GetPlayerHeroId takes integer player_id returns integer
        return udg_player_hero_id[player_id]
    endfunction
    // 检查单位是否为本局英雄
    function Hero_IsPlayerHero takes unit unit_id returns boolean
        return IsUnitType(unit_id, UNIT_TYPE_HERO)
    endfunction
    // 获取英雄名称
    function Hero_GetName takes integer hero_id returns string
        local string name
        if hero_id == HERO_RUODIE then
            set name="若蝶"
        elseif hero_id == HERO_XIAOXIA then
            set name="潇侠"
        elseif hero_id == HERO_ZHANHEN then
            set name="斩恨"
        elseif hero_id == HERO_JINXUAN then
            set name="瑾轩"
        elseif hero_id == HERO_KONGYAO then
            set name="空瑶"
        elseif hero_id == HERO_JIANDAO then
            set name="剑刀"
        elseif hero_id == HERO_SHENXING then
            set name="神行"
        elseif hero_id == HERO_CANGLANG then
            set name="苍狼"
        elseif hero_id == HERO_HONGLING then
            set name="红绫"
        elseif hero_id == HERO_YUEHUA then
            set name="月华"
        else
            set name="未知"
        endif
        return name
    endfunction
    // 获取英雄被动名称
    function HeroPassive_GetName takes integer hero_id returns string
        local string name
        if hero_id == HERO_RUODIE then
            set name="蝶舞"
        elseif hero_id == HERO_XIAOXIA then
            set name="侠义"
        elseif hero_id == HERO_ZHANHEN then
            set name="杀伐"
        elseif hero_id == HERO_JINXUAN then
            set name="谋略"
        elseif hero_id == HERO_KONGYAO then
            set name="仙影"
        elseif hero_id == HERO_JIANDAO then
            set name="铁壁"
        elseif hero_id == HERO_SHENXING then
            set name="敏捷"
        elseif hero_id == HERO_CANGLANG then
            set name="狂野"
        elseif hero_id == HERO_HONGLING then
            set name="灵犀"
        elseif hero_id == HERO_YUEHUA then
            set name="仙子"
        else
            set name="无"
        endif
        return name
    endfunction
    // 清理玩家英雄数据
    function Hero_CleanupPlayer takes integer player_id returns nothing
        set udg_player_hero[player_id]=null
        set udg_player_hero_id[player_id]=0
    endfunction
    // ============================================================================
    // Distance Between Points
    // ============================================================================
    // 计算两点之间的距离
    // ============================================================================
    function DistanceBetweenPointsEx takes real x1,real y1,real x2,real y2 returns real
        local real dx
        local real dy
        set dx=x2 - x1
        set dy=y2 - y1
        return SquareRoot(dx * dx + dy * dy)
    endfunction
    // ============================================================================
    // Get Game Time
    // ============================================================================
    // 获取游戏时间
    // ============================================================================
    function GetGameTime takes nothing returns real
        return udg_game_time
    endfunction
    // 判断玩家是否为用户
    function IsPlayerUser takes player p returns boolean
        return GetPlayerSlotState(p) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(p) == MAP_CONTROL_USER
    endfunction

//library CommonFunction ends
//library DungeonMonsterData:
// ============================================================================
// 检查角色类型是否有效
// ============================================================================
function DungeonMonsterData___IsValidRoleType takes integer role_type returns boolean
    // 角色类型范围: 1-6
    return role_type >= ROLE_TYPE_MELEE_DPS and role_type <= ROLE_TYPE_SUMMONER
endfunction
// ============================================================================
// 检查小怪索引是否有效
// ============================================================================
function DungeonMonsterData___IsValidMonsterIndex takes integer index returns boolean
    // 小怪索引范围: 101 (1*100+1) 到 614 (6*100+14)
    return index >= 101 and index <= 614
endfunction
// ============================================================================
// 检查BOSS索引是否有效
// ============================================================================
function DungeonMonsterData___IsValidBossIndex takes integer index returns boolean
    // BOSS索引范围: 101 (1*100+1) 到 514 (5*100+14)
    return index >= 101 and index <= 514
endfunction
// ============================================================================
// 检查技能ID是否有效
// ============================================================================
function DungeonMonsterData___IsValidSkillId takes integer skill_id returns boolean
    // 使用常量定义技能ID范围
    return skill_id >= SKILL_ID_MIN and skill_id <= SKILL_ID_MAX
endfunction
// ============================================================================
// 检查BOSS类型是否有效
// ============================================================================
function DungeonMonsterData___IsValidBossType takes integer boss_type returns boolean
    // BOSS类型范围: 1-5
    return boss_type >= BOSS_TYPE_STRENGTH and boss_type <= BOSS_TYPE_SUMMONER
endfunction
// ============================================================================
// 检查主题类型是否有效
// ============================================================================
function IsValidThemeType takes integer theme_type returns boolean
    // 主题类型范围: 1-14
    return theme_type >= THEME_TYPE_HEIFENG and theme_type <= THEME_TYPE_FINAL
endfunction
// ============================================================================
// 检查技能类型是否有效
// ============================================================================
function DungeonMonsterData___IsValidSkillType takes integer skill_type returns boolean
    // 技能类型范围: 1-8
    return skill_type >= SKILL_TYPE_ATTACK and skill_type <= SKILL_TYPE_AOE
endfunction
// ============================================================================
// MonsterData_GetMonsterIndex
// ============================================================================
// 计算小怪配置索引
// 参数:
//   role_type - 角色类型 (1-6)
//   theme_type - 主题类型 (1-14)
// 返回: 小怪配置索引，如果参数无效则返回0
// ============================================================================
function MonsterData_GetMonsterIndex takes integer role_type,integer theme_type returns integer
    // 参数验证，防止索引计算溢出
    if not DungeonMonsterData___IsValidRoleType(role_type) or not IsValidThemeType(theme_type) then
        return 0
    endif
    call DisplayTextToPlayer(Player(0), 0, 0, "|cffff0000[系统]|r计算小怪索引: 角色类型=" + I2S(role_type) + ", 主题类型=" + I2S(theme_type))
    return ( role_type * 100 ) + theme_type
endfunction
// ============================================================================
// MonsterData_GetBossIndex
// ============================================================================
// 计算BOSS配置索引
// 参数:
//   boss_type - BOSS类型 (1-5)
//   theme_type - 主题类型 (1-14)
// 返回: BOSS配置索引，如果参数无效则返回0
// ============================================================================
function MonsterData_GetBossIndex takes integer boss_type,integer theme_type returns integer
    // 参数验证，防止索引计算溢出
    if not DungeonMonsterData___IsValidBossType(boss_type) or not IsValidThemeType(theme_type) then
        return 0
    endif
    return ( boss_type * 100 ) + theme_type
endfunction
// ============================================================================
// 显示错误消息
// ============================================================================
function DungeonMonsterData___ShowError takes string message returns nothing
    // 使用第一个玩家显示错误，避免多人游戏不同步
    call DisplayTextToPlayer(Player(0), 0, 0, "|cffff0000[系统]|r怪物数据错误: " + message)
endfunction
// ============================================================================
// 检查怪物数据是否已初始化
// ============================================================================
function DungeonMonsterData___CheckMonsterDataInitialized takes nothing returns boolean
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return false
    endif
    return true
endfunction
// ============================================================================
// 设置小怪类型配置
// ============================================================================
function MonsterData_SetMonsterType takes integer role_type,integer theme_type,integer unit_id,integer base_hp,integer base_attack,integer base_defense,integer move_speed,integer attack_range returns nothing
    local integer index
    // 参数验证
    if not DungeonMonsterData___IsValidRoleType(role_type) then
        call DungeonMonsterData___ShowError("角色类型超出范围 (1-6)")
        return
    endif
    if not IsValidThemeType(theme_type) then
        call DungeonMonsterData___ShowError("主题类型超出范围 (1-14)")
        return
    endif
    if base_hp < 0 then
        call DungeonMonsterData___ShowError("基础生命值不能为负数")
        return
    endif
    if base_attack < 0 then
        call DungeonMonsterData___ShowError("基础攻击力不能为负数")
        return
    endif
    if base_defense < 0 then
        call DungeonMonsterData___ShowError("基础防御不能为负数")
        return
    endif
    if move_speed < 0 then
        call DungeonMonsterData___ShowError("移动速度不能为负数")
        return
    endif
    if attack_range < 0 then
        call DungeonMonsterData___ShowError("攻击范围不能为负数")
        return
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    call DisplayTextToPlayer(Player(0), 0, 0, "|cffff0000[系统]|r设置小怪类型配置: 角色类型=" + I2S(role_type) + ", 主题类型=" + I2S(theme_type) + ", 单位ID=" + I2S(unit_id) + ", 基础生命值=" + I2S(base_hp) + ", 基础攻击力=" + I2S(base_attack) + ", 基础防御=" + I2S(base_defense) + ", 移动速度=" + I2S(move_speed) + ", 攻击范围=" + I2S(attack_range))
    call DisplayTextToPlayer(Player(0), 0, 0, "index=" + I2S(index))
    set udg_monster_unit_id[index]=unit_id
    set udg_monster_base_hp[index]=base_hp
    set udg_monster_base_attack[index]=base_attack
    set udg_monster_base_defense[index]=base_defense
    set udg_monster_move_speed[index]=move_speed
    set udg_monster_attack_range[index]=attack_range
endfunction
// ============================================================================
// 设置小怪技能配置
// ============================================================================
function MonsterData_SetMonsterSkill takes integer role_type,integer theme_type,integer skill_id,integer skill_type returns nothing
    local integer index
    // 参数验证
    if not DungeonMonsterData___IsValidRoleType(role_type) then
        call DungeonMonsterData___ShowError("角色类型超出范围 (1-6)")
        return
    endif
    if not IsValidThemeType(theme_type) then
        call DungeonMonsterData___ShowError("主题类型超出范围 (1-14)")
        return
    endif
    if not DungeonMonsterData___IsValidSkillId(skill_id) then
        call DungeonMonsterData___ShowError("技能ID超出范围 (1001-1014)")
        return
    endif
    if not DungeonMonsterData___IsValidSkillType(skill_type) then
        call DungeonMonsterData___ShowError("技能类型超出范围 (1-8)")
        return
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    set udg_monster_skill_id[index]=skill_id
    set udg_monster_skill_type[index]=skill_type
endfunction
// ============================================================================
// 设置BOSS配置
// ============================================================================
function MonsterData_SetBossConfig takes integer boss_type,integer theme_type,integer unit_id,integer base_hp,integer base_attack,integer base_defense,integer move_speed,integer attack_range,integer attribute_bonus returns nothing
    local integer index
    // 参数验证
    if not DungeonMonsterData___IsValidBossType(boss_type) then
        call DungeonMonsterData___ShowError("BOSS类型超出范围 (1-5)")
        return
    endif
    if not IsValidThemeType(theme_type) then
        call DungeonMonsterData___ShowError("主题类型超出范围 (1-14)")
        return
    endif
    if base_hp < 0 then
        call DungeonMonsterData___ShowError("基础生命值不能为负数")
        return
    endif
    if base_attack < 0 then
        call DungeonMonsterData___ShowError("基础攻击力不能为负数")
        return
    endif
    if base_defense < 0 then
        call DungeonMonsterData___ShowError("基础防御不能为负数")
        return
    endif
    if move_speed < 0 then
        call DungeonMonsterData___ShowError("移动速度不能为负数")
        return
    endif
    if attack_range < 0 then
        call DungeonMonsterData___ShowError("攻击范围不能为负数")
        return
    endif
    if attribute_bonus < 0 or attribute_bonus > 100 then
        call DungeonMonsterData___ShowError("属性加成百分比超出范围 (0-100)")
        return
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    set udg_boss_unit_id[index]=unit_id
    set udg_boss_base_hp[index]=base_hp
    set udg_boss_base_attack[index]=base_attack
    set udg_boss_base_defense[index]=base_defense
    set udg_boss_move_speed[index]=move_speed
    set udg_boss_attack_range[index]=attack_range
    set udg_boss_attribute_bonus[index]=attribute_bonus
endfunction
// ============================================================================
// 设置BOSS技能配置
// ============================================================================
function MonsterData_SetBossSkill takes integer boss_type,integer theme_type,integer skill_id,integer skill_type returns nothing
    local integer index
    // 参数验证
    if not DungeonMonsterData___IsValidBossType(boss_type) then
        call DungeonMonsterData___ShowError("BOSS类型超出范围 (1-5)")
        return
    endif
    if not IsValidThemeType(theme_type) then
        call DungeonMonsterData___ShowError("主题类型超出范围 (1-14)")
        return
    endif
    if not DungeonMonsterData___IsValidSkillId(skill_id) then
        call DungeonMonsterData___ShowError("技能ID超出范围 (1001-1014)")
        return
    endif
    if not DungeonMonsterData___IsValidSkillType(skill_type) then
        call DungeonMonsterData___ShowError("技能类型超出范围 (1-8)")
        return
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    set udg_boss_skill_id[index]=skill_id
    set udg_boss_skill_type[index]=skill_type
endfunction
// ============================================================================
// MonsterData_GetMonsterUnitId
// ============================================================================
// 获取小怪单位ID
// 参数:
//   role_type - 角色类型 (1-6)
//   theme_type - 主题类型 (1-14)
// 返回: 小怪单位ID，如果数据未初始化或参数无效则返回0
// ============================================================================
function MonsterData_GetMonsterUnitId takes integer role_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not DungeonMonsterData___CheckMonsterDataInitialized() then
        return 0
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidMonsterIndex(index) then
        return 0
    endif
    return udg_monster_unit_id[index]
endfunction
// ============================================================================
// 获取小怪基础生命值
// ============================================================================
function MonsterData_GetMonsterBaseHp takes integer role_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidMonsterIndex(index) then
        return 0
    endif
    return udg_monster_base_hp[index]
endfunction
// ============================================================================
// 获取小怪基础攻击力
// ============================================================================
function MonsterData_GetMonsterBaseAttack takes integer role_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidMonsterIndex(index) then
        return 0
    endif
    return udg_monster_base_attack[index]
endfunction
// ============================================================================
// 获取小怪基础防御
// ============================================================================
function MonsterData_GetMonsterBaseDefense takes integer role_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidMonsterIndex(index) then
        return 0
    endif
    return udg_monster_base_defense[index]
endfunction
// ============================================================================
// 获取小怪移动速度
// ============================================================================
function MonsterData_GetMonsterMoveSpeed takes integer role_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidMonsterIndex(index) then
        return 0
    endif
    return udg_monster_move_speed[index]
endfunction
// ============================================================================
// 获取小怪攻击范围
// ============================================================================
function MonsterData_GetMonsterAttackRange takes integer role_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidMonsterIndex(index) then
        return 0
    endif
    return udg_monster_attack_range[index]
endfunction
// ============================================================================
// 获取小怪技能ID
// ============================================================================
function MonsterData_GetMonsterSkillId takes integer role_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidMonsterIndex(index) then
        return 0
    endif
    return udg_monster_skill_id[index]
endfunction
// ============================================================================
// 获取小怪技能类型
// ============================================================================
function MonsterData_GetMonsterSkillType takes integer role_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetMonsterIndex(role_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidMonsterIndex(index) then
        return 0
    endif
    return udg_monster_skill_type[index]
endfunction
// ============================================================================
// 获取BOSS单位ID
// ============================================================================
function MonsterData_GetBossUnitId takes integer boss_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidBossIndex(index) then
        return 0
    endif
    return udg_boss_unit_id[index]
endfunction
// ============================================================================
// 获取BOSS基础生命值
// ============================================================================
function MonsterData_GetBossBaseHp takes integer boss_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidBossIndex(index) then
        return 0
    endif
    return udg_boss_base_hp[index]
endfunction
// ============================================================================
// 获取BOSS基础攻击力
// ============================================================================
function MonsterData_GetBossBaseAttack takes integer boss_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidBossIndex(index) then
        return 0
    endif
    return udg_boss_base_attack[index]
endfunction
// ============================================================================
// 获取BOSS基础防御
// ============================================================================
function MonsterData_GetBossBaseDefense takes integer boss_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidBossIndex(index) then
        return 0
    endif
    return udg_boss_base_defense[index]
endfunction
// ============================================================================
// 获取BOSS移动速度
// ============================================================================
function MonsterData_GetBossMoveSpeed takes integer boss_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidBossIndex(index) then
        return 0
    endif
    return udg_boss_move_speed[index]
endfunction
// ============================================================================
// 获取BOSS攻击范围
// ============================================================================
function MonsterData_GetBossAttackRange takes integer boss_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidBossIndex(index) then
        return 0
    endif
    return udg_boss_attack_range[index]
endfunction
// ============================================================================
// 获取BOSS技能ID
// ============================================================================
function MonsterData_GetBossSkillId takes integer boss_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidBossIndex(index) then
        return 0
    endif
    return udg_boss_skill_id[index]
endfunction
// ============================================================================
// 获取BOSS技能类型
// ============================================================================
function MonsterData_GetBossSkillType takes integer boss_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidBossIndex(index) then
        return 0
    endif
    return udg_boss_skill_type[index]
endfunction
// ============================================================================
// 获取BOSS属性加成
// ============================================================================
function MonsterData_GetBossAttributeBonus takes integer boss_type,integer theme_type returns integer
    local integer index
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    set index=MonsterData_GetBossIndex(boss_type , theme_type)
    if index == 0 or not DungeonMonsterData___IsValidBossIndex(index) then
        return 0
    endif
    return udg_boss_attribute_bonus[index]
endfunction
// ============================================================================
// 获取技能名称
// ============================================================================
function MonsterData_GetSkillName takes integer skill_id returns string
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return ""
    endif
    if not DungeonMonsterData___IsValidSkillId(skill_id) then
        return ""
    endif
    return s__Skill_skill_name[GetSkillById(skill_id)]
endfunction
// ============================================================================
// 获取技能类型
// ============================================================================
function MonsterData_GetSkillType takes integer skill_id returns integer
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    if not DungeonMonsterData___IsValidSkillId(skill_id) then
        return 0
    endif
    return s__Skill_skill_type[GetSkillById(skill_id)]
endfunction
// ============================================================================
// 获取技能伤害
// ============================================================================
function MonsterData_GetSkillDamage takes integer skill_id returns real
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0.0
    endif
    if not DungeonMonsterData___IsValidSkillId(skill_id) then
        return 0.0
    endif
    return s__Skill_skill_damage_coefficient[GetSkillById(skill_id)]
endfunction
// ============================================================================
// 获取技能冷却时间
// ============================================================================
function MonsterData_GetSkillCooldown takes integer skill_id returns real
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0.0
    endif
    if not DungeonMonsterData___IsValidSkillId(skill_id) then
        return 0.0
    endif
    return s__Skill_skill_cooldown[GetSkillById(skill_id)]
endfunction
// ============================================================================
// 获取技能魔法消耗
// ============================================================================
function MonsterData_GetSkillManaCost takes integer skill_id returns integer
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0
    endif
    if not DungeonMonsterData___IsValidSkillId(skill_id) then
        return 0
    endif
    return s__Skill_skill_magic_cost[GetSkillById(skill_id)]
endfunction
// ============================================================================
// 获取技能范围
// ============================================================================
function MonsterData_GetSkillRange takes integer skill_id returns real
    // 检查数据是否已初始化
    if not udg_monster_data_initialized then
        call DungeonMonsterData___ShowError("怪物数据未初始化")
        return 0.0
    endif
    if not DungeonMonsterData___IsValidSkillId(skill_id) then
        return 0.0
    endif
    return s__Skill_skill_cast_range[GetSkillById(skill_id)]
endfunction
// ============================================================================
// 初始化怪物数据
// ============================================================================
function InitDungeonMonsterData takes nothing returns nothing
    local integer role_type
    local integer theme_type
    local integer boss_type
    local integer skill_id
    // 初始化标记
    set udg_monster_data_initialized=true
    // ========================================================================
    // 初始化黑风寨主题小怪配置 (THEME_TYPE_HEIFENG = 1)
    // ========================================================================
    set theme_type=THEME_TYPE_HEIFENG
    // 近战输出小怪
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n101' , 400 , 25 , 3 , 280 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_NORMAL_ATTACK , SKILL_TYPE_ATTACK)
    // 远程射手小怪
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n102' , 300 , 20 , 2 , 300 , 550)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_RANGE_SHOT , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n103' , 600 , 15 , 10 , 240 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_DEFENSIVE_STANCE , SKILL_TYPE_DEFENSE)
    // 法师控制小怪
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n104' , 250 , 30 , 1 , 270 , 500)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_FREEZE , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n105' , 250 , 10 , 3 , 280 , 300)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_HEAL , SKILL_TYPE_HEAL)
    // 召唤师小怪
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n106' , 350 , 20 , 5 , 260 , 200)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_SUMMON_MINIONS , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化山贼主题小怪配置 (THEME_TYPE_BANDIT = 2)
    // ========================================================================
    set theme_type=THEME_TYPE_BANDIT
    // 近战输出小怪
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n111' , 500 , 30 , 5 , 300 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_HEAVY_STRIKE , SKILL_TYPE_ATTACK)
    // 远程射手小怪
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n112' , 400 , 25 , 3 , 320 , 600)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_RANGE_SHOT , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n113' , 800 , 20 , 15 , 250 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_DEFENSIVE_STANCE , SKILL_TYPE_DEFENSE)
    // 法师控制小怪
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n114' , 350 , 35 , 2 , 280 , 500)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_FREEZE , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n115' , 300 , 15 , 4 , 290 , 300)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_HEAL , SKILL_TYPE_HEAL)
    // 召唤师小怪
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n116' , 450 , 25 , 6 , 270 , 200)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_SUMMON_MINIONS , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化山贼主题BOSS配置
    // ========================================================================
    // 力量型BOSS
    set boss_type=BOSS_TYPE_STRENGTH
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n001' , 5000 , 100 , 30 , 280 , 150 , 20)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_BERSERK , SKILL_TYPE_BUFF)
    // 防御型BOSS
    set boss_type=BOSS_TYPE_DEFENSE
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n002' , 8000 , 70 , 50 , 240 , 100 , 30)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_DEFENSIVE_STANCE , SKILL_TYPE_DEFENSE)
    // 敏捷型BOSS
    set boss_type=BOSS_TYPE_AGILITY
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n003' , 4000 , 120 , 20 , 350 , 600 , 25)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_PRECISION_SHOT , SKILL_TYPE_ATTACK)
    // 法师型BOSS
    set boss_type=BOSS_TYPE_CASTER
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n004' , 3500 , 150 , 15 , 300 , 500 , 35)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_FLAME_STORM , SKILL_TYPE_AOE)
    // 召唤型BOSS
    set boss_type=BOSS_TYPE_SUMMONER
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n005' , 4500 , 90 , 25 , 260 , 200 , 40)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_SUMMON_MINIONS , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化寺庙主题小怪配置 (THEME_TYPE_SHAOLIN = 3)
    // ========================================================================
    set theme_type=THEME_TYPE_SHAOLIN
    // 近战输出小怪
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n121' , 550 , 35 , 8 , 290 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_COMBO_STRIKE , SKILL_TYPE_ATTACK)
    // 远程射手小怪
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n122' , 450 , 30 , 5 , 310 , 650)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_PRECISION_SHOT , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n123' , 900 , 25 , 20 , 240 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_TAUNT , SKILL_TYPE_CONTROL)
    // 法师控制小怪
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n124' , 400 , 40 , 4 , 270 , 550)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_FIREBALL , SKILL_TYPE_ATTACK)
    // 治疗辅助小怪
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n125' , 350 , 20 , 6 , 280 , 350)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_HEAL , SKILL_TYPE_HEAL)
    // 召唤师小怪
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n126' , 500 , 30 , 8 , 260 , 250)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_SUMMON_MINIONS , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化寺庙主题BOSS配置
    // ========================================================================
    // 力量型BOSS
    set boss_type=BOSS_TYPE_STRENGTH
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n006' , 5500 , 110 , 35 , 270 , 150 , 25)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_BERSERK , SKILL_TYPE_BUFF)
    // 防御型BOSS
    set boss_type=BOSS_TYPE_DEFENSE
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n007' , 8500 , 75 , 55 , 230 , 100 , 35)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_DEFENSIVE_STANCE , SKILL_TYPE_DEFENSE)
    // 敏捷型BOSS
    set boss_type=BOSS_TYPE_AGILITY
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n008' , 4200 , 130 , 25 , 340 , 650 , 30)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_PRECISION_SHOT , SKILL_TYPE_ATTACK)
    // 法师型BOSS
    set boss_type=BOSS_TYPE_CASTER
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n009' , 3700 , 160 , 18 , 290 , 550 , 40)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_FLAME_STORM , SKILL_TYPE_AOE)
    // 召唤型BOSS
    set boss_type=BOSS_TYPE_SUMMONER
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n010' , 4800 , 95 , 30 , 250 , 250 , 45)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_SUMMON_MINIONS , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化洞穴主题小怪配置 (THEME_TYPE_MING = 4)
    // ========================================================================
    set theme_type=THEME_TYPE_MING
    // 近战输出小怪
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n131' , 600 , 40 , 10 , 280 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_HEAVY_STRIKE , SKILL_TYPE_ATTACK)
    // 远程射手小怪
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n132' , 500 , 35 , 6 , 300 , 700)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_RANGE_SHOT , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n133' , 1000 , 30 , 25 , 230 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_DEFENSIVE_STANCE , SKILL_TYPE_DEFENSE)
    // 法师控制小怪
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n134' , 450 , 45 , 5 , 260 , 600)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_FREEZE , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n135' , 400 , 25 , 8 , 270 , 400)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_HEAL , SKILL_TYPE_HEAL)
    // 召唤师小怪
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n136' , 550 , 35 , 10 , 250 , 300)
    call MonsterData_SetMonsterSkill(role_type , theme_type , ENEMY_SKILL_SUMMON_MINIONS , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化洞穴主题BOSS配置
    // ========================================================================
    // 力量型BOSS
    set boss_type=BOSS_TYPE_STRENGTH
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n011' , 6000 , 120 , 40 , 260 , 150 , 30)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_BERSERK , SKILL_TYPE_BUFF)
    // 防御型BOSS
    set boss_type=BOSS_TYPE_DEFENSE
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n012' , 9000 , 80 , 60 , 220 , 100 , 40)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_DEFENSIVE_STANCE , SKILL_TYPE_DEFENSE)
    // 敏捷型BOSS
    set boss_type=BOSS_TYPE_AGILITY
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n013' , 4400 , 140 , 30 , 330 , 700 , 35)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_PRECISION_SHOT , SKILL_TYPE_ATTACK)
    // 法师型BOSS
    set boss_type=BOSS_TYPE_CASTER
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n014' , 3900 , 170 , 20 , 280 , 600 , 45)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_FLAME_STORM , SKILL_TYPE_AOE)
    // 召唤型BOSS
    set boss_type=BOSS_TYPE_SUMMONER
    call MonsterData_SetBossConfig(boss_type , theme_type , 'n015' , 5100 , 100 , 35 , 240 , 300 , 50)
    call MonsterData_SetBossSkill(boss_type , theme_type , ENEMY_SKILL_SUMMON_MINIONS , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化深层洞穴主题小怪配置 (THEME_TYPE_DARK = 5)
    // ========================================================================
    set theme_type=THEME_TYPE_DARK
    // 近战输出小怪 - 机关剑士
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n141' , 650 , 45 , 11 , 285 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91003 , SKILL_TYPE_ATTACK)
    // 远程射手小怪 - 机关弩手
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n142' , 550 , 38 , 7 , 310 , 720)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91005 , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪 - 机关重甲
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n143' , 1100 , 33 , 27 , 235 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91006 , SKILL_TYPE_DEFENSE)
    // 法师控制小怪 - 机关术士
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n144' , 500 , 50 , 6 , 265 , 620)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91009 , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪 - 机关医者
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n145' , 440 , 28 , 9 , 275 , 420)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91010 , SKILL_TYPE_HEAL)
    // 召唤师小怪 - 机关工匠
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n146' , 600 , 39 , 11 , 255 , 320)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91011 , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化竹林秘境主题小怪配置 (THEME_TYPE_BAMBOO = 6)
    // ========================================================================
    set theme_type=THEME_TYPE_BAMBOO
    // 近战输出小怪 - 竹林剑客
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n151' , 700 , 50 , 12 , 290 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91003 , SKILL_TYPE_ATTACK)
    // 远程射手小怪 - 竹叶镖手
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n152' , 600 , 42 , 8 , 320 , 750)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91005 , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪 - 竹甲卫士
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n153' , 1200 , 36 , 30 , 240 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91006 , SKILL_TYPE_DEFENSE)
    // 法师控制小怪 - 竹笛乐师
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n154' , 550 , 55 , 7 , 270 , 650)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91009 , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪 - 竹露医者
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n155' , 480 , 31 , 10 , 280 , 450)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91010 , SKILL_TYPE_HEAL)
    // 召唤师小怪 - 竹阵法师
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n156' , 650 , 43 , 12 , 260 , 350)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91011 , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化逍遥山庄主题小怪配置 (THEME_TYPE_XIAOYAO = 7)
    // ========================================================================
    set theme_type=THEME_TYPE_XIAOYAO
    // 近战输出小怪 - 琴剑客
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n161' , 770 , 55 , 14 , 300 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91003 , SKILL_TYPE_ATTACK)
    // 远程射手小怪 - 棋射手
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n162' , 660 , 46 , 9 , 330 , 770)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91005 , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪 - 书卷卫士
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n163' , 1320 , 40 , 33 , 250 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91006 , SKILL_TYPE_DEFENSE)
    // 法师控制小怪 - 画境术士
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n164' , 605 , 60 , 8 , 280 , 670)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91009 , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪 - 琴音医者
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n165' , 530 , 34 , 11 , 290 , 460)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91010 , SKILL_TYPE_HEAL)
    // 召唤师小怪 - 四艺召唤师
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n166' , 715 , 47 , 13 , 270 , 360)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91011 , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化梅花坞主题小怪配置 (THEME_TYPE_PLUM = 8)
    // ========================================================================
    set theme_type=THEME_TYPE_PLUM
    // 近战输出小怪 - 寒梅剑客
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n171' , 850 , 61 , 16 , 315 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91003 , SKILL_TYPE_ATTACK)
    // 远程射手小怪 - 梅枝射手
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n172' , 725 , 51 , 10 , 345 , 785)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91005 , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪 - 梅干卫士
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n173' , 1450 , 44 , 37 , 260 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91006 , SKILL_TYPE_DEFENSE)
    // 法师控制小怪 - 梅香术士
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n174' , 665 , 66 , 9 , 295 , 685)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91009 , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪 - 梅蕊医者
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n175' , 580 , 37 , 12 , 305 , 475)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91010 , SKILL_TYPE_HEAL)
    // 召唤师小怪 - 梅花召唤师
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n176' , 785 , 52 , 15 , 285 , 375)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91011 , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化五行峰主题小怪配置 (THEME_TYPE_KONGTONG = 9)
    // ========================================================================
    set theme_type=THEME_TYPE_KONGTONG
    // 近战输出小怪 - 金行剑客
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n181' , 940 , 68 , 18 , 350 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91003 , SKILL_TYPE_ATTACK)
    // 远程射手小怪 - 木行射手
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n182' , 800 , 56 , 11 , 380 , 800)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91005 , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪 - 水行卫士
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n183' , 1600 , 48 , 41 , 285 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91006 , SKILL_TYPE_DEFENSE)
    // 法师控制小怪 - 火行术士
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n184' , 735 , 73 , 10 , 325 , 700)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91009 , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪 - 土行医者
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n185' , 640 , 41 , 13 , 335 , 490)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91010 , SKILL_TYPE_HEAL)
    // 召唤师小怪 - 五行阵法师
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n186' , 865 , 57 , 17 , 315 , 390)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91011 , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化水月洞主题小怪配置 (THEME_TYPE_WATER_MOON = 10)
    // ========================================================================
    set theme_type=THEME_TYPE_WATER_MOON
    // 近战输出小怪 - 镜花剑客
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n191' , 1035 , 75 , 20 , 385 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91003 , SKILL_TYPE_ATTACK)
    // 远程射手小怪 - 水月射手
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n192' , 880 , 62 , 12 , 418 , 880)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91005 , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪 - 幻影卫士
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n193' , 1760 , 53 , 45 , 314 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91006 , SKILL_TYPE_DEFENSE)
    // 法师控制小怪 - 虚幻术士
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n194' , 810 , 80 , 11 , 358 , 770)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91009 , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪 - 倒影医者
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n195' , 705 , 45 , 14 , 369 , 540)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91010 , SKILL_TYPE_HEAL)
    // 召唤师小怪 - 镜月召唤师
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n196' , 950 , 63 , 19 , 347 , 430)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91011 , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化剑圣谷主题小怪配置 (THEME_TYPE_SWORD = 11)
    // ========================================================================
    set theme_type=THEME_TYPE_SWORD
    // 近战输出小怪 - 剑圣传人
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1A1' , 1140 , 83 , 22 , 424 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91003 , SKILL_TYPE_ATTACK)
    // 远程射手小怪 - 剑气射手
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1A2' , 968 , 68 , 13 , 460 , 968)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91005 , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪 - 剑盾卫士
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1A3' , 1936 , 58 , 50 , 345 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91006 , SKILL_TYPE_DEFENSE)
    // 法师控制小怪 - 剑心术士
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1A4' , 891 , 88 , 12 , 394 , 847)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91009 , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪 - 剑魂医者
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1A5' , 776 , 50 , 15 , 406 , 594)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91010 , SKILL_TYPE_HEAL)
    // 召唤师小怪 - 剑灵召唤师
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1A6' , 1045 , 69 , 21 , 382 , 473)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91011 , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化云梦泽主题小怪配置 (THEME_TYPE_MARSH = 12)
    // ========================================================================
    set theme_type=THEME_TYPE_MARSH
    // 近战输出小怪 - 毒雾剑客
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1B1' , 1254 , 91 , 24 , 466 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91003 , SKILL_TYPE_ATTACK)
    // 远程射手小怪 - 沼泽射手
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1B2' , 1065 , 75 , 14 , 506 , 1065)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91005 , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪 - 毒瘴卫士
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1B3' , 2130 , 64 , 55 , 380 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91006 , SKILL_TYPE_DEFENSE)
    // 法师控制小怪 - 毒雾术士
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1B4' , 980 , 97 , 13 , 433 , 932)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91009 , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪 - 沼泽医者
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1B5' , 854 , 55 , 16 , 447 , 653)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91010 , SKILL_TYPE_HEAL)
    // 召唤师小怪 - 毒泽召唤师
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1B6' , 1150 , 76 , 23 , 420 , 520)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91011 , SKILL_TYPE_SUMMON)
    // ========================================================================
    // 初始化武林圣地主题小怪配置 (THEME_TYPE_SACRED = 13)
    // ========================================================================
    set theme_type=THEME_TYPE_SACRED
    // 近战输出小怪 - 剑宗传人
    set role_type=ROLE_TYPE_MELEE_DPS
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1C1' , 1379 , 100 , 26 , 513 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91003 , SKILL_TYPE_ATTACK)
    // 远程射手小怪 - 弓宗高手
    set role_type=ROLE_TYPE_RANGER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1C2' , 1172 , 83 , 15 , 557 , 1172)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91005 , SKILL_TYPE_ATTACK)
    // 坦克肉盾小怪 - 盾宗卫士
    set role_type=ROLE_TYPE_TANK
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1C3' , 2343 , 70 , 61 , 418 , 100)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91006 , SKILL_TYPE_DEFENSE)
    // 法师控制小怪 - 术宗大师
    set role_type=ROLE_TYPE_CASTER_CONTROL
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1C4' , 1078 , 107 , 14 , 476 , 1025)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91009 , SKILL_TYPE_CONTROL)
    // 治疗辅助小怪 - 医宗圣手
    set role_type=ROLE_TYPE_HEALER_SUPPORT
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1C5' , 939 , 61 , 18 , 492 , 718)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91010 , SKILL_TYPE_HEAL)
    // 召唤师小怪 - 召唤宗师
    set role_type=ROLE_TYPE_SUMMONER
    call MonsterData_SetMonsterType(role_type , theme_type , 'n1C6' , 1265 , 84 , 25 , 462 , 572)
    call MonsterData_SetMonsterSkill(role_type , theme_type , 91011 , SKILL_TYPE_SUMMON)
endfunction

//library DungeonMonsterData ends
//library GeneralBonusSystem:
//以下函数仅仅是让技能ID出现在代码里，不然SLK优化器会删除这些技能
function GeneralBonusSystem___DisplayAllAbilityId takes nothing returns nothing
    local integer aid=0
    set aid='YDl0'
    set aid='YDl1'
    set aid='YDl2'
    set aid='YDl3'
    set aid='YDl4'
    set aid='YDl5'
    set aid='YDl6'
    set aid='YDl7'
    set aid='YDl8'
    set aid='YDl9'
    set aid='YDla'
    set aid='YDlb'
    set aid='YDlc'
    set aid='YDld'
    set aid='YDle'
    set aid='YDlf'
    set aid='YDlg'
    set aid='YDlh'
    set aid='YDli'
    set aid='YDlj'
    set aid='YDlk'
    set aid='YDll'
    set aid='YDlm'
    set aid='YDln'
    set aid='YDm0'
    set aid='YDm1'
    set aid='YDm2'
    set aid='YDm3'
    set aid='YDm4'
    set aid='YDm5'
    set aid='YDm6'
    set aid='YDm7'
    set aid='YDm8'
    set aid='YDm9'
    set aid='YDma'
    set aid='YDmb'
    set aid='YDmc'
    set aid='YDmd'
    set aid='YDme'
    set aid='YDmf'
    set aid='YDc0'
    set aid='YDc1'
    set aid='YDc2'
    set aid='YDc3'
    set aid='YDc4'
    set aid='YDc5'
    set aid='YDc6'
    set aid='YDc7'
    set aid='YDc8'
    set aid='YDc9'
    set aid='YDca'
    set aid='YDcb'
    set aid='YDcc'
    set aid='YDb0'
    set aid='YDb1'
    set aid='YDb2'
    set aid='YDb3'
    set aid='YDb4'
    set aid='YDb5'
    set aid='YDb6'
    set aid='YDb7'
    set aid='YDb8'
    set aid='YDb9'
    set aid='YDba'
    set aid='YDbb'
    set aid='YDbc'
    set aid='YDbd'
    set aid='YDbe'
    set aid='YDbf'
    set aid='YDbg'
    set aid='YDbh'
    set aid='YDbi'
    set aid='YDbj'
    set aid='YDbk'
    set aid='YDbl'
    set aid='YDbm'
    set aid='YDbn'
    set aid='YDs0'
    set aid='YDs1'
    set aid='YDs2'
    set aid='YDs3'
    set aid='YDs4'
    set aid='YDs5'
    set aid='YDs6'
    set aid='YDs7'
    set aid='YDs8'
    set aid='YDs9'
endfunction
    function GeneralBonusSystem___UnitClearBonus takes unit u,integer bonusType returns nothing
        local integer i=GeneralBonusSystem___ABILITY_COUNT[bonusType + 1] - 1
        loop
            exitwhen i < GeneralBonusSystem___ABILITY_COUNT[bonusType]
            call UnitRemoveAbility(u, GeneralBonusSystem___BonusAbilitys[i])
            set i=i - 1
        endloop
        call YDWESaveIntegerByString(I2S(YDWEH2I(u)) , "bonusType" + I2S(bonusType) , 0)
    endfunction
    function GeneralBonusSystem___SetUnitMaxState takes unit u,integer bonusType,real value returns boolean
        local integer v=R2I(value)
        local integer s=0
        local integer o=0
        local unitstate state
        local integer i=GeneralBonusSystem___ABILITY_COUNT[bonusType + 1] - 2
        local integer a=GeneralBonusSystem___ABILITY_NUM[bonusType]
        if bonusType == 0 and ( value > 16777216 or value <= 0 ) then
            call BJDebugMsg("输入数据无效")
            return false
        endif
        if bonusType == 1 and ( value > 65535 or value <= 0 ) then
            call BJDebugMsg("输入数据无效")
            return false
        endif
        if bonusType == 0 then
            set state=UNIT_STATE_MAX_LIFE
          elseif bonusType == 1 then
            set state=UNIT_STATE_MAX_MANA
          else
            call BJDebugMsg("无效状态")
            return false
        endif
        // 与当前状态进行对比，得到需要添加的属性值
        set v=v - R2I(GetUnitState(u, state))
        call YDWESaveIntegerByString(I2S(YDWEH2I(u)) , "bonusType" + I2S(bonusType) , v)
        if v > 0 then
            // 负数血牌/蓝牌，添加删除后最大生命值永久增加
            set o=3
          elseif v < 0 then
            // 正数血牌/蓝牌，添加删除后最大生命值永久减少
            set o=2
            set v=- v
          else
            return false
        endif
        loop
            exitwhen i < GeneralBonusSystem___ABILITY_COUNT[bonusType]
            if v >= GeneralBonusSystem___PowersOf2[i] then
                call UnitAddAbility(u, GeneralBonusSystem___BonusAbilitys[i])
                call SetUnitAbilityLevel(u, GeneralBonusSystem___BonusAbilitys[i], o)
                call UnitRemoveAbility(u, GeneralBonusSystem___BonusAbilitys[i])
                set v=v - GeneralBonusSystem___PowersOf2[i]
            endif
            set i=i - 1
        endloop
        return true
    endfunction
function GeneralBonusSystem___UnitSetBonus takes unit u,integer bonusType,integer ammount returns boolean
    local integer i
    //设置属性为0不进行Loop
    if ammount == 0 then
        call GeneralBonusSystem___UnitClearBonus(u , bonusType)
        return false
    endif
    if ammount < GeneralBonusSystem___MinBonus[bonusType] or ammount > GeneralBonusSystem___MaxBonus[bonusType] then
        call BJDebugMsg("BonusSystem Error: Bonus too high or low (" + I2S(ammount) + ")")
        return false
    elseif bonusType < 0 or bonusType >= GeneralBonusSystem___BONUS_TYPES then
        call BJDebugMsg("BonusSystem Error: Invalid bonus type (" + I2S(bonusType) + ")")
        return false
    endif
    call YDWESaveIntegerByString(I2S(YDWEH2I(u)) , "bonusType" + I2S(bonusType) , ammount)
    if ammount < 0 then
        set ammount=GeneralBonusSystem___MaxBonus[bonusType] + ammount + 1
        call UnitAddAbility(u, GeneralBonusSystem___BonusAbilitys[GeneralBonusSystem___ABILITY_COUNT[bonusType + 1] - 1])
        call UnitMakeAbilityPermanent(u, true, GeneralBonusSystem___BonusAbilitys[GeneralBonusSystem___ABILITY_COUNT[bonusType + 1] - 1])
      else
        call UnitRemoveAbility(u, GeneralBonusSystem___BonusAbilitys[GeneralBonusSystem___ABILITY_COUNT[bonusType + 1] - 1])
    endif
    set i=GeneralBonusSystem___ABILITY_COUNT[bonusType + 1] - 2
    loop
        exitwhen i < GeneralBonusSystem___ABILITY_COUNT[bonusType]
        if ammount >= GeneralBonusSystem___PowersOf2[i] then
            call UnitAddAbility(u, GeneralBonusSystem___BonusAbilitys[i])
            call UnitMakeAbilityPermanent(u, true, GeneralBonusSystem___BonusAbilitys[i])
            set ammount=ammount - GeneralBonusSystem___PowersOf2[i]
        else
            call UnitRemoveAbility(u, GeneralBonusSystem___BonusAbilitys[i])
        endif
        set i=i - 1
    endloop
    if not YDWEGetBooleanByString(I2S(YDWEH2I(u)) , "bonusMark") then
        call YDWESaveBooleanByString(I2S(YDWEH2I(u)) , "bonusMark" , true)
        set GeneralBonusSystem___UnitCount=GeneralBonusSystem___UnitCount + 1
        set GeneralBonusSystem___Units[GeneralBonusSystem___UnitCount]=u
    endif
    return true
endfunction
function GeneralBonusSystem___UnitGetBonus takes unit u,integer bonusType returns integer
    return YDWEGetIntegerByString(I2S(YDWEH2I(u)) , "bonusType" + I2S(bonusType))
endfunction
function GeneralBonusSystem___AddUnitMaxState takes unit u,integer bonusType,real value returns boolean
    local unitstate state
    if bonusType == 0 then
        set state=UNIT_STATE_MAX_LIFE
      elseif bonusType == 1 then
        set state=UNIT_STATE_MAX_MANA
      else
        return false
    endif
    return GeneralBonusSystem___SetUnitMaxState(u , bonusType , value + GetUnitState(u, state))
endfunction
function GeneralBonusSystem___UnitAddBonus takes unit u,integer bonusType,integer ammount returns boolean
    return GeneralBonusSystem___UnitSetBonus(u , bonusType , GeneralBonusSystem___UnitGetBonus(u , bonusType) + ammount)
endfunction
function GeneralBonusSystem___FlushUnits takes nothing returns nothing
    local integer i= GeneralBonusSystem___UnitCount
    local string h
    loop
        exitwhen i < 1
        if GetUnitTypeId(GeneralBonusSystem___Units[i]) == 0 then
            set h=I2S(YDWEH2I(GeneralBonusSystem___Units[i]))
            call YDWESaveIntegerByString(h , "bonusType0" , 0)
            call YDWESaveIntegerByString(h , "bonusType1" , 0)
            call YDWESaveIntegerByString(h , "bonusType2" , 0)
            call YDWESaveIntegerByString(h , "bonusType3" , 0)
            call YDWESaveIntegerByString(h , "bonusType4" , 0)
            call YDWESaveBooleanByString(h , "bonusMark" , false)
            set GeneralBonusSystem___Units[i]=GeneralBonusSystem___Units[GeneralBonusSystem___UnitCount]
            set GeneralBonusSystem___Units[GeneralBonusSystem___UnitCount]=null
            set GeneralBonusSystem___UnitCount=GeneralBonusSystem___UnitCount - 1
        endif
        set i=i - 1
    endloop
endfunction
function YDWEUnitSetBonus takes unit u,integer bonusType,integer ammount returns nothing
    if bonusType == 0 or bonusType == 1 then
        call GeneralBonusSystem___SetUnitMaxState(u , bonusType , ammount)
      else
        call GeneralBonusSystem___UnitSetBonus(u , bonusType , ammount)
    endif
endfunction
function YDWEUnitAddBonus takes unit u,integer bonusType,integer ammount returns nothing
    if bonusType == 0 or bonusType == 1 then
        call GeneralBonusSystem___AddUnitMaxState(u , bonusType , ammount)
      else
        call GeneralBonusSystem___UnitAddBonus(u , bonusType , ammount)
    endif
endfunction
function GeneralBonusSystemUnitSetBonus takes unit u,integer bonusType,integer mod,integer ammount returns nothing
    if mod == 0 then
        call YDWEUnitAddBonus(u , bonusType , ammount)
      elseif mod == 1 then
        call YDWEUnitAddBonus(u , bonusType , 0 - ammount)
      else
        call YDWEUnitSetBonus(u , bonusType , ammount)
    endif
endfunction
function YDWEGeneralBonusSystemUnitGetBonus takes unit u,integer bonusType returns integer
    return YDWEGetIntegerByString(I2S(YDWEH2I(u)) , "bonusType" + I2S(bonusType))
endfunction
//private keyword BonusAbilitys
function GeneralBonusSystem___InitializeAbilitys takes nothing returns nothing
    local integer i=0
    local integer m=0
    set GeneralBonusSystem___ABILITY_COUNT[0]=0 //life max
set GeneralBonusSystem___ABILITY_COUNT[1]=24 //mana max
set GeneralBonusSystem___ABILITY_COUNT[2]=39 //armor
set GeneralBonusSystem___ABILITY_COUNT[3]=52 //attack
set GeneralBonusSystem___ABILITY_COUNT[4]=76 // attack speed
set GeneralBonusSystem___ABILITY_COUNT[5]=86
    set GeneralBonusSystem___ABILITY_NUM[0]=24
    set GeneralBonusSystem___ABILITY_NUM[1]=15
    set GeneralBonusSystem___ABILITY_NUM[2]=13
    set GeneralBonusSystem___ABILITY_NUM[3]=24
    set GeneralBonusSystem___ABILITY_NUM[4]=10
    // Bonus Mod - Life MaxState abilitys
    loop
        exitwhen i > 9
        set GeneralBonusSystem___YDWEBONUS_MyChar[i]='0' + m
        set m=m + 1
        set i=i + 1
    endloop
    set m=0
    loop
        exitwhen i > 26
        set GeneralBonusSystem___YDWEBONUS_MyChar[i]='a' + m
        set m=m + 1
        set i=i + 1
    endloop
    set i=0
    set m=0
    loop
        exitwhen m > ( GeneralBonusSystem___ABILITY_NUM[0] - 1 )
        set GeneralBonusSystem___BonusAbilitys[i]='YDl0' - '0' + GeneralBonusSystem___YDWEBONUS_MyChar[m] // +1
        set i=i + 1
        set m=m + 1
    endloop
    // Bonus Mod - Mana MaxState abilitys
    set m=0
    loop
        exitwhen m > ( GeneralBonusSystem___ABILITY_NUM[1] - 1 )
        set GeneralBonusSystem___BonusAbilitys[i]='YDm0' - '0' + GeneralBonusSystem___YDWEBONUS_MyChar[m] // +1
        set i=i + 1
        set m=m + 1
    endloop
    // Bonus Mod - Armor abilitys
    set m=0
    loop
        exitwhen m > ( GeneralBonusSystem___ABILITY_NUM[2] - 1 )
        set GeneralBonusSystem___BonusAbilitys[i]='YDc0' - '0' + GeneralBonusSystem___YDWEBONUS_MyChar[m] // +1
        set i=i + 1
        set m=m + 1
    endloop
    // Bonus Mod - Attack abilitys
    set m=0
    loop
        exitwhen m > ( GeneralBonusSystem___ABILITY_NUM[3] - 1 )
        set GeneralBonusSystem___BonusAbilitys[i]='YDb0' - '0' + GeneralBonusSystem___YDWEBONUS_MyChar[m] // +1
        set i=i + 1
        set m=m + 1
    endloop
    // Bonus Mod - Attack Speed abilitys
    set m=0
    loop
        exitwhen m > ( GeneralBonusSystem___ABILITY_NUM[4] - 1 )
        set GeneralBonusSystem___BonusAbilitys[i]='YDs0' - '0' + GeneralBonusSystem___YDWEBONUS_MyChar[m] // +1
        set i=i + 1
        set m=m + 1
    endloop
endfunction
function GeneralBonusSystem___Initialize takes nothing returns nothing
    local integer i= 1
    local unit u
    local integer n=0
    local integer add=0
    call GeneralBonusSystem___InitializeAbilitys()
    loop
        set i=1
        set GeneralBonusSystem___PowersOf2[add]=1
            loop
                set GeneralBonusSystem___PowersOf2[add + 1]=GeneralBonusSystem___PowersOf2[add] * 2
                set add=add + 1
                set i=i + 1
                exitwhen i == GeneralBonusSystem___ABILITY_NUM[n]
            endloop
        set GeneralBonusSystem___MaxBonus[n]=GeneralBonusSystem___PowersOf2[add] - 1
        set GeneralBonusSystem___MinBonus[n]=- GeneralBonusSystem___PowersOf2[add]
        set add=add + 1
        set n=n + 1
        exitwhen n >= 4
    endloop
    //预读技能
    if GeneralBonusSystem___PRELOAD_ABILITYS then
        set u=CreateUnit(Player(15), GeneralBonusSystem___PRELOAD_DUMMY_UNIT, 0, 0, 0)
        set i=0
        loop
            exitwhen i == GeneralBonusSystem___ABILITY_COUNT[5]
            call UnitAddAbility(u, GeneralBonusSystem___BonusAbilitys[i])
            set i=i + 1
        endloop
        call RemoveUnit(u)
        set u=null
    endif
    //回收数据
    call TimerStart(CreateTimer(), 10, true, function GeneralBonusSystem___FlushUnits)
endfunction

//library GeneralBonusSystem ends
//library SectSystem:
    // ============================================================================
    // 检查玩家是否可以选择指定门派
    // ============================================================================
    function Sect_CanSelect takes integer player_id,integer sect_id returns boolean
        // 检查门派ID是否有效
        if sect_id < SECT_SHAOLIN or sect_id > SECT_EMEI then
            return false
        endif
        // 检查玩家是否已经选择过门派
        if udg_player_sect_selected[player_id] != 0 then
            return false
        endif
        return true
    endfunction
    // ============================================================================
    // 执行门派选择操作
    // ============================================================================
    function Sect_Select takes integer player_id,integer sect_id returns boolean
        if not Sect_CanSelect(player_id , sect_id) then
            return false
        endif
        // 设置玩家门派选择状态
        set udg_player_sect_selected[player_id]=sect_id
        set udg_player_sect_completed[player_id]=true
        return true
    endfunction
    // ============================================================================
    // 获取玩家已选择的门派ID
    // ============================================================================
    function Sect_GetSelected takes integer player_id returns integer
        return udg_player_sect_selected[player_id]
    endfunction
    // ============================================================================
    // 检查玩家是否已选择门派
    // ============================================================================
    function Sect_HasSelected takes integer player_id returns boolean
        return udg_player_sect_selected[player_id] != 0
    endfunction
    // ============================================================================
    // 获取玩家门派名称
    // ============================================================================
    function Sect_GetName takes integer player_id returns string
        local integer sect_id
        local string result
        set sect_id=udg_player_sect_selected[player_id]
        if sect_id == 0 then
            set result="未入门派"
        else
            set result=SectData_GetName(sect_id)
        endif
        return result
    endfunction
    // ============================================================================
    // 获取玩家已解锁的技能数量
    // ============================================================================
    function Sect_GetSkillCount takes integer player_id returns integer
        local integer sect_id
        local integer count
        set sect_id=udg_player_sect_selected[player_id]
        if sect_id == 0 then
            return 0
        endif
        set count=0
        // 检查第一技能是否解锁
        if SectData_GetSkillUnlockLevel(sect_id , SKILL_SLOT_FIRST) > 0 then
            set count=count + 1
        endif
        // 检查第二技能是否解锁
        if SectData_GetSkillUnlockLevel(sect_id , SKILL_SLOT_SECOND) > 0 then
            set count=count + 1
        endif
        // 检查第三技能是否解锁
        if SectData_GetSkillUnlockLevel(sect_id , SKILL_SLOT_THIRD) > 0 then
            set count=count + 1
        endif
        return count
    endfunction
    // ============================================================================
    // 重置玩家门派选择状态
    // ============================================================================
    function Sect_Reset takes integer player_id returns nothing
        set udg_player_sect_selected[player_id]=0
        set udg_player_sect_completed[player_id]=false
    endfunction
    // ============================================================================
    // 检查指定槽位的技能是否已解锁
    // ============================================================================
    function Sect_IsSkillUnlocked takes integer player_id,integer slot returns boolean
        return udg_skill_unlocked[player_id * 20 + slot]
    endfunction
    // ============================================================================
    // 标记指定槽位的技能已解锁
    // ============================================================================
    function Sect_MarkSkillUnlocked takes integer player_id,integer slot returns nothing
        set udg_skill_unlocked[player_id * 20 + slot]=true
    endfunction
    // ============================================================================
    // 为玩家解锁指定槽位的技能
    // 使用UnitAddAbility将技能直接添加到英雄身上
    // ============================================================================
    function Sect_UnlockSkill takes integer player_id,integer slot returns nothing
        local player p
        local unit hero
        local integer sect_id
        local integer skill_id
        local string skill_name
        local integer slot_index
        // 检查是否已解锁
        if Sect_IsSkillUnlocked(player_id , slot) then
            return
        endif
        // 获取玩家门派和技能信息
        set sect_id=udg_player_sect_selected[player_id]
        if sect_id == 0 then
            return
        endif
        set skill_id=SectData_GetSkillId(sect_id , slot)
        set skill_name=SectData_GetSkillName(sect_id , slot)
        set p=Player(player_id)
        set hero=GetTriggerUnit()
        // 检查技能ID是否有效
        if skill_id == 0 then
            return
        endif
        // 添加技能到英雄
        call UnitAddAbility(hero, skill_id)
        call UnitMakeAbilityPermanent(hero, true, skill_id)
        // 标记为已解锁
        call Sect_MarkSkillUnlocked(player_id , slot)
        // 显示技能解锁提示
        call DisplayTextToPlayer(p, 0, 0, "|cFF00FF00[门派技能] 已解锁「" + skill_name + "」！|r")
        set p=null
        set hero=null
    endfunction
    // ============================================================================
    // 检查玩家在当前等级是否有技能可解锁
    // 根据等级检查对应技能槽位，满足条件则解锁
    // ============================================================================
    function Sect_CheckSkillUnlock takes integer player_id returns nothing
        local integer sect_id
        local integer current_level
        local integer unlock_level
        local unit hero
        // 检查是否已选择门派
        set sect_id=udg_player_sect_selected[player_id]
        if sect_id == 0 then
            return
        endif
        // 获取玩家英雄当前等级
        set hero=GetTriggerUnit()
        set current_level=GetHeroLevel(hero)
        // 检查第一技能（Lv.1解锁）
        set unlock_level=SectData_GetSkillUnlockLevel(sect_id , SKILL_SLOT_FIRST)
        if current_level >= unlock_level and unlock_level > 0 then
            call Sect_UnlockSkill(player_id , SKILL_SLOT_FIRST)
        endif
        // 检查第二技能（Lv.6解锁）
        set unlock_level=SectData_GetSkillUnlockLevel(sect_id , SKILL_SLOT_SECOND)
        if current_level >= unlock_level and unlock_level > 0 then
            call Sect_UnlockSkill(player_id , SKILL_SLOT_SECOND)
        endif
        // 检查第三技能（Lv.12解锁）
        set unlock_level=SectData_GetSkillUnlockLevel(sect_id , SKILL_SLOT_THIRD)
        if current_level >= unlock_level and unlock_level > 0 then
            call Sect_UnlockSkill(player_id , SKILL_SLOT_THIRD)
        endif
        set hero=null
    endfunction
    // ============================================================================
    // 处理玩家升级事件
    // 当玩家升级时检查是否有技能可解锁
    // ============================================================================
    function Sect_ProcessHeroLevel takes nothing returns nothing
        local integer player_id
        set player_id=GetPlayerId(GetTriggerPlayer())
        call Sect_CheckSkillUnlock(player_id)
    endfunction
    // ============================================================================
    // 处理玩家拾取门派道具事件
    // 当玩家拾取到门派信物道具时触发门派选择逻辑
    // ============================================================================
    function Sect_ProcessPickupItem takes nothing returns nothing
        local player p
        local unit picked_unit
        local item picked_item
        local integer item_type_id
        local integer player_id
        local integer target_sect_id
        local string l__sect_name
        set p=GetTriggerPlayer()
        set picked_unit=GetTriggerUnit()
        set picked_item=GetManipulatedItem()
        set item_type_id=GetItemTypeId(picked_item)
        set player_id=GetPlayerId(p)
        // 根据物品ID判断是否为门派道具
        set target_sect_id=SectData_GetSectByItemId(item_type_id)
        if target_sect_id != 0 then
            // 是门派道具，检查是否可以加入门派
            // 情况1：检查门派是否开放（MVP阶段只开放1-3）
            if target_sect_id < SECT_SHAOLIN or target_sect_id > SECT_EMEI then
                // 门派未开放
                call DisplayTextToPlayer(p, 0, 0, "|cFFFF0000[系统]|r该门派暂未开放！")
                return
            endif
            // 情况2：检查玩家是否已加入门派
            if udg_player_sect_selected[player_id] != 0 then
                // 玩家已加入门派
                call DisplayTextToPlayer(p, 0, 0, "|cFFFF0000[系统]|r你已加入门派，无法重复加入！")
                return
            endif
            // 情况3：门派有效且开放，玩家未加入 → 正常加入
            if Sect_Select(player_id , target_sect_id) then
                set l__sect_name=SectData_GetName(target_sect_id)
                call DisplayTextToPlayer(p, 0, 0, "|cFF00FF00[系统]|r恭喜加入" + l__sect_name + "！")
                // 传送英雄回主城
                if picked_unit != null and GetUnitState(picked_unit, UNIT_STATE_LIFE) > 0.0 then
                    call SetUnitPosition(picked_unit, MAIN_CITY_X, MAIN_CITY_Y)
                    call PanCameraToTimedForPlayer(p, MAIN_CITY_X, MAIN_CITY_Y, 0.1)
                    call DisplayTextToPlayer(p, 0, 0, "|cFF00FF00[系统]|r已传送回主城。")
                endif
            endif
        endif
        set p=null
        set picked_unit=null
        set picked_item=null
    endfunction
    // ============================================================================
    // 门派系统初始化函数
    // 初始化玩家门派完成状态、物品拾取事件监听和升级事件监听
    // ============================================================================
    function InitSectSystem takes nothing returns nothing
        local integer player_index
        local integer slot_index
        set player_index=0
        loop
            exitwhen player_index > 11
            set udg_player_sect_completed[player_index]=false
            // 初始化技能解锁状态
            set slot_index=0
            loop
                exitwhen slot_index > 5
                set udg_skill_unlocked[player_index * 20 + slot_index]=false
                set slot_index=slot_index + 1
            endloop
            // 创建物品拾取事件触发器
            set pick_item_trigger[player_index]=CreateTrigger()
            call TriggerRegisterPlayerUnitEvent(pick_item_trigger[player_index], Player(player_index), EVENT_PLAYER_UNIT_PICKUP_ITEM, null)
            call TriggerAddAction(pick_item_trigger[player_index], function Sect_ProcessPickupItem)
            // 创建升级事件触发器
            set level_up_trigger[player_index]=CreateTrigger()
            call TriggerRegisterPlayerUnitEvent(level_up_trigger[player_index], Player(player_index), EVENT_PLAYER_HERO_LEVEL, null)
            call TriggerAddAction(level_up_trigger[player_index], function Sect_ProcessHeroLevel)
            set player_index=player_index + 1
        endloop
        set udg_sect_system_initialized=true
    endfunction

//library SectSystem ends
//library YDWEEnableCreepSleepBJNull:
function YDWEEnableCreepSleepBJNull takes boolean enable returns nothing
    call SetPlayerState(Player(PLAYER_NEUTRAL_AGGRESSIVE), PLAYER_STATE_NO_CREEP_SLEEP, IntegerTertiaryOp(enable, 0, 1))
    // If we're disabling, attempt to wake any already-sleeping creeps.
    if ( not enable ) then
        call YDWEWakePlayerUnitsNull(Player(PLAYER_NEUTRAL_AGGRESSIVE))
    endif
endfunction

//library YDWEEnableCreepSleepBJNull ends
//library BossSkillSystem:
// ============================================================================
// Get Boss Type By Unit Id
// ============================================================================
// 根据单位ID获取BOSS类型
// ============================================================================
function BossSkillSystem___GetBossTypeByUnitId takes integer unit_id returns integer
    local integer i
    local integer j
    local integer index
    set i=BOSS_TYPE_STRENGTH
    loop
        exitwhen i > BOSS_TYPE_SUMMONER
        set j=THEME_TYPE_HEIFENG
        loop
            exitwhen j > THEME_TYPE_FINAL
            set index=i * INDEX_MULTIPLIER + j
            if udg_boss_unit_id[index] == unit_id then
                return i
            endif
            set j=j + 1
        endloop
        set i=i + 1
    endloop
    return 0
endfunction
// ============================================================================
// Get Boss Index
// ============================================================================
// 根据BOSS类型和主题类型获取索引
// 使用常量 INDEX_MULTIPLIER 代替魔法数字
// ============================================================================
function BossSkillSystem___GetBossIndex takes integer boss_type,integer theme_type returns integer
    return boss_type * INDEX_MULTIPLIER + theme_type
endfunction
// ============================================================================
// Get Boss Skill Cooldown
// ============================================================================
// 获取BOSS技能冷却时间
// 使用常量 INDEX_MULTIPLIER 代替魔法数字
// ============================================================================
function BossSkillSystem___GetBossSkillCooldown takes integer boss_type,integer skill_slot returns real
    local integer index
    set index=boss_type * INDEX_MULTIPLIER + skill_slot
    return udg_boss_skill_cooldown[index]
endfunction
// ============================================================================
// Set Boss Skill Cooldown
// ============================================================================
// 设置BOSS技能冷却时间
// 使用常量 INDEX_MULTIPLIER 代替魔法数字
// ============================================================================
function BossSkillSystem___SetBossSkillCooldown takes integer boss_type,integer skill_slot,real cooldown returns nothing
    local integer index
    set index=boss_type * INDEX_MULTIPLIER + skill_slot
    set udg_boss_skill_cooldown[index]=cooldown
endfunction
// ============================================================================
// Is Skill Ready
// ============================================================================
// 检查技能是否冷却完成
// ============================================================================
function BossSkillSystem___IsSkillReady takes unit boss,integer skill_slot returns boolean
    local integer handle_id
    local real last_used
    local real current_time
    local real cooldown
    local integer index
    if boss == null then
        return false
    endif
    set handle_id=GetHandleId(boss)
    set index=handle_id * INDEX_MULTIPLIER + skill_slot
    set last_used=udg_boss_skill_last_used[index]
    set current_time=GetGameTime()
    set cooldown=BossSkillSystem___GetBossSkillCooldown(udg_boss_type[handle_id] , skill_slot)
    return ( current_time - last_used ) >= cooldown
endfunction
// ============================================================================
// Get Available Skill Slots
// ============================================================================
// 获取可用的技能槽数量
// ============================================================================
function BossSkillSystem___GetAvailableSkillSlots takes unit boss returns integer
    local integer handle_id
    local integer count
    local integer i
    if boss == null then
        return 0
    endif
    set handle_id=GetHandleId(boss)
    set count=0
    set i=1
    loop
        exitwhen i > BOSS_SKILL_SLOT_COUNT
        if BossSkillSystem___IsSkillReady(boss , i) then
            set count=count + 1
        endif
        set i=i + 1
    endloop
    return count
endfunction
// ============================================================================
// Select Skill Slot
// ============================================================================
// 选择要施放的技能槽
// ============================================================================
function BossSkillSystem___SelectSkillSlot takes unit boss returns integer
    local integer handle_id
    local integer boss_type
    local integer phase
    local integer available_slots
    local integer selected_slot
    local integer i
    if boss == null then
        return 0
    endif
    set handle_id=GetHandleId(boss)
    set boss_type=udg_boss_type[handle_id]
    set phase=udg_boss_phase[handle_id]
    set available_slots=BossSkillSystem___GetAvailableSkillSlots(boss)
    if available_slots == 0 then
        return 0
    endif
    // 根据BOSS类型和阶段选择技能
    if boss_type == BOSS_TYPE_STRENGTH then
        // 力量型BOSS：优先使用攻击技能
        set i=1
        loop
            exitwhen i > BOSS_SKILL_SLOT_COUNT
            if BossSkillSystem___IsSkillReady(boss , i) and udg_boss_skill_type[handle_id * INDEX_MULTIPLIER + i] == SKILL_TYPE_ATTACK then
                return i
            endif
            set i=i + 1
        endloop
    elseif boss_type == BOSS_TYPE_DEFENSE then
        // 防御型BOSS：优先使用防御技能
        set i=1
        loop
            exitwhen i > BOSS_SKILL_SLOT_COUNT
            if BossSkillSystem___IsSkillReady(boss , i) and udg_boss_skill_type[handle_id * INDEX_MULTIPLIER + i] == SKILL_TYPE_DEFENSE then
                return i
            endif
            set i=i + 1
        endloop
    elseif boss_type == BOSS_TYPE_AGILITY then
        // 敏捷型BOSS：优先使用控制技能
        set i=1
        loop
            exitwhen i > BOSS_SKILL_SLOT_COUNT
            if BossSkillSystem___IsSkillReady(boss , i) and udg_boss_skill_type[handle_id * INDEX_MULTIPLIER + i] == SKILL_TYPE_CONTROL then
                return i
            endif
            set i=i + 1
        endloop
    elseif boss_type == BOSS_TYPE_CASTER then
        // 法师型BOSS：优先使用范围技能
        set i=1
        loop
            exitwhen i > BOSS_SKILL_SLOT_COUNT
            if BossSkillSystem___IsSkillReady(boss , i) and udg_boss_skill_type[handle_id * INDEX_MULTIPLIER + i] == SKILL_TYPE_AOE then
                return i
            endif
            set i=i + 1
        endloop
    elseif boss_type == BOSS_TYPE_SUMMONER then
        // 召唤型BOSS：优先使用召唤技能
        set i=1
        loop
            exitwhen i > BOSS_SKILL_SLOT_COUNT
            if BossSkillSystem___IsSkillReady(boss , i) and udg_boss_skill_type[handle_id * INDEX_MULTIPLIER + i] == SKILL_TYPE_SUMMON then
                return i
            endif
            set i=i + 1
        endloop
    endif
    // 如果没有找到优先技能，选择第一个可用的技能
    set i=1
    loop
        exitwhen i > BOSS_SKILL_SLOT_COUNT
        if BossSkillSystem___IsSkillReady(boss , i) then
            return i
        endif
        set i=i + 1
    endloop
    return 0
endfunction
// ============================================================================
// Get Closest Enemy Unit
// ============================================================================
// 获取最近的敌方单位
// ============================================================================
function GetClosestEnemyUnit takes unit boss returns unit
    local group enemy_group
    local unit closest_unit
    local unit current_unit
    local real boss_x
    local real boss_y
    local real current_distance
    local real min_distance
    if boss == null then
        return null
    endif
    set boss_x=GetUnitX(boss)
    set boss_y=GetUnitY(boss)
    set enemy_group=CreateGroup()
    call GroupEnumUnitsInRange(enemy_group, boss_x, boss_y, 1000.0, null)
    set closest_unit=null
    set min_distance=999999.0
    loop
        set current_unit=FirstOfGroup(enemy_group)
        exitwhen current_unit == null
        if IsUnitEnemy(current_unit, GetOwningPlayer(boss)) and not IsUnitDeadBJ(current_unit) then
            set current_distance=DistanceBetweenPointsEx(boss_x , boss_y , GetUnitX(current_unit) , GetUnitY(current_unit))
            if current_distance < min_distance then
                set min_distance=current_distance
                set closest_unit=current_unit
            endif
        endif
        call GroupRemoveUnit(enemy_group, current_unit)
    endloop
    call DestroyGroup(enemy_group)
    set enemy_group=null
    return closest_unit
endfunction
// ============================================================================
// Cast Strength Boss Skill
// ============================================================================
// 施放力量型BOSS技能
// ============================================================================
function BossSkillSystem___CastStrengthBossSkill takes unit boss,integer skill_slot returns nothing
    local integer handle_id
    local integer skill_id
    local unit target
    local real boss_x
    local real boss_y
    if boss == null then
        return
    endif
    set handle_id=GetHandleId(boss)
    set skill_id=udg_boss_skill_id[handle_id * INDEX_MULTIPLIER + skill_slot]
    // 获取最近的敌方单位作为目标
    set target=GetClosestEnemyUnit(boss)
    if target != null then
        // 施放技能
        call IssueTargetOrderById(boss, skill_id, target)
        // 更新技能最后使用时间
        set udg_boss_skill_last_used[handle_id * INDEX_MULTIPLIER + skill_slot]=GetGameTime()
        // 显示技能施放效果
        set boss_x=GetUnitX(boss)
        set boss_y=GetUnitY(boss)
        call AddSpecialEffectTarget("Abilities\\Spells\\Orc\\WarStomp\\WarStompCaster.mdl", boss, "origin")
        set target=null
    endif
endfunction
// ============================================================================
// Cast Defense Boss Skill
// ============================================================================
// 施放防御型BOSS技能
// ============================================================================
function BossSkillSystem___CastDefenseBossSkill takes unit boss,integer skill_slot returns nothing
    local integer handle_id
    local integer skill_id
    if boss == null then
        return
    endif
    set handle_id=GetHandleId(boss)
    set skill_id=udg_boss_skill_id[handle_id * INDEX_MULTIPLIER + skill_slot]
    // 对自己施放防御技能
    call IssueImmediateOrderById(boss, skill_id)
    // 更新技能最后使用时间
    set udg_boss_skill_last_used[handle_id * INDEX_MULTIPLIER + skill_slot]=GetGameTime()
    // 显示技能施放效果
    call AddSpecialEffectTarget("Abilities\\Spells\\Human\\Defend\\DefendCaster.mdl", boss, "origin")
endfunction
// ============================================================================
// Cast Agility Boss Skill
// ============================================================================
// 施放敏捷型BOSS技能
// ============================================================================
function BossSkillSystem___CastAgilityBossSkill takes unit boss,integer skill_slot returns nothing
    local integer handle_id
    local integer skill_id
    local unit target
    if boss == null then
        return
    endif
    set handle_id=GetHandleId(boss)
    set skill_id=udg_boss_skill_id[handle_id * INDEX_MULTIPLIER + skill_slot]
    // 获取最近的敌方单位作为目标
    set target=GetClosestEnemyUnit(boss)
    if target != null then
        // 施放控制技能
        call IssueTargetOrderById(boss, skill_id, target)
        // 更新技能最后使用时间
        set udg_boss_skill_last_used[handle_id * INDEX_MULTIPLIER + skill_slot]=GetGameTime()
        // 显示技能施放效果
        call AddSpecialEffectTarget("Abilities\\Spells\\Human\\Polymorph\\PolyMorphTarget.mdl", target, "origin")
        set target=null
    endif
endfunction
// ============================================================================
// Cast Caster Boss Skill
// ============================================================================
// 施放法师型BOSS技能
// ============================================================================
function BossSkillSystem___CastCasterBossSkill takes unit boss,integer skill_slot returns nothing
    local integer handle_id
    local integer skill_id
    local real boss_x
    local real boss_y
    if boss == null then
        return
    endif
    set handle_id=GetHandleId(boss)
    set skill_id=udg_boss_skill_id[handle_id * INDEX_MULTIPLIER + skill_slot]
    // 获取BOSS位置
    set boss_x=GetUnitX(boss)
    set boss_y=GetUnitY(boss)
    // 在BOSS位置施放范围技能
    call IssuePointOrderById(boss, skill_id, boss_x, boss_y)
    // 更新技能最后使用时间
    set udg_boss_skill_last_used[handle_id * INDEX_MULTIPLIER + skill_slot]=GetGameTime()
    // 显示技能施放效果
    call AddSpecialEffect("Abilities\\Spells\\Human\\FlameStrike\\FlameStrike1.mdl", boss_x, boss_y)
endfunction
// ============================================================================
// Cast Summoner Boss Skill
// ============================================================================
// 施放召唤型BOSS技能
// ============================================================================
function BossSkillSystem___CastSummonerBossSkill takes unit boss,integer skill_slot returns nothing
    local integer handle_id
    local integer skill_id
    local real boss_x
    local real boss_y
    if boss == null then
        return
    endif
    set handle_id=GetHandleId(boss)
    set skill_id=udg_boss_skill_id[handle_id * INDEX_MULTIPLIER + skill_slot]
    // 获取BOSS位置
    set boss_x=GetUnitX(boss)
    set boss_y=GetUnitY(boss)
    // 在BOSS位置施放召唤技能
    call IssuePointOrderById(boss, skill_id, boss_x + 200.0, boss_y)
    // 更新技能最后使用时间
    set udg_boss_skill_last_used[handle_id * INDEX_MULTIPLIER + skill_slot]=GetGameTime()
    // 显示技能施放效果
    call AddSpecialEffect("Abilities\\Spells\\Undead\\AnimateDead\\AnimateDeadTarget.mdl", boss_x + 200.0, boss_y)
endfunction
// ============================================================================
// Update Boss Phase
// ============================================================================
// 更新BOSS阶段
// ============================================================================
function BossSkillSystem___UpdateBossPhase takes unit boss returns nothing
    local integer handle_id
    local real current_hp
    local real max_hp
    local real hp_percent
    if boss == null then
        return
    endif
    set handle_id=GetHandleId(boss)
    set current_hp=GetUnitState(boss, UNIT_STATE_LIFE)
    set max_hp=GetUnitState(boss, UNIT_STATE_MAX_LIFE)
    if max_hp > 0.0 then
        set hp_percent=current_hp / max_hp * 100.0
        set udg_boss_hp_percent[handle_id]=hp_percent
        // 检查是否需要切换阶段
        if hp_percent <= 50.0 and udg_boss_phase[handle_id] == BOSS_PHASE_1 then
            set udg_boss_phase[handle_id]=BOSS_PHASE_2
            // 进入第二阶段，增强BOSS能力
            call SetUnitState(boss, UNIT_STATE_MAX_LIFE, max_hp * 1.5)
            call SetUnitState(boss, UNIT_STATE_LIFE, GetUnitState(boss, UNIT_STATE_MAX_LIFE))
            call SetUnitAbilityLevel(boss, GetUnitAbilityLevel(boss, 'Aatk'), 2)
            // 显示阶段切换效果
            call AddSpecialEffectTarget("Abilities\\Spells\\Human\\Avatar\\AvatarCaster.mdl", boss, "origin")
            call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000BOSS进入狂暴状态！|r")
        endif
    endif
endfunction
// ============================================================================
// Boss AI Timer Callback
// ============================================================================
// BOSS AI计时器回调函数
// ============================================================================
function BossSkillSystem___BossAITimerCallback takes nothing returns nothing
    local timer t
    local unit boss
    local integer handle_id
    local integer skill_slot
    local integer boss_type
    set t=GetExpiredTimer()
    set handle_id=GetHandleId(t)
    set boss=udg_boss_unit_ref[handle_id]
    if boss == null or IsUnitDeadBJ(boss) then
        // BOSS已死亡，销毁计时器
        call DestroyTimer(t)
        set udg_boss_ai_timer[handle_id]=null
        set t=null
        set boss=null
        return
    endif
    // 更新BOSS阶段
    call BossSkillSystem___UpdateBossPhase(boss)
    // 选择技能
    set skill_slot=BossSkillSystem___SelectSkillSlot(boss)
    if skill_slot > 0 then
        set boss_type=udg_boss_type[handle_id]
        // 根据BOSS类型施放技能
        if boss_type == BOSS_TYPE_STRENGTH then
            call BossSkillSystem___CastStrengthBossSkill(boss , skill_slot)
        elseif boss_type == BOSS_TYPE_DEFENSE then
            call BossSkillSystem___CastDefenseBossSkill(boss , skill_slot)
        elseif boss_type == BOSS_TYPE_AGILITY then
            call BossSkillSystem___CastAgilityBossSkill(boss , skill_slot)
        elseif boss_type == BOSS_TYPE_CASTER then
            call BossSkillSystem___CastCasterBossSkill(boss , skill_slot)
        elseif boss_type == BOSS_TYPE_SUMMONER then
            call BossSkillSystem___CastSummonerBossSkill(boss , skill_slot)
        endif
    endif
    set t=null
    set boss=null
endfunction
// ============================================================================
// Initialize Boss Skills
// ============================================================================
// 初始化BOSS技能
// 添加参数验证和错误处理
// ============================================================================
function InitializeBossSkills takes unit boss,integer dungeon_id returns nothing
    local integer handle_id
    local integer unit_id
    local integer boss_type
    local integer theme_type
    local integer boss_index
    local integer i
    local integer skill_slot_index
    // 参数验证
    if boss == null then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000错误: InitializeBossSkills - boss参数为空|r")
        return
    endif
    if dungeon_id < 1 or dungeon_id > 14 then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000错误: InitializeBossSkills - dungeon_id参数无效 (" + I2S(dungeon_id) + ")|r")
        return
    endif
    set handle_id=GetHandleId(boss)
    set unit_id=GetUnitTypeId(boss)
    set boss_type=BossSkillSystem___GetBossTypeByUnitId(unit_id)
    if boss_type == 0 then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000错误: InitializeBossSkills - 无法识别BOSS类型 (单位ID: " + I2S(unit_id) + ")|r")
        return
    endif
    // 默认使用第一个主题类型（山贼主题）
    set theme_type=THEME_TYPE_HEIFENG
    set boss_index=BossSkillSystem___GetBossIndex(boss_type , theme_type)
    // 存储BOSS信息
    set udg_boss_unit_ref[handle_id]=boss
    set udg_boss_type[handle_id]=boss_type
    set udg_boss_dungeon_id[handle_id]=dungeon_id
    set udg_boss_phase[handle_id]=BOSS_PHASE_1
    set udg_boss_hp_percent[handle_id]=100.0
    // 初始化技能数据
    set i=1
    loop
        exitwhen i > BOSS_SKILL_SLOT_COUNT
        set skill_slot_index=handle_id * INDEX_MULTIPLIER + i
        // 从怪物数据配置中获取技能ID和类型
        set udg_boss_skill_id[skill_slot_index]=udg_boss_skill_id[boss_index]
        set udg_boss_skill_type[skill_slot_index]=udg_boss_skill_type[boss_index]
        set udg_boss_skill_last_used[skill_slot_index]=0.0
        set udg_boss_skill_available[skill_slot_index]=true
        set i=i + 1
    endloop
    // 设置技能冷却时间（根据BOSS类型）
    if boss_type == BOSS_TYPE_STRENGTH then
        call BossSkillSystem___SetBossSkillCooldown(boss_type , 1 , 10.0) // 主要攻击技能
call BossSkillSystem___SetBossSkillCooldown(boss_type , 2 , 15.0) // 次要攻击技能
call BossSkillSystem___SetBossSkillCooldown(boss_type , 3 , 20.0) // 控制技能
call BossSkillSystem___SetBossSkillCooldown(boss_type , 4 , 30.0) // 大招
elseif boss_type == BOSS_TYPE_DEFENSE then
        call BossSkillSystem___SetBossSkillCooldown(boss_type , 1 , 8.0) // 防御技能
call BossSkillSystem___SetBossSkillCooldown(boss_type , 2 , 12.0) // 反击技能
call BossSkillSystem___SetBossSkillCooldown(boss_type , 3 , 25.0) // 护盾技能
call BossSkillSystem___SetBossSkillCooldown(boss_type , 4 , 40.0) // 无敌技能
elseif boss_type == BOSS_TYPE_AGILITY then
        call BossSkillSystem___SetBossSkillCooldown(boss_type , 1 , 6.0) // 快速攻击
call BossSkillSystem___SetBossSkillCooldown(boss_type , 2 , 10.0) // 闪避技能
call BossSkillSystem___SetBossSkillCooldown(boss_type , 3 , 15.0) // 控制技能
call BossSkillSystem___SetBossSkillCooldown(boss_type , 4 , 25.0) // 连击技能
elseif boss_type == BOSS_TYPE_CASTER then
        call BossSkillSystem___SetBossSkillCooldown(boss_type , 1 , 8.0) // 单体法术
call BossSkillSystem___SetBossSkillCooldown(boss_type , 2 , 12.0) // 范围法术
call BossSkillSystem___SetBossSkillCooldown(boss_type , 3 , 20.0) // 控制法术
call BossSkillSystem___SetBossSkillCooldown(boss_type , 4 , 35.0) // 终极法术
elseif boss_type == BOSS_TYPE_SUMMONER then
        call BossSkillSystem___SetBossSkillCooldown(boss_type , 1 , 10.0) // 召唤小怪
call BossSkillSystem___SetBossSkillCooldown(boss_type , 2 , 15.0) // 召唤精英
call BossSkillSystem___SetBossSkillCooldown(boss_type , 3 , 25.0) // 召唤BOSS
call BossSkillSystem___SetBossSkillCooldown(boss_type , 4 , 45.0) // 召唤大军
endif
    set boss=null
endfunction
// ============================================================================
// Start Boss AI Timer
// ============================================================================
// 启动BOSS AI计时器
// 添加参数验证和错误处理
// ============================================================================
function StartBossAITimer takes unit boss returns nothing
    local integer handle_id
    local timer t
    // 参数验证
    if boss == null then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000错误: StartBossAITimer - boss参数为空|r")
        return
    endif
    set handle_id=GetHandleId(boss)
    // 检查是否已存在计时器
    if udg_boss_ai_timer[handle_id] != null then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000警告: StartBossAITimer - BOSS已存在AI计时器|r")
        return
    endif
    // 创建并启动计时器
    set t=CreateTimer()
    set udg_boss_ai_timer[handle_id]=t
    call TimerStart(t, BOSS_AI_UPDATE_INTERVAL, true, function BossSkillSystem___BossAITimerCallback)
    set t=null
    set boss=null
endfunction
// ============================================================================
// Cleanup Boss Data
// ============================================================================
// 清理BOSS数据
// 添加参数验证和错误处理
// ============================================================================
function CleanupBossData takes unit boss returns nothing
    local integer handle_id
    local timer t
    local integer i
    // 参数验证
    if boss == null then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000错误: CleanupBossData - boss参数为空|r")
        return
    endif
    set handle_id=GetHandleId(boss)
    // 检查是否有数据需要清理
    if udg_boss_unit_ref[handle_id] == null then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000警告: CleanupBossData - BOSS数据已清理或不存在|r")
        return
    endif
    // 销毁计时器
    set t=udg_boss_ai_timer[handle_id]
    if t != null then
        call DestroyTimer(t)
        set udg_boss_ai_timer[handle_id]=null
        set t=null
    endif
    // 清理单位引用
    set udg_boss_unit_ref[handle_id]=null
    set udg_boss_type[handle_id]=0
    set udg_boss_dungeon_id[handle_id]=0
    set udg_boss_phase[handle_id]=0
    set udg_boss_hp_percent[handle_id]=0.0
    // 清理技能数据
    set i=1
    loop
        exitwhen i > BOSS_SKILL_SLOT_COUNT
        set udg_boss_skill_id[handle_id * INDEX_MULTIPLIER + i]=0
        set udg_boss_skill_type[handle_id * INDEX_MULTIPLIER + i]=0
        set udg_boss_skill_last_used[handle_id * INDEX_MULTIPLIER + i]=0.0
        set udg_boss_skill_available[handle_id * INDEX_MULTIPLIER + i]=false
        set i=i + 1
    endloop
    set boss=null
endfunction
// ============================================================================
// Get Boss Phase
// ============================================================================
// 获取BOSS当前阶段
// 添加参数验证和错误处理
// ============================================================================
function GetBossPhase takes unit boss returns integer
    local integer handle_id
    // 参数验证
    if boss == null then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000错误: GetBossPhase - boss参数为空|r")
        return 0
    endif
    set handle_id=GetHandleId(boss)
    // 检查是否有BOSS数据
    if udg_boss_unit_ref[handle_id] == null then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000错误: GetBossPhase - BOSS数据未初始化|r")
        return 0
    endif
    return udg_boss_phase[handle_id]
endfunction
// ============================================================================
// Get Boss HP Percent
// ============================================================================
// 获取BOSS生命值百分比
// 添加参数验证和错误处理
// ============================================================================
function GetBossHPPercent takes unit boss returns real
    local integer handle_id
    // 参数验证
    if boss == null then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000错误: GetBossHPPercent - boss参数为空|r")
        return 0.0
    endif
    set handle_id=GetHandleId(boss)
    // 检查是否有BOSS数据
    if udg_boss_unit_ref[handle_id] == null then
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cffff0000错误: GetBossHPPercent - BOSS数据未初始化|r")
        return 0.0
    endif
    return udg_boss_hp_percent[handle_id]
endfunction
// ============================================================================
// Is Boss In Phase 2
// ============================================================================
// 检查BOSS是否处于第二阶段
// ============================================================================
function IsBossInPhase2 takes unit boss returns boolean
    return GetBossPhase(boss) == BOSS_PHASE_2
endfunction
// ============================================================================
// Initialization Function
// ============================================================================
// 系统初始化函数
// ============================================================================
function InitBossSkillSystem takes nothing returns nothing
    local integer i
    local integer j
    // 初始化技能冷却时间数组
    set i=BOSS_TYPE_STRENGTH
    loop
        exitwhen i > BOSS_TYPE_SUMMONER
        set j=1
        loop
            exitwhen j > BOSS_SKILL_SLOT_COUNT
            call BossSkillSystem___SetBossSkillCooldown(i , j , 10.0) // 默认冷却时间
set j=j + 1
        endloop
        set i=i + 1
    endloop
    set udg_boss_skill_system_initialized[0]=true
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "BOSS技能系统初始化完成")
endfunction

//library BossSkillSystem ends
//library CultivationSystem:
    // ============================================================================
    // 获取玩家当前历练值
    // ============================================================================
    function Cultivation_GetExp takes integer player_id returns integer
        if player_id < 0 or player_id > 11 then
            return 0
        endif
        return udg_cultivation_exp[player_id]
    endfunction
    // ============================================================================
    // 获取玩家当前历练等级
    // ============================================================================
    function Cultivation_GetLevel takes integer player_id returns integer
        if player_id < 0 or player_id > 11 then
            return 1
        endif
        return udg_cultivation_level[player_id]
    endfunction
    // ============================================================================
    // 获取玩家历练伤害加成百分比
    // ============================================================================
    function Cultivation_GetBonus takes integer player_id returns integer
        local integer level
        if player_id < 0 or player_id > 11 then
            return 0
        endif
        set level=udg_cultivation_level[player_id]
        return udg_cultivation_bonus[level]
    endfunction
    // ============================================================================
    // 获取玩家历练伤害加成（用于伤害计算的小数形式）
    // ============================================================================
    function Cultivation_GetBonusReal takes integer player_id returns real
        return I2R(Cultivation_GetBonus(player_id)) / 100.0
    endfunction
    // ============================================================================
    // 处理升级事件
    // 当玩家历练等级提升时触发，显示提示并处理解锁内容
    // ============================================================================
    function Cultivation_OnLevelUp takes integer player_id,integer new_level returns nothing
        local player p
        local string level_name
        local string unlock_info
        local integer old_level
        local integer old_bonus
        local integer new_bonus
        set p=Player(player_id)
        set old_level=udg_cultivation_level[player_id]
        set old_bonus=udg_cultivation_bonus[old_level]
        set new_bonus=udg_cultivation_bonus[new_level]
        set level_name=udg_cultivation_name[new_level]
        set unlock_info=CultivationData_GetUnlockInfo(new_level)
        // 显示升级提示
        call DisplayTextToPlayer(p, 0, 0, "|cFFFF00FF========================================|r")
        call DisplayTextToPlayer(p, 0, 0, "|cFFFF00FF⚡ 历练等级提升！⚡|r")
        call DisplayTextToPlayer(p, 0, 0, "|cFFFFFF00境界：「|r" + level_name + "|cFFFFFF00」|r")
        call DisplayTextToPlayer(p, 0, 0, "|cFF00FF00伤害加成：|r" + I2S(old_bonus) + "% → |c00FF00FF" + I2S(new_bonus) + "%|r")
        // 显示解锁内容
        if unlock_info != "" then
            call DisplayTextToPlayer(p, 0, 0, "|cFF00FFFF新解锁：|r" + unlock_info)
        endif
        call DisplayTextToPlayer(p, 0, 0, "|cFFFF00FF========================================|r")
        // 处理各等级解锁内容
        if new_level == 2 then
            set udg_unlock_mid_dungeon[player_id]=true
            set udg_unlock_graduation_skill[player_id]=true
        elseif new_level == 3 then
            set udg_unlock_high_dungeon[player_id]=true
        elseif new_level == 4 then
            set udg_unlock_elite_dungeon[player_id]=true
        elseif new_level == 5 then
            set udg_unlock_ultimate_dungeon[player_id]=true
        elseif new_level == 6 then
            set udg_unlock_b_encounter[player_id]=true
        elseif new_level == 7 then
            set udg_unlock_a_encounter[player_id]=true
        endif
        // 通知任务系统历练等级提升
        // call Quest_OnCultivationLevelUp(player_id, new_level)
        set p=null
    endfunction
    // ============================================================================
    // 检查玩家历练等级是否需要提升
    // 内部调用，当历练值变化时自动检查
    // ============================================================================
    function Cultivation_CheckLevelUp takes integer player_id returns nothing
        local integer exp
        local integer current_level
        local integer new_level
        local boolean has_upgraded
        set exp=udg_cultivation_exp[player_id]
        set current_level=udg_cultivation_level[player_id]
        set has_upgraded=false
        // 检查是否可以升级
        loop
            exitwhen current_level >= 7 // 已满级
if exp >= udg_cultivation_threshold[current_level + 1] then
                set current_level=current_level + 1
                set has_upgraded=true
            else
                exitwhen true
            endif
        endloop
        // 如果有升级
        if has_upgraded then
            set udg_cultivation_level[player_id]=current_level
            call Cultivation_OnLevelUp(player_id , current_level)
        endif
    endfunction
    // ============================================================================
    // 添加历练值
    // 每次获得历练值时调用，会自动检查是否升级
    // ============================================================================
    function Cultivation_AddExp takes integer player_id,integer amount returns nothing
        local player p
        local integer old_exp
        local integer new_exp
        local integer old_level
        local integer new_level
        local integer old_bonus
        local integer new_bonus
        // 参数校验
        if player_id < 0 or player_id > 11 then
            return
        endif
        if amount <= 0 then
            return
        endif
        // 检查是否已满级
        if udg_cultivation_level[player_id] >= 7 then
            return
        endif
        set p=Player(player_id)
        set old_exp=udg_cultivation_exp[player_id]
        set old_level=udg_cultivation_level[player_id]
        set new_exp=old_exp + amount
        set new_exp=new_exp
        // 更新历练值
        set udg_cultivation_exp[player_id]=new_exp
        // 检查升级
        call Cultivation_CheckLevelUp(player_id)
        // 获取当前等级（可能已升级）
        set new_level=udg_cultivation_level[player_id]
        set new_bonus=udg_cultivation_bonus[new_level]
        // 如果升级了，显示提示
        if new_level > old_level then
            // 升级提示在Cultivation_OnLevelUp中处理
        elseif new_exp > old_exp then
            // 历练值增加但未升级，显示简要提示（可选）
            call DisplayTextToPlayer(p, 0, 0, "|cFFFFAA00获得 " + I2S(amount) + " 历练值|r")
        endif
        set p=null
    endfunction
    // ============================================================================
    // 获取历练进度百分比
    // ============================================================================
    function Cultivation_GetProgress takes integer player_id returns integer
        local integer level
        local integer current_exp
        local integer threshold
        local integer next_threshold
        local integer progress
        if player_id < 0 or player_id > 11 then
            return 0
        endif
        set level=udg_cultivation_level[player_id]
        // 满级
        if level >= 7 then
            return 100
        endif
        set current_exp=udg_cultivation_exp[player_id]
        set threshold=udg_cultivation_threshold[level]
        set next_threshold=udg_cultivation_threshold[level + 1]
        if next_threshold <= threshold then
            return 0
        endif
        set progress=R2I(I2R(current_exp - threshold) / I2R(next_threshold - threshold) * 100.0)
        if progress < 0 then
            set progress=0
        elseif progress > 100 then
            set progress=100
        endif
        return progress
    endfunction
    // ============================================================================
    // 获取距离下一级还需要多少历练值
    // ============================================================================
    function Cultivation_GetNextLevelExp takes integer player_id returns integer
        local integer level
        local integer current_exp
        local integer next_threshold
        if player_id < 0 or player_id > 11 then
            return 0
        endif
        set level=udg_cultivation_level[player_id]
        // 满级
        if level >= 7 then
            return 0
        endif
        set current_exp=udg_cultivation_exp[player_id]
        set next_threshold=udg_cultivation_threshold[level + 1]
        return next_threshold - current_exp
    endfunction
    // ============================================================================
    // 玩家升级事件处理
    // ============================================================================
    function Cultivation_ProcessHeroLevel takes nothing returns nothing
        // 此函数预留，用于未来可能的英雄等级与历练系统联动
        // 目前历练系统独立于英雄等级运行
    endfunction
    // ============================================================================
    // 历练系统初始化函数
    // ============================================================================
    function InitCultivationSystem takes nothing returns nothing
        local integer player_index
        // 初始化各玩家触发器
        set player_index=0
        loop
            exitwhen player_index > 11
            set udg_cultivation_initialized[player_index]=false
            set player_index=player_index + 1
        endloop
        set udg_cultivation_initialized[0]=true
    endfunction

//library CultivationSystem ends
//library HeroAttributeSystem:
    // ==========================================
    // 初始化函数
    // ==========================================
    function InitHeroAttributeSystem takes nothing returns nothing
        local integer i
        // 创建主哈希表
        set udg_hero_attribute_ht=InitHashtable()
        // 初始化玩家英雄映射数组
        set i=0
        loop
            exitwhen i > 11
            set udg_player_hero[i]=null
            set udg_player_hero_id[i]=0
            set i=i + 1
        endloop
        set HeroSystemInitialized[0]=true
    endfunction
    // ==========================================
    // 属性操作接口 - 原生属性 (War3直接支持)
    // ==========================================
    // 获取气血
    function HeroAttr_GetHealth takes unit hero returns real
        return GetUnitState(hero, UNIT_STATE_LIFE)
    endfunction
    // 设置气血
    function HeroAttr_SetHealth takes unit hero,real value returns nothing
        call SetUnitState(hero, UNIT_STATE_LIFE, value)
    endfunction
    // 获取内力
    function HeroAttr_GetMana takes unit hero returns real
        return GetUnitState(hero, UNIT_STATE_MANA)
    endfunction
    // 设置内力
    function HeroAttr_SetMana takes unit hero,real value returns nothing
        call SetUnitState(hero, UNIT_STATE_MANA, value)
    endfunction
    // 获取气血上限
    function HeroAttr_GetMaxHealth takes unit hero returns real
        return GetUnitState(hero, UNIT_STATE_MAX_LIFE)
    endfunction
    // 设置气血上限 (YDWE万能属性系统)
    function HeroAttr_SetMaxHealth takes unit hero,real value returns nothing
        call GeneralBonusSystemUnitSetBonus(hero , BONUS_TYPE_MAX_LIFE , MODE_SET , R2I(value))
    endfunction
    // 获取内力上限
    function HeroAttr_GetMaxMana takes unit hero returns real
        return GetUnitState(hero, UNIT_STATE_MAX_MANA)
    endfunction
    // 设置内力上限 (YDWE万能属性系统)
    function HeroAttr_SetMaxMana takes unit hero,real value returns nothing
        call GeneralBonusSystemUnitSetBonus(hero , BONUS_TYPE_MAX_MANA , MODE_SET , R2I(value))
    endfunction
    // 获取根骨
    function HeroAttr_GetConstitution takes unit hero returns integer
        return GetHeroStr(hero, false)
    endfunction
    // 设置根骨
    function HeroAttr_SetConstitution takes unit hero,integer value returns nothing
        call SetHeroStr(hero, value, true)
    endfunction
    // 增加根骨
    function HeroAttr_AddConstitution takes unit hero,integer delta returns nothing
        local integer current= HeroAttr_GetConstitution(hero)
        call HeroAttr_SetConstitution(hero , current + delta)
    endfunction
    // 获取悟性
    function HeroAttr_GetIntelligence takes unit hero returns integer
        return GetHeroInt(hero, false)
    endfunction
    // 设置悟性
    function HeroAttr_SetIntelligence takes unit hero,integer value returns nothing
        call SetHeroInt(hero, value, true)
    endfunction
    // 增加悟性
    function HeroAttr_AddIntelligence takes unit hero,integer delta returns nothing
        local integer current= HeroAttr_GetIntelligence(hero)
        call HeroAttr_SetIntelligence(hero , current + delta)
    endfunction
    // 获取身法
    function HeroAttr_GetAgility takes unit hero returns integer
        return GetHeroAgi(hero, false)
    endfunction
    // 设置身法
    function HeroAttr_SetAgility takes unit hero,integer value returns nothing
        call SetHeroAgi(hero, value, true)
    endfunction
    // 增加身法
    function HeroAttr_AddAgility takes unit hero,integer delta returns nothing
        local integer current= HeroAttr_GetAgility(hero)
        call HeroAttr_SetAgility(hero , current + delta)
    endfunction
    // 获取攻击速度
    function HeroAttr_GetTechnique takes unit hero returns integer
        return R2I(LoadReal(udg_hero_attribute_ht, GetHandleId(hero), ATTR_TECHNIQUE))
    endfunction
    // 设置攻击速度
    function HeroAttr_SetTechnique takes unit hero,integer value returns nothing
        call GeneralBonusSystemUnitSetBonus(hero , BONUS_TYPE_ATTACK_SPEED , MODE_SET , R2I(value))
        // 保存到哈希表
        call SaveReal(udg_hero_attribute_ht, GetHandleId(hero), ATTR_TECHNIQUE, value)
    endfunction
    // 增加攻击速度
    function HeroAttr_AddTechnique takes unit hero,integer delta returns nothing
        local integer current= HeroAttr_GetTechnique(hero)
        call HeroAttr_SetTechnique(hero , current + delta)
    endfunction
    // ==========================================
    // 属性操作接口 - 通用接口
    // ==========================================
    // 获取属性值 (通用接口，自动判断属性类型)
    function HeroAttr_Get takes unit hero,integer attr_id returns real
        local integer hero_key= GetHandleId(hero)
        local real value= 0.0
        // 判断是否为War3原生属性
        if attr_id == ATTR_HEALTH then
            // 气血 (当前值，非上限)
            return HeroAttr_GetHealth(hero)
        elseif attr_id == ATTR_MANA then
            // 内力 (当前值，非上限)
            return HeroAttr_GetMana(hero)
        elseif attr_id == ATTR_CONSTITUTION then
            // 根骨
            return I2R(HeroAttr_GetConstitution(hero))
        elseif attr_id == ATTR_INTELLIGENCE then
            // 悟性
            return I2R(HeroAttr_GetIntelligence(hero))
        elseif attr_id == ATTR_AGILITY then
            // 身法
            return I2R(HeroAttr_GetAgility(hero))
        elseif attr_id == ATTR_TECHNIQUE then
            // 武技
            return I2R(HeroAttr_GetTechnique(hero))
        elseif attr_id == ATTR_MAX_HEALTH then
            // 气血上限
            return HeroAttr_GetMaxHealth(hero)
        elseif attr_id == ATTR_MAX_MANA then
            // 内力上限
            return HeroAttr_GetMaxMana(hero)
        else
            // 其他属性使用哈希表
            return LoadReal(udg_hero_attribute_ht, hero_key, attr_id)
        endif
    endfunction
    // 设置属性值 (通用接口，自动判断属性类型)
    function HeroAttr_Set takes unit hero,integer attr_id,real value returns nothing
        local integer hero_key= GetHandleId(hero)
        // 判断是否为War3原生属性
        if attr_id == ATTR_HEALTH then
            // 气血
            call HeroAttr_SetHealth(hero , value)
        elseif attr_id == ATTR_MANA then
            // 内力
            call HeroAttr_SetMana(hero , value)
        elseif attr_id == ATTR_CONSTITUTION then
            // 根骨
            call HeroAttr_SetConstitution(hero , R2I(value))
        elseif attr_id == ATTR_INTELLIGENCE then
            // 悟性
            call HeroAttr_SetIntelligence(hero , R2I(value))
        elseif attr_id == ATTR_AGILITY then
            // 身法
            call HeroAttr_SetAgility(hero , R2I(value))
        elseif attr_id == ATTR_TECHNIQUE then
            // 武技
            call HeroAttr_SetTechnique(hero , R2I(value))
        elseif attr_id == ATTR_MAX_HEALTH then
            // 气血上限
            call HeroAttr_SetMaxHealth(hero , value)
        elseif attr_id == ATTR_MAX_MANA then
            // 内力上限
            call HeroAttr_SetMaxMana(hero , value)
        else
            // 其他属性使用哈希表
            call SaveReal(udg_hero_attribute_ht, hero_key, attr_id, value)
        endif
    endfunction
    // 增加属性值
    function HeroAttr_Add takes unit hero,integer attr_id,real delta returns nothing
        local real current= HeroAttr_Get(hero , attr_id)
        call HeroAttr_Set(hero , attr_id , current + delta)
    endfunction
    // 获取战斗属性
    function HeroAttr_GetAttack takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_ATTACK)
    endfunction
    function HeroAttr_GetSpellPower takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_SPELL_POWER)
    endfunction
    function HeroAttr_GetCritRate takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_CRIT_RATE)
    endfunction
    function HeroAttr_GetCritDamage takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_CRIT_DAMAGE)
    endfunction
    // 获取元素属性
    function HeroAttr_GetFirePower takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_FIRE_POWER)
    endfunction
    function HeroAttr_GetIcePower takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_ICE_POWER)
    endfunction
    function HeroAttr_GetThunderPower takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_THUNDER_POWER)
    endfunction
    function HeroAttr_GetPoisonPower takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_POISON_POWER)
    endfunction
    // 获取防御属性
    function HeroAttr_GetArmor takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_ARMOR)
    endfunction
    function HeroAttr_GetResistance takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_RESISTANCE)
    endfunction
    // 获取闪避率
    function HeroAttr_GetDodge takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_DODGE)
    endfunction
    // 获取吸血率
    function HeroAttr_GetLifesteal takes unit hero returns real
        return HeroAttr_Get(hero , ATTR_LIFESTEAL)
    endfunction
    // ==========================================
    // 英雄被动系统
    // ==========================================
    // 应用英雄被动效果 
    // FIXME
    function HeroPassive_Apply takes unit hero,integer hero_id returns nothing
        local integer player_id
        local integer hero_key
        if hero == null then
            return
        endif
        set player_id=GetPlayerId(GetOwningPlayer(hero))
        set hero_key=GetHandleId(hero)
        // 保存英雄引用
        set udg_player_hero[player_id]=hero
        set udg_player_hero_id[player_id]=hero_id
        // 根据英雄ID应用被动
        if hero_id == HERO_RUODIE then
            // 若蝶 - 蝶舞: 闪避+5%, 移动速度+5% 移速直接在英雄物编中处理
            call HeroAttr_Add(hero , ATTR_DODGE , 5.0)
        elseif hero_id == HERO_XIAOXIA then
            // 潇侠 - 侠义: 友伤+5%
            call SaveBoolean(udg_hero_attribute_ht, hero_key, 200, true)
        elseif hero_id == HERO_ZHANHEN then
            // 斩恨 - 杀伐: 对低血敌人伤害+10%
            call SaveBoolean(udg_hero_attribute_ht, hero_key, 201, true)
        elseif hero_id == HERO_JINXUAN then
            // 瑾轩 - 谋略: 经验+10%, 历练+10%
            call SaveReal(udg_hero_attribute_ht, hero_key, 202, 0.10)
            call SaveReal(udg_hero_attribute_ht, hero_key, 203, 0.10)
        elseif hero_id == HERO_KONGYAO then
            // 空瑶 - 仙影: 闪避+10%, 涅槃冷却-20%
            call HeroAttr_Add(hero , ATTR_DODGE , 10.0)
            call SaveReal(udg_hero_attribute_ht, hero_key, 204, - 20.0)
        elseif hero_id == HERO_JIANDAO then
            // 剑刀 - 铁壁: 护体+10%, 受伤时20%几率反击
            call HeroAttr_Add(hero , ATTR_ARMOR , 10.0)
            call SaveBoolean(udg_hero_attribute_ht, hero_key, 205, true)
            call SaveReal(udg_hero_attribute_ht, hero_key, 206, 20.0)
        elseif hero_id == HERO_SHENXING then
            // 神行 - 敏捷: 移动速度+10%, 冷却-5%
            call SetUnitMoveSpeed(hero, GetUnitMoveSpeed(hero) * 1.10)
            call HeroAttr_Add(hero , ATTR_COOLDOWN , - 5.0)
        elseif hero_id == HERO_CANGLANG then
            // 苍狼 - 狂野: 会心+10%, 吸血+5%
            call HeroAttr_Add(hero , ATTR_CRIT_RATE , 10.0)
            call HeroAttr_Add(hero , ATTR_LIFESTEAL , 5.0)
        elseif hero_id == HERO_HONGLING then
            // 红绫 - 灵犀: 会心+5%, 要害+10%
            call HeroAttr_Add(hero , ATTR_CRIT_RATE , 5.0)
            call HeroAttr_Add(hero , ATTR_CRIT_DAMAGE , 10.0)
        elseif hero_id == HERO_YUEHUA then
            // 月华 - 仙子: 移动速度+5%, 闪避+10%, 涅槃冷却-20%
            call SetUnitMoveSpeed(hero, GetUnitMoveSpeed(hero) * 1.05)
            call HeroAttr_Add(hero , ATTR_DODGE , 10.0)
            call SaveReal(udg_hero_attribute_ht, hero_key, 207, - 20.0)
        endif
    endfunction
    // 获取英雄被动加成值
    function HeroPassive_GetBonus takes unit hero,integer bonus_type returns real
        local integer hero_id
        local real bonus
        if hero == null then
            return 0.0
        endif
        set hero_id=udg_player_hero_id[GetPlayerId(GetOwningPlayer(hero))]
        set bonus=0.0
        // 根据加成类型和英雄ID返回对应值
        if bonus_type == 1 then
            // 移动速度加成
            if hero_id == HERO_RUODIE then
                set bonus=0.05
            elseif hero_id == HERO_SHENXING then
                set bonus=0.10
            elseif hero_id == HERO_YUEHUA then
                set bonus=0.05
            endif
        elseif bonus_type == 2 then
            // 闪避加成
            if hero_id == HERO_RUODIE then
                set bonus=5.0
            elseif hero_id == HERO_KONGYAO then
                set bonus=10.0
            elseif hero_id == HERO_YUEHUA then
                set bonus=10.0
            endif
        elseif bonus_type == 3 then
            // 会心加成
            if hero_id == HERO_CANGLANG then
                set bonus=10.0
            elseif hero_id == HERO_HONGLING then
                set bonus=5.0
            endif
        elseif bonus_type == 4 then
            // 要害加成
            if hero_id == HERO_HONGLING then
                set bonus=10.0
            endif
        elseif bonus_type == 5 then
            // 护体加成
            if hero_id == HERO_JIANDAO then
                set bonus=10.0
            endif
        elseif bonus_type == 6 then
            // 经验加成
            if hero_id == HERO_JINXUAN then
                set bonus=0.10
            endif
        elseif bonus_type == 7 then
            // 历练加成
            if hero_id == HERO_JINXUAN then
                set bonus=0.10
            endif
        endif
        return bonus
    endfunction
    // 检查英雄是否有特定被动标记
    function HeroPassive_HasFlag takes unit hero,integer flag_id returns boolean
        local integer hero_key
        if hero == null then
            return false
        endif
        set hero_key=GetHandleId(hero)
        return LoadBoolean(udg_hero_attribute_ht, hero_key, flag_id)
    endfunction
    // 获取英雄被动数值标记
    function HeroPassive_GetFlagValue takes unit hero,integer flag_id returns real
        local integer hero_key
        if hero == null then
            return 0.0
        endif
        set hero_key=GetHandleId(hero)
        return LoadReal(udg_hero_attribute_ht, hero_key, flag_id)
    endfunction
    // ==========================================
    // 英雄创建与初始化
    // ==========================================
    // 初始化英雄属性
    function Hero_InitAttributes takes unit hero,integer hero_id returns nothing
        local integer player_id
        if hero == null then
            return
        endif
        set player_id=GetPlayerId(GetOwningPlayer(hero))
        // 保存英雄引用
        set udg_player_hero[player_id]=hero
        set udg_player_hero_id[player_id]=hero_id
        // 初始化核心属性 (使用原生API)
        call HeroAttr_SetMaxHealth(hero , 500.0)
        call HeroAttr_SetHealth(hero , 500.0)
        call HeroAttr_SetMaxMana(hero , 300.0)
        call HeroAttr_SetMana(hero , 300.0)
        call HeroAttr_SetConstitution(hero , 10)
        call HeroAttr_SetIntelligence(hero , 10)
        call HeroAttr_SetAgility(hero , 10)
        call HeroAttr_Set(hero , ATTR_TECHNIQUE , 0.0)
        // 初始化战斗属性 (使用哈希表)
        call HeroAttr_Set(hero , ATTR_ATTACK , 20.0)
        call HeroAttr_Set(hero , ATTR_SPELL_POWER , 20.0)
        call HeroAttr_Set(hero , ATTR_CRIT_RATE , 5.0)
        call HeroAttr_Set(hero , ATTR_CRIT_DAMAGE , 150.0)
        call HeroAttr_Set(hero , ATTR_FIRE_POWER , 0.0)
        call HeroAttr_Set(hero , ATTR_ICE_POWER , 0.0)
        call HeroAttr_Set(hero , ATTR_THUNDER_POWER , 0.0)
        call HeroAttr_Set(hero , ATTR_POISON_POWER , 0.0)
        call HeroAttr_Set(hero , ATTR_ARMOR , 0.0)
        call HeroAttr_Set(hero , ATTR_RESISTANCE , 0.0)
        // 初始化技能属性
        call HeroAttr_Set(hero , ATTR_COOLDOWN , 0.0)
        call HeroAttr_Set(hero , ATTR_RANGE , 0.0)
        call HeroAttr_Set(hero , ATTR_COST , 0.0)
        call HeroAttr_Set(hero , ATTR_HASTE , 0.0)
        // 初始化特殊属性
        call HeroAttr_Set(hero , ATTR_BERSERK , 0.0)
        call HeroAttr_Set(hero , ATTR_NIRVANA , 0.0)
        call HeroAttr_Set(hero , ATTR_PENETRATION , 0.0)
        // 初始化扩展属性
        call HeroAttr_Set(hero , ATTR_DODGE , 0.0)
        call HeroAttr_Set(hero , ATTR_LIFESTEAL , 0.0)
        // 应用英雄被动
        call HeroPassive_Apply(hero , hero_id)
    endfunction
    // 增加英雄经验 (同时应用被动加成)
    function Hero_AddExperience takes unit hero,real amount returns nothing
        local real bonus
        local integer player_id
        if hero == null then
            return
        endif
        set player_id=GetPlayerId(GetOwningPlayer(hero))
        set bonus=HeroPassive_GetBonus(hero , 6) // 经验加成

        // 基础经验 + 被动加成
        call AddHeroXP(hero, R2I(amount * ( 1.0 + bonus )), true)
    endfunction
 // ============================================================================
    // Calculate Skill Damage
    // ============================================================================
    // 计算技能伤害
    // ============================================================================
    function HeroAttr_GetAttribute takes unit unit_id,integer attribute_type returns integer
        local integer attribute= 0
        if attribute_type == SKILL_ATTRIBUTE_TYPE_STR then
            set attribute=10 * HeroAttr_GetConstitution(unit_id) + R2I(HeroAttr_GetAttack(unit_id))
        elseif attribute_type == SKILL_ATTRIBUTE_TYPE_AGI then
            set attribute=20 * HeroAttr_GetAgility(unit_id)
        elseif attribute_type == SKILL_ATTRIBUTE_TYPE_INT then
            set attribute=10 * HeroAttr_GetIntelligence(unit_id) + R2I(HeroAttr_GetSpellPower(unit_id))
        elseif attribute_type == SKILL_ATTRIBUTE_TYPE_ALL then
            set attribute=( HeroAttr_GetConstitution(unit_id) + HeroAttr_GetAgility(unit_id) + HeroAttr_GetIntelligence(unit_id) ) * 7
        endif
        return attribute
    endfunction
    // 获取元素强度
    function HeroAttr_GetElementPower takes unit unit_id,integer element_type returns real
        local real element_power= 0.0
        if element_type == SKILL_ELEMENT_TYPE_FIRE then
            set element_power=HeroAttr_GetFirePower(unit_id)
        elseif element_type == SKILL_ELEMENT_TYPE_ICE then
            set element_power=HeroAttr_GetIcePower(unit_id)
        elseif element_type == SKILL_ELEMENT_TYPE_LIGHTNING then
            set element_power=HeroAttr_GetThunderPower(unit_id)
        elseif element_type == SKILL_ELEMENT_TYPE_POISON then
            set element_power=HeroAttr_GetPoisonPower(unit_id)
        elseif element_type == SKILL_ELEMENT_TYPE_ALL then
            set element_power=( HeroAttr_GetFirePower(unit_id) + HeroAttr_GetIcePower(unit_id) + HeroAttr_GetThunderPower(unit_id) + HeroAttr_GetPoisonPower(unit_id) ) / 4
        endif
        return element_power
    endfunction
    // 获取伤害减伤
    function HeroAttr_GetDamageReduction takes unit unit_id,integer damage_type returns real
        local real damage_reduction= 0.0
        if damage_type == SKILL_DAMAGE_TYPE_PHYSICAL then
            set damage_reduction=0.06 * HeroAttr_GetArmor(unit_id) / ( 1 + 0.06 * HeroAttr_GetResistance(unit_id) )
        elseif damage_type == SKILL_DAMAGE_TYPE_MAGICAL then
            set damage_reduction=0.06 * HeroAttr_GetResistance(unit_id) / ( 1 + 0.06 * HeroAttr_GetArmor(unit_id) )
        endif
        return damage_reduction
    endfunction
    function CalculateSkillDamage takes unit caster,unit target,integer skillId returns real
        local player p= GetOwningPlayer(caster)
        local integer player_id= GetPlayerId(p)
        local integer skill= GetSkillById(skillId)
        local real damage_coefficient= s__Skill_skill_damage_coefficient[skill]
        local integer attribute_type= s__Skill_skill_attribute_type[skill]
        local integer element_type= s__Skill_skill_element_type[skill]
        local integer damage_type= s__Skill_skill_damage_type[skill]
        local integer attribute= 0
local real section_coefficient= 1.0
local real element_power= 0.0
local real element_bonus= 0.0
local real equipment_bonus= 0.0
local real suit_bonus= 0.0
local real damage1= 0.0
        local real damage2= 0.0
        local real damage3= 0.0
        local real final_damage= 0.0
        local real cultivation_bonus= 0.0
local real critical_bonus= 1.0
local real damage_reduction= 0.0

        
        local integer section_id= udg_player_sect_selected[player_id]
        if section_id != 0 then
            set section_coefficient=sect_coefficient[section_id]
        endif
        // 如果caster为非玩家单位，需要设定一套默认属性
        if IsPlayerUser(p) then
            set attribute=HeroAttr_GetAttribute(caster , attribute_type)
            set cultivation_bonus=udg_cultivation_bonus[player_id] * 0.01
            set element_power=HeroAttr_GetElementPower(caster , element_type)
            if GetRandomReal(0, 100) <= HeroAttr_GetCritRate(caster) then
                set critical_bonus=HeroAttr_GetCritDamage(caster) * 0.01
            endif
        else
            set attribute=100
            set cultivation_bonus=0.0
            set element_power=0.5
            if GetRandomReal(0, 100) <= 20.0 then
                set critical_bonus=1.5
            endif
            set damage_reduction=HeroAttr_GetDamageReduction(target , damage_type)
        endif
        // 伤害1 = 当前属性 * 门派系数 * (1 + 历练加成)
        set damage1=attribute * section_coefficient * ( 1 + cultivation_bonus )
        // 伤害2 = 伤害1 + 装备属性加成
        set damage2=damage1 + equipment_bonus
        // 元素加成 = (火劲+冰劲+雷劲+毒劲) / 伤害2，上限 0.5  **不同技能对应不同元素加成**
        set element_bonus=RMinBJ(0.5, element_power / damage2)
        
        // 伤害3 = （伤害2 + 套装额外加成） * (1 + 元素加成)
        set damage3=( damage2 + suit_bonus ) * ( 1 + element_bonus )
        // 最终伤害 = 伤害3 * 暴击加成 * 技能系数 * 减伤（由护体和抗性决定）
        set final_damage=damage3 * critical_bonus * damage_coefficient * ( 1 - damage_reduction )
        return final_damage
    endfunction
    function DealDamage takes unit caster,unit target,real damage returns nothing
        call UnitDamageTarget(caster, target, damage, true, false, ATTACK_TYPE_MAGIC, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
    endfunction

//library HeroAttributeSystem ends
//library DungeonSystem:
    // ============================================================================
    // 检查玩家历练等级是否解锁指定副本
    // ============================================================================
    function DungeonSystem_IsUnlocked takes player p,integer dungeon_id returns boolean
        local integer player_id
        local integer cultivation_level
        local integer unlock_start
        local integer unlock_end
        set player_id=GetPlayerId(p)
        set cultivation_level=1
        // 此处需要对接历练系统获取实际历练等级
        // set cultivation_level = udg_player_cultivation_level[player_id]
        set unlock_start=( cultivation_level - 1 ) * UNLOCK_COUNT_PER_LEVEL + 1
        set unlock_end=cultivation_level * UNLOCK_COUNT_PER_LEVEL
        if dungeon_id >= unlock_start and dungeon_id <= unlock_end then
            return true
        endif
        return false
    endfunction
    // ============================================================================
    // 获取玩家已解锁的副本数量
    // ============================================================================
    function DungeonSystem_GetUnlockedCount takes player p returns integer
        local integer cultivation_level
        set cultivation_level=1
        // set cultivation_level = udg_player_cultivation_level[GetPlayerId(p)]
        return cultivation_level * UNLOCK_COUNT_PER_LEVEL
    endfunction
    // ============================================================================
    // 购买副本进入物品
    // ============================================================================
    function DungeonSystem_BuyEntryItem takes player p,integer dungeon_id returns boolean
        local integer player_id
        local item purchase_item
        set player_id=GetPlayerId(p)
        if not DungeonSystem_IsUnlocked(p , dungeon_id) then
            call DisplayTextToPlayer(p, 0, 0, "|cffff0000你的历练等级不足，无法进入此副本！|r")
            return false
        endif
        set purchase_item=CreateItem(DungeonData_GetItemId(dungeon_id), 0.00, 0.00)
        if purchase_item != null then
            call UnitAddItemSwapped(purchase_item, Hero_GetPlayerHero(player_id))
            call DisplayTextToPlayer(p, 0, 0, "|cff00ff00已购买「" + DungeonData_GetName(dungeon_id) + "」进入凭证！|r")
            set purchase_item=null
            return true
        else
            call DisplayTextToPlayer(p, 0, 0, "|cffff0000购买失败！|r")
            return false
        endif
    endfunction
    // ============================================================================
    // 获取副本难度倍数
    // ============================================================================
    function DungeonSystem_GetDifficultyMultiplier takes integer dungeon_id returns real
        local integer quality
        set quality=DungeonData_GetQuality(dungeon_id)
        if quality == DUNGEON_QUALITY_NORMAL then
            return 1.00
        elseif quality == DUNGEON_QUALITY_HARD then
            return 1.50
        elseif quality == DUNGEON_QUALITY_ELITE then
            return 2.00
        elseif quality == DUNGEON_QUALITY_MYTH then
            return 3.00
        endif
        return 1.00
    endfunction
    
    // ============================================================================
    // 启动副本战斗
    // ============================================================================
    function DungeonSystem_StartBattle takes player p,integer dungeon_id returns nothing
        local unit boss
        local real boss_x
        local real boss_y
        local real multiplier
        set boss_x=DungeonData_GetEntranceX(dungeon_id) + 800.00
        set boss_y=DungeonData_GetEntranceY(dungeon_id)
        set multiplier=DungeonSystem_GetDifficultyMultiplier(dungeon_id)
        set boss=CreateUnitAtLoc(p, DungeonData_GetBossUnitId(dungeon_id), Location(boss_x, boss_y), 0.00)
        call SetUnitState(boss, UNIT_STATE_MAX_LIFE, GetUnitState(boss, UNIT_STATE_MAX_LIFE) * multiplier) // FIXME
call SetUnitState(boss, UNIT_STATE_LIFE, GetUnitState(boss, UNIT_STATE_MAX_LIFE))
        // 初始化BOSS技能系统
        call InitializeBossSkills(boss , dungeon_id)
        call StartBossAITimer(boss)
        // 生成第一波小怪
        if dungeon_id >= 1 and dungeon_id <= 14 then
            // call SpawnMonsterWave(dungeon_id, 1)
        endif
        set boss=null
    endfunction
    // ============================================================================
    // 进入副本
    // ============================================================================
    function DungeonSystem_Enter takes player p,integer dungeon_id returns boolean
        local integer player_id
        local unit hero
        set player_id=GetPlayerId(p)
        set hero=Hero_GetPlayerHero(player_id)
        if not DungeonSystem_IsUnlocked(p , dungeon_id) then
            call DisplayTextToPlayer(p, 0, 0, "|cffff0000你的历练等级不足，无法进入此副本！|r")
            return false
        endif
        set udg_player_current_dungeon[player_id]=dungeon_id
        call DungeonData_SetState(dungeon_id , DUNGEON_STATE_ACTIVE)
        call DungeonData_AddPlayerCount(dungeon_id)
        set udg_dungeon_boss_alive[dungeon_id]=true
        call SetUnitPosition(hero, DungeonData_GetEntranceX(dungeon_id), DungeonData_GetEntranceY(dungeon_id))
        // 同时移动镜头
        call PanCameraToTimedForPlayer(p, DungeonData_GetEntranceX(dungeon_id), DungeonData_GetEntranceY(dungeon_id), 0.1)
        call DungeonSystem_StartBattle(p , dungeon_id)
        call DisplayTextToPlayer(p, 0, 0, "|cff00ff00已进入副本：「" + DungeonData_GetName(dungeon_id) + "」|r")
        call DisplayTextToPlayer(p, 0, 0, "|cffffff00目标：击败BOSS|r")
        set hero=null
        return true
    endfunction
    // ============================================================================
    // CleanupActiveMonsters
    // ============================================================================
    // 清理活跃怪物列表
    // 参数:
    //   dungeon_id - 副本ID
    // 返回: 清理的怪物数量
    // ============================================================================
    function CleanupActiveMonsters takes integer dungeon_id returns integer
        local integer i
        local integer max_count
        local unit monster
        local integer cleaned_count
        local integer base_index
        // 参数验证
        if dungeon_id < 1 or dungeon_id > 14 then
            return 0
        endif
        set max_count=udg_max_active_monsters[dungeon_id]
        set cleaned_count=0
        set base_index=dungeon_id * MONSTER_ARRAY_MULTIPLIER
        // 清理所有活跃怪物
        set i=0
        loop
            exitwhen i >= max_count
            set monster=udg_active_monsters[base_index + i]
            if monster != null then
                call RemoveUnit(monster)
                set udg_active_monsters[base_index + i]=null
                set cleaned_count=cleaned_count + 1
                set monster=null
            endif
            set i=i + 1
        endloop
        set udg_active_monster_count[dungeon_id]=0
        set udg_current_wave_number[dungeon_id]=0
        return cleaned_count
    endfunction
    // ============================================================================
    // 离开副本
    // ============================================================================
    function DungeonSystem_Exit takes player p returns nothing
        local integer player_id
        local integer dungeon_id
        local unit hero
        set player_id=GetPlayerId(p)
        set dungeon_id=udg_player_current_dungeon[player_id]
        set hero=Hero_GetPlayerHero(player_id)
        if dungeon_id == 0 then
            return
        endif
        call SetUnitPosition(hero, DUNGEON_AREA_CENTER_X, DUNGEON_AREA_CENTER_Y)
        set udg_player_current_dungeon[player_id]=0
        call DungeonData_RemovePlayerCount(dungeon_id)
        if DungeonData_GetPlayerCount(dungeon_id) <= 0 then
            call DungeonData_SetState(dungeon_id , DUNGEON_STATE_IDLE)
            call DungeonData_SetPlayerCount(dungeon_id , 0)
            // 清理副本中的小怪
            if dungeon_id >= 1 and dungeon_id <= 14 then
                call CleanupActiveMonsters(dungeon_id)
            endif
        endif
        call DisplayTextToPlayer(p, 0, 0, "|cff888888已离开副本。|r")
        set hero=null
    endfunction
    // ============================================================================
    // 玩家拾取副本进入物品事件处理
    // ============================================================================
    function DungeonSystem_TrigItemPickup_Actions takes nothing returns nothing
        local unit picker
        local item picked_item
        local integer item_id
        local integer dungeon_id
        local integer player_id
        set picker=GetTriggerUnit()
        set picked_item=GetManipulatedItem()
        set item_id=GetItemTypeId(picked_item)
        set player_id=GetPlayerId(GetOwningPlayer(picker))
        set dungeon_id=DungeonData_GetDungeonIdByItemId(item_id)
        if dungeon_id > 0 then
            if udg_player_current_dungeon[player_id] != 0 then
                call DisplayTextToPlayer(GetOwningPlayer(picker), 0, 0, "|cffff0000你已经在副本中！|r")
                return
            endif
            call DungeonSystem_Enter(GetOwningPlayer(picker) , dungeon_id)
        endif
        set picker=null
        set picked_item=null
    endfunction
    // ============================================================================
    // 初始化物品拾取监听触发器
    // ============================================================================
    function DungeonSystem_InitItemPickupTrigger takes nothing returns nothing
        local trigger t
        set t=CreateTrigger()
        call TriggerRegisterAnyUnitEventBJ(t, EVENT_PLAYER_UNIT_PICKUP_ITEM)
        call TriggerAddAction(t, function DungeonSystem_TrigItemPickup_Actions)
        set t=null
    endfunction
    // ============================================================================
    // 获取副本掉落品质
    // ============================================================================
    function DungeonSystem_GetDropQuality takes integer dungeon_id returns integer
        local integer quality
        set quality=DungeonData_GetQuality(dungeon_id)
        if quality == DUNGEON_QUALITY_NORMAL then
            return DROP_QUALITY_COMMON
        elseif quality == DUNGEON_QUALITY_HARD then
            return DROP_QUALITY_RARE
        elseif quality == DUNGEON_QUALITY_ELITE then
            return DROP_QUALITY_EPIC
        elseif quality == DUNGEON_QUALITY_MYTH then
            return DROP_QUALITY_LEGEND
        endif
        return DROP_QUALITY_COMMON
    endfunction
    // ============================================================================
    // 发放装备奖励
    // ============================================================================
    function DungeonSystem_GrantEquipmentReward takes unit hero,integer dungeon_id returns nothing
        local integer drop_quality
        local item reward_item= null
        set drop_quality=DungeonSystem_GetDropQuality(dungeon_id)
        // set reward_item = CreateRandomEquipment(drop_quality) // FIXME
        if reward_item != null then
            call UnitAddItemSwapped(reward_item, hero)
            call DisplayTextToPlayer(GetOwningPlayer(hero), 0, 0, "|cff00ff00获得装备：「" + GetItemName(reward_item) + "」|r")
        endif
        set reward_item=null
    endfunction
    
    // ============================================================================
    // 发放材料奖励
    // ============================================================================
    function DungeonSystem_GrantMaterialReward takes unit hero,integer dungeon_id returns nothing
        // 需要与装备系统对接
    endfunction
    // ============================================================================
    // 添加玩家神话碎片
    // ============================================================================
    function DungeonSystem_AddPlayerMythFragment takes integer player_id,integer amount returns nothing
        local integer current_fragments
        set current_fragments=LoadInteger(YDHT, player_id, StringHash("MythFragment"))
        set current_fragments=current_fragments + amount
        call SaveInteger(YDHT, player_id, StringHash("MythFragment"), current_fragments)
    endfunction
    // ============================================================================
    // 发放神话碎片奖励
    // ============================================================================
    function DungeonSystem_GrantMythFragmentReward takes player p,integer dungeon_id returns nothing
        local integer player_id
        local integer fragment_count
        local real drop_rate
        set player_id=GetPlayerId(p)
        set fragment_count=GetRandomInt(FRAGMENT_DROP_MIN, FRAGMENT_DROP_MAX)
        set drop_rate=udg_fragment_drop_rate
        set fragment_count=R2I(I2R(fragment_count) * drop_rate)
        if fragment_count < 1 then
            set fragment_count=1
        endif
        call DungeonSystem_AddPlayerMythFragment(player_id , fragment_count)
        call DisplayTextToPlayer(p, 0, 0, "|cffff00ff获得神话碎片 x" + I2S(fragment_count) + "|r")
    endfunction
    // ============================================================================
    // 发放武学书籍奖励
    // ============================================================================
    function DungeonSystem_GrantMartialBookReward takes player p,integer dungeon_id returns nothing
        local integer book_item_id
        local unit hero
        local integer player_id
        set player_id=GetPlayerId(p)
        set hero=Hero_GetPlayerHero(player_id)
        set book_item_id=DungeonData_GetMartialBookId(dungeon_id)
        if book_item_id != 0 and GetRandomInt(1, 100) <= 30 then
            call UnitAddItemByIdSwapped(book_item_id, hero)
            call DisplayTextToPlayer(p, 0, 0, "|cff00ff00获得武学书籍！|r")
        endif
        set hero=null
    endfunction
    // ============================================================================
    // 发放首通奖励
    // ============================================================================
    function DungeonSystem_GrantFirstClearBonus takes player p returns nothing
        call DisplayTextToPlayer(p, 0, 0, "|cff00ff00首通额外奖励：神话碎片 x5|r")
        call DungeonSystem_AddPlayerMythFragment(GetPlayerId(p) , 5)
    endfunction
    // ============================================================================
    // 发放副本奖励
    // ============================================================================
    function DungeonSystem_GrantRewards takes player p,integer dungeon_id returns nothing
        local integer player_id
        local unit hero
        set player_id=GetPlayerId(p)
        set hero=Hero_GetPlayerHero(player_id)
        call DungeonSystem_GrantEquipmentReward(hero , dungeon_id)
        call DungeonSystem_GrantMaterialReward(hero , dungeon_id)
        if dungeon_id == DUNGEON_D013 or dungeon_id == DUNGEON_D014 then
            call DungeonSystem_GrantMythFragmentReward(p , dungeon_id)
        endif
        call DungeonSystem_GrantMartialBookReward(p , dungeon_id)
        if udg_player_dungeon_completed_today[player_id] == 0 then
            call DungeonSystem_GrantFirstClearBonus(p)
            set udg_player_dungeon_completed_today[player_id]=1
        endif
        set hero=null
    endfunction
    // ============================================================================
    // 检查副本内是否有存活BOSS
    // ============================================================================
    function DungeonSystem_HasAliveBoss takes integer dungeon_id returns boolean
        local group g
        local unit enum_unit
        local boolean found
        local integer boss_unit_id
        set g=CreateGroup()
        set found=false
        set boss_unit_id=DungeonData_GetBossUnitId(dungeon_id)
        call GroupEnumUnitsOfPlayer(g, Player(0), null)
        loop
            set enum_unit=FirstOfGroup(g)
            exitwhen enum_unit == null
            if GetUnitTypeId(enum_unit) == boss_unit_id then
                if GetUnitState(enum_unit, UNIT_STATE_LIFE) > 0 then
                    set found=true
                endif
            endif
            call GroupRemoveUnit(g, enum_unit)
        endloop
        call DestroyGroup(g)
        set g=null
        set enum_unit=null
        return found
    endfunction
    // ============================================================================
    // 检查玩家是否在副本中
    // ============================================================================
    function DungeonSystem_IsPlayerInDungeon takes player p returns boolean
        return udg_player_current_dungeon[GetPlayerId(p)] != 0
    endfunction
    // ============================================================================
    // 获取玩家当前所在副本ID
    // ============================================================================
    function DungeonSystem_GetPlayerDungeon takes player p returns integer
        return udg_player_current_dungeon[GetPlayerId(p)]
    endfunction
    // ============================================================================
    // 副本完成自动离开
    // ============================================================================
    function DungeonSystem_ExitAfterComplete takes nothing returns nothing
        local integer player_id
        local integer dungeon_id
        set player_id=0
        loop
            exitwhen player_id > 11
            if udg_player_current_dungeon[player_id] != 0 then
                set dungeon_id=udg_player_current_dungeon[player_id]
                call DungeonSystem_Exit(Player(player_id))
            endif
            set player_id=player_id + 1
        endloop
    endfunction
    // ============================================================================
    // BOSS死亡事件处理
    // ============================================================================
    function DungeonSystem_OnBossDeath takes unit dead_boss returns nothing
        local integer dungeon_id
        local integer player_id
        local player p
        local integer i
        set dungeon_id=0
        set i=1
        loop
            exitwhen i > 14
            if GetUnitTypeId(dead_boss) == DungeonData_GetBossUnitId(i) then
                set dungeon_id=i
                exitwhen true
            endif
            set i=i + 1
        endloop
        if dungeon_id == 0 then
            return
        endif
        if DungeonSystem_HasAliveBoss(dungeon_id) then
            return
        endif
        set udg_dungeon_boss_alive[dungeon_id]=false
        call DungeonData_SetState(dungeon_id , DUNGEON_STATE_COMPLETE)
        call DungeonData_AddCompleteCount(dungeon_id)
        set p=Player(0)
        set player_id=0
        loop
            exitwhen player_id > 11
            if udg_player_current_dungeon[player_id] == dungeon_id then
                set p=Player(player_id)
                exitwhen true
            endif
            set player_id=player_id + 1
        endloop
        call DungeonSystem_GrantRewards(p , dungeon_id)
        call DisplayTextToPlayer(p, 0, 0, "|cff00ff00恭喜！成功通关「" + DungeonData_GetName(dungeon_id) + "」！|r")
        // 清理副本中的小怪
        if dungeon_id >= 1 and dungeon_id <= 14 then
            call CleanupActiveMonsters(dungeon_id)
        endif
        // 清理BOSS数据
        call CleanupBossData(dead_boss)
        call TimerStart(CreateTimer(), 3.00, false, function DungeonSystem_ExitAfterComplete)
    endfunction
    // ============================================================================
    // 创建副本商店对话框
    // ============================================================================
    function DungeonSystem_CreateShopDialog takes player p returns nothing
        local integer player_id
        local integer unlocked_count
        local integer i
        local dialog d
        local button db
        set player_id=GetPlayerId(p)
        set unlocked_count=DungeonSystem_GetUnlockedCount(p)
        set d=DialogCreate()
        call DialogSetMessage(d, "副本商店 - 选择要购买的副本进入凭证")
        set i=1
        loop
            exitwhen i > unlocked_count
            exitwhen i > 14
            set db=DialogAddButton(d, DungeonData_GetName(i) + " (Lv." + I2S(DungeonData_GetMinLevel(i)) + "-" + I2S(DungeonData_GetMaxLevel(i)) + ")", 0)
            set i=i + 1
        endloop
        set db=DialogAddButton(d, "离开", 1)
        call DialogDisplay(p, d, true)
        set d=null
        set db=null
    endfunction
    // ============================================================================
    // 副本系统初始化
    // ============================================================================
    function InitDungeonSystem takes nothing returns nothing
        local integer i
        // 初始化副本数据
        call InitDungeonData()
        // 初始化玩家状态
        set i=0
        loop
            exitwhen i > 11
            set udg_player_current_dungeon[i]=0
            set udg_player_dungeon_completed_today[i]=0
            set i=i + 1
        endloop
        // 初始化BOSS状态
        set i=1
        loop
            exitwhen i > 14
            set udg_dungeon_boss_alive[i]=false
            set i=i + 1
        endloop
        // 初始化掉落倍率
        set udg_fragment_drop_rate=1.00
        // 初始化物品拾取触发器
        call DungeonSystem_InitItemPickupTrigger()
        call DisplayTextToPlayer(Player(0), 0, 0, "|cff00ff00副本系统初始化完成！|r")
    endfunction

//library DungeonSystem ends
//library EnemySkill:
    
    // ============================================================================
    // 敌人技能效果函数
    // ============================================================================
    // ============================================================================
    // 连击效果处理
    // ============================================================================
    function EnemySkillEffect_End2 takes nothing returns nothing
        local timer t= GetExpiredTimer()
        local unit caster= LoadUnitHandle(YDHT, GetHandleId(t), 0)
        local unit target= LoadUnitHandle(YDHT, GetHandleId(t), 1)
        local integer count= LoadInteger(YDHT, GetHandleId(t), 2)
        local integer skill_id= LoadInteger(YDHT, GetHandleId(t), 3)
        local real damage= 0.0
        if count > 0 and IsUnitAliveBJ(caster) and IsUnitAliveBJ(target) then
            call SetUnitAnimation(caster, "attack")
            set damage=CalculateSkillDamage(caster , target , skill_id)
            call DealDamage(caster , target , damage)
            call SaveInteger(YDHT, GetHandleId(t), 2, count - 1)
        else
            call SetUnitAnimation(caster, "stand")
            call DestroyTimer(t)
        endif
        set t=null
        set caster=null
        set target=null
    endfunction
    // ============================================================================
    // 远程射击效果处理
    // ============================================================================
    function EnemySkillEffect_End3 takes nothing returns nothing
        local timer t= GetExpiredTimer()
        local unit caster= LoadUnitHandle(YDHT, GetHandleId(t), 0)
        local unit target= LoadUnitHandle(YDHT, GetHandleId(t), 1)
        local integer skill_id= LoadInteger(YDHT, GetHandleId(t), 2)
        local real damage= 0.0
        local unit missile= null
        if IsUnitAliveBJ(caster) and IsUnitAliveBJ(target) then
            // 创建投射物（这里简单使用风暴之锤的模型作为演示，实际可根据需要替换）
            set missile=CreateUnit(GetOwningPlayer(caster), 'h000', GetUnitX(caster), GetUnitY(caster), 0)
            call UnitApplyTimedLife(missile, 'BTLF', 1.0)
            call SetUnitPathing(missile, false)
            // 模拟投射物飞行逻辑（简化版，直接造成伤害）FIXME
            set damage=CalculateSkillDamage(caster , target , skill_id)
            call DealDamage(caster , target , damage)
        endif
        call SetUnitAnimation(caster, "stand")
        call DestroyTimer(t)
        set t=null
        set caster=null
        set target=null
        set missile=null
    endfunction
    // ============================================================================
    // 防御姿态效果处理
    // ============================================================================
    function EnemySkillEffect_End4 takes nothing returns nothing
        local timer t= GetExpiredTimer()
        local unit caster= LoadUnitHandle(YDHT, GetHandleId(t), 0)
        local integer defense_bonus= LoadInteger(YDHT, GetHandleId(t), 1)
        if IsUnitAliveBJ(caster) then
            // 移除防御加成（这里假设有一个RemoveUnitBonus的API，实际需要根据属性系统实现）
            // call RemoveUnitBonus(caster, BONUS_TYPE_DEFENSE, defense_bonus)
            // 简单演示：播放消失动画或提示
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\Defend\\DefendCaster.mdl", caster, "overhead"))
        endif
        call DestroyTimer(t)
        set t=null
        set caster=null
    endfunction
    // ============================================================================
    // 冰冻术效果处理
    // ============================================================================
    function EnemySkillEffect_End5 takes nothing returns nothing
        local timer t= GetExpiredTimer()
        local unit target= LoadUnitHandle(YDHT, GetHandleId(t), 0)
        if IsUnitAliveBJ(target) then
            // 恢复单位速度（简单设置回默认值，实际需根据属性系统）
            call SetUnitMoveSpeed(target, GetUnitDefaultMoveSpeed(target))
            call SetUnitVertexColor(target, 255, 255, 255, 255)
        endif
        call DestroyTimer(t)
        set t=null
        set target=null
    endfunction
    // ============================================================================
    // 狂暴效果处理
    // ============================================================================
    function EnemySkillEffect_End6 takes nothing returns nothing
        local timer t= GetExpiredTimer()
        local unit caster= LoadUnitHandle(YDHT, GetHandleId(t), 0)
        if IsUnitAliveBJ(caster) then
            // 移除狂暴效果
            // call RemoveUnitBonus(caster, BONUS_TYPE_ATTACK_SPEED, 0.5)
            // 提示结束
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl", caster, "overhead"))
        endif
        call DestroyTimer(t)
        set t=null
        set caster=null
    endfunction
    // ============================================================================
    // 虚弱诅咒效果处理
    // ============================================================================
    function EnemySkillEffect_End7 takes nothing returns nothing
        local timer t= GetExpiredTimer()
        local unit target= LoadUnitHandle(YDHT, GetHandleId(t), 0)
        if IsUnitAliveBJ(target) then
            // 恢复属性
            // call RemoveUnitBonus(target, BONUS_TYPE_ATTACK, -20)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Undead\\Curse\\CurseTarget.mdl", target, "overhead"))
        endif
        call DestroyTimer(t)
        set t=null
        set target=null
    endfunction
    function EnemySkillEffect_End1 takes nothing returns nothing
        local timer t= GetExpiredTimer()
        local unit caster= LoadUnitHandle(YDHT, GetHandleId(t), 0)
        call SetUnitAnimation(caster, "stand")
        call DestroyTimer(t)
        set t=null
        set caster=null
    endfunction
    function EnemySkillEffect takes nothing returns boolean
        local unit caster= GetTriggerUnit()
        local unit target= GetSpellTargetUnit()
        local unit missile= null
        local integer skill= GetSkillByUnitAndTemplateId(caster , 'A000')
        local integer skill_id= s__Skill_skill_id[skill]
        local real damage= 0.0
        local timer t= null
        if skill_id == 0 then
            return false
        endif
        if skill_id == ENEMY_SKILL_NORMAL_ATTACK then
            call SetUnitAnimation(caster, "attack")
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
            set damage=CalculateSkillDamage(caster , target , skill_id)
            call DealDamage(caster , target , damage)
        elseif skill_id == ENEMY_SKILL_HEAVY_STRIKE then
            call SetUnitAnimation(caster, "attack slam")
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
            set damage=CalculateSkillDamage(caster , target , skill_id)
            call DealDamage(caster , target , damage)
        elseif skill_id == ENEMY_SKILL_COMBO_STRIKE then
            // 连击：连续攻击3次，每次间隔0.3秒
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call SaveUnitHandle(YDHT, GetHandleId(t), 1, target)
            call SaveInteger(YDHT, GetHandleId(t), 2, 3) // 攻击次数
call SaveInteger(YDHT, GetHandleId(t), 3, skill_id)
            call TimerStart(t, 0.3, true, function EnemySkillEffect_End2)
            // 立即执行第一次攻击
            call SetUnitAnimation(caster, "attack")
            set damage=CalculateSkillDamage(caster , target , skill_id)
            call DealDamage(caster , target , damage)
        elseif skill_id == ENEMY_SKILL_RANGE_SHOT then
            // 远程射击：播放攻击动作，0.3秒后造成伤害
            call SetUnitAnimation(caster, "attack")
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call SaveUnitHandle(YDHT, GetHandleId(t), 1, target)
            call SaveInteger(YDHT, GetHandleId(t), 2, skill_id)
            call TimerStart(t, 0.3, false, function EnemySkillEffect_End3)
        elseif skill_id == ENEMY_SKILL_PRECISION_SHOT then
            // 精准射击：高伤害单体攻击，带暴击特效
            call SetUnitAnimation(caster, "attack")
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
            
            set damage=CalculateSkillDamage(caster , target , skill_id)
            call DealDamage(caster , target , damage)
            // 额外特效
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\NightElf\\CriticalStrike\\CriticalStrike.mdl", target, "overhead"))
            
        elseif skill_id == ENEMY_SKILL_DEFENSIVE_STANCE then
            // 防御姿态：增加防御力，持续10秒
            call SetUnitAnimation(caster, "spell")
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\Defend\\DefendCaster.mdl", caster, "overhead"))
            
            // 增加防御力（示例值：20点）
            // call AddUnitBonus(caster, BONUS_TYPE_DEFENSE, 20)
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call SaveInteger(YDHT, GetHandleId(t), 1, 20) // 保存增加的防御值
call TimerStart(t, 10.0, false, function EnemySkillEffect_End4)
        elseif skill_id == ENEMY_SKILL_TAUNT then
            // 嘲讽：强制周围敌人攻击自己，持续5秒
            call SetUnitAnimation(caster, "spell")
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\NightElf\\Taunt\\TauntCaster.mdl", caster, "overhead"))
            
            // 选取周围300范围内的敌对单位
            call GroupEnumUnitsInRange(udg_temp_group, GetUnitX(caster), GetUnitY(caster), 300.0, null)
            loop
                set target=FirstOfGroup(udg_temp_group)
                exitwhen target == null
                if IsUnitEnemy(target, GetOwningPlayer(caster)) and IsUnitAliveBJ(target) then
                    // 强制攻击施法者
                    call IssueTargetOrder(target, "attack", caster)
                    // 播放受嘲讽特效
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Other\\HowlOfTerror\\HowlTarget.mdl", target, "overhead"))
                endif
                call GroupRemoveUnit(udg_temp_group, target)
            endloop
            
            // 清除临时组
            call GroupClear(udg_temp_group)
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
        elseif skill_id == ENEMY_SKILL_FIREBALL then
            // 火球术：发射火球，造成伤害
            call SetUnitAnimation(caster, "spell")
            
            // 创建投射物
            set missile=CreateUnit(GetOwningPlayer(caster), 'h000', GetUnitX(caster), GetUnitY(caster), 0)
            call UnitApplyTimedLife(missile, 'BTLF', 1.0)
            call SetUnitPathing(missile, false)
            // 替换为火球模型
            // call SetUnitModel(missile, "Abilities\\Weapons\\FireBallMissile\\FireBallMissile.mdl")
            
            set damage=CalculateSkillDamage(caster , target , skill_id)
            call DealDamage(caster , target , damage)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Other\\Incinerate\\FireLordDeathExplode.mdl", target, "origin"))
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
        elseif skill_id == ENEMY_SKILL_FREEZE then
            // 冰冻术：伤害并减速
            call SetUnitAnimation(caster, "spell")
            
            set damage=CalculateSkillDamage(caster , target , skill_id)
            call DealDamage(caster , target , damage)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Undead\\FrostNova\\FrostNovaTarget.mdl", target, "origin"))
            
            // 减速效果：降低50%移动速度，持续3秒
            call SetUnitMoveSpeed(target, GetUnitMoveSpeed(target) * 0.5)
            call SetUnitVertexColor(target, 100, 100, 255, 255) // 变蓝提示

            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, target)
            call TimerStart(t, 3.0, false, function EnemySkillEffect_End5)
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
        elseif skill_id == ENEMY_SKILL_HEAL then
            // 治疗术：随机治疗周围600范围内的友军单位
            call SetUnitAnimation(caster, "spell")
            
            // 选取周围友军
            call GroupEnumUnitsInRange(udg_temp_group, GetUnitX(caster), GetUnitY(caster), 600.0, null)
            set target=null
            // 简单筛选：找第一个非满血的友军（或随机一个）
            loop
                set target=FirstOfGroup(udg_temp_group)
                exitwhen target == null
                if IsUnitAlly(target, GetOwningPlayer(caster)) and IsUnitAliveBJ(target) and GetUnitState(target, UNIT_STATE_LIFE) < GetUnitState(target, UNIT_STATE_MAX_LIFE) then
                    // 找到目标，跳出循环
                    call GroupClear(udg_temp_group)
                    exitwhen true
                endif
                call GroupRemoveUnit(udg_temp_group, target)
            endloop
            
            // 如果没找到受伤队友，就治疗自己
            if target == null then
                set target=caster
            endif
            
            if target != null then
                // 计算治疗量
                set damage=CalculateSkillDamage(caster , target , skill_id)
                call SetUnitState(target, UNIT_STATE_LIFE, GetUnitState(target, UNIT_STATE_LIFE) + damage)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\Heal\\HealTarget.mdl", target, "origin"))
            endif
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
        elseif skill_id == ENEMY_SKILL_SUMMON_MINIONS then
            // 召唤小怪：在周围召唤两个援军
            call SetUnitAnimation(caster, "spell")
            
            // 在随机位置召唤两个单位（假设召唤单位类型为 'n000'，实际需根据副本配置动态获取或配置）
            // 这里暂用 步兵(hfoo) 作为演示
            call CreateUnit(GetOwningPlayer(caster), 'hfoo', GetUnitX(caster) + 150, GetUnitY(caster), 0)
            call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Human\\MassTeleport\\MassTeleportTarget.mdl", GetUnitX(caster) + 150, GetUnitY(caster)))
            
            call CreateUnit(GetOwningPlayer(caster), 'hfoo', GetUnitX(caster) - 150, GetUnitY(caster), 0)
            call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Human\\MassTeleport\\MassTeleportTarget.mdl", GetUnitX(caster) - 150, GetUnitY(caster)))
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
        elseif skill_id == ENEMY_SKILL_BERSERK then
            // 狂暴：提升攻速，持续15秒
            call SetUnitAnimation(caster, "spell")
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl", caster, "overhead"))
            
            // 增加50%攻速（需要属性系统支持）
            // call AddUnitBonus(caster, BONUS_TYPE_ATTACK_SPEED, 0.5)
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 15.0, false, function EnemySkillEffect_End6)
            
        elseif skill_id == ENEMY_SKILL_WEAKEN_CURSE then
            // 虚弱诅咒：削弱目标属性，持续8秒
            call SetUnitAnimation(caster, "spell")
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Undead\\Curse\\CurseTarget.mdl", target, "overhead"))
            
            // 减少目标攻击力（示例值：20点）
            // call AddUnitBonus(target, BONUS_TYPE_ATTACK, -20)
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, target)
            call TimerStart(t, 8.0, false, function EnemySkillEffect_End7)
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
        elseif skill_id == ENEMY_SKILL_FLAME_STORM then
            // 烈焰风暴：对目标区域造成伤害
            call SetUnitAnimation(caster, "spell")
            
            // 在目标位置创建特效
            call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Human\\FlameStrike\\FlameStrike1.mdl", GetUnitX(target), GetUnitY(target)))
            
            // 选取范围内的敌人造成伤害
            call GroupEnumUnitsInRange(udg_temp_group, GetUnitX(target), GetUnitY(target), 400.0, null)
            loop
                set target=FirstOfGroup(udg_temp_group)
                exitwhen target == null
                if IsUnitEnemy(target, GetOwningPlayer(caster)) and IsUnitAliveBJ(target) then
                    set damage=CalculateSkillDamage(caster , target , skill_id)
                    call DealDamage(caster , target , damage)
                endif
                call GroupRemoveUnit(udg_temp_group, target)
            endloop
            
            set t=CreateTimer()
            call SaveUnitHandle(YDHT, GetHandleId(t), 0, caster)
            call TimerStart(t, 0.5, false, function EnemySkillEffect_End1)
        endif
        set target=null
        set t=null
        set missile=null
        return false
    endfunction
    function InitEnemySkill takes nothing returns nothing
        local trigger t= CreateTrigger()
        set udg_enemy_skills[1]=s__Skill_create(ENEMY_SKILL_NORMAL_ATTACK , "普通攻击" , "进行一次普通攻击" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_UNIT , 'A000' , 1.0 , 0 , 1000 , 1 , SKILL_ATTRIBUTE_TYPE_ALL , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_PHYSICAL)
        set udg_enemy_skills[2]=s__Skill_create(ENEMY_SKILL_HEAVY_STRIKE , "重击" , "对目标造成重度伤害" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_UNIT , 'A000' , 5.0 , 20 , 150.0 , 2.0 , SKILL_ATTRIBUTE_TYPE_ALL , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_PHYSICAL)
        set udg_enemy_skills[3]=s__Skill_create(ENEMY_SKILL_COMBO_STRIKE , "连击" , "连续攻击目标" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_UNIT , 'A000' , 3.0 , 15 , 100.0 , 1.5 , SKILL_ATTRIBUTE_TYPE_ALL , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_PHYSICAL)
        set udg_enemy_skills[4]=s__Skill_create(ENEMY_SKILL_RANGE_SHOT , "远程射击" , "远程攻击目标" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_UNIT , 'A000' , 2.0 , 10 , 600.0 , 1.2 , SKILL_ATTRIBUTE_TYPE_ALL , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_PHYSICAL)
        set udg_enemy_skills[5]=s__Skill_create(ENEMY_SKILL_PRECISION_SHOT , "精准射击" , "精准打击弱点" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_UNIT , 'A000' , 8.0 , 30 , 800.0 , 2.4 , SKILL_ATTRIBUTE_TYPE_ALL , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_PHYSICAL)
        set udg_enemy_skills[6]=s__Skill_create(ENEMY_SKILL_DEFENSIVE_STANCE , "防御姿态" , "提升自身防御" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_NONE , 'A000' , 10.0 , 25 , 0.0 , 0.0 , SKILL_ATTRIBUTE_TYPE_ALL , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_PHYSICAL)
        set udg_enemy_skills[7]=s__Skill_create(ENEMY_SKILL_TAUNT , "嘲讽" , "嘲讽周围敌人" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_NONE , 'A000' , 15.0 , 20 , 300.0 , 0.0 , SKILL_ATTRIBUTE_TYPE_ALL , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_PHYSICAL)
        set udg_enemy_skills[8]=s__Skill_create(ENEMY_SKILL_FIREBALL , "火球术" , "发射火球攻击" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_UNIT , 'A000' , 6.0 , 40 , 500.0 , 3.0 , SKILL_ATTRIBUTE_TYPE_INT , SKILL_ELEMENT_TYPE_FIRE , SKILL_DAMAGE_TYPE_MAGICAL)
        set udg_enemy_skills[9]=s__Skill_create(ENEMY_SKILL_FREEZE , "冰冻术" , "冻结目标" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_UNIT , 'A000' , 8.0 , 35 , 400.0 , 1.6 , SKILL_ATTRIBUTE_TYPE_INT , SKILL_ELEMENT_TYPE_ICE , SKILL_DAMAGE_TYPE_MAGICAL)
        set udg_enemy_skills[10]=s__Skill_create(ENEMY_SKILL_HEAL , "治疗术" , "治疗友军" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_UNIT , 'A000' , 10.0 , 50 , 300.0 , 4.0 , SKILL_ATTRIBUTE_TYPE_INT , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_MAGICAL)
        set udg_enemy_skills[11]=s__Skill_create(ENEMY_SKILL_SUMMON_MINIONS , "召唤小怪" , "召唤援军" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_NONE , 'A000' , 20.0 , 60 , 0.0 , 0.0 , SKILL_ATTRIBUTE_TYPE_ALL , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_MAGICAL)
        set udg_enemy_skills[12]=s__Skill_create(ENEMY_SKILL_BERSERK , "狂暴" , "大幅提升攻速" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_NONE , 'A000' , 30.0 , 40 , 0.0 , 0.0 , SKILL_ATTRIBUTE_TYPE_ALL , SKILL_ELEMENT_TYPE_ALL , SKILL_DAMAGE_TYPE_PHYSICAL)
        set udg_enemy_skills[13]=s__Skill_create(ENEMY_SKILL_WEAKEN_CURSE , "虚弱诅咒" , "削弱目标属性" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_UNIT , 'A000' , 12.0 , 25 , 350.0 , 0.0 , SKILL_ATTRIBUTE_TYPE_INT , SKILL_ELEMENT_TYPE_POISON , SKILL_DAMAGE_TYPE_MAGICAL)
        set udg_enemy_skills[14]=s__Skill_create(ENEMY_SKILL_FLAME_STORM , "烈焰风暴" , "区域火焰伤害" , SKILL_TYPE_ACTIVE , SKILL_TARGET_TYPE_POINT , 'A000' , 25.0 , 80 , 400.0 , 4.0 , SKILL_ATTRIBUTE_TYPE_INT , SKILL_ELEMENT_TYPE_FIRE , SKILL_DAMAGE_TYPE_MAGICAL)
        set udg_enemy_skill_count=14
        // 登记玩家单位使用技能事件
        call TriggerRegisterAnyUnitEventBJ(t, EVENT_PLAYER_UNIT_SPELL_EFFECT)
        call TriggerAddCondition(t, Condition(function EnemySkillEffect))
        set t=null
    endfunction

//library EnemySkill ends
//library EquipmentSystem:
    // ============================================================================
    // 参数验证函数
    // ============================================================================
    function EquipmentSystem_ValidatePlayerId takes integer player_id returns boolean
        return player_id >= 0 and player_id < 12
    endfunction
    function EquipmentSystem_ValidateUnit takes unit u returns boolean
        return u != null and IsUnitType(u, UNIT_TYPE_HERO)
    endfunction
    function EquipmentSystem_ValidateEquipId takes integer equip_id returns boolean
        return equip_id >= 1 and equip_id <= udg_equip_count
    endfunction
    function EquipmentSystem_ValidateSlot takes integer slot returns boolean
        return slot >= 1 and slot <= 6
    endfunction
    // ============================================================================
    // 错误日志记录
    // ============================================================================
    function EquipmentSystem_LogError takes string message returns nothing
        call DisplayTextToPlayer(Player(0), 0, 0, "[装备系统错误] " + message)
        // 可以扩展为写入文件或发送到调试服务器
    endfunction
    function EquipmentSystem_LogWarning takes string message returns nothing
        call DisplayTextToPlayer(Player(0), 0, 0, "[装备系统警告] " + message)
    endfunction
    // ============================================================================
    // 缓存管理函数
    // ============================================================================
    function EquipmentSystem_InvalidateCache takes integer player_id returns nothing
        if EquipmentSystem_ValidatePlayerId(player_id) then
            set udg_player_equip_cache_valid[player_id]=false
            set udg_player_equip_cache_time[player_id]=0.0
        endif
    endfunction
    function EquipmentSystem_UpdateCache takes integer player_id returns nothing
        local real current_time= GetGameTime()
        if not EquipmentSystem_ValidatePlayerId(player_id) then
            return
        endif
        // 如果缓存有效且未过期(5秒内)，直接返回
        if udg_player_equip_cache_valid[player_id] and current_time - udg_player_equip_cache_time[player_id] < 5.0 then
            return
        endif
        // 重新计算属性加成
        // call EquipmentSystem_CalculateTotalBonus(player_id)
        // 更新缓存状态
        set udg_player_equip_cache_valid[player_id]=true
        set udg_player_equip_cache_time[player_id]=current_time
    endfunction
    function EquipmentSystem_GetCachedAttackBonus takes integer player_id returns real
        call EquipmentSystem_UpdateCache(player_id)
        return udg_player_equip_attack_bonus[player_id]
    endfunction
    function EquipmentSystem_GetCachedSpellPowerBonus takes integer player_id returns real
        call EquipmentSystem_UpdateCache(player_id)
        return udg_player_equip_spell_power_bonus[player_id]
    endfunction
    function EquipmentSystem_GetCachedHealthBonus takes integer player_id returns real
        call EquipmentSystem_UpdateCache(player_id)
        return udg_player_equip_health_bonus[player_id]
    endfunction
    // ============================================================================
    // 性能监控
    // ============================================================================
    function EquipmentSystem_StartPerformanceTimer takes nothing returns real
        return GetGameTime()
    endfunction
    function EquipmentSystem_EndPerformanceTimer takes real start_time,string operation_name returns nothing
        local real end_time= GetGameTime()
        local real duration= end_time - start_time
        if duration > 0.1 then // 超过100毫秒记录警告
call EquipmentSystem_LogWarning(operation_name + " 执行时间: " + R2S(duration) + "秒")
        endif
    endfunction
    // ============================================================================
    // 辅助函数：获取二维数组索引
    // ============================================================================
    function EquipmentSystem___GetPlayerSlotIndex takes integer player_id,integer slot returns integer
        return player_id * 6 + ( slot - 1 )
    endfunction
    // ============================================================================
    // 辅助函数：HeroAttr_Subtract（如果不存在则创建）
    // ============================================================================
    function HeroAttr_Subtract takes unit hero,integer attr_id,real delta returns nothing
        call HeroAttr_Add(hero , attr_id , - delta)
    endfunction
    // ============================================================================
    // 应用装备基础属性到英雄
    // ============================================================================
    function EquipmentSystem_ApplyBaseAttributes takes unit hero,integer equip_id returns nothing
        local real attack_value= I2R(udg_equip_attack[equip_id])
        local real spell_power_value= I2R(udg_equip_spell_power[equip_id])
        local real health_value= I2R(udg_equip_health[equip_id])
        local real armor_value= I2R(udg_equip_armor[equip_id])
        local real resistance_value= I2R(udg_equip_resistance[equip_id])
        local real move_speed_value= I2R(udg_equip_move_speed[equip_id])
        local real crit_rate_value= I2R(udg_equip_crit_rate[equip_id])
        local real crit_damage_value= I2R(udg_equip_crit_damage[equip_id])
        local real cooldown_value= I2R(udg_equip_cooldown[equip_id])
        local real range_value= I2R(udg_equip_range[equip_id])
        local real cost_value= I2R(udg_equip_cost[equip_id])
        local real haste_value= I2R(udg_equip_haste[equip_id])
        // 应用基础属性
        if attack_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_ATTACK , attack_value)
        endif
        if spell_power_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_SPELL_POWER , spell_power_value)
        endif
        if health_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_MAX_HEALTH , health_value)
        endif
        if armor_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_ARMOR , armor_value)
        endif
        if resistance_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_RESISTANCE , resistance_value)
        endif
        // 移动速度特殊处理（War3原生属性）
        if move_speed_value > 0.0 then
            call SetUnitMoveSpeed(hero, GetUnitDefaultMoveSpeed(hero) + move_speed_value)
        endif
        // 应用百分比属性
        if crit_rate_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_CRIT_RATE , crit_rate_value)
        endif
        if crit_damage_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_CRIT_DAMAGE , crit_damage_value)
        endif
        if cooldown_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_COOLDOWN , cooldown_value)
        endif
        if range_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_RANGE , range_value)
        endif
        if cost_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_COST , cost_value)
        endif
        if haste_value > 0.0 then
            call HeroAttr_Add(hero , ATTR_HASTE , haste_value)
        endif
    endfunction
    // ============================================================================
    // 应用装备元素属性到英雄
    // ============================================================================
    function EquipmentSystem_ApplyElementAttributes takes unit hero,integer equip_id returns nothing
        local integer element_type= udg_equip_element[equip_id]
        local real element_value= I2R(udg_equip_element_value[equip_id])
        if element_type == ELEMENT_NONE or element_value <= 0.0 then
            return
        endif
        if element_type == ELEMENT_FIRE then
            call HeroAttr_Add(hero , ATTR_FIRE_POWER , element_value)
        elseif element_type == ELEMENT_ICE then
            call HeroAttr_Add(hero , ATTR_ICE_POWER , element_value)
        elseif element_type == ELEMENT_THUNDER then
            call HeroAttr_Add(hero , ATTR_THUNDER_POWER , element_value)
        elseif element_type == ELEMENT_POISON then
            call HeroAttr_Add(hero , ATTR_POISON_POWER , element_value)
        endif
    endfunction
    // ============================================================================
    // 应用装备特殊效果到英雄
    // ============================================================================
    function EquipmentSystem_ApplySpecialEffects takes unit hero,integer equip_id returns nothing
        local integer special_type= udg_equip_special_type[equip_id]
        local real special_value= I2R(udg_equip_special_value[equip_id])
        if special_type == 0 or special_value <= 0.0 then
            return
        endif
        // 特殊效果类型映射
        if special_type == 1 then // 减伤%
call HeroAttr_Add(hero , ATTR_DAMAGE_REDUCTION , special_value)
        elseif special_type == 2 then // 恢复%
call HeroAttr_Add(hero , ATTR_HEAL_BONUS , special_value)
        elseif special_type == 3 then // 内力值
call SetUnitState(hero, UNIT_STATE_MAX_MANA, GetUnitState(hero, UNIT_STATE_MAX_MANA) + special_value)
        elseif special_type == 4 then // 护体值
call HeroAttr_Add(hero , ATTR_ARMOR , special_value)
        elseif special_type == 5 then // 冷却% (特殊)
call HeroAttr_Add(hero , ATTR_COOLDOWN_BONUS , special_value)
        elseif special_type == 6 then // 治疗%
call HeroAttr_Add(hero , ATTR_HEAL_BONUS , special_value)
        elseif special_type == 7 then // 急速%
call HeroAttr_Add(hero , ATTR_HASTE , special_value)
        elseif special_type == 8 then // 法强值
call HeroAttr_Add(hero , ATTR_SPELL_POWER , special_value)
        elseif special_type == 9 then // 抗性值
call HeroAttr_Add(hero , ATTR_RESISTANCE , special_value)
        elseif special_type == 10 then // 闪避%
call HeroAttr_Add(hero , ATTR_DODGE_BONUS , special_value)
        elseif special_type == 11 then // 移动速度%
call HeroAttr_Add(hero , ATTR_MOVE_SPEED_BONUS , special_value)
        elseif special_type == 12 then // 免疫减速
if special_value > 0.0 then
                call HeroAttr_Set(hero , ATTR_SLOW_IMMUNE , 1.0)
            endif
        elseif special_type == 13 then // 法力恢复%
call HeroAttr_Add(hero , ATTR_MANA_REGEN_BONUS , special_value)
        elseif special_type == 14 then // 范围%
call HeroAttr_Add(hero , ATTR_RANGE_BONUS , special_value)
        elseif special_type == 15 then // 全属性%
call HeroAttr_Add(hero , ATTR_ALL_ATTR_BONUS , special_value)
        elseif special_type == 16 then // 攻击%
call HeroAttr_Add(hero , ATTR_ATTACK_BONUS , special_value)
        elseif special_type == 17 then // 法强%
call HeroAttr_Add(hero , ATTR_SPELL_POWER_BONUS , special_value)
        elseif special_type == 99 then // 浴火重生
if special_value > 0.0 then
                call HeroAttr_Set(hero , ATTR_REBIRTH , 1.0)
            endif
        endif
    endfunction
    // ============================================================================
    // 从英雄移除装备基础属性
    // ============================================================================
    function EquipmentSystem_RemoveBaseAttributes takes unit hero,integer equip_id returns nothing
        local real attack_value= I2R(udg_equip_attack[equip_id])
        local real spell_power_value= I2R(udg_equip_spell_power[equip_id])
        local real health_value= I2R(udg_equip_health[equip_id])
        local real armor_value= I2R(udg_equip_armor[equip_id])
        local real resistance_value= I2R(udg_equip_resistance[equip_id])
        local real move_speed_value= I2R(udg_equip_move_speed[equip_id])
        local real crit_rate_value= I2R(udg_equip_crit_rate[equip_id])
        local real crit_damage_value= I2R(udg_equip_crit_damage[equip_id])
        local real cooldown_value= I2R(udg_equip_cooldown[equip_id])
        local real range_value= I2R(udg_equip_range[equip_id])
        local real cost_value= I2R(udg_equip_cost[equip_id])
        local real haste_value= I2R(udg_equip_haste[equip_id])
        // 移除基础属性
        if attack_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_ATTACK , attack_value)
        endif
        if spell_power_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_SPELL_POWER , spell_power_value)
        endif
        if health_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_MAX_HEALTH , health_value)
        endif
        if armor_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_ARMOR , armor_value)
        endif
        if resistance_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_RESISTANCE , resistance_value)
        endif
        // 移动速度特殊处理
        if move_speed_value > 0.0 then
            call SetUnitMoveSpeed(hero, GetUnitMoveSpeed(hero) - move_speed_value)
        endif
        // 移除百分比属性
        if crit_rate_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_CRIT_RATE , crit_rate_value)
        endif
        if crit_damage_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_CRIT_DAMAGE , crit_damage_value)
        endif
        if cooldown_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_COOLDOWN , cooldown_value)
        endif
        if range_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_RANGE , range_value)
        endif
        if cost_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_COST , cost_value)
        endif
        if haste_value > 0.0 then
            call HeroAttr_Subtract(hero , ATTR_HASTE , haste_value)
        endif
    endfunction
    // ============================================================================
    // 从英雄移除装备元素属性
    // ============================================================================
    function EquipmentSystem_RemoveElementAttributes takes unit hero,integer equip_id returns nothing
        local integer element_type= udg_equip_element[equip_id]
        local real element_value= I2R(udg_equip_element_value[equip_id])
        if element_type == ELEMENT_NONE or element_value <= 0.0 then
            return
        endif
        if element_type == ELEMENT_FIRE then
            call HeroAttr_Subtract(hero , ATTR_FIRE_POWER , element_value)
        elseif element_type == ELEMENT_ICE then
            call HeroAttr_Subtract(hero , ATTR_ICE_POWER , element_value)
        elseif element_type == ELEMENT_THUNDER then
            call HeroAttr_Subtract(hero , ATTR_THUNDER_POWER , element_value)
        elseif element_type == ELEMENT_POISON then
            call HeroAttr_Subtract(hero , ATTR_POISON_POWER , element_value)
        endif
    endfunction
    // ============================================================================
    // 从英雄移除装备特殊效果
    // ============================================================================
    function EquipmentSystem_RemoveSpecialEffects takes unit hero,integer equip_id returns nothing
        local integer special_type= udg_equip_special_type[equip_id]
        local real special_value= I2R(udg_equip_special_value[equip_id])
        if special_type == 0 or special_value <= 0.0 then
            return
        endif
        // 特殊效果类型映射
        if special_type == 1 then // 减伤%
call HeroAttr_Subtract(hero , ATTR_DAMAGE_REDUCTION , special_value)
        elseif special_type == 2 then // 恢复%
call HeroAttr_Subtract(hero , ATTR_HEAL_BONUS , special_value)
        elseif special_type == 3 then // 内力值
call SetUnitState(hero, UNIT_STATE_MAX_MANA, GetUnitState(hero, UNIT_STATE_MAX_MANA) - special_value)
        elseif special_type == 4 then // 护体值
call HeroAttr_Subtract(hero , ATTR_ARMOR , special_value)
        elseif special_type == 5 then // 冷却% (特殊)
call HeroAttr_Subtract(hero , ATTR_COOLDOWN_BONUS , special_value)
        elseif special_type == 6 then // 治疗%
call HeroAttr_Subtract(hero , ATTR_HEAL_BONUS , special_value)
        elseif special_type == 7 then // 急速%
call HeroAttr_Subtract(hero , ATTR_HASTE , special_value)
        elseif special_type == 8 then // 法强值
call HeroAttr_Subtract(hero , ATTR_SPELL_POWER , special_value)
        elseif special_type == 9 then // 抗性值
call HeroAttr_Subtract(hero , ATTR_RESISTANCE , special_value)
        elseif special_type == 10 then // 闪避%
call HeroAttr_Subtract(hero , ATTR_DODGE_BONUS , special_value)
        elseif special_type == 11 then // 移动速度%
call HeroAttr_Subtract(hero , ATTR_MOVE_SPEED_BONUS , special_value)
        elseif special_type == 12 then // 免疫减速
if special_value > 0.0 then
                call HeroAttr_Set(hero , ATTR_SLOW_IMMUNE , 0.0)
            endif
        elseif special_type == 13 then // 法力恢复%
call HeroAttr_Subtract(hero , ATTR_MANA_REGEN_BONUS , special_value)
        elseif special_type == 14 then // 范围%
call HeroAttr_Subtract(hero , ATTR_RANGE_BONUS , special_value)
        elseif special_type == 15 then // 全属性%
call HeroAttr_Subtract(hero , ATTR_ALL_ATTR_BONUS , special_value)
        elseif special_type == 16 then // 攻击%
call HeroAttr_Subtract(hero , ATTR_ATTACK_BONUS , special_value)
        elseif special_type == 17 then // 法强%
call HeroAttr_Subtract(hero , ATTR_SPELL_POWER_BONUS , special_value)
        elseif special_type == 99 then // 浴火重生
if special_value > 0.0 then
                call HeroAttr_Set(hero , ATTR_REBIRTH , 0.0)
            endif
        endif
    endfunction
    // ============================================================================
    // 应用装备所有属性到英雄
    // ============================================================================
    function EquipmentSystem_ApplyEquipmentAttributes takes unit hero,integer equip_id returns nothing
        local player owner
        // 参数验证
        if not EquipmentSystem_ValidateUnit(hero) then
            set owner=GetOwningPlayer(hero)
            if owner != null then
                call DisplayTextToPlayer(owner, 0, 0, "错误: 无效的英雄单位")
            endif
            call EquipmentSystem_LogError("无效的英雄单位，装备ID: " + I2S(equip_id))
            return
        endif
        if not EquipmentSystem_ValidateEquipId(equip_id) then
            call DisplayTextToPlayer(GetOwningPlayer(hero), 0, 0, "错误: 无效的装备ID")
            call EquipmentSystem_LogError("无效的装备ID: " + I2S(equip_id))
            return
        endif
        call EquipmentSystem_ApplyBaseAttributes(hero , equip_id)
        call EquipmentSystem_ApplyElementAttributes(hero , equip_id)
        call EquipmentSystem_ApplySpecialEffects(hero , equip_id)
        // 显示提示信息
        call DisplayTextToPlayer(GetOwningPlayer(hero), 0, 0, "装备 " + EquipmentData_GetName(equip_id) + " 属性已应用")
        // 排泄局部handle变量
        set owner=null
    endfunction
    // ============================================================================
    // 从英雄移除装备所有属性
    // ============================================================================
    function EquipmentSystem_RemoveEquipmentAttributes takes unit hero,integer equip_id returns nothing
        // 参数验证
        if not EquipmentSystem_ValidateUnit(hero) then
            call EquipmentSystem_LogError("移除属性时无效的英雄单位，装备ID: " + I2S(equip_id))
            return
        endif
        if not EquipmentSystem_ValidateEquipId(equip_id) then
            call DisplayTextToPlayer(GetOwningPlayer(hero), 0, 0, "错误: 无效的装备ID")
            call EquipmentSystem_LogError("移除属性时无效的装备ID: " + I2S(equip_id))
            return
        endif
        call EquipmentSystem_RemoveBaseAttributes(hero , equip_id)
        call EquipmentSystem_RemoveElementAttributes(hero , equip_id)
        call EquipmentSystem_RemoveSpecialEffects(hero , equip_id)
        // 显示提示信息
        call DisplayTextToPlayer(GetOwningPlayer(hero), 0, 0, "装备 " + EquipmentData_GetName(equip_id) + " 属性已移除")
    endfunction
    // ============================================================================
    // 显示装备信息
    // ============================================================================
    function EquipmentSystem_ShowEquipmentInfo takes integer player_id,integer equip_id,boolean isPickup returns nothing
        local string action= "拾取"
        local string msg
        if not isPickup then
            set action="扔下"
        endif
        set msg=action + "装备: " + EquipmentData_GetName(equip_id) + " (" + EQUIP_QUALITY_NAME[EquipmentData_GetQuality(equip_id)] + ")"
        // 显示基础属性
        if udg_equip_attack[equip_id] > 0 then
            set msg=msg + " | 武力+" + I2S(udg_equip_attack[equip_id])
        endif
        if udg_equip_spell_power[equip_id] > 0 then
            set msg=msg + " | 法强+" + I2S(udg_equip_spell_power[equip_id])
        endif
        if udg_equip_health[equip_id] > 0 then
            set msg=msg + " | 气血+" + I2S(udg_equip_health[equip_id])
        endif
        // 显示特殊效果
        if udg_equip_special_type[equip_id] > 0 then
            set msg=msg + " | 特效"
        endif
        call DisplayTextToPlayer(Player(player_id), 0, 0, msg)
    endfunction
    
    // ============================================================================
    // 处理装备拾取
    // ============================================================================
    function EquipmentSystem_OnEquipmentPickup takes integer player_id,unit hero,integer equip_id,item item_obj returns nothing
        local integer slot
        local integer old_equip_id
        local real start_time
        // 性能监控开始
        set start_time=EquipmentSystem_StartPerformanceTimer()
        // 参数验证
        if not EquipmentSystem_ValidatePlayerId(player_id) then
            call EquipmentSystem_LogError("拾取装备时无效的玩家ID: " + I2S(player_id))
            return
        endif
        if not EquipmentSystem_ValidateUnit(hero) then
            call EquipmentSystem_LogError("拾取装备时无效的英雄单位，玩家ID: " + I2S(player_id))
            return
        endif
        if not EquipmentSystem_ValidateEquipId(equip_id) then
            call EquipmentSystem_LogError("拾取装备时无效的装备ID: " + I2S(equip_id))
            return
        endif
        if not udg_equipment_system_initialized[player_id] then
            call EquipmentSystem_LogError("装备系统未初始化，玩家ID: " + I2S(player_id))
            return
        endif
        // 获取装备槽位
        set slot=EquipmentData_GetSlot(equip_id)
        if not EquipmentSystem_ValidateSlot(slot) then
            call DisplayTextToPlayer(Player(player_id), 0, 0, "装备槽位无效")
            call EquipmentSystem_LogError("无效的装备槽位: " + I2S(slot) + "，装备ID: " + I2S(equip_id))
            return
        endif
        // 检查槽位是否已有装备
        set old_equip_id=udg_player_equipped_item_id[EquipmentSystem___GetPlayerSlotIndex(player_id , slot)]
        if old_equip_id > 0 then
            // 先移除旧装备属性
            call EquipmentSystem_RemoveEquipmentAttributes(hero , old_equip_id)
            call DisplayTextToPlayer(Player(player_id), 0, 0, "替换装备: " + EquipmentData_GetName(old_equip_id))
        endif
        // 应用新装备属性
        call EquipmentSystem_ApplyEquipmentAttributes(hero , equip_id)
        // 更新玩家装备状态
        set udg_player_equipped_item_id[EquipmentSystem___GetPlayerSlotIndex(player_id , slot)]=equip_id
        // 显示装备信息
        call EquipmentSystem_ShowEquipmentInfo(player_id , equip_id , true)
        // 性能监控结束
        call EquipmentSystem_EndPerformanceTimer(start_time , "装备拾取处理")
        // 更新缓存
        call EquipmentSystem_InvalidateCache(player_id)
        // 排泄局部handle变量
        set item_obj=null
    endfunction
    // ============================================================================
    // 处理装备扔下
    // ============================================================================
    function EquipmentSystem_OnEquipmentDrop takes integer player_id,unit hero,integer equip_id,item item_obj returns nothing
        local integer slot
        local integer current_equip_id
        local real start_time
        // 性能监控开始
        set start_time=EquipmentSystem_StartPerformanceTimer()
        // 参数验证
        if not EquipmentSystem_ValidatePlayerId(player_id) then
            call EquipmentSystem_LogError("扔下装备时无效的玩家ID: " + I2S(player_id))
            return
        endif
        if not EquipmentSystem_ValidateUnit(hero) then
            call EquipmentSystem_LogError("扔下装备时无效的英雄单位，玩家ID: " + I2S(player_id))
            return
        endif
        if not EquipmentSystem_ValidateEquipId(equip_id) then
            call EquipmentSystem_LogError("扔下装备时无效的装备ID: " + I2S(equip_id))
            return
        endif
        if not udg_equipment_system_initialized[player_id] then
            call EquipmentSystem_LogError("装备系统未初始化，玩家ID: " + I2S(player_id))
            return
        endif
        // 获取装备槽位
        set slot=EquipmentData_GetSlot(equip_id)
        if not EquipmentSystem_ValidateSlot(slot) then
            call EquipmentSystem_LogError("无效的装备槽位: " + I2S(slot) + "，装备ID: " + I2S(equip_id))
            return
        endif
        // 检查当前槽位装备是否匹配
        set current_equip_id=udg_player_equipped_item_id[EquipmentSystem___GetPlayerSlotIndex(player_id , slot)]
        if current_equip_id != equip_id then
            // 装备不匹配，可能是其他玩家的装备
            call EquipmentSystem_LogWarning("装备不匹配，当前: " + I2S(current_equip_id) + "，扔下: " + I2S(equip_id))
            return
        endif
        // 移除装备属性
        call EquipmentSystem_RemoveEquipmentAttributes(hero , equip_id)
        // 清空玩家装备状态
        set udg_player_equipped_item_id[EquipmentSystem___GetPlayerSlotIndex(player_id , slot)]=0
        // 显示装备信息
        call EquipmentSystem_ShowEquipmentInfo(player_id , equip_id , false)
        // 性能监控结束
        call EquipmentSystem_EndPerformanceTimer(start_time , "装备扔下处理")
        // 更新缓存
        call EquipmentSystem_InvalidateCache(player_id)
        // 排泄局部handle变量
        set item_obj=null
    endfunction
    
    // ============================================================================
    // 初始化函数
    // ============================================================================
    function InitEquipmentSystem takes nothing returns nothing
        local integer i= 0
        local integer j
        local integer index
        loop
            exitwhen i >= 12
            set udg_equipment_system_initialized[i]=false
            // 初始化装备状态数组（模拟二维数组）
            set j=0
            loop
                exitwhen j >= 6
                set index=EquipmentSystem___GetPlayerSlotIndex(i , j + 1)
                set udg_player_equipped_item_id[index]=0
                set j=j + 1
            endloop
            // 初始化属性加成数组
            set udg_player_equip_attack_bonus[i]=0.0
            set udg_player_equip_spell_power_bonus[i]=0.0
            set udg_player_equip_health_bonus[i]=0.0
            set udg_player_equip_armor_bonus[i]=0.0
            set udg_player_equip_resistance_bonus[i]=0.0
            set udg_player_equip_move_speed_bonus[i]=0.0
            set udg_player_equip_crit_rate_bonus[i]=0.0
            set udg_player_equip_crit_damage_bonus[i]=0.0
            set udg_player_equip_cooldown_bonus[i]=0.0
            set udg_player_equip_range_bonus[i]=0.0
            set udg_player_equip_cost_bonus[i]=0.0
            set udg_player_equip_haste_bonus[i]=0.0
            // 特殊效果
            set udg_player_equip_damage_reduction_bonus[i]=0.0
            set udg_player_equip_heal_bonus[i]=0.0
            set udg_player_equip_attack_bonus_percent[i]=0.0
            set udg_player_equip_move_speed_bonus_percent[i]=0.0
            set udg_player_equip_dodge_bonus[i]=0.0
            set udg_player_equip_all_attr_bonus[i]=0.0
            // 元素属性
            set udg_player_equip_fire_power_bonus[i]=0.0
            set udg_player_equip_ice_power_bonus[i]=0.0
            set udg_player_equip_thunder_power_bonus[i]=0.0
            set udg_player_equip_poison_power_bonus[i]=0.0
            // 缓存机制
            set udg_player_equip_cache_valid[i]=false
            set udg_player_equip_cache_time[i]=0.0
            set udg_equipment_system_initialized[i]=true
            set i=i + 1
        endloop
        call DisplayTextToPlayer(Player(0), 0, 0, "装备属性系统初始化完成")
    endfunction
    // ============================================================================
    // 辅助函数和工具函数
    // ============================================================================
    // ============================================================================
    // 获取玩家当前装备ID
    // ============================================================================
    function EquipmentSystem_GetPlayerEquippedItem takes integer player_id,integer slot returns integer
        if player_id < 0 or player_id >= 12 or slot < 1 or slot > 6 then
            return 0
        endif
        return udg_player_equipped_item_id[EquipmentSystem___GetPlayerSlotIndex(player_id , slot)]
    endfunction
    // ============================================================================
    // 检查装备槽位是否可用
    // ============================================================================
    function EquipmentSystem_IsSlotAvailable takes integer player_id,integer slot returns boolean
        local integer current_equip_id= EquipmentSystem_GetPlayerEquippedItem(player_id , slot)
        return current_equip_id == 0
    endfunction
    // ============================================================================
    // 获取玩家装备总数
    // ============================================================================
    function EquipmentSystem_GetPlayerEquipmentCount takes integer player_id returns integer
        local integer count= 0
        local integer slot= 1
        loop
            exitwhen slot > 6
            if EquipmentSystem_GetPlayerEquippedItem(player_id , slot) > 0 then
                set count=count + 1
            endif
            set slot=slot + 1
        endloop
        return count
    endfunction
    // ============================================================================
    // 计算玩家装备总属性加成
    // ============================================================================
    function EquipmentSystem_CalculateTotalBonus takes integer player_id returns nothing
        local integer slot
        local integer equip_id
        local real total_attack= 0.0
        local real total_spell_power= 0.0
        local real total_health= 0.0
        set slot=1
        loop
            exitwhen slot > 6
            set equip_id=EquipmentSystem_GetPlayerEquippedItem(player_id , slot)
            if equip_id > 0 then
                set total_attack=total_attack + I2R(udg_equip_attack[equip_id])
                set total_spell_power=total_spell_power + I2R(udg_equip_spell_power[equip_id])
                set total_health=total_health + I2R(udg_equip_health[equip_id])
            endif
            set slot=slot + 1
        endloop
        // 更新缓存
        set udg_player_equip_attack_bonus[player_id]=total_attack
        set udg_player_equip_spell_power_bonus[player_id]=total_spell_power
        set udg_player_equip_health_bonus[player_id]=total_health
    endfunction
    // ============================================================================
    // 显示玩家装备状态
    // ============================================================================
    function EquipmentSystem_ShowPlayerEquipmentStatus takes integer player_id returns nothing
        local integer slot
        local integer equip_id
        local string msg
        call DisplayTextToPlayer(Player(player_id), 0, 0, "=== 装备状态 ===")
        set slot=1
        loop
            exitwhen slot > 6
            set equip_id=EquipmentSystem_GetPlayerEquippedItem(player_id , slot)
            if equip_id > 0 then
                set msg=EQUIP_SLOT_NAME[slot] + ": " + EquipmentData_GetName(equip_id)
                call DisplayTextToPlayer(Player(player_id), 0, 0, msg)
            else
                set msg=EQUIP_SLOT_NAME[slot] + ": 空"
                call DisplayTextToPlayer(Player(player_id), 0, 0, msg)
            endif
            set slot=slot + 1
        endloop
    endfunction

//library EquipmentSystem ends
//library HeroSelectionSystem:
// ============================================================================
// 英雄信息配置
// ============================================================================
function GetHeroInfo takes integer hero_id returns string
    // hero_id: 1-10 对应10个英雄
    if hero_id == HERO_RUODIE then
        return "若蝶 - 灵巧型英雄\n被动：蝶舞（闪避+5%，移动速度+5%）"
    elseif hero_id == HERO_XIAOXIA then
        return "潇侠 - 侠义型英雄\n被动：侠义（友伤+5%，攻击同一敌人叠加）"
    elseif hero_id == HERO_ZHANHEN then
        return "斩恨 - 杀伐型英雄\n被动：杀伐（对低血敌人伤害+10%）"
    elseif hero_id == HERO_JINXUAN then
        return "瑾轩 - 谋略型英雄\n被动：谋略（经验+10%，历练+10%）"
    elseif hero_id == HERO_KONGYAO then
        return "空瑶 - 飘逸型英雄\n被动：仙影（闪避+10%，涅槃冷却-20%）"
    elseif hero_id == HERO_JIANDAO then
        return "剑刀 - 刚猛型英雄\n被动：铁壁（护体+10%，受伤时反击）"
    elseif hero_id == HERO_SHENXING then
        return "神行 - 敏捷型英雄\n被动：敏捷（移动速度+10%，冷却-5%）"
    elseif hero_id == HERO_CANGLANG then
        return "苍狼 - 旷野型英雄\n被动：狂野（会心+10%，吸血+5%）"
    elseif hero_id == HERO_HONGLING then
        return "红绫 - 灵犀型英雄\n被动：灵犀（会心+5%，要害+10%）"
    elseif hero_id == HERO_YUEHUA then
        return "月华 - 仙子型英雄\n被动：仙子（移动速度+5%，闪避+10%，涅槃冷却-20%）"
    endif
    return "未知英雄"
endfunction
// ============================================================================
// 获取单位对应的英雄ID
// ============================================================================
// 地图单位变量对应表（基于unit.ini）：
// gg_unit_O000_0001 -> 若蝶 (HERO_RUODIE = 1)
// gg_unit_O001_0008 -> 潇侠 (HERO_XIAOXIA = 2)
// gg_unit_O002_0010 -> 斩恨 (HERO_ZHANHEN = 3)
// gg_unit_O003_0005 -> 瑾轩 (HERO_JINXUAN = 4)
// gg_unit_O004_0006 -> 空瑶 (HERO_KONGYAO = 5)
// gg_unit_O005_0004 -> 剑刀 (HERO_JIANDAO = 6)
// gg_unit_O006_0007 -> 神行 (HERO_SHENXING = 7)
// gg_unit_O007_0002 -> 苍狼 (HERO_CANGLANG = 8)
// gg_unit_O008_0003 -> 红绫 (HERO_HONGLING = 9)
// gg_unit_O009_0009 -> 月华 (HERO_YUEHUA = 10)
// ============================================================================
function GetHeroIdFromUnit takes unit u returns integer
    if u == gg_unit_O000_0001 then
        return HERO_RUODIE // 若蝶
elseif u == gg_unit_O001_0008 then
        return HERO_XIAOXIA // 潇侠
elseif u == gg_unit_O002_0010 then
        return HERO_ZHANHEN // 斩恨
elseif u == gg_unit_O003_0005 then
        return HERO_JINXUAN // 瑾轩
elseif u == gg_unit_O004_0006 then
        return HERO_KONGYAO // 空瑶
elseif u == gg_unit_O005_0004 then
        return HERO_JIANDAO // 剑刀
elseif u == gg_unit_O006_0007 then
        return HERO_SHENXING // 神行
elseif u == gg_unit_O007_0002 then
        return HERO_CANGLANG // 苍狼
elseif u == gg_unit_O008_0003 then
        return HERO_HONGLING // 红绫
elseif u == gg_unit_O009_0009 then
        return HERO_YUEHUA // 月华
endif
    return 0 // 无效单位
endfunction
// ============================================================================
// 检查单位是否可选择
// ============================================================================
function IsHeroSelectable takes unit u returns boolean
    return GetHeroIdFromUnit(u) != 0
endfunction
// ============================================================================
// 英雄选择事件处理
// ============================================================================
function OnHeroSelected takes nothing returns nothing
    local player p= GetTriggerPlayer()
    local unit selected_unit= GetTriggerUnit()
    local integer player_id= GetPlayerId(p)
    local real current_time= udg_game_time
    local real last_time= g_last_select_time[player_id]
    local unit last_unit= g_last_select_unit[player_id]
    local integer hero_id
    local string hero_name
    local string hero_info
    // 检查是否已选择过英雄
    if g_hero_selected[player_id] then
        set p=null
        set selected_unit=null
        return
    endif
    // 检查是否选择了有效的英雄单位
    set hero_id=GetHeroIdFromUnit(selected_unit)
    if hero_id == 0 then
        set p=null
        set selected_unit=null
        return
    endif
    set hero_name=GetUnitName(selected_unit)
    set hero_info=GetHeroInfo(hero_id)
    if TEST_MODE then
        call BJDebugMsg("Current Time: " + R2S(current_time) + ", Last Time: " + R2S(last_time))
    endif
    // 检查是否是双击（选择了同一个单位且时间间隔小于阈值）
    if last_unit == selected_unit and ( current_time - last_time ) < HERO_DOUBLE_CLICK_TIME then
        // 双击确认：归属单位给玩家
        call SetUnitOwner(selected_unit, p, true)
        // 移除无敌技能 (Avul)
        call UnitRemoveAbility(selected_unit, 'Avul')
        // 传送到出生点
        call SetUnitPosition(selected_unit, HERO_SPAWN_X, HERO_SPAWN_Y)
        // 标记玩家已选择英雄
        set g_hero_selected[player_id]=true
        // 提示玩家选择成功
        call DisplayTextToPlayer(p, 0, 0, "|c00FFFF00英雄选择成功！你选择了：|r " + hero_name)
        // 初始化英雄属性
        call Hero_InitAttributes(selected_unit , hero_id)
        // 记录玩家英雄
        set udg_player_hero[player_id]=selected_unit
        set udg_player_hero_id[player_id]=hero_id
        // 清空记录
        set g_last_select_unit[player_id]=null
        set g_last_select_time[player_id]=- 5
    else
        // 第一次选择：显示英雄信息
        call DisplayTextToPlayer(p, 0, 0, "|c00FFFF00" + hero_name + "|r")
        call DisplayTextToPlayer(p, 0, 0, hero_info)
        call DisplayTextToPlayer(p, 0, 0, "|c00AAAAAA（再次点击确认选择）|r")
        // 记录本次选择
        set g_last_select_unit[player_id]=selected_unit
        set g_last_select_time[player_id]=current_time
    endif
    // 清理本地变量
    set p=null
    set selected_unit=null
    set last_unit=null
endfunction
// ============================================================================
// 初始化函数
// ============================================================================
function InitHeroSelectionSystem takes nothing returns nothing
    local integer i= 0
    local trigger select_trigger
    call UnitAddAbility(gg_unit_O000_0001, 'Avul')
    call UnitAddAbility(gg_unit_O001_0008, 'Avul')
    call UnitAddAbility(gg_unit_O002_0010, 'Avul')
    call UnitAddAbility(gg_unit_O003_0005, 'Avul')
    call UnitAddAbility(gg_unit_O004_0006, 'Avul')
    call UnitAddAbility(gg_unit_O005_0004, 'Avul')
    call UnitAddAbility(gg_unit_O006_0007, 'Avul')
    call UnitAddAbility(gg_unit_O007_0002, 'Avul')
    call UnitAddAbility(gg_unit_O008_0003, 'Avul')
    call UnitAddAbility(gg_unit_O009_0009, 'Avul')
    
    // 初始化玩家选择状态
    loop
        exitwhen i > 11
        set g_last_select_unit[i]=null
        set g_last_select_time[i]=- 5
        set g_hero_selected[i]=false
        set i=i + 1
    endloop
    // 创建选择触发器
    set select_trigger=CreateTrigger()
    // 为所有玩家注册选择事件
    set i=0
    loop
        exitwhen i >= 12
        call TriggerRegisterPlayerUnitEvent(select_trigger, Player(i), EVENT_PLAYER_UNIT_SELECTED, null)
        set i=i + 1
    endloop
    // 添加触发动作
    call TriggerAddAction(select_trigger, function OnHeroSelected)
    set select_trigger=null
endfunction
// ============================================================================
// 公共接口函数
// ============================================================================
// 检查玩家是否已选择英雄
function IsPlayerHeroSelected takes integer player_id returns boolean
    if player_id < 0 or player_id > 11 then
        return false
    endif
    return g_hero_selected[player_id]
endfunction
// 获取玩家已选择的英雄单位
function GetPlayerSelectedHero takes integer player_id returns unit
    if player_id < 0 or player_id > 11 then
        return null
    endif
    return udg_player_hero[player_id]
endfunction

//library HeroSelectionSystem ends
//library DungeonMonsterSystem:
// ============================================================================
// GetDifficultyCoefficient
// ============================================================================
// 根据副本品质获取难度系数
// 参数:
//   dungeon_id - 副本ID (1-14)
// 返回: 难度系数 (1.0-2.0)
// ============================================================================
function GetDifficultyCoefficient takes integer dungeon_id returns real
    local integer quality
    // 参数验证
    if dungeon_id < 1 or dungeon_id > 14 then
        return DIFFICULTY_COEFFICIENT_NORMAL
    endif
    set quality=DungeonData_GetQuality(dungeon_id)
    if quality == DUNGEON_QUALITY_NORMAL then
        return DIFFICULTY_COEFFICIENT_NORMAL
    elseif quality == DUNGEON_QUALITY_HARD then
        return DIFFICULTY_COEFFICIENT_HARD
    elseif quality == DUNGEON_QUALITY_ELITE then
        return DIFFICULTY_COEFFICIENT_ELITE
    elseif quality == DUNGEON_QUALITY_MYTH then
        return DIFFICULTY_COEFFICIENT_MYTH
    endif
    return DIFFICULTY_COEFFICIENT_NORMAL
endfunction
// ============================================================================
// CalculateScaledAttribute
// ============================================================================
// 基于基础属性和波次计算缩放属性
// 使用指数增长公式: 属性 = 基础属性 × (难度系数)^波次
// 参数:
//   base_value - 基础属性值
//   difficulty_coefficient - 难度系数
//   wave_number - 波次 (1-5)
// 返回: 缩放后的属性值
// ============================================================================
function DungeonMonsterSystem___CalculateScaledAttribute takes integer base_value,real difficulty_coefficient,integer wave_number returns integer
    local real scaled_value
    // 参数验证
    if base_value < 0 then
        set base_value=0
    endif
    if difficulty_coefficient < 1.0 then
        set difficulty_coefficient=1.0
    endif
    if wave_number < 1 then
        set wave_number=1
    elseif wave_number > MAX_WAVES then
        set wave_number=MAX_WAVES
    endif
    // 计算指数增长: 属性 = 基础属性 × (难度系数)^(波次-1)
    // 第一波使用基础属性，后续波次按指数增长
    set scaled_value=I2R(base_value) * Pow(difficulty_coefficient, I2R(wave_number - 1))
    // 确保最小值为1
    if scaled_value < 1.0 then
        set scaled_value=1.0
    endif
    return R2I(scaled_value)
endfunction
// ============================================================================
// GetRandomRoleType
// ============================================================================
// 根据主题类型获取随机角色类型
// 不同主题类型有不同的角色类型权重分布
// 参数:
//   theme_type - 主题类型 (1-14)
// 返回: 随机角色类型 (1-6)
// ============================================================================
function DungeonMonsterSystem___GetRandomRoleType takes integer theme_type returns integer
    local integer random_value
    local integer role_type
    // 参数验证
    if not IsValidThemeType(theme_type) then
        return ROLE_TYPE_MELEE_DPS
    endif
    // 根据主题类型调整角色类型权重
    if theme_type == THEME_TYPE_BANDIT then
        // 山贼主题：近战和远程为主
        set random_value=GetRandomInt(1, 100)
        if random_value <= WEIGHT_MELEE_DPS then
            set role_type=ROLE_TYPE_MELEE_DPS
        elseif random_value <= WEIGHT_MELEE_DPS + WEIGHT_RANGER then
            set role_type=ROLE_TYPE_RANGER
        else
            set role_type=ROLE_TYPE_TANK
        endif
    elseif theme_type == THEME_TYPE_SHAOLIN then
        // 寺庙主题：坦克和治疗为主
        set random_value=GetRandomInt(1, 100)
        if random_value <= WEIGHT_TANK then
            set role_type=ROLE_TYPE_TANK
        elseif random_value <= WEIGHT_TANK + WEIGHT_HEALER_SUPPORT then
            set role_type=ROLE_TYPE_HEALER_SUPPORT
        else
            set role_type=ROLE_TYPE_MELEE_DPS
        endif
    elseif theme_type == THEME_TYPE_BAMBOO then
        // 森林主题：远程和召唤师为主
        set random_value=GetRandomInt(1, 100)
        if random_value <= WEIGHT_RANGER then
            set role_type=ROLE_TYPE_RANGER
        elseif random_value <= WEIGHT_RANGER + WEIGHT_ASSASSIN then
            set role_type=ROLE_TYPE_SUMMONER
        else
            set role_type=ROLE_TYPE_MELEE_DPS
        endif
    elseif theme_type == THEME_TYPE_MING then
        // 洞穴主题：近战和坦克为主
        set random_value=GetRandomInt(1, 100)
        if random_value <= WEIGHT_MELEE_DPS then
            set role_type=ROLE_TYPE_MELEE_DPS
        elseif random_value <= WEIGHT_MELEE_DPS + WEIGHT_TANK then
            set role_type=ROLE_TYPE_TANK
        else
            set role_type=ROLE_TYPE_RANGER
        endif
    else
        // 默认：均匀分布
        set role_type=GetRandomInt(1, 6)
    endif
    return role_type
endfunction
// ============================================================================
// GenerateSpawnPosition
// ============================================================================
// 在圆形范围内生成均匀分布的位置
// 参数:
//   center_x - 中心点X坐标
//   center_y - 中心点Y坐标
//   radius - 生成半径
//   index - 当前怪物索引 (0-based)
//   total - 总怪物数量
// 返回: 通过全局变量返回坐标
// ============================================================================
function DungeonMonsterSystem___GenerateSpawnPosition takes real center_x,real center_y,real radius,integer index,integer total returns nothing
    local real angle
    local real distance
    // 参数验证
    if radius < MIN_SPAWN_RADIUS then
        set radius=MIN_SPAWN_RADIUS
    elseif radius > MAX_SPAWN_RADIUS then
        set radius=MAX_SPAWN_RADIUS
    endif
    if total <= 0 then
        set total=1
    endif
    if index < 0 then
        set index=0
    elseif index >= total then
        set index=total - 1
    endif
    // 计算角度: 将圆分成total份
    set angle=( 2.0 * bj_PI * I2R(index) ) / I2R(total)
    // 计算距离: 在半径范围内随机分布
    set distance=radius * ( 0.7 + 0.3 * GetRandomReal(0.0, 1.0) )
    // 计算坐标并存储到全局变量
    set udg_temp_spawn_x=center_x + distance * Cos(angle)
    set udg_temp_spawn_y=center_y + distance * Sin(angle)
endfunction
// ============================================================================
// CreateMonsterUnit
// ============================================================================
// 创建怪物单位并设置基本属性
// 注意：由于War3版本兼容性问题，攻击力和防御需要通过单位数据编辑器预先配置
// 本函数只设置生命值和移动速度
// 参数:
//   unit_id - 单位ID
//   spawn_x - 生成位置X坐标
//   spawn_y - 生成位置Y坐标
//   scaled_hp - 缩放后的生命值
//   scaled_attack - 缩放后的攻击力（仅用于记录，实际攻击力在单位编辑器中配置）
//   scaled_defense - 缩放后的防御（仅用于记录，实际防御在单位编辑器中配置）
//   move_speed - 移动速度
//   attack_range - 攻击范围
// 返回: 创建的单位
// ============================================================================
function DungeonMonsterSystem___CreateMonsterUnit takes integer unit_id,real spawn_x,real spawn_y,integer scaled_hp,integer scaled_attack,integer scaled_defense,integer move_speed,integer attack_range returns unit
    local unit monster
    // 参数验证
    if unit_id == 0 then
        return null
    endif
    // 创建单位
    set monster=CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), unit_id, spawn_x, spawn_y, 0.0)
    if monster == null then
        return null
    endif
    // 设置单位属性
    call GeneralBonusSystemUnitSetBonus(monster , BONUS_TYPE_MAX_LIFE , MODE_SET , scaled_hp)
    call SetUnitState(monster, UNIT_STATE_LIFE, I2R(scaled_hp))
    // 注意: SetUnitBaseDamage 和 BlzSetUnitArmor 是War3的API，但可能在某些版本中不可用
    // 这里使用更兼容的方式设置攻击力和防御
    // 对于非英雄单位，我们只能设置生命值和移动速度
    // 攻击力和防御需要通过单位数据编辑器预先配置
    call GeneralBonusSystemUnitSetBonus(monster , BONUS_TYPE_ATTACK , MODE_SET , scaled_attack)
    call GeneralBonusSystemUnitSetBonus(monster , BONUS_TYPE_ARMOR , MODE_SET , scaled_defense)
    call SetUnitMoveSpeed(monster, I2R(move_speed))
    call SetUnitAcquireRange(monster, I2R(attack_range))
    return monster
endfunction
// ============================================================================
// SpawnSingleMonster
// ============================================================================
// 生成单个小怪（使用全局变量存储坐标）
// 参数:
//   dungeon_id - 副本ID
//   wave_number - 波次
//   spawn_index - 生成索引
//   total_monsters - 总怪物数量
// 返回: 生成的小怪单位
// ============================================================================
function SpawnSingleMonster takes integer dungeon_id,integer wave_number,integer spawn_index,integer total_monsters returns unit
    local integer theme_type
    local integer role_type
    local integer unit_id
    local integer base_hp
    local integer base_attack
    local integer base_defense
    local integer move_speed
    local integer attack_range
    local real difficulty_coefficient
    local integer scaled_hp
    local integer scaled_attack
    local integer scaled_defense
    local unit monster
    // 参数验证
    if dungeon_id < 1 or dungeon_id > 14 then
        return null
    endif
    if wave_number < 1 or wave_number > MAX_WAVES then
        return null
    endif
    if spawn_index < 0 then
        return null
    endif
    if total_monsters <= 0 then
        return null
    endif
    // 获取副本主题类型
    // set theme_type = DungeonData_GetThemeType(dungeon_id)
    set theme_type=1
    if not IsValidThemeType(theme_type) then
        set theme_type=THEME_TYPE_BANDIT
    endif
    // 获取随机角色类型
    set role_type=DungeonMonsterSystem___GetRandomRoleType(theme_type)
    // 获取小怪配置
    set unit_id=MonsterData_GetMonsterUnitId(role_type , theme_type)
    set base_hp=MonsterData_GetMonsterBaseHp(role_type , theme_type)
    set base_attack=MonsterData_GetMonsterBaseAttack(role_type , theme_type)
    set base_defense=MonsterData_GetMonsterBaseDefense(role_type , theme_type)
    set move_speed=MonsterData_GetMonsterMoveSpeed(role_type , theme_type)
    set attack_range=MonsterData_GetMonsterAttackRange(role_type , theme_type)
    // 检查配置是否有效
    if unit_id == 0 then
        return null
    endif
    // 获取难度系数
    set difficulty_coefficient=GetDifficultyCoefficient(dungeon_id)
    // 计算缩放属性
    set scaled_hp=DungeonMonsterSystem___CalculateScaledAttribute(base_hp , difficulty_coefficient , wave_number)
    set scaled_attack=DungeonMonsterSystem___CalculateScaledAttribute(base_attack , difficulty_coefficient , wave_number)
    set scaled_defense=DungeonMonsterSystem___CalculateScaledAttribute(base_defense , difficulty_coefficient , wave_number)
    // 生成位置（使用全局变量）
    call DungeonMonsterSystem___GenerateSpawnPosition(udg_spawn_center_x[dungeon_id] , udg_spawn_center_y[dungeon_id] , udg_spawn_radius[dungeon_id] , spawn_index , total_monsters)
    // 创建单位
    set monster=DungeonMonsterSystem___CreateMonsterUnit(unit_id , udg_temp_spawn_x , udg_temp_spawn_y , scaled_hp , scaled_attack , scaled_defense , move_speed , attack_range)
    // 设置怪物角色类型和主题类型（用于AI系统）
    if monster != null then
        set udg_monster_role_type[GetHandleId(monster)]=role_type
        set udg_monster_theme_type[GetHandleId(monster)]=theme_type
    endif
    return monster
endfunction
// ============================================================================
// AddMonsterToActiveList
// ============================================================================
// 将怪物添加到活跃怪物列表
// 参数:
//   dungeon_id - 副本ID
//   monster - 怪物单位
// 返回: 是否添加成功
// ============================================================================
function AddMonsterToActiveList takes integer dungeon_id,unit monster returns boolean
    local integer current_count
    local integer max_count
    local integer i
    local integer base_index
    // 参数验证
    if dungeon_id < 1 or dungeon_id > 14 then
        return false
    endif
    if monster == null then
        return false
    endif
    set current_count=udg_active_monster_count[dungeon_id]
    set max_count=udg_max_active_monsters[dungeon_id]
    // 检查是否达到最大数量
    if current_count >= max_count then
        return false
    endif
    // 预先计算基索引
    set base_index=dungeon_id * MONSTER_ARRAY_MULTIPLIER
    // 查找空闲位置
    set i=0
    loop
        exitwhen i >= max_count
        if udg_active_monsters[base_index + i] == null then
            set udg_active_monsters[base_index + i]=monster
            set udg_active_monster_count[dungeon_id]=current_count + 1
            return true
        endif
        set i=i + 1
    endloop
    return false
endfunction
// ============================================================================
// RemoveMonsterFromActiveList
// ============================================================================
// 从活跃怪物列表中移除怪物
// 参数:
//   dungeon_id - 副本ID
//   monster - 怪物单位
// 返回: 是否移除成功
// ============================================================================
function RemoveMonsterFromActiveList takes integer dungeon_id,unit monster returns boolean
    local integer i
    local integer max_count
    local integer base_index
    // 参数验证
    if dungeon_id < 1 or dungeon_id > 14 then
        return false
    endif
    if monster == null then
        return false
    endif
    set max_count=udg_max_active_monsters[dungeon_id]
    set base_index=dungeon_id * MONSTER_ARRAY_MULTIPLIER
    // 查找并移除怪物
    set i=0
    loop
        exitwhen i >= max_count
        if udg_active_monsters[base_index + i] == monster then
            set udg_active_monsters[base_index + i]=null
            set udg_active_monster_count[dungeon_id]=udg_active_monster_count[dungeon_id] - 1
            return true
        endif
        set i=i + 1
    endloop
    return false
endfunction
// ============================================================================
// SpawnMonsterWave
// ============================================================================
// 生成一波小怪
// 参数:
//   dungeon_id - 副本ID
//   wave_number - 波次
// 返回: 生成的怪物数量
// ============================================================================
function SpawnMonsterWave takes integer dungeon_id,integer wave_number returns integer
    local integer monsters_to_spawn
    local integer i
    local unit monster
    local integer spawned_count
    local integer current_count
    local integer max_count
    // 参数验证
    if dungeon_id < 1 or dungeon_id > 14 then
        return 0
    endif
    if wave_number < 1 or wave_number > MAX_WAVES then
        return 0
    endif
    // 检查系统是否已初始化
    if not udg_monster_system_initialized then
        return 0
    endif
    // 获取当前活跃怪物数量
    set current_count=udg_active_monster_count[dungeon_id]
    set max_count=udg_max_active_monsters[dungeon_id]
    // 计算可生成的怪物数量
    set monsters_to_spawn=udg_monsters_per_wave[dungeon_id]
    if monsters_to_spawn < MIN_MONSTERS_PER_WAVE then
        set monsters_to_spawn=MIN_MONSTERS_PER_WAVE
    elseif monsters_to_spawn > MAX_MONSTERS_PER_WAVE then
        set monsters_to_spawn=MAX_MONSTERS_PER_WAVE
    endif
    // 考虑当前活跃怪物数量
    if current_count + monsters_to_spawn > max_count then
        set monsters_to_spawn=max_count - current_count
    endif
    if monsters_to_spawn <= 0 then
        return 0
    endif
    // 生成怪物
    set spawned_count=0
    set i=0
    loop
        exitwhen i >= monsters_to_spawn
        set monster=SpawnSingleMonster(dungeon_id , wave_number , i , monsters_to_spawn)
        if monster != null then
            if AddMonsterToActiveList(dungeon_id , monster) then
                set spawned_count=spawned_count + 1
            else
                // 如果无法添加到列表，则移除单位
                call RemoveUnit(monster)
            endif
            set monster=null
        endif
        set i=i + 1
    endloop
    // 更新当前波次
    set udg_current_wave_number[dungeon_id]=wave_number
    // 显示波次信息
    call DisplayTextToPlayer(Player(0), 0, 0, "|cffffcc00第 " + I2S(wave_number) + " 波小怪已生成 (" + I2S(spawned_count) + " 只)|r")
    return spawned_count
endfunction
// ============================================================================
// StartNextWave
// ============================================================================
// 开始下一波小怪
// 参数:
//   dungeon_id - 副本ID
// 返回: 下一波波次号，如果无法开始则返回0
// ============================================================================
function StartNextWave takes integer dungeon_id returns integer
    local integer next_wave
    local timer wave_timer
    // 参数验证
    if dungeon_id < 1 or dungeon_id > 14 then
        return 0
    endif
    // 检查系统是否已初始化
    if not udg_monster_system_initialized then
        return 0
    endif
    // 计算下一波
    set next_wave=udg_current_wave_number[dungeon_id] + 1
    if next_wave > MAX_WAVES then
        return 0
    endif
    // 生成下一波小怪
    call SpawnMonsterWave(dungeon_id , next_wave)
    // 清理局部变量
    set wave_timer=null
    return next_wave
endfunction
// ============================================================================
// InitializeMonsterSystemForDungeon
// ============================================================================
// 为指定副本初始化怪物系统
// 参数:
//   dungeon_id - 副本ID
// 返回: 是否初始化成功
// ============================================================================
function InitializeMonsterSystemForDungeon takes integer dungeon_id returns boolean
    local real entrance_x
    local real entrance_y
    // 参数验证
    if dungeon_id < 1 or dungeon_id > 14 then
        return false
    endif
    // 获取副本入口位置
    set entrance_x=DungeonData_GetEntranceX(dungeon_id)
    set entrance_y=DungeonData_GetEntranceY(dungeon_id)
    // 设置生成中心点（在入口位置基础上偏移）
    set udg_spawn_center_x[dungeon_id]=entrance_x + SPAWN_OFFSET_X
    set udg_spawn_center_y[dungeon_id]=entrance_y + SPAWN_OFFSET_Y
    // 设置生成半径
    set udg_spawn_radius[dungeon_id]=DEFAULT_SPAWN_RADIUS
    // 设置每波怪物数量（根据副本难度调整）
    if DungeonData_GetQuality(dungeon_id) == DUNGEON_QUALITY_NORMAL then
        set udg_monsters_per_wave[dungeon_id]=MONSTERS_NORMAL
    elseif DungeonData_GetQuality(dungeon_id) == DUNGEON_QUALITY_HARD then
        set udg_monsters_per_wave[dungeon_id]=MONSTERS_HARD
    elseif DungeonData_GetQuality(dungeon_id) == DUNGEON_QUALITY_ELITE then
        set udg_monsters_per_wave[dungeon_id]=MONSTERS_ELITE
    elseif DungeonData_GetQuality(dungeon_id) == DUNGEON_QUALITY_MYTH then
        set udg_monsters_per_wave[dungeon_id]=MONSTERS_MYTH
    else
        set udg_monsters_per_wave[dungeon_id]=MONSTERS_NORMAL
    endif
    // 设置最大活跃怪物数量
    set udg_max_active_monsters[dungeon_id]=MAX_ACTIVE_MONSTERS
    // 重置当前波次和怪物数量
    set udg_current_wave_number[dungeon_id]=0
    set udg_active_monster_count[dungeon_id]=0
    return true
endfunction
// ============================================================================
// InitDungeonMonsterSystem
// ============================================================================
// 初始化副本怪物系统
// ============================================================================
function InitDungeonMonsterSystem takes nothing returns nothing
    local integer i
    // 初始化所有副本的怪物系统
    set i=1
    loop
        exitwhen i > 14
        call InitializeMonsterSystemForDungeon(i)
        set i=i + 1
    endloop
    // 设置初始化标记
    set udg_monster_system_initialized=true
    call DisplayTextToPlayer(Player(0), 0, 0, "|cff00ff00副本怪物系统初始化完成！|r")
endfunction

//library DungeonMonsterSystem ends
//library EquipmentTriggers:
    // ============================================================================
    // 装备拾取事件处理
    // ============================================================================
    function Trig_EquipmentPickup_Actions takes nothing returns nothing
        local unit hero= GetTriggerUnit()
        local item pickedItem= GetManipulatedItem()
        local integer player_id= GetPlayerId(GetOwningPlayer(hero))
        local integer item_type_id= GetItemTypeId(pickedItem)
        local integer equip_id
        // 安全检查
        if hero == null or pickedItem == null then
            return
        endif
        // 根据物品类型ID查询装备ID
        set equip_id=EquipmentData_GetEquipIdByItemType(item_type_id)
        if equip_id == 0 then
            // 不是装备物品，忽略
            return
        endif
        // 调用装备系统处理拾取
        call EquipmentSystem_OnEquipmentPickup(player_id , hero , equip_id , pickedItem)
        // 排泄局部handle变量
        set hero=null
        set pickedItem=null
    endfunction
    // ============================================================================
    // 装备扔下事件处理
    // ============================================================================
    function Trig_EquipmentDrop_Actions takes nothing returns nothing
        local unit hero= GetTriggerUnit()
        local item droppedItem= GetManipulatedItem()
        local integer player_id= GetPlayerId(GetOwningPlayer(hero))
        local integer item_type_id= GetItemTypeId(droppedItem)
        local integer equip_id
        // 安全检查
        if hero == null or droppedItem == null then
            return
        endif
        // 根据物品类型ID查询装备ID
        set equip_id=EquipmentData_GetEquipIdByItemType(item_type_id)
        if equip_id == 0 then
            // 不是装备物品，忽略
            return
        endif
        // 调用装备系统处理扔下
        call EquipmentSystem_OnEquipmentDrop(player_id , hero , equip_id , droppedItem)
        // 排泄局部handle变量
        set hero=null
        set droppedItem=null
    endfunction
    // ============================================================================
    // 初始化装备拾取触发器
    // ============================================================================
    function InitEquipmentPickupTrigger takes nothing returns nothing
        local integer i= 0
        set gg_trg_EquipmentPickup=CreateTrigger()
        // 为所有玩家注册单位拾取物品事件
        loop
            exitwhen i >= 12
            call TriggerRegisterPlayerUnitEvent(gg_trg_EquipmentPickup, Player(i), EVENT_PLAYER_UNIT_PICKUP_ITEM, null)
            set i=i + 1
        endloop
        // 添加触发动作
        call TriggerAddAction(gg_trg_EquipmentPickup, function Trig_EquipmentPickup_Actions)
        call DisplayTextToPlayer(Player(0), 0, 0, "装备拾取触发器初始化完成")
    endfunction
    // ============================================================================
    // 初始化装备扔下触发器
    // ============================================================================
    function InitEquipmentDropTrigger takes nothing returns nothing
        local integer i= 0
        set gg_trg_EquipmentDrop=CreateTrigger()
        // 为所有玩家注册单位扔下物品事件
        loop
            exitwhen i >= 12
            call TriggerRegisterPlayerUnitEvent(gg_trg_EquipmentDrop, Player(i), EVENT_PLAYER_UNIT_DROP_ITEM, null)
            set i=i + 1
        endloop
        // 添加触发动作
        call TriggerAddAction(gg_trg_EquipmentDrop, function Trig_EquipmentDrop_Actions)
        call DisplayTextToPlayer(Player(0), 0, 0, "装备扔下触发器初始化完成")
    endfunction
    // ============================================================================
    // 装备测试事件处理
    // ============================================================================
    function Trig_EquipmentTest_Actions takes nothing returns nothing
        local player p= GetTriggerPlayer()
        local integer player_id= GetPlayerId(p)
        local unit hero= udg_player_hero[player_id]
        if hero == null then
            call DisplayTextToPlayer(p, 0, 0, "没有英雄单位")
            return
        endif
        // 显示玩家装备状态
        call EquipmentSystem_ShowPlayerEquipmentStatus(player_id)
        // 显示装备属性加成
        call DisplayTextToPlayer(p, 0, 0, "装备属性加成:")
        call DisplayTextToPlayer(p, 0, 0, "武力: " + R2S(udg_player_equip_attack_bonus[player_id]))
        call DisplayTextToPlayer(p, 0, 0, "法强: " + R2S(udg_player_equip_spell_power_bonus[player_id]))
        call DisplayTextToPlayer(p, 0, 0, "气血: " + R2S(udg_player_equip_health_bonus[player_id]))
        // 排泄局部handle变量
        set p=null
        set hero=null
    endfunction
    // ============================================================================
    // 初始化装备测试触发器
    // ============================================================================
    function InitEquipmentTestTrigger takes nothing returns nothing
        local integer i= 0
        set gg_trg_EquipmentTest=CreateTrigger()
        // 为所有玩家注册聊天事件
        loop
            exitwhen i >= 12
            call TriggerRegisterPlayerChatEvent(gg_trg_EquipmentTest, Player(i), "-equipstatus", true)
            set i=i + 1
        endloop
        // 添加触发动作
        call TriggerAddAction(gg_trg_EquipmentTest, function Trig_EquipmentTest_Actions)
        call DisplayTextToPlayer(Player(0), 0, 0, "装备测试触发器初始化完成")
    endfunction
    // ============================================================================
    // 初始化装备触发器系统
    // ============================================================================
    function InitEquipmentTriggers takes nothing returns nothing
        call InitEquipmentPickupTrigger()
        call InitEquipmentDropTrigger()
        call InitEquipmentTestTrigger()
        call DisplayTextToPlayer(Player(0), 0, 0, "装备触发器系统初始化完成")
    endfunction

//library EquipmentTriggers ends
//library TestEquipmentDebug:
    // ============================================================================
    // 显示装备详细信息
    // ============================================================================
    function ShowEquipmentDetails takes player p,integer equip_id returns nothing
        local string msg
        if equip_id < 1 or equip_id > udg_equip_count then
            call DisplayTextToPlayer(p, 0, 0, "装备ID无效")
            return
        endif
        set msg="=== 装备详细信息 ==="
        call DisplayTextToPlayer(p, 0, 0, msg)
        set msg="名称: " + EquipmentData_GetName(equip_id)
        call DisplayTextToPlayer(p, 0, 0, msg)
        set msg="槽位: " + EQUIP_SLOT_NAME[EquipmentData_GetSlot(equip_id)]
        call DisplayTextToPlayer(p, 0, 0, msg)
        set msg="品质: " + EQUIP_QUALITY_NAME[EquipmentData_GetQuality(equip_id)]
        call DisplayTextToPlayer(p, 0, 0, msg)
        // 基础属性
        if udg_equip_attack[equip_id] > 0 then
            set msg="武力: +" + I2S(udg_equip_attack[equip_id])
            call DisplayTextToPlayer(p, 0, 0, msg)
        endif
        if udg_equip_spell_power[equip_id] > 0 then
            set msg="法强: +" + I2S(udg_equip_spell_power[equip_id])
            call DisplayTextToPlayer(p, 0, 0, msg)
        endif
        if udg_equip_health[equip_id] > 0 then
            set msg="气血: +" + I2S(udg_equip_health[equip_id])
            call DisplayTextToPlayer(p, 0, 0, msg)
        endif
        // 元素属性
        if udg_equip_element[equip_id] != ELEMENT_NONE then
            set msg="元素: " + ELEMENT_NAME[udg_equip_element[equip_id]] + " +" + I2S(udg_equip_element_value[equip_id])
            call DisplayTextToPlayer(p, 0, 0, msg)
        endif
        // 特殊效果
        if udg_equip_special_type[equip_id] > 0 then
            set msg="特效: 类型" + I2S(udg_equip_special_type[equip_id]) + " 值" + I2S(udg_equip_special_value[equip_id])
            call DisplayTextToPlayer(p, 0, 0, msg)
        endif
        // 排泄局部handle变量
        set p=null
    endfunction
    // ============================================================================
    // 测试所有装备
    // ============================================================================
    function TestAllEquipment takes player p returns nothing
        local integer i= 1
        local integer count= 0
        call DisplayTextToPlayer(p, 0, 0, "=== 测试所有装备 ===")
        loop
            exitwhen i > udg_equip_count
            if count < 10 then // 只显示前10个
call ShowEquipmentDetails(p , i)
                set count=count + 1
            endif
            set i=i + 1
        endloop
        call DisplayTextToPlayer(p, 0, 0, "共 " + I2S(udg_equip_count) + " 件装备")
        // 排泄局部handle变量
        set p=null
    endfunction
    // ============================================================================
    // 测试装备属性应用
    // ============================================================================
    function TestEquipmentAttributes takes player p returns nothing
        local integer player_id= GetPlayerId(p)
        local unit hero= udg_player_hero[player_id]
        local integer test_equip_id= 1

        if hero == null then
            call DisplayTextToPlayer(p, 0, 0, "没有英雄单位")
            return
        endif
        call DisplayTextToPlayer(p, 0, 0, "=== 测试装备属性应用 ===")
        // 显示当前属性
        call DisplayTextToPlayer(p, 0, 0, "应用前攻击力: " + R2S(GetHeroStr(hero, true)))
        // 应用装备属性
        call EquipmentSystem_ApplyEquipmentAttributes(hero , test_equip_id)
        // 显示应用后属性
        call DisplayTextToPlayer(p, 0, 0, "应用后攻击力: " + R2S(GetHeroStr(hero, true)))
        // 等待2秒
        call TriggerSleepAction(2.0)
        // 移除装备属性
        call EquipmentSystem_RemoveEquipmentAttributes(hero , test_equip_id)
        // 显示移除后属性
        call DisplayTextToPlayer(p, 0, 0, "移除后攻击力: " + R2S(GetHeroStr(hero, true)))
        // 排泄局部handle变量
        set p=null
        set hero=null
    endfunction
    // ============================================================================
    // 装备调试事件处理
    // ============================================================================
    function Trig_TestEquipDebug_Actions takes nothing returns nothing
        local player p= GetTriggerPlayer()
        local string cmd= GetEventPlayerChatString()
        if cmd == "-equipall" then
            call TestAllEquipment(p)
        elseif cmd == "-equiptest" then
            call TestEquipmentAttributes(p)
        elseif SubString(cmd, 0, 8) == "-equipid" then
            call ShowEquipmentDetails(p , S2I(SubString(cmd, 9, 12)))
        endif
        // 排泄局部handle变量
        set p=null
    endfunction
    // ============================================================================
    // 初始化装备调试
    // ============================================================================
    function InitTestEquipmentDebug takes nothing returns nothing
        local integer i= 0
        set gg_trg_TestEquipDebug=CreateTrigger()
        // 为所有玩家注册聊天事件
        loop
            exitwhen i >= 12
            call TriggerRegisterPlayerChatEvent(gg_trg_TestEquipDebug, Player(i), "-equipall", true)
            call TriggerRegisterPlayerChatEvent(gg_trg_TestEquipDebug, Player(i), "-equiptest", true)
            call TriggerRegisterPlayerChatEvent(gg_trg_TestEquipDebug, Player(i), "-equipid", false)
            set i=i + 1
        endloop
        // 添加触发动作
        call TriggerAddAction(gg_trg_TestEquipDebug, function Trig_TestEquipDebug_Actions)
        call DisplayTextToPlayer(Player(0), 0, 0, "装备调试系统初始化完成")
    endfunction

//library TestEquipmentDebug ends
//library MonsterAISystem:
    // ========================================================================
    // 全局变量
    // ========================================================================
    // ========================================================================
    // DistanceBetweenUnits
    // ========================================================================
    // 计算两个单位之间的距离
    // 参数:
    //   unit1 - 第一个单位
    //   unit2 - 第二个单位
    // 返回: 两个单位之间的距离
    // ========================================================================
    function MonsterAISystem___DistanceBetweenUnits takes unit unit1,unit unit2 returns real
        local real x1= GetUnitX(unit1)
        local real y1= GetUnitY(unit1)
        local real x2= GetUnitX(unit2)
        local real y2= GetUnitY(unit2)
        local real dx= x2 - x1
        local real dy= y2 - y1
        return SquareRoot(dx * dx + dy * dy)
    endfunction
    // ========================================================================
    // GetNearestPlayerHero
    // ========================================================================
    // 获取最近的玩家英雄
    // 参数:
    //   monster - 怪物单位
    // 返回: 最近的玩家英雄单位，如果没有则返回null
    // ========================================================================
    function MonsterAISystem___GetNearestPlayerHero takes unit monster returns unit
        local unit nearest_hero= null
        local real min_distance= 999999.0
        local integer i= 0
        local unit current_hero
        local real distance
        if monster == null then
            return null
        endif
        loop
            exitwhen i >= 12 // 所有玩家

            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING then
                // 使用Hero_GetPlayerHero函数获取玩家英雄
                set current_hero=Hero_GetPlayerHero(i)
                if current_hero != null and GetUnitState(current_hero, UNIT_STATE_LIFE) > 0.0 then
                    set distance=MonsterAISystem___DistanceBetweenUnits(monster , current_hero)
                    if distance < min_distance then
                        set min_distance=distance
                        set nearest_hero=current_hero
                    endif
                endif
            endif
            set i=i + 1
        endloop
        return nearest_hero
    endfunction
    // ========================================================================
    // SetMonsterRoleType
    // ========================================================================
    // 设置怪物角色类型
    // 参数:
    //   monster - 怪物单位
    //   role_type - 角色类型 (1-6)
    // ========================================================================
    function SetMonsterRoleType takes unit monster,integer role_type returns nothing
        local integer monster_id
        if monster == null or role_type < 1 or role_type > 6 then
            return
        endif
        set monster_id=GetHandleId(monster)
        set udg_monster_role_type[monster_id]=role_type
    endfunction
    // ========================================================================
    // GetMonsterRoleType
    // ========================================================================
    // 获取怪物角色类型
    // 参数:
    //   monster - 怪物单位
    // 返回: 角色类型 (1-6)，如果无效则返回0
    // ========================================================================
    function GetMonsterRoleType takes unit monster returns integer
        local integer monster_id
        if monster == null then
            return 0
        endif
        set monster_id=GetHandleId(monster)
        return udg_monster_role_type[monster_id]
    endfunction
    // ========================================================================
    // SetMonsterThemeType
    // ========================================================================
    // 设置怪物主题类型
    // 参数:
    //   monster - 怪物单位
    //   theme_type - 主题类型 (1-14)
    // ========================================================================
    function SetMonsterThemeType takes unit monster,integer theme_type returns nothing
        local integer monster_id
        if monster == null or theme_type < 1 or theme_type > 14 then
            return
        endif
        set monster_id=GetHandleId(monster)
        set udg_monster_theme_type[monster_id]=theme_type
    endfunction
    // ========================================================================
    // GetMonsterThemeType
    // ========================================================================
    // 获取怪物主题类型
    // 参数:
    //   monster - 怪物单位
    // 返回: 主题类型 (1-14)，如果无效则返回0
    // ========================================================================
    function GetMonsterThemeType takes unit monster returns integer
        local integer monster_id
        if monster == null then
            return 0
        endif
        set monster_id=GetHandleId(monster)
        return udg_monster_theme_type[monster_id]
    endfunction
    // ========================================================================
    // GetUnitAttackRange
    // ========================================================================
    // 获取单位攻击范围（兼容版本）
    // 参数:
    //   u - 单位
    // 返回: 攻击范围
    // ========================================================================
    function MonsterAISystem___GetUnitAttackRange takes unit u returns integer
        local integer role_type
        local integer theme_type
        local integer attack_range
        // 参数验证
        if u == null then
            return 128
        endif
        // 尝试从怪物数据系统获取攻击范围
        set role_type=GetMonsterRoleType(u)
        set theme_type=GetMonsterThemeType(u)
        if role_type >= 1 and role_type <= 6 and theme_type >= 1 and theme_type <= 14 then
            set attack_range=MonsterData_GetMonsterAttackRange(role_type , theme_type)
            if attack_range > 0 then
                return attack_range
            endif
        endif
        // 使用兼容方法获取攻击范围（如果API可用）
        // 在较新的War3版本中可以使用BlzGetUnitWeaponIntegerField
        // 这里返回默认值
        return 128 // 默认攻击范围
endfunction
    // ========================================================================
    // UpdateMonsterAI
    // ========================================================================
    // 小怪基础AI - 简单移动和攻击
    // 参数:
    //   monster - 怪物单位
    // ========================================================================
    function UpdateMonsterAI takes unit monster returns nothing
        local integer monster_id
        local unit current_target
        local real current_time
        local real distance
        local integer attack_range
        local real attack_speed
        // 参数验证
        if monster == null then
            return
        endif
        set monster_id=GetHandleId(monster)
        set current_target=udg_monster_targets[monster_id]
        set current_time=GetGameTime()
        // 如果当前目标无效或死亡，寻找新目标
        if current_target == null or GetUnitState(current_target, UNIT_STATE_LIFE) <= 0.0 then
            set current_target=MonsterAISystem___GetNearestPlayerHero(monster)
            set udg_monster_targets[monster_id]=current_target
        endif
        if current_target == null then
            return // 没有找到目标
endif
        // 检查是否在攻击范围内
        set distance=MonsterAISystem___DistanceBetweenUnits(monster , current_target)
        set attack_range=MonsterAISystem___GetUnitAttackRange(monster)
        // set attack_speed = GetUnitAttackSpeed(monster)
        set attack_speed=1.0
        if attack_range <= 0 then
            set attack_range=128 // 默认攻击范围
endif
        if attack_speed <= 0 then
            set attack_speed=1.0 // 默认攻击速度
endif
        if distance <= I2R(attack_range + 50) then // 增加50的缓冲距离
// 在攻击范围内，攻击目标
if current_time - udg_monster_last_attack_time[monster_id] >= 1.0 / attack_speed then
                call IssueTargetOrderById(monster, 851983, current_target) // 攻击目标
set udg_monster_last_attack_time[monster_id]=current_time
            endif
        else
            // 不在攻击范围内，移动到目标
            call IssuePointOrderById(monster, 851986, GetUnitX(current_target), GetUnitY(current_target))
        endif
    endfunction
    // ========================================================================
    // UpdateMonsterSkillAI
    // ========================================================================
    // 小怪技能AI - 简单冷却检查
    // 参数:
    //   monster - 怪物单位
    //   role_type - 角色类型
    // ========================================================================
    function UpdateMonsterSkillAI takes unit monster,integer role_type returns nothing
        local integer monster_id
        local integer theme_type
        local integer skill_id
        // 参数验证
        if monster == null or role_type < 1 or role_type > 6 then
            return
        endif
        set monster_id=GetHandleId(monster)
        // 获取怪物主题类型
        set theme_type=GetMonsterThemeType(monster)
        if theme_type < 1 or theme_type > 14 then
            return // 无效的主题类型
endif
        // 从怪物数据系统获取技能ID
        set skill_id=MonsterData_GetMonsterSkillId(role_type , theme_type)
        // 如果有技能且冷却结束，随机使用技能
        if skill_id != 0 and GetRandomInt(1, 100) <= 10 then // 10%几率使用技能
call IssueImmediateOrderById(monster, skill_id)
        endif
    endfunction
    // ========================================================================
    // UpdateMonstersAITimerCallback
    // ========================================================================
    // 小怪AI计时器回调
    // ========================================================================
    function UpdateMonstersAITimerCallback takes nothing returns nothing
        local integer i= 0
        local unit monster
        local integer role_type
        // 检查系统是否已初始化
        if not udg_monster_ai_system_initialized then
            return
        endif
        // 更新所有活跃小怪的AI
        loop
            exitwhen i >= udg_all_active_monster_count
            set monster=udg_active_monsters[i]
            if monster != null and GetUnitState(monster, UNIT_STATE_LIFE) > 0.0 then
                // 更新基础AI
                call UpdateMonsterAI(monster)
                // 根据角色类型更新技能AI
                set role_type=GetMonsterRoleType(monster)
                if role_type > 0 then
                    call UpdateMonsterSkillAI(monster , role_type)
                endif
            else
                // 移除死亡或无效的怪物
                if i < udg_all_active_monster_count then
                    // 清理怪物角色类型和主题类型映射
                    if monster != null then
                        set udg_monster_role_type[GetHandleId(monster)]=0
                        set udg_monster_theme_type[GetHandleId(monster)]=0
                    endif
                    set udg_active_monsters[i]=udg_active_monsters[udg_all_active_monster_count - 1]
                    set udg_active_monsters[udg_all_active_monster_count - 1]=null
                    set udg_all_active_monster_count=udg_all_active_monster_count - 1
                    set i=i - 1 // 重新检查当前位置
endif
            endif
            set i=i + 1
        endloop
    endfunction
    // ========================================================================
    // StartMonstersAITimer
    // ========================================================================
    // 启动小怪AI计时器
    // 返回: 创建的计时器
    // ========================================================================
    function StartMonstersAITimer takes nothing returns timer
        local timer t= CreateTimer()
        call TimerStart(t, 0.5, true, function UpdateMonstersAITimerCallback)
        return t
    endfunction
    // ========================================================================
    // InitMonsterAISystem
    // ========================================================================
    // 初始化怪物AI系统
    // ========================================================================
    function InitMonsterAISystem takes nothing returns nothing
        local integer i= 0
        // 初始化数组
        loop
            exitwhen i >= 8192 // handle_id 最大索引
set udg_monster_targets[i]=null
            set udg_monster_last_attack_time[i]=0.0
            set udg_monster_role_type[i]=0
            set udg_monster_theme_type[i]=0
            set i=i + 1
        endloop
        // 启动小怪AI计时器
        call StartMonstersAITimer()
        // 设置初始化标记
        set udg_monster_ai_system_initialized=true
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cff00ff00怪物AI系统初始化完成|r")
    endfunction

//library MonsterAISystem ends
//library GameInit:
    // ============================================================================
    // Initialization Function
    // ============================================================================
    function DelayInit takes nothing returns nothing
        // 初始化其他系统
        call InitHeroAttributeSystem() // 英雄属性系统
call InitSectSystem() // 门派系统
call InitDungeonSystem() // 副本系统
call InitDungeonMonsterData() // 副本怪物数据
call InitDungeonMonsterSystem() // 副本怪物系统
call InitBossSkillSystem() // BOSS技能系统
call InitMonsterAISystem() // 怪物AI系统
call InitCultivationSystem() // 历练系统
call InitEquipmentSystem() // 装备系统
call InitEquipmentTriggers() // 装备触发器
call InitTestEquipmentGenerate() // 测试装备生成
call InitTestEquipmentDebug() // 装备调试系统
// call InitQuestSystem() // 任务系统
call InitDefenseSystem() // 防守系统
// call InitAchievementSystem()
// call InitSaveLoadSystem()
call InitGameTimeSystem() // 游戏时间系统

        // 显示欢迎信息
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "|cFFFFCC00《快意江湖》 v" + I2S(GAME_VERSION_MAJOR) + "." + I2S(GAME_VERSION_MINOR) + "." + I2S(GAME_VERSION_PATCH) + "|r")
        call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "系统初始化完成")
    endfunction
    function OnInit takes nothing returns nothing
        local integer i
        local timer t= CreateTimer()
        // 初始化游戏状态
        set i=0
        loop
            exitwhen i > 11
            set udg_game_status[i]=0
            set udg_current_difficulty[i]=1
            set udg_game_start_time[i]=0.0
            set udg_player_sect[i]=0
            set udg_player_cultivation[i]=0
            set i=i + 1
        endloop
        set udg_game_initialized[0]=true
        call DzUnlockOpCodeLimit(true)
        call TimerStart(t, 0.03, false, function DelayInit)
        set t=null
    endfunction
    // ============================================================================
    // Get Game Version
    // ============================================================================
    function GetGameVersion takes nothing returns string
        return I2S(GAME_VERSION_MAJOR) + "." + I2S(GAME_VERSION_MINOR) + "." + I2S(GAME_VERSION_PATCH)
    endfunction
    // ============================================================================
    // Set Game Status
    // ============================================================================
    function SetGameStatus takes integer player_index,integer status returns nothing
        set udg_game_status[player_index]=status
        if status == 1 then
            // 游戏开始
            set udg_game_start_time[player_index]=DzAPI_Map_GetGameStartTime()
            call DisplayTextToPlayer(Player(player_index), 0, 0, "游戏开始！")
        elseif status == 3 then
            // 游戏结束
            call DisplayTextToPlayer(Player(player_index), 0, 0, "游戏结束！")
        endif
    endfunction
    // ============================================================================
    // Get Game Status
    // ============================================================================
    function GetGameStatus takes integer player_index returns integer
        return udg_game_status[player_index]
    endfunction
    // ============================================================================
    // Get Player Sect
    // ============================================================================
    function GetPlayerSect takes integer player_index returns integer
        return udg_player_sect[player_index]
    endfunction
    // ============================================================================
    // Set Player Sect
    // ============================================================================
    function SetPlayerSect takes integer player_index,integer sect_id returns nothing
        set udg_player_sect[player_index]=sect_id
    endfunction
    // ============================================================================
    // Get Player Cultivation
    // ============================================================================
    function GetPlayerCultivation takes integer player_index returns integer
        return udg_player_cultivation[player_index]
    endfunction
    // ============================================================================
    // Set Player Cultivation
    // ============================================================================
    function SetPlayerCultivation takes integer player_index,integer cultivation returns nothing
        set udg_player_cultivation[player_index]=cultivation
    endfunction
    // ============================================================================
    // Get Current Difficulty
    // ============================================================================
    function GetCurrentDifficulty takes integer player_index returns integer
        return udg_current_difficulty[player_index]
    endfunction
    // ============================================================================
    // Set Current Difficulty
    // ============================================================================
    function SetCurrentDifficulty takes integer player_index,integer difficulty returns nothing
        set udg_current_difficulty[player_index]=difficulty
    endfunction
// // 测试模式开关
// #ifndef RELEASE_MODE
//     // 开发模式下包含测试文件
//     #include "test_quest_comprehensive.j"
//     call InitQuestTestTriggers()
// #endif

//library GameInit ends
//===========================================================================
// 
// 快意江湖
// 
//   Warcraft III map script
//   Generated by the Warcraft III World Editor
//   Date: Mon Mar 09 11:14:08 2026
//   Map Author: Zeikale
// 
//===========================================================================
//***************************************************************************
//*
//*  Global Variables
//*
//***************************************************************************
function InitGlobals takes nothing returns nothing
endfunction
//***************************************************************************
//*
//*  Unit Creation
//*
//***************************************************************************
//===========================================================================
function CreateUnitsForPlayer0 takes nothing returns nothing
    local player p= Player(0)
    local unit u
    local integer unitID
    local trigger t
    local real life
    set u=CreateUnit(p, 'O008', - 8947.4, 2297.3, 296.720)
endfunction
//===========================================================================
function CreateUnitsForPlayer5 takes nothing returns nothing
    local player p= Player(5)
    local unit u
    local integer unitID
    local trigger t
    local real life
    set gg_unit_O000_0001=CreateUnit(p, 'O000', 4424.3, - 2831.1, 15.766)
    call SetUnitState(gg_unit_O000_0001, UNIT_STATE_MANA, 0)
    set gg_unit_O007_0002=CreateUnit(p, 'O007', 4627.1, - 2793.2, 309.989)
    call SetUnitState(gg_unit_O007_0002, UNIT_STATE_MANA, 0)
    set gg_unit_O008_0003=CreateUnit(p, 'O008', 4837.9, - 2785.1, 54.109)
    call SetUnitState(gg_unit_O008_0003, UNIT_STATE_MANA, 0)
    set gg_unit_O005_0004=CreateUnit(p, 'O005', 5118.2, - 2809.4, 247.255)
    call SetUnitState(gg_unit_O005_0004, UNIT_STATE_MANA, 0)
    set gg_unit_O003_0005=CreateUnit(p, 'O003', 5322.0, - 2786.2, 324.326)
    call SetUnitState(gg_unit_O003_0005, UNIT_STATE_MANA, 0)
    set gg_unit_O004_0006=CreateUnit(p, 'O004', 4462.3, - 3114.1, 93.551)
    call SetUnitState(gg_unit_O004_0006, UNIT_STATE_MANA, 0)
    set gg_unit_O006_0007=CreateUnit(p, 'O006', 4675.6, - 3126.7, 193.069)
    call SetUnitState(gg_unit_O006_0007, UNIT_STATE_MANA, 0)
    set gg_unit_O001_0008=CreateUnit(p, 'O001', 4950.6, - 3119.3, 23.511)
    call SetUnitState(gg_unit_O001_0008, UNIT_STATE_MANA, 0)
    set gg_unit_O009_0009=CreateUnit(p, 'O009', 5166.7, - 3119.3, 195.683)
    call SetUnitState(gg_unit_O009_0009, UNIT_STATE_MANA, 0)
    set gg_unit_O002_0010=CreateUnit(p, 'O002', 5383.2, - 3114.2, 181.533)
    call SetUnitState(gg_unit_O002_0010, UNIT_STATE_MANA, 0)
    set u=CreateUnit(p, 'o102', - 999.7, - 1833.7, 270.000)
    set u=CreateUnit(p, 'o103', - 419.3, - 1829.1, 270.000)
    set u=CreateUnit(p, 'o101', 6056.9, - 2793.1, 172.470)
    set u=CreateUnit(p, 'o100', 6065.9, - 3125.6, 164.990)
endfunction
//===========================================================================
function CreateNeutralPassiveBuildings takes nothing returns nothing
    local player p= Player(PLAYER_NEUTRAL_PASSIVE)
    local unit u
    local integer unitID
    local trigger t
    local real life
    set u=CreateUnit(p, 'n000', 320.0, - 256.0, 270.000)
endfunction
//===========================================================================
function CreateNeutralPassive takes nothing returns nothing
    local player p= Player(PLAYER_NEUTRAL_PASSIVE)
    local unit u
    local integer unitID
    local trigger t
    local real life
    set u=CreateUnit(p, 'nvl2', - 9490.5, 2145.5, 344.168)
    set u=CreateUnit(p, 'nvl2', - 9401.2, 2176.9, 179.280)
    set u=CreateUnit(p, 'nvl2', - 9117.3, 2292.8, 255.385)
    set u=CreateUnit(p, 'nvl2', - 9037.7, 2201.3, 93.958)
    set u=CreateUnit(p, 'nvl2', - 9092.6, 2408.7, 54.604)
    set u=CreateUnit(p, 'nvk2', - 9398.3, 2312.8, 187.542)
    set u=CreateUnit(p, 'nvk2', - 9091.6, 2114.8, 223.040)
    set u=CreateUnit(p, 'nvlw', - 9509.4, 2258.2, 90.959)
    set u=CreateUnit(p, 'nvlw', - 9457.3, 2362.6, 280.325)
endfunction
//===========================================================================
function CreatePlayerBuildings takes nothing returns nothing
endfunction
//===========================================================================
function CreatePlayerUnits takes nothing returns nothing
    call CreateUnitsForPlayer0()
    call CreateUnitsForPlayer5()
endfunction
//===========================================================================
function CreateAllUnits takes nothing returns nothing
    call CreateNeutralPassiveBuildings()
    call CreatePlayerBuildings()
    call CreateNeutralPassive()
    call CreatePlayerUnits()
endfunction
//***************************************************************************
//*
//*  Custom Script Code
//*
//***************************************************************************
//TESH.scrollpos=0
//TESH.alwaysfold=0
//===========================================================================
//修改生命
//===========================================================================

// ============================================================================
// Game Initialization
// ============================================================================
// 游戏初始化系统
// ============================================================================
// Hero Attribute System
// ============================================================================
// 英雄属性系统 - 管理23个局内属性 + 2个扩展属性、10位英雄被动
// ============================================================================
// 存储策略：
// - 气血/内力/根骨/悟性/身法：使用War3原生API
// - 其他属性：使用哈希表存储
// ============================================================================
// Sect Data Configuration
// ============================================================================
// 门派数据配置模块 - 少林、武当、峨眉 (MVP)
// 包含门派类型枚举、定位枚举、门派ID、技能配置和玩家选择状态
// ============================================================================
// ============================================================================
// Sect System Core
// ============================================================================
// 门派系统核心模块 - 门派选择功能 (MVP)
// 包含门派选择判断、选择操作、状态查询、物品拾取事件处理和技能解锁系统
// ============================================================================
// ============================================================================
// Dungeon Data Configuration
// ============================================================================
// 副本数据配置模块
// 包含副本ID常量、类型常量、品质常量、物品ID和副本配置数据表
// ============================================================================
// ============================================================================
// Dungeon System Core
// ============================================================================
// 副本系统核心模块
// 包含副本进入判断、副本操作、物品拾取事件处理、奖励系统和状态查询
// ============================================================================
// ============================================================================
// Hero Selection System
// ============================================================================
// 英雄选择系统
// 功能：
// 1. 监听单位选择事件
// 2. 第一次选择：显示英雄信息
// 3. 第二次选择（双击）：将单位归属于玩家，移除无敌，传送到出生点
// ============================================================================
// ============================================================================
// Game Time System
// ============================================================================
// 游戏时间系统
// 功能：
// 1. 记录游戏运行时间（秒）
// 2. 提供每秒触发的计时器
// ============================================================================
// ============================================================================
// Cultivation Data Configuration
// ============================================================================
// 历练系统数据配置模块
// 包含历练等级枚举、阈值表、名称表、伤害加成表
// ============================================================================
// ============================================================================
// Cultivation System Core
// ============================================================================
// 历练系统核心模块
// 包含历练值添加、等级检查、伤害加成计算、升级事件处理
// ============================================================================
        // ============================================================================
// Equipment Data Configuration
// ============================================================================
// 装备系统数据配置模块
// 包含装备类型枚举、品质枚举、装备数据表、掉落来源表
// ============================================================================
// ============================================================================
// Equipment Attribute System
// ============================================================================
// 装备属性系统 - 处理装备拾取/扔下时的属性加成和移除
// ============================================================================
// ============================================================================
// Equipment Triggers
// ============================================================================
// 装备触发器系统 - 处理装备拾取和扔下事件
// ============================================================================
// Equipment Test Generation
// ============================================================================
// 装备测试生成模块 - 用于测试装备系统
// ============================================================================
// Equipment Debug Commands
// ============================================================================
// 装备调试命令模块
// ============================================================================
// #include "09_quest_system.j"
// ============================================================================
// Dungeon Monster Data Configuration
// ============================================================================
// 副本怪物数据配置模块
// 包含6种小怪角色类型、5种BOSS类型、怪物属性配置和技能配置
// ============================================================================
// Dungeon Monster Spawn System
// ============================================================================
// 副本小怪生成系统
// 包含难度系数计算、波次属性缩放、小怪生成、怪物追踪等功能
// ============================================================================
// Attack Monster Data Definitions
// ============================================================================
// 包含防守系统中进攻怪物的常量和数据定义
// ============================================================================
// Attack Monster System
// ============================================================================
// 防守系统核心模块 - 进攻怪物管理系统
// 处理怪物生成、AI及波次管理
// ============================================================================
// Boss Skill System
// ============================================================================
// BOSS技能系统
// 实现5种BOSS类型的技能系统，包括技能冷却管理、阶段切换(50%生命值)、以及基于BOSS类型的技能选择逻辑
// ============================================================================
// Monster AI System
// ============================================================================
// 怪物简化AI系统
// 包含小怪基础AI、BOSS AI计时器、目标选择、技能AI等功能
// ============================================================================
//***************************************************************************
//*
//*  Triggers
//*
//***************************************************************************
//===========================================================================
// Trigger: firstOccur
//===========================================================================
//TESH.scrollpos=0
//TESH.alwaysfold=0
//===========================================================================
// Trigger: firstOccur
//===========================================================================
function Trig_firstOccurActions takes nothing returns nothing
	call YDWEH2I(GetTriggerUnit())
    call DzAPI_Map_GetGameStartTime()
    call DzSetUnitAbilityRange(GetTriggerUnit(), 'XXXX', 300)
endfunction
//===========================================================================
function InitTrig_firstOccur takes nothing returns nothing
	set gg_trg_firstOccur=CreateTrigger()
	call TriggerAddAction(gg_trg_firstOccur, function Trig_firstOccurActions)
endfunction
//===========================================================================
// Trigger: fisrtOccur-2
//===========================================================================
//===========================================================================
// Trigger: fisrtOccur-2
//===========================================================================
function Trig_fisrtOccur_2Actions takes nothing returns nothing
	call ShowUnitShow(gg_unit_O000_0001)
	call ShowUnitShow(gg_unit_O007_0002)
	call ShowUnitShow(gg_unit_O008_0003)
	call ShowUnitShow(gg_unit_O005_0004)
	call ShowUnitShow(gg_unit_O003_0005)
	call ShowUnitShow(gg_unit_O004_0006)
	call ShowUnitShow(gg_unit_O006_0007)
	call ShowUnitShow(gg_unit_O001_0008)
	call ShowUnitShow(gg_unit_O009_0009)
	call ShowUnitShow(gg_unit_O002_0010)
endfunction
//===========================================================================
function InitTrig_fisrtOccur_2 takes nothing returns nothing
	set gg_trg_fisrtOccur_2=CreateTrigger()
	call TriggerAddAction(gg_trg_fisrtOccur_2, function Trig_fisrtOccur_2Actions)
endfunction
//===========================================================================
// Trigger: init
//===========================================================================
function Trig_initActions takes nothing returns nothing
    call FogMaskEnableOff()
    call FogEnableOff()
    call UseTimeOfDayBJ(false)
    call DzUnlockOpCodeLimit(true)
    call YDWEEnableCreepSleepBJNull(false)
endfunction
//===========================================================================
function InitTrig_init takes nothing returns nothing
    set gg_trg_init=CreateTrigger()
    call TriggerAddAction(gg_trg_init, function Trig_initActions)
endfunction
//===========================================================================
// Trigger: firstSecond
//===========================================================================
function Trig_firstSecondActions takes nothing returns nothing
    call PanCameraToTimed(5000.00, - 3000.00, 0.00)
endfunction
//===========================================================================
function InitTrig_firstSecond takes nothing returns nothing
    set gg_trg_firstSecond=CreateTrigger()
    call TriggerRegisterTimerEventSingle(gg_trg_firstSecond, 0.10)
    call TriggerAddAction(gg_trg_firstSecond, function Trig_firstSecondActions)
endfunction
//===========================================================================
function InitCustomTriggers takes nothing returns nothing
    call InitTrig_firstOccur()
    call InitTrig_fisrtOccur_2()
    call InitTrig_init()
    call InitTrig_firstSecond()
endfunction
//===========================================================================
function RunInitializationTriggers takes nothing returns nothing
    call ConditionalTriggerExecute(gg_trg_init)
endfunction
//***************************************************************************
//*
//*  Players
//*
//***************************************************************************
function InitCustomPlayerSlots takes nothing returns nothing
    // Player 0
    call SetPlayerStartLocation(Player(0), 0)
    call SetPlayerColor(Player(0), ConvertPlayerColor(0))
    call SetPlayerRacePreference(Player(0), RACE_PREF_HUMAN)
    call SetPlayerRaceSelectable(Player(0), true)
    call SetPlayerController(Player(0), MAP_CONTROL_USER)
    // Player 1
    call SetPlayerStartLocation(Player(1), 1)
    call SetPlayerColor(Player(1), ConvertPlayerColor(1))
    call SetPlayerRacePreference(Player(1), RACE_PREF_HUMAN)
    call SetPlayerRaceSelectable(Player(1), true)
    call SetPlayerController(Player(1), MAP_CONTROL_USER)
    // Player 2
    call SetPlayerStartLocation(Player(2), 2)
    call SetPlayerColor(Player(2), ConvertPlayerColor(2))
    call SetPlayerRacePreference(Player(2), RACE_PREF_HUMAN)
    call SetPlayerRaceSelectable(Player(2), true)
    call SetPlayerController(Player(2), MAP_CONTROL_USER)
    // Player 3
    call SetPlayerStartLocation(Player(3), 3)
    call SetPlayerColor(Player(3), ConvertPlayerColor(3))
    call SetPlayerRacePreference(Player(3), RACE_PREF_HUMAN)
    call SetPlayerRaceSelectable(Player(3), true)
    call SetPlayerController(Player(3), MAP_CONTROL_USER)
    // Player 4
    call SetPlayerStartLocation(Player(4), 4)
    call SetPlayerColor(Player(4), ConvertPlayerColor(4))
    call SetPlayerRacePreference(Player(4), RACE_PREF_HUMAN)
    call SetPlayerRaceSelectable(Player(4), true)
    call SetPlayerController(Player(4), MAP_CONTROL_USER)
    // Player 5
    call SetPlayerStartLocation(Player(5), 5)
    call SetPlayerColor(Player(5), ConvertPlayerColor(5))
    call SetPlayerRacePreference(Player(5), RACE_PREF_NIGHTELF)
    call SetPlayerRaceSelectable(Player(5), true)
    call SetPlayerController(Player(5), MAP_CONTROL_COMPUTER)
    // Player 6
    call SetPlayerStartLocation(Player(6), 6)
    call SetPlayerColor(Player(6), ConvertPlayerColor(6))
    call SetPlayerRacePreference(Player(6), RACE_PREF_NIGHTELF)
    call SetPlayerRaceSelectable(Player(6), true)
    call SetPlayerController(Player(6), MAP_CONTROL_COMPUTER)
    // Player 7
    call SetPlayerStartLocation(Player(7), 7)
    call SetPlayerColor(Player(7), ConvertPlayerColor(7))
    call SetPlayerRacePreference(Player(7), RACE_PREF_ORC)
    call SetPlayerRaceSelectable(Player(7), true)
    call SetPlayerController(Player(7), MAP_CONTROL_COMPUTER)
    // Player 8
    call SetPlayerStartLocation(Player(8), 8)
    call SetPlayerColor(Player(8), ConvertPlayerColor(8))
    call SetPlayerRacePreference(Player(8), RACE_PREF_ORC)
    call SetPlayerRaceSelectable(Player(8), true)
    call SetPlayerController(Player(8), MAP_CONTROL_COMPUTER)
    // Player 9
    call SetPlayerStartLocation(Player(9), 9)
    call SetPlayerColor(Player(9), ConvertPlayerColor(9))
    call SetPlayerRacePreference(Player(9), RACE_PREF_ORC)
    call SetPlayerRaceSelectable(Player(9), true)
    call SetPlayerController(Player(9), MAP_CONTROL_COMPUTER)
endfunction
function InitCustomTeams takes nothing returns nothing
    // Force: TRIGSTR_011
    call SetPlayerTeam(Player(0), 0)
    call SetPlayerState(Player(0), PLAYER_STATE_ALLIED_VICTORY, 1)
    call SetPlayerTeam(Player(1), 0)
    call SetPlayerState(Player(1), PLAYER_STATE_ALLIED_VICTORY, 1)
    call SetPlayerTeam(Player(2), 0)
    call SetPlayerState(Player(2), PLAYER_STATE_ALLIED_VICTORY, 1)
    call SetPlayerTeam(Player(3), 0)
    call SetPlayerState(Player(3), PLAYER_STATE_ALLIED_VICTORY, 1)
    call SetPlayerTeam(Player(4), 0)
    call SetPlayerState(Player(4), PLAYER_STATE_ALLIED_VICTORY, 1)
    call SetPlayerTeam(Player(5), 0)
    call SetPlayerState(Player(5), PLAYER_STATE_ALLIED_VICTORY, 1)
    call SetPlayerTeam(Player(6), 0)
    call SetPlayerState(Player(6), PLAYER_STATE_ALLIED_VICTORY, 1)
    //   Allied
    call SetPlayerAllianceStateAllyBJ(Player(0), Player(1), true)
    call SetPlayerAllianceStateAllyBJ(Player(0), Player(2), true)
    call SetPlayerAllianceStateAllyBJ(Player(0), Player(3), true)
    call SetPlayerAllianceStateAllyBJ(Player(0), Player(4), true)
    call SetPlayerAllianceStateAllyBJ(Player(0), Player(5), true)
    call SetPlayerAllianceStateAllyBJ(Player(0), Player(6), true)
    call SetPlayerAllianceStateAllyBJ(Player(1), Player(0), true)
    call SetPlayerAllianceStateAllyBJ(Player(1), Player(2), true)
    call SetPlayerAllianceStateAllyBJ(Player(1), Player(3), true)
    call SetPlayerAllianceStateAllyBJ(Player(1), Player(4), true)
    call SetPlayerAllianceStateAllyBJ(Player(1), Player(5), true)
    call SetPlayerAllianceStateAllyBJ(Player(1), Player(6), true)
    call SetPlayerAllianceStateAllyBJ(Player(2), Player(0), true)
    call SetPlayerAllianceStateAllyBJ(Player(2), Player(1), true)
    call SetPlayerAllianceStateAllyBJ(Player(2), Player(3), true)
    call SetPlayerAllianceStateAllyBJ(Player(2), Player(4), true)
    call SetPlayerAllianceStateAllyBJ(Player(2), Player(5), true)
    call SetPlayerAllianceStateAllyBJ(Player(2), Player(6), true)
    call SetPlayerAllianceStateAllyBJ(Player(3), Player(0), true)
    call SetPlayerAllianceStateAllyBJ(Player(3), Player(1), true)
    call SetPlayerAllianceStateAllyBJ(Player(3), Player(2), true)
    call SetPlayerAllianceStateAllyBJ(Player(3), Player(4), true)
    call SetPlayerAllianceStateAllyBJ(Player(3), Player(5), true)
    call SetPlayerAllianceStateAllyBJ(Player(3), Player(6), true)
    call SetPlayerAllianceStateAllyBJ(Player(4), Player(0), true)
    call SetPlayerAllianceStateAllyBJ(Player(4), Player(1), true)
    call SetPlayerAllianceStateAllyBJ(Player(4), Player(2), true)
    call SetPlayerAllianceStateAllyBJ(Player(4), Player(3), true)
    call SetPlayerAllianceStateAllyBJ(Player(4), Player(5), true)
    call SetPlayerAllianceStateAllyBJ(Player(4), Player(6), true)
    call SetPlayerAllianceStateAllyBJ(Player(5), Player(0), true)
    call SetPlayerAllianceStateAllyBJ(Player(5), Player(1), true)
    call SetPlayerAllianceStateAllyBJ(Player(5), Player(2), true)
    call SetPlayerAllianceStateAllyBJ(Player(5), Player(3), true)
    call SetPlayerAllianceStateAllyBJ(Player(5), Player(4), true)
    call SetPlayerAllianceStateAllyBJ(Player(5), Player(6), true)
    call SetPlayerAllianceStateAllyBJ(Player(6), Player(0), true)
    call SetPlayerAllianceStateAllyBJ(Player(6), Player(1), true)
    call SetPlayerAllianceStateAllyBJ(Player(6), Player(2), true)
    call SetPlayerAllianceStateAllyBJ(Player(6), Player(3), true)
    call SetPlayerAllianceStateAllyBJ(Player(6), Player(4), true)
    call SetPlayerAllianceStateAllyBJ(Player(6), Player(5), true)
    //   Shared Vision
    call SetPlayerAllianceStateVisionBJ(Player(0), Player(1), true)
    call SetPlayerAllianceStateVisionBJ(Player(0), Player(2), true)
    call SetPlayerAllianceStateVisionBJ(Player(0), Player(3), true)
    call SetPlayerAllianceStateVisionBJ(Player(0), Player(4), true)
    call SetPlayerAllianceStateVisionBJ(Player(0), Player(5), true)
    call SetPlayerAllianceStateVisionBJ(Player(0), Player(6), true)
    call SetPlayerAllianceStateVisionBJ(Player(1), Player(0), true)
    call SetPlayerAllianceStateVisionBJ(Player(1), Player(2), true)
    call SetPlayerAllianceStateVisionBJ(Player(1), Player(3), true)
    call SetPlayerAllianceStateVisionBJ(Player(1), Player(4), true)
    call SetPlayerAllianceStateVisionBJ(Player(1), Player(5), true)
    call SetPlayerAllianceStateVisionBJ(Player(1), Player(6), true)
    call SetPlayerAllianceStateVisionBJ(Player(2), Player(0), true)
    call SetPlayerAllianceStateVisionBJ(Player(2), Player(1), true)
    call SetPlayerAllianceStateVisionBJ(Player(2), Player(3), true)
    call SetPlayerAllianceStateVisionBJ(Player(2), Player(4), true)
    call SetPlayerAllianceStateVisionBJ(Player(2), Player(5), true)
    call SetPlayerAllianceStateVisionBJ(Player(2), Player(6), true)
    call SetPlayerAllianceStateVisionBJ(Player(3), Player(0), true)
    call SetPlayerAllianceStateVisionBJ(Player(3), Player(1), true)
    call SetPlayerAllianceStateVisionBJ(Player(3), Player(2), true)
    call SetPlayerAllianceStateVisionBJ(Player(3), Player(4), true)
    call SetPlayerAllianceStateVisionBJ(Player(3), Player(5), true)
    call SetPlayerAllianceStateVisionBJ(Player(3), Player(6), true)
    call SetPlayerAllianceStateVisionBJ(Player(4), Player(0), true)
    call SetPlayerAllianceStateVisionBJ(Player(4), Player(1), true)
    call SetPlayerAllianceStateVisionBJ(Player(4), Player(2), true)
    call SetPlayerAllianceStateVisionBJ(Player(4), Player(3), true)
    call SetPlayerAllianceStateVisionBJ(Player(4), Player(5), true)
    call SetPlayerAllianceStateVisionBJ(Player(4), Player(6), true)
    call SetPlayerAllianceStateVisionBJ(Player(5), Player(0), true)
    call SetPlayerAllianceStateVisionBJ(Player(5), Player(1), true)
    call SetPlayerAllianceStateVisionBJ(Player(5), Player(2), true)
    call SetPlayerAllianceStateVisionBJ(Player(5), Player(3), true)
    call SetPlayerAllianceStateVisionBJ(Player(5), Player(4), true)
    call SetPlayerAllianceStateVisionBJ(Player(5), Player(6), true)
    call SetPlayerAllianceStateVisionBJ(Player(6), Player(0), true)
    call SetPlayerAllianceStateVisionBJ(Player(6), Player(1), true)
    call SetPlayerAllianceStateVisionBJ(Player(6), Player(2), true)
    call SetPlayerAllianceStateVisionBJ(Player(6), Player(3), true)
    call SetPlayerAllianceStateVisionBJ(Player(6), Player(4), true)
    call SetPlayerAllianceStateVisionBJ(Player(6), Player(5), true)
    // Force: TRIGSTR_012
    call SetPlayerTeam(Player(7), 1)
    call SetPlayerTeam(Player(8), 1)
    call SetPlayerTeam(Player(9), 1)
    //   Allied
    call SetPlayerAllianceStateAllyBJ(Player(7), Player(8), true)
    call SetPlayerAllianceStateAllyBJ(Player(7), Player(9), true)
    call SetPlayerAllianceStateAllyBJ(Player(8), Player(7), true)
    call SetPlayerAllianceStateAllyBJ(Player(8), Player(9), true)
    call SetPlayerAllianceStateAllyBJ(Player(9), Player(7), true)
    call SetPlayerAllianceStateAllyBJ(Player(9), Player(8), true)
    //   Shared Vision
    call SetPlayerAllianceStateVisionBJ(Player(7), Player(8), true)
    call SetPlayerAllianceStateVisionBJ(Player(7), Player(9), true)
    call SetPlayerAllianceStateVisionBJ(Player(8), Player(7), true)
    call SetPlayerAllianceStateVisionBJ(Player(8), Player(9), true)
    call SetPlayerAllianceStateVisionBJ(Player(9), Player(7), true)
    call SetPlayerAllianceStateVisionBJ(Player(9), Player(8), true)
endfunction
function InitAllyPriorities takes nothing returns nothing
    call SetStartLocPrioCount(0, 1)
    call SetStartLocPrio(0, 0, 3, MAP_LOC_PRIO_HIGH)
    call SetStartLocPrioCount(1, 1)
    call SetStartLocPrio(1, 0, 4, MAP_LOC_PRIO_HIGH)
    call SetStartLocPrioCount(2, 1)
    call SetStartLocPrio(2, 0, 1, MAP_LOC_PRIO_HIGH)
    call SetStartLocPrioCount(3, 2)
    call SetStartLocPrio(3, 0, 0, MAP_LOC_PRIO_HIGH)
    call SetStartLocPrio(3, 1, 1, MAP_LOC_PRIO_LOW)
    call SetStartLocPrioCount(4, 1)
    call SetStartLocPrio(4, 0, 1, MAP_LOC_PRIO_HIGH)
endfunction
//***************************************************************************
//*
//*  Main Initialization
//*
//***************************************************************************
//===========================================================================
function main takes nothing returns nothing
    call SetCameraBounds(- 11520.0 + GetCameraMargin(CAMERA_MARGIN_LEFT), - 11776.0 + GetCameraMargin(CAMERA_MARGIN_BOTTOM), 11520.0 - GetCameraMargin(CAMERA_MARGIN_RIGHT), 11264.0 - GetCameraMargin(CAMERA_MARGIN_TOP), - 11520.0 + GetCameraMargin(CAMERA_MARGIN_LEFT), 11264.0 - GetCameraMargin(CAMERA_MARGIN_TOP), 11520.0 - GetCameraMargin(CAMERA_MARGIN_RIGHT), - 11776.0 + GetCameraMargin(CAMERA_MARGIN_BOTTOM))
    call SetDayNightModels("Environment\\DNC\\DNCLordaeron\\DNCLordaeronTerrain\\DNCLordaeronTerrain.mdl", "Environment\\DNC\\DNCLordaeron\\DNCLordaeronUnit\\DNCLordaeronUnit.mdl")
    call NewSoundEnvironment("Default")
    call SetAmbientDaySound("LordaeronSummerDay")
    call SetAmbientNightSound("LordaeronSummerNight")
    call SetMapMusic("Music", true, 0)
    call CreateAllUnits()
    call InitBlizzard()

call ExecuteFunc("jasshelper__initstructs841559156")
call ExecuteFunc("InitCultivationData")
call ExecuteFunc("InitDungeonData")
call ExecuteFunc("InitEquipmentData")
call ExecuteFunc("InitGameTimeSystem")
call ExecuteFunc("LBKKAPI___Init")
call ExecuteFunc("InitSectData")
call ExecuteFunc("InitTestEquipmentGenerate")
call ExecuteFunc("InitializeYD")
call ExecuteFunc("InitDungeonMonsterData")
call ExecuteFunc("GeneralBonusSystem___Initialize")
call ExecuteFunc("InitEnemySkill")
call ExecuteFunc("InitHeroSelectionSystem")
call ExecuteFunc("InitEquipmentTriggers")
call ExecuteFunc("InitTestEquipmentDebug")
call ExecuteFunc("OnInit")

    call InitGlobals()
    call InitCustomTriggers()
    call RunInitializationTriggers()
endfunction
//***************************************************************************
//*
//*  Map Configuration
//*
//***************************************************************************
function config takes nothing returns nothing
    call SetMapName("快意江湖")
    call SetMapDescription("没有说明")
    call SetPlayers(10)
    call SetTeams(10)
    call SetGamePlacement(MAP_PLACEMENT_TEAMS_TOGETHER)
    call DefineStartLocation(0, 2240.0, - 10240.0)
    call DefineStartLocation(1, 1088.0, 3584.0)
    call DefineStartLocation(2, 10304.0, 2816.0)
    call DefineStartLocation(3, - 4864.0, - 5760.0)
    call DefineStartLocation(4, - 3520.0, 7360.0)
    call DefineStartLocation(5, - 1920.0, 1152.0)
    call DefineStartLocation(6, - 10112.0, - 4864.0)
    call DefineStartLocation(7, 8000.0, 1024.0)
    call DefineStartLocation(8, 6208.0, - 1152.0)
    call DefineStartLocation(9, - 10432.0, - 1472.0)
    // Player setup
    call InitCustomPlayerSlots()
    call InitCustomTeams()
    call InitAllyPriorities()
endfunction
// [DzSetUnitMoveType]  
// title = "设置单位移动类型[NEW]"  
// description = "设置 ${单位} 的移动类型：${movetype} "  
// comment = ""  
// category = TC_KKPRE  
// [[.args]]  
// type = unit  
// [[.args]]  
// type = MoveTypeName  
// default = MoveTypeName01  




//Struct method generated initializers/callers:
function sa__Skill_onDestroy takes nothing returns boolean
local integer this=f__arg_this
            set s__Skill_skill_id[this]=0
            set s__Skill_skill_name[this]=""
            set s__Skill_skill_desc[this]=""
            set s__Skill_skill_type[this]=0
            set s__Skill_skill_target_type[this]=0
            set s__Skill_skill_template_id[this]=0
            set s__Skill_skill_cooldown[this]=0.0
            set s__Skill_skill_magic_cost[this]=0
            set s__Skill_skill_cast_range[this]=0.0
            set s__Skill_skill_damage_coefficient[this]=0.0
            set s__Skill_skill_attribute_type[this]=0
            set s__Skill_skill_element_type[this]=0
            set s__Skill_skill_damage_type[this]=0
   return true
endfunction

function jasshelper__initstructs841559156 takes nothing returns nothing
    set st__Skill_onDestroy=CreateTrigger()
    call TriggerAddCondition(st__Skill_onDestroy,Condition( function sa__Skill_onDestroy))


endfunction


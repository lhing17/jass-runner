"""JASS类型层次结构管理。"""


class TypeHierarchy:
    """管理JASS类型之间的继承关系。

    JASS使用handle作为所有游戏对象的基类，
    unit、item、timer等都继承自handle。
    """

    # handle子类型映射: {子类型: 父类型}
    HANDLE_SUBTYPES = {
        'unit': 'handle',
        'item': 'handle',
        'timer': 'handle',
        'trigger': 'handle',
        'player': 'handle',
        'destructable': 'handle',
        'itempool': 'handle',
        'unitpool': 'handle',
        'group': 'handle',
        'force': 'handle',
        'rect': 'handle',
        'region': 'handle',
        'sound': 'handle',
        'effect': 'handle',
        'location': 'handle',
    }

    @classmethod
    def is_subtype(cls, subtype: str, basetype: str) -> bool:
        """判断subtype是否是basetype的子类型。

        参数：
            subtype: 子类型名称
            basetype: 基类型名称

        返回：
            如果是子类型返回True，否则返回False
        """
        if subtype == basetype:
            return True

        # 检查handle类型层次
        current = subtype
        while current in cls.HANDLE_SUBTYPES:
            parent = cls.HANDLE_SUBTYPES[current]
            if parent == basetype:
                return True
            current = parent

        return False

    @classmethod
    def get_base_type(cls, type_name: str) -> str:
        """获取类型的基类型。

        对于handle子类型，返回'handle'。
        对于其他类型，返回其自身。

        参数：
            type_name: 类型名称

        返回：
            基类型名称
        """
        if type_name in cls.HANDLE_SUBTYPES:
            return cls.HANDLE_SUBTYPES[type_name]
        return type_name

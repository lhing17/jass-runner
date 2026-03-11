"""FourCC 工具函数。

FourCC（Four Character Code）是 JASS 中用于表示单位类型、技能类型等的 4 字符代码。
"""

def fourcc_to_int(fourcc: str) -> int:
    """将FourCC字符串转换为整数。

    参数：
        fourcc: 4个字符的字符串，如'hfoo'

    返回：
        32位整数表示

    示例：
        >>> fourcc_to_int('hfoo')
        1213484355
    """
    if len(fourcc) != 4:
        raise ValueError(f"FourCC必须是4个字符，得到: {fourcc}")
    return int.from_bytes(fourcc.encode('ascii'), 'big')


def int_to_fourcc(value: int) -> str:
    """将整数转换为FourCC字符串。

    参数：
        value: 32位整数

    返回：
        4个字符的字符串

    示例：
        >>> int_to_fourcc(1213484355)
        'hfoo'
    """
    try:
        return value.to_bytes(4, 'big').decode('ascii')
    except Exception:
        return str(value)


def is_fourcc(value) -> bool:
    """检查值是否为有效的FourCC格式。

    参数：
        value: 要检查的值（字符串或整数）

    返回：
        如果是有效的FourCC格式返回True
    """
    if isinstance(value, str):
        return len(value) == 4 and value.isascii()
    if isinstance(value, int):
        return 0 <= value <= 0xFFFFFFFF
    return False

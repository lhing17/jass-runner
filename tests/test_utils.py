"""工具函数测试。"""

import pytest


def test_fourcc_to_int():
    """测试FourCC字符串转换为整数。"""
    from jass_runner.utils import fourcc_to_int

    # 测试常见单位类型 (little-endian)
    assert fourcc_to_int('hfoo') == 1869571688  # 'hfoo' -> 0x6F6F6668
    assert fourcc_to_int('hkni') == 1768188776  # 'hkni' -> 0x696E6B68
    assert fourcc_to_int('hpea') == 1634035304  # 'hpea' -> 0x61657068

    # 测试技能类型
    assert fourcc_to_int('AHdr') == 1918981185  # 'AHdr' -> 0x72644841


def test_fourcc_to_int_invalid_length():
    """测试FourCC长度验证。"""
    from jass_runner.utils import fourcc_to_int

    with pytest.raises(ValueError, match="FourCC必须是4个字符"):
        fourcc_to_int('hf')  # 太短

    with pytest.raises(ValueError, match="FourCC必须是4个字符"):
        fourcc_to_int('hfooo')  # 太长


def test_int_to_fourcc():
    """测试整数转换为FourCC字符串。"""
    from jass_runner.utils import int_to_fourcc

    assert int_to_fourcc(1869571688) == 'hfoo'
    assert int_to_fourcc(1768188776) == 'hkni'
    assert int_to_fourcc(1634035304) == 'hpea'


def test_fourcc_roundtrip():
    """测试FourCC转换的往返一致性。"""
    from jass_runner.utils import fourcc_to_int, int_to_fourcc

    test_codes = ['hfoo', 'hkni', 'hpea', 'AHdr', 'Amnz']

    for code in test_codes:
        assert int_to_fourcc(fourcc_to_int(code)) == code


def test_is_fourcc_with_string():
    """测试is_fourcc检查字符串。"""
    from jass_runner.utils import is_fourcc

    assert is_fourcc('hfoo') is True
    assert is_fourcc('hkni') is True

    # 无效长度
    assert is_fourcc('hf') is False
    assert is_fourcc('hfooo') is False


def test_is_fourcc_with_int():
    """测试is_fourcc检查整数。"""
    from jass_runner.utils import is_fourcc

    assert is_fourcc(1213484355) is True  # 有效FourCC整数
    assert is_fourcc(0) is True
    assert is_fourcc(0xFFFFFFFF) is True

    # 超出范围
    assert is_fourcc(-1) is False
    assert is_fourcc(0x100000000) is False


def test_is_fourcc_with_other_types():
    """测试is_fourcc拒绝其他类型。"""
    from jass_runner.utils import is_fourcc

    assert is_fourcc(None) is False
    assert is_fourcc(3.14) is False
    assert is_fourcc([]) is False

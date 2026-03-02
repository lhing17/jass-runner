"""TypeChecker模块测试。"""

import pytest
from jass_runner.types.errors import JassTypeError


def test_is_compatible_same_type():
    """相同类型总是兼容。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    assert checker.is_compatible('integer', 'integer') is True
    assert checker.is_compatible('real', 'real') is True


def test_is_compatible_integer_to_real():
    """integer可隐式转为real。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    assert checker.is_compatible('integer', 'real') is True


def test_is_compatible_real_to_integer():
    """real不可隐式转为integer。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    assert checker.is_compatible('real', 'integer') is False


def test_is_compatible_unit_to_handle():
    """unit可赋值给handle（协变）。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    assert checker.is_compatible('unit', 'handle') is True


def test_check_assignment_integer_to_real():
    """integer赋值给real变量应转换成功。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()
    result = checker.check_assignment('real', 10, 'integer')

    assert result == 10.0
    assert isinstance(result, float)


def test_check_assignment_string_to_integer_raises():
    """string赋值给integer应抛出异常。"""
    from jass_runner.types.checker import TypeChecker

    checker = TypeChecker()

    with pytest.raises(JassTypeError) as exc_info:
        checker.check_assignment('integer', 'hello', 'string')

    assert 'string' in str(exc_info.value)
    assert 'integer' in str(exc_info.value)

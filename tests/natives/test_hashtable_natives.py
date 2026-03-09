"""Hashtable Native 函数测试"""

import pytest
from unittest.mock import MagicMock


class TestInitHashtable:
    """测试 InitHashtable native 函数"""

    def test_init_hashtable_returns_hashtable(self):
        """测试 InitHashtable 返回 hashtable"""
        from jass_runner.natives.hashtable_natives import InitHashtable

        mock_state = MagicMock()
        mock_state.handle_manager.create_hashtable.return_value = MagicMock(id="hashtable_1")

        native = InitHashtable()
        result = native.execute(mock_state)

        assert result is not None
        mock_state.handle_manager.create_hashtable.assert_called_once()

    def test_init_hashtable_without_handle_manager(self):
        """测试没有 handle_manager 时返回 None"""
        from jass_runner.natives.hashtable_natives import InitHashtable

        mock_state = MagicMock()
        delattr(mock_state, 'handle_manager')

        native = InitHashtable()
        result = native.execute(mock_state)

        assert result is None


class TestSaveOperations:
    """测试 Save* native 函数"""

    def test_save_integer(self):
        """测试 SaveInteger"""
        from jass_runner.natives.hashtable_natives import SaveInteger

        mock_ht = MagicMock()
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = SaveInteger()
        native.execute(mock_state, "hashtable_1", 0, 0, 42)

        mock_state.handle_manager.get_hashtable.assert_called_once_with("hashtable_1")
        mock_ht.save_integer.assert_called_once_with(0, 0, 42)

    def test_save_real(self):
        """测试 SaveReal"""
        from jass_runner.natives.hashtable_natives import SaveReal

        mock_ht = MagicMock()
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = SaveReal()
        native.execute(mock_state, "hashtable_1", 0, 0, 3.14)

        mock_ht.save_real.assert_called_once_with(0, 0, 3.14)

    def test_save_str_returns_true(self):
        """测试 SaveStr 返回 True"""
        from jass_runner.natives.hashtable_natives import SaveStr

        mock_ht = MagicMock()
        mock_ht.save_string.return_value = True
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = SaveStr()
        result = native.execute(mock_state, "hashtable_1", 0, 0, "hello")

        assert result is True

    def test_save_unit_handle(self):
        """测试 SaveUnitHandle"""
        from jass_runner.natives.hashtable_natives import SaveUnitHandle

        mock_ht = MagicMock()
        mock_ht.save_unit_handle.return_value = True
        mock_unit = MagicMock()
        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = mock_ht

        native = SaveUnitHandle()
        result = native.execute(mock_state, "hashtable_1", 0, 0, mock_unit)

        assert result is True
        mock_ht.save_unit_handle.assert_called_once_with(0, 0, mock_unit)

    def test_save_invalid_hashtable(self):
        """测试无效的 hashtable 记录警告"""
        from jass_runner.natives.hashtable_natives import SaveInteger

        mock_state = MagicMock()
        mock_state.handle_manager.get_hashtable.return_value = None

        native = SaveInteger()
        result = native.execute(mock_state, "invalid_ht", 0, 0, 42)

        assert result is None

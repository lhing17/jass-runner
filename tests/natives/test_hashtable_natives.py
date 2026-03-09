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

"""JASS 常量加载器。

负责解析和加载 common.j、blizzard.j 中的常量定义。
"""

import os
import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConstantLoader:
    """JASS 常量加载器。"""

    def __init__(self, interpreter):
        """初始化常量加载器。

        参数:
            interpreter: JASS 解释器实例，用于存储常量和创建 handle
        """
        self.interpreter = interpreter
        # 预编译正则表达式
        self.constant_pattern = re.compile(
            r'^\s*constant\s+(\w+)\s+(\w+)\s*=\s*([^/\r\n]+)',
            re.MULTILINE
        )
        self.func_call_pattern = re.compile(r'(\w+)\((\d+)\)')

    def load_from_file(self, filepath: str) -> None:
        """从文件加载常量定义。

        参数:
            filepath: 文件路径
        """
        if not os.path.exists(filepath):
            logger.warning(f"常量文件未找到: {filepath}")
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self._parse_content(content)
        except Exception as e:
            logger.error(f"解析常量文件失败 {filepath}: {e}")

    def _parse_content(self, content: str) -> None:
        """解析内容中的常量定义。"""
        for match in self.constant_pattern.finditer(content):
            const_type = match.group(1)
            const_name = match.group(2)
            const_value_str = match.group(3).strip()

            # 转换值为Python类型并存储到解释器的全局变量
            value = self._convert_value(const_type, const_value_str)
            self.interpreter.global_context.variables[const_name] = value

    def _convert_value(self, const_type: str, const_value: str) -> Any:
        """将JASS常量值转换为Python值。"""
        if const_type == 'integer':
            return self._parse_integer(const_value)
        elif const_type == 'real':
            return self._parse_real(const_value)
        elif const_type == 'boolean':
            return const_value.lower() == 'true'
        elif const_type == 'string':
            return const_value.strip('"')
        elif const_type == 'code':
            return None  # code 类型通常为 null 或函数引用，常量中一般为 null
        else:
            # 处理 handle 类型 (如 playerstate, unitevent 等)
            return self._parse_handle_type(const_type, const_value)

    def _parse_integer(self, value: str) -> int:
        try:
            # 处理十六进制 (0x...) 和普通整数
            if value.startswith('0x') or value.startswith('$'):
                 return int(value.replace('$', '0x'), 16)
            # 处理字符常量 'hfoo'
            if value.startswith("'") and value.endswith("'") and len(value) == 6:
                from .fourcc import fourcc_to_int
                return fourcc_to_int(value[1:-1])
            return int(value)
        except (ValueError, ImportError):
            logger.warning(f"无法解析整数常量: {value}")
            return 0

    def _parse_real(self, value: str) -> float:
        try:
            return float(value)
        except ValueError:
            logger.warning(f"无法解析实数常量: {value}")
            return 0.0

    def _parse_handle_type(self, const_type: str, const_value: str) -> Any:
        """处理 Handle 类型的常量转换。"""
        # 尝试匹配 ConvertXxx(int) 格式
        match = self.func_call_pattern.search(const_value)
        if match:
            func_name = match.group(1)
            arg_value = int(match.group(2))

            # 根据类型创建相应的 Handle 对象
            # 注意：这会产生副作用（创建 Handle），但在加载 common.j 时是必要的
            handle_manager = self.interpreter.state_context.handle_manager

            if const_type == 'playerunitevent':
                 return handle_manager.create_playerunit_event(arg_value)
            elif const_type == 'playerevent':
                return handle_manager.create_playerevent(arg_value)
            elif const_type == 'gameevent':
                return handle_manager.create_gameevent(arg_value)
            elif const_type == 'unitevent':
                return handle_manager.create_unitevent(arg_value)
            elif const_type == 'limitop':
                return handle_manager.create_limitop(arg_value)
            elif const_type == 'widgetevent':
                return handle_manager.create_widgetevent(arg_value)
            elif const_type == 'dialogevent':
                return handle_manager.create_dialogevent(arg_value)
            elif const_type == 'gamestate':
                 return handle_manager.create_gamestate(arg_value)
            elif const_type == 'igamestate':
                 return handle_manager.create_igamestate(arg_value)
            elif const_type == 'fgamestate':
                 return handle_manager.create_fgamestate(arg_value)
            elif const_type == 'playerstate':
                 return arg_value # 许多 state 只是整数别名，视具体实现而定，这里假设先返回整数或后续完善 Handle
            elif const_type == 'unitstate':
                 return arg_value
            elif const_type == 'alliancetype':
                 return arg_value
            # ... 其他类型待补充

            # 如果没有匹配的特殊处理，返回原始整数值（模拟 Handle ID）
            return arg_value

        # 如果不是函数调用，可能是 null 或其他变量引用
        if const_value == 'null':
            return None
        
        return const_value

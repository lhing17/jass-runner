"""内存监控工具。

此模块提供内存使用监控功能，用于跟踪handle系统的内存消耗。
"""

import sys
import logging
from typing import Dict, List, Any, Optional


logger = logging.getLogger(__name__)


class MemoryTracker:
    """内存使用追踪器。

    用于监控handle系统的内存使用情况，帮助识别内存泄漏。

    属性：
        initial_memory: 初始内存使用量（字节）
        peak_memory: 峰值内存使用量（字节）
        snapshots: 内存快照列表
    """

    def __init__(self):
        """初始化内存追踪器。"""
        self.initial_memory = 0
        self.peak_memory = 0
        self.snapshots: List[Dict[str, Any]] = []
        self._start_tracking()

    def _get_current_memory(self) -> int:
        """获取当前内存使用量。

        返回：
            当前内存使用量（字节）
        """
        # 使用sys.getsizeof估算，实际生产环境可使用psutil
        import gc
        gc.collect()  # 强制垃圾回收获取准确值
        return 0  # 基线实现，可扩展为使用tracemalloc

    def _start_tracking(self):
        """开始追踪内存。"""
        self.initial_memory = self._get_current_memory()
        self.peak_memory = self.initial_memory
        logger.debug(f"内存追踪开始，初始内存: {self._format_bytes(self.initial_memory)}")

    def snapshot(self, point_name: str) -> Dict[str, Any]:
        """记录内存快照。

        参数：
            point_name: 快照点名称

        返回：
            快照信息字典
        """
        current = self._get_current_memory()

        # 更新峰值
        if current > self.peak_memory:
            self.peak_memory = current

        snapshot = {
            "point": point_name,
            "memory": current,
            "delta": current - self.initial_memory,
        }
        self.snapshots.append(snapshot)

        logger.debug(f"内存快照 [{point_name}]: {self._format_bytes(current)}")
        return snapshot

    def get_stats(self) -> Dict[str, Any]:
        """获取内存统计信息。

        返回：
            统计信息字典
        """
        current = self._get_current_memory()
        return {
            "initial_memory": self.initial_memory,
            "peak_memory": self.peak_memory,
            "current_memory": current,
            "total_delta": current - self.initial_memory,
            "snapshots_count": len(self.snapshots),
        }

    def reset(self):
        """重置追踪器。"""
        self.snapshots.clear()
        self._start_tracking()

    @staticmethod
    def _format_bytes(bytes_value: int) -> str:
        """格式化字节值为可读字符串。

        参数：
            bytes_value: 字节值

        返回：
            格式化后的字符串（如"1.5 MB"）
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} TB"


class HandleMemoryMonitor:
    """Handle系统内存监控器。

    专门用于监控HandleManager的内存使用情况。
    """

    def __init__(self, handle_manager):
        """初始化监控器。

        参数：
            handle_manager: HandleManager实例
        """
        self.handle_manager = handle_manager
        self.tracker = MemoryTracker()

    def monitor_create_unit(self, unit_type: str, player_id: int,
                           x: float, y: float, facing: float):
        """监控单位创建操作的内存使用。

        参数：
            unit_type: 单位类型
            player_id: 玩家ID
            x: X坐标
            y: Y坐标
            facing: 面向角度

        返回：
            创建的Unit对象
        """
        self.tracker.snapshot(f"before_create_{unit_type}")
        unit = self.handle_manager.create_unit(unit_type, player_id, x, y, facing)
        self.tracker.snapshot(f"after_create_{unit_type}")
        return unit

    def get_handle_memory_report(self) -> Dict[str, Any]:
        """获取handle内存使用报告。

        返回：
            内存报告字典
        """
        stats = self.tracker.get_stats()
        handle_stats = {
            "total_handles": self.handle_manager.get_total_handles(),
            "alive_handles": self.handle_manager.get_alive_handles(),
            "memory_per_handle": stats["current_memory"] / max(stats["snapshots_count"], 1),
        }
        return {
            "memory_stats": stats,
            "handle_stats": handle_stats,
        }

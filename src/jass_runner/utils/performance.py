"""性能监控工具。

此模块提供性能监控功能，用于跟踪handle系统的性能指标。
"""

import time
import logging
import functools
from typing import Dict, List, Any, Optional, Callable
from collections import defaultdict


logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """性能监控器。

    用于跟踪handle系统的性能指标，如操作耗时。

    属性：
        metrics: 性能指标字典
    """

    def __init__(self):
        """初始化性能监控器。"""
        self.metrics: Dict[str, List[float]] = defaultdict(list)

    def record(self, operation: str, duration: float):
        """记录操作耗时。

        参数：
            operation: 操作名称
            duration: 耗时（秒）
        """
        self.metrics[operation].append(duration)

    def get_stats(self, operation: str) -> Dict[str, Any]:
        """获取指定操作的统计信息。

        参数：
            operation: 操作名称

        返回：
            统计信息字典
        """
        times = self.metrics.get(operation, [])
        if not times:
            return {"count": 0, "min": 0, "max": 0, "avg": 0, "total": 0}

        return {
            "count": len(times),
            "min": min(times),
            "max": max(times),
            "avg": sum(times) / len(times),
            "total": sum(times),
        }

    def get_report(self) -> Dict[str, Dict[str, Any]]:
        """生成完整性能报告。

        返回：
            所有操作的统计信息字典
        """
        return {op: self.get_stats(op) for op in self.metrics.keys()}

    def reset(self):
        """重置所有指标。"""
        self.metrics.clear()

    def log_report(self):
        """将性能报告输出到日志。"""
        report = self.get_report()
        logger.info("=" * 50)
        logger.info("性能监控报告")
        logger.info("=" * 50)

        for operation, stats in report.items():
            logger.info(f"\n操作: {operation}")
            logger.info(f"  调用次数: {stats['count']}")
            logger.info(f"  最小耗时: {stats['min']*1000:.3f} ms")
            logger.info(f"  最大耗时: {stats['max']*1000:.3f} ms")
            logger.info(f"  平均耗时: {stats['avg']*1000:.3f} ms")
            logger.info(f"  总耗时: {stats['total']*1000:.3f} ms")


def track_performance(operation_name: str):
    """性能监控装饰器。

    用于自动追踪函数执行时间。

    参数：
        operation_name: 操作名称

    返回：
        装饰器函数

    示例：
        @track_performance("create_unit")
        def create_unit(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                # 使用全局监控器记录
                _global_monitor.record(operation_name, duration)
        return wrapper
    return decorator


# 全局性能监控器
_global_monitor = PerformanceMonitor()


def get_global_monitor() -> PerformanceMonitor:
    """获取全局性能监控器。

    返回：
        全局PerformanceMonitor实例
    """
    return _global_monitor


def reset_global_monitor():
    """重置全局性能监控器。"""
    _global_monitor.reset()

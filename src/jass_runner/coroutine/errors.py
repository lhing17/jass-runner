"""协程错误定义。"""


class CoroutineError(Exception):
    """协程执行错误基类。"""
    pass


class CoroutineStackOverflow(CoroutineError):
    """协程调用栈溢出。"""
    pass

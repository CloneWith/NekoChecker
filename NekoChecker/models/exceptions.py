class AnsweringBannedException(Exception):
    timeout: int

    def __init__(self, timeout: int):
        self.timeout = timeout

    def __str__(self):
        return f"该题因短时间内多次错误，已被暂时禁止答题，请在 {self.timeout} 秒后再试。"

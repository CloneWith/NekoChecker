from pydantic import BaseModel
from typing import Optional


class Question(BaseModel):
    id: int = 0
    description: str = ""
    format: str = ""
    format_re: str = ""
    answer: str = ""
    tries_count: int = 0
    max_tries: int = -1
    solved: bool = False
    last_wrong_times: list[float] = []  # 记录错误时间戳
    banned_until: Optional[float] = None  # 被禁止答题的截止时间

    def record_wrong(self):
        import time
        now = time.time()
        self.last_wrong_times.append(now)
        # 只保留最近 5 次
        self.last_wrong_times = self.last_wrong_times[-5:]
        # 判断 30 秒内错误次数
        recent = [t for t in self.last_wrong_times if now - t < 30]
        if len(recent) >= 3:
            self.banned_until = now + 60  # 禁止 60 秒
            return True
        return False

    def is_banned(self):
        import time
        if self.banned_until is None:
            return False
        return time.time() < self.banned_until

    def check_pattern(self, flag: str):
        import re
        re.compile(flag)

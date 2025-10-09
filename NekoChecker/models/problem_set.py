from enum import Enum

from pydantic import BaseModel

from NekoChecker.models.question import Question
from NekoChecker.utils.cli import print_and_log


class FlagType(Enum):
    Static = 1
    EnvironmentVariables = 2
    LocalFile = 3


class ProblemSet(BaseModel):
    id: int = 0
    description: str = ""
    questions: list[Question] = []
    flag_type: FlagType = FlagType.Static
    static_flag: str = "flag{fake_flag}"
    flag_env_var: str = ""
    flag_file_path: str = ""

    def get_flag(self) -> str:
        """
        根据 flag_type 获取 flag。
        """
        if self.flag_type == FlagType.Static:
            return self.static_flag
        elif self.flag_type == FlagType.EnvironmentVariables:
            import os
            result = os.environ.get(self.flag_env_var)
            if result is None:
                print_and_log("未能获取 Flag，请联系运维。", "warn")
                return "flag{!!!not_found!!!}"

            return result
        elif self.flag_type == FlagType.LocalFile:
            try:
                with open(self.flag_file_path, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception:
                print_and_log("未能获取 Flag，请联系运维。", "warn")
                return "flag{!!!not_found!!!}"

        print_and_log("未能获取 Flag，请联系运维。", "warn")
        return "flag{!!!unknown_type!!!}"

    def get_solved_count(self) -> int:
        total_count = 0
        
        for q in self.questions:
            if q.solved:
                total_count += 1
                
        return total_count

    def all_solved(self) -> bool:
        """
        判断所有题目是否已回答正确。
        """
        return all(q.solved for q in self.questions)

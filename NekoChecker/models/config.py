from pydantic import BaseModel

from NekoChecker.models.problem_set import ProblemSet


class Config(BaseModel):
    name: str = "某个不知名比赛"
    problem_sets: list[ProblemSet]

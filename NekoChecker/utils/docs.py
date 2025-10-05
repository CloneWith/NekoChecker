import NekoChecker
from NekoChecker.utils import bold, tint

DESCRIPTION = "A lightweight and interactive command line answer checker."


def display_help():
    """
    显示 NekoChecker 交互命令帮助信息。
    """
    help_text = '''
NekoChecker 交互命令帮助：
    list / ls                 查看题库列表
    show [题库编号]            查看题库及题目答题情况
    answer <题库编号> <题号>    回答指定题目
    start [题库编号]           回答题库中所有未解决问题
    flag [题库编号]            获取题库 Flag
    save                      保存进度
    help                      显示本帮助信息
    exit                      退出程序
'''
    print(help_text)


"""Some constant strings and utilities for documents."""


def print_version():
    """
    Print project version information.

    输出项目版本信息。
    """
    print(
        f"""{bold(tint('NekoChecker', 'blue'))} version {NekoChecker.__version__}
By {" & ".join(NekoChecker.__authors__)}, licensed under {NekoChecker.__license__}
{DESCRIPTION}
"""
    )

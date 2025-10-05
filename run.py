import sys
from NekoChecker import main
from NekoChecker.utils.cli import print_and_log

PROBLEM_SET_LOCATION: str = "./problems.json"

if __name__ == "__main__":
    location = PROBLEM_SET_LOCATION
    if len(sys.argv) <= 1:
        print_and_log("未传递题库参数，尝试从默认位置读取！")
    else:
        location = sys.argv[1]

    sys.exit(main.main_loop(location))

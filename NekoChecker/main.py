import os

from NekoChecker.models.config import Config
from NekoChecker.models.exceptions import AnsweringBannedException
from NekoChecker.utils import tint, bold
from NekoChecker.utils.docs import display_help, print_version
from NekoChecker.utils.cli import print_and_log, exit_with_code


def load_config(json_path: str) -> Config:
    if not os.path.exists(json_path):
        print_and_log(f"配置文件不存在: {json_path}", "error", __name__)
        exit_with_code(1)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            sets = Config.model_validate_json(f.read())
            return sets
    except Exception as e:
        print_and_log(f"解析失败: {e}", "error", __name__)
        exit_with_code(1)
        raise RuntimeError("配置解析失败")


def main_loop(path: str):
    def save_config_to_file():
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(config.model_dump_json(indent=2))
            print_and_log(f"进度已保存！", "info", __name__)
        except Exception as e:
            print_and_log(f"保存失败: {e}", "error", __name__)

    def get_problem_set(idx: int):
        if idx < 0 or idx >= len(problem_sets):
            print_and_log("题组编号无效！", "error", __name__)
            return None
        return problem_sets[idx]

    def get_question(ps, q_idx: int):
        if q_idx < 0 or q_idx >= len(ps.questions):
            print_and_log("题号无效！", "error", __name__)
            return None
        return ps.questions[q_idx]

    def check_and_display_flag(ps, requested: bool = False):
        if ps.all_solved():
            flag = ps.get_flag()
            if not requested:
                print_and_log("恭喜！你已完成该题组。", "right_answer", __name__)
            print_and_log(f"{bold(f'[{ps.id}]')} {ps.description} 的 Flag: {bold(tint(flag, 'green'))}", "right_answer",
                          __name__)
        else:
            if requested:
                print_and_log("还未完成所有题目，不能获得 Flag...", "wrong_answer", __name__)

    def answer_logic(q):
        if hasattr(q, "is_banned") and q.is_banned():
            import time
            left = int(q.banned_until - time.time())
            raise AnsweringBannedException(left)

        print_and_log(f"[{q.id}] {q.description}", "info", __name__)
        if q.format is not None:
            print_and_log(f"格式：{q.format}", "info", __name__)

        try:
            user_ans = input(bold("Answer > "))
        except KeyboardInterrupt:
            print()
            return False
        # 格式校验
        if getattr(q, "format_re", None):
            import re
            if not re.fullmatch(q.format_re, user_ans):
                print_and_log(f"答案格式错误，应为: {q.format}", "error", __name__)
                return True
        if user_ans == q.answer:
            q.solved = True
            print_and_log("回答正确！", "right_answer", __name__)
        else:
            print_and_log("回答错误...", "wrong_answer", __name__)
            if hasattr(q, "record_wrong") and q.record_wrong():
                print_and_log("该题短时间内多次错误，已被禁止答题 60 秒！", "warn", __name__)
        save_config_to_file()
        return True

    def start_answering(ps_idx: int):
        ps = get_problem_set(ps_idx)
        if ps is None:
            return
        print_and_log(f"进入题组: {ps.description}", "info", __name__)
        for q_idx, q in enumerate(ps.questions):
            try:
                if q.solved:
                    continue
                if not answer_logic(q):
                    return
            except AnsweringBannedException as ex:
                print_and_log(ex.__str__(), "error", __name__)
                print_and_log("该题被禁止回答，正在跳过。", "warn", __name__)
                continue
        check_and_display_flag(ps)

    config = load_config(path)
    problem_sets = config.problem_sets
    print_and_log(f"欢迎来到 {bold(tint(config.name, 'blue'))}！目前有 {len(config.problem_sets)} 个题组。", "info",
                  __name__)
    print_and_log(f"初来乍到，输入 {bold(tint('help', 'blue'))} 获取使用帮助。", "info", __name__)

    def show_problem_set(idx: int):
        ps = get_problem_set(idx)
        if ps is None:
            return
        progress_str: str = f"{ps.get_solved_count()}/{len(ps.questions)}"
        print_and_log(f"题组: {ps.description} (已完成 {bold(progress_str)})", "info", __name__)
        for q in ps.questions:
            status = bold(tint("[✔]", "green")) if q.solved else bold(tint("[-]", "yellow"))
            print_and_log(f"{status} {q.id}. {q.description}", "info", __name__)
            
            if q.format is not None:
                print_and_log(f"{bold(tint('[.]', 'blue'))} 格式：{q.format}", "info", __name__)

    def answer_question(ps_idx: int, q_idx: int):
        ps = get_problem_set(ps_idx)
        if ps is None:
            return
        q = get_question(ps, q_idx)
        if q is None:
            return
        answer_logic(q)
        check_and_display_flag(ps)

    while True:
        try:
            cmd = input(f"{bold(tint('NekoChecker', 'blue'))} > ").strip()
        except KeyboardInterrupt:
            print()
            print_and_log("退出 NekoChecker...", "info", __name__)
            break

        if cmd == "list" or cmd == "ls":
            for i, ps in enumerate(problem_sets):
                print_and_log(f"{bold(f'[{i}]')} {ps.description} ({ps.get_solved_count()}/{len(ps.questions)})",
                              "info", __name__)
        elif cmd.startswith("show "):
            try:
                idx = int(cmd.split()[1])
                show_problem_set(idx)
            except Exception:
                print_and_log("用法: show <题组编号>", "error", __name__)
        elif cmd.startswith("answer "):
            try:
                parts = cmd.split()
                ps_idx = int(parts[1])
                q_idx = int(parts[2])
                answer_question(ps_idx, q_idx)
            except AnsweringBannedException as e:
                print_and_log(e.__str__(), "error", __name__)
            except Exception:
                print_and_log("用法: answer <题组编号> <题号>", "error", __name__)
        elif cmd == "save":
            save_config_to_file()
        elif cmd == "flag":
            for ps in problem_sets:
                check_and_display_flag(ps, True)
        elif cmd == "start":
            if len(problem_sets) == 0:
                print_and_log("没有可回答的问题！", "warn", __name__)

            for i in range(len(problem_sets)):
                start_answering(i)
        elif cmd.startswith("start "):
            try:
                idx = int(cmd.split()[1])
                start_answering(idx)
            except Exception:
                print_and_log("用法: start <题组编号>", "error", __name__)
        elif cmd == "help":
            display_help()
        elif cmd == "about":
            print_version()
        elif cmd == "exit":
            save_config_to_file()
            print_and_log("退出 NekoChecker...", "info", __name__)
            break
        elif cmd == "":
            continue
        else:
            print_and_log("未知指令。输入 help 查看可用命令。", "info", __name__)
    return 0

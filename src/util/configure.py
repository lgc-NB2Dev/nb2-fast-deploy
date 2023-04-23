import json
import os
import shutil
import subprocess
import traceback
from pathlib import Path
from typing import Callable, List, Optional, Tuple, TypeVar, Union

from utils import CLEAR_CMD, ENVIRON_PATHS, IS_WIN

PYPI_MIRROR_CUSTOM = "custom"
PYPI_MIRROR_NONE = "none"
PYPI_MIRROR_KEEP = "keep"
PYPI_MIRRORS: List[Tuple[str, str]] = [
    ("清华", "https://pypi.tuna.tsinghua.edu.cn/simple"),
    ("豆瓣", "http://pypi.douban.com/simple/"),
    ("阿里", "http://mirrors.aliyun.com/pypi/simple/"),
    ("自定义", PYPI_MIRROR_CUSTOM),
    ("不使用", PYPI_MIRROR_NONE),
    ("维持现有", PYPI_MIRROR_KEEP),
]

HEADER = "欢迎使用 NoneBot2 快速部署配置向导\n取消配置请按下 Ctrl+C\n"

# use_sudo = False
no_clear = False
pypi_mirror = PYPI_MIRROR_KEEP
python_path = "python3"

T = TypeVar("T")


def clear():
    if no_clear:
        return

    os.system(CLEAR_CMD)
    print(HEADER)


def system(cmd: List[str]) -> int:
    # if use_sudo:
    #     cmd = cmd.copy()
    #     cmd.insert(0, "sudo")

    formatted = " ".join([(f'"{x}"' if " " in x else x) for x in cmd])
    print(f"> {formatted}")

    res = subprocess.run(cmd).returncode
    if res:
        print(f"× 返回代码 {res}")

    return res


def systems(cmd: List[List[str]]) -> int:
    for c in cmd:
        res = system(c)
        if res:
            return res
    return 0


def check(prompt: str) -> bool:
    while True:
        ok = input(prompt).strip().lower()
        if ok == "y":
            return True
        if ok == "n":
            return False
        print("输入错误！请重新输入")


# def set_use_sudo():
#     ok = check('接下来的操作是否要使用 "sudo"? (Y/N) ')
#     if ok:
#         global use_sudo
#         use_sudo = True


def select(list: List[T]) -> T:
    while True:
        try:
            index = int(input(f"请输入 (1 - {len(list)}): ").strip())
            index -= 1
            return list[index]
        except (ValueError, IndexError):
            print("选择错误，请重新输入！")


def check_python_ver(path: str = python_path) -> bool:
    proc = subprocess.run(
        [path, "-c", "import sys; print(int(sys.version_info >= (3, 8)))"],
        encoding="u8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    ret = bool(proc.stdout.strip())

    if not ret:
        print("选择的 Python 版本小于 3.8，不支持 NoneBot2")

    return ret


def get_win_python_path() -> str:
    env_path = os.environ["PATH"].split(";")

    founded: List[str] = []
    for p in env_path:
        p = os.path.join(p, "python.exe")
        if os.path.exists(p):
            founded.append(p)
    founded = [x for x in set(founded) if "WindowsApps" not in x]
    founded.sort()

    if len(founded) == 1:
        return founded[0]

    print("你想要使用哪个 Python ？")
    for i, p in enumerate(founded):
        print(f"{i+1}. {p}")

    path = select(founded)
    if not check_python_ver(path):
        print("请重新选择 Python")
        return get_win_python_path()

    return path


def input_pypi_mirror() -> str:
    while True:
        url = input("请输入你要使用的镜像源地址：").strip()
        ok = check("请检查你输入的 URL 是否正确 (Y/N) ")
        if ok:
            return url


def get_pypi_mirror() -> Optional[str]:
    print("你想要使用哪个 pip 镜像源？")
    for i, (n, _) in enumerate(PYPI_MIRRORS):
        print(f"{i+1}. {n}")

    selected = select(PYPI_MIRRORS)[1]
    if selected == PYPI_MIRROR_CUSTOM:
        return input_pypi_mirror()
    if selected == PYPI_MIRROR_NONE:
        return None
    return selected


def configure_pip_mirror() -> int:
    if pypi_mirror == PYPI_MIRROR_KEEP:
        return 0

    # ignore err
    if pypi_mirror:
        return system(
            [python_path, "-m", "pip", "config", "set", "global.index-url", pypi_mirror]
        )

    system([python_path, "-m", "pip", "config", "unset", "global.index-url"])
    return 0


def install_pre_reqs() -> int:
    return system([python_path, "-m", "pip", "install", "pip", "pdm", "nb-cli", "-U"])


def del_path(*path: Union[Path, str]):
    pathes = (x if isinstance(x, Path) else Path(x) for x in path)
    for f in pathes:
        if f.exists():
            if f.is_dir():
                shutil.rmtree(f)
            else:
                f.unlink()


def configure_proj() -> int:
    # 如果有更好的方法欢迎提供
    venv_path = os.path.abspath(
        ".venv/Scripts/python.exe" if IS_WIN else ".venv/bin/python"
    )
    cmd = [
        ["pdm", "config", "-l", "python.use_venv", "True"],
        ["pdm", "config", "-l", "venv.in_project", "True"],
        ["pdm", "use", python_path],
        ["pdm", "venv", "create", "--force"],
        ["pdm", "use", venv_path],
        ["pdm", "install", "--no-self"],
    ]

    if not pypi_mirror:
        cmd.insert(0, ["pdm", "config", "-l", "-d", "pypi.url"])
    elif pypi_mirror != PYPI_MIRROR_KEEP:
        cmd.insert(0, ["pdm", "config", "-l", "pypi.url", pypi_mirror])

    for i in cmd:
        i.insert(0, "-m")
        i.insert(0, python_path)

    return systems(cmd)


def setup_gocq() -> int:
    ok = check("你想要在 NoneBot 中内置 GoCQ 启动器吗？(Y/N) ")

    if not ok:
        return 0

    return system(
        [python_path, "-m", "nb_cli", "plugin", "install", "nonebot-plugin-gocqhttp"]
    )


def find_line(lines: List[str], prefix: str) -> int:
    for i, x in enumerate(lines):
        if x.startswith(prefix):
            return i
    raise ValueError(f'Line Prefix "{prefix}" Not Found')


def get_input_lines(validator: Optional[Callable[[str], bool]] = None) -> List[str]:
    lines: List[str] = []

    while True:
        inp = input("> ").strip()

        if not inp:
            break

        if validator and (not validator(inp)):
            print("输入格式有误，请重新输入")
            continue

        lines.append(inp)

    return lines


def get_input(
    validator: Optional[Callable[[str], bool]] = None,
    allow_empty: bool = True,
) -> str:
    while True:
        inp = input("> ").strip()

        if (not inp) and allow_empty:
            break

        if validator and (not validator(inp)):
            print("输入格式有误，请重新输入")
            continue

        break

    return inp


def _configure_env():
    env_path = Path(".env.prod")
    env_file = env_path.read_text(encoding="u8").split("\n")

    superuser_line = find_line(env_file, "SUPERUSER")
    nickname_line = find_line(env_file, "NICKNAME")
    # command_prefix_line = find_line(env_file, "COMMAND_PREFIX")
    # host_line = find_line(env_file, "HOST")
    port_line = find_line(env_file, "PORT")

    print("现在让我们来配置一下 .env 的基础配置项")
    print("如果该项输入完毕，直接回车即可开始输入下一项")
    print("如果输错了想要重新配置，可以等到接下来的步骤完成后回来重新填写")

    print()
    print("请输入机器人的超级用户 QQ (SUPERUSER)")
    print("超级用户拥有对 Bot 的最高权限")
    superusers = get_input_lines(lambda x: 5 <= len(x) <= 10 and x.isdigit())
    env_file[superuser_line] = f"SUPERUSER={json.dumps(superusers)}"

    print()
    print("请输入机器人的昵称 (NICKNAME)")
    print("消息中包含机器人昵称可以代替艾特")
    nickname = get_input_lines()
    env_file[nickname_line] = f"NICKNAME={json.dumps(nickname, ensure_ascii=False)}"

    # print()
    # print("请输入机器人的命令起始字符 (COMMAND_PREFIX)")
    # print("一般只有 on_command 匹配规则适用")
    # print('如果有一个指令为 查询，当该配置项中有 "/" 时使用 "/查询" 才能够触发')
    # print('不填将使用默认值：""; "/"; "#"')

    # print()
    # print("请输入 NoneBot 监听的 IP 或 主机名 (HOST)")
    # print("如果要对公网开放，请改成 0.0.0.0")
    # print("不填将使用默认值：127.0.0.1")

    print()
    print("请输入 NoneBot 监听的端口 (PORT)")
    print("请保证该端口号与连接端配置相同 或与端口映射配置相关")
    print("使用内置 GoCQ 启动器的用户请忽略")
    print("不填将使用 .env 文件内的默认值")
    port = get_input(lambda x: x.isdigit() and 1 <= int(x) <= 65535)
    if port:
        env_file[port_line] = f"PORT={port}"

    print()
    print("请检查你刚才填写的配置，不正确请输入 N 返回重新填写")
    print()
    print(env_file[superuser_line])
    print(env_file[nickname_line])
    print(env_file[port_line])
    print()
    ok = check("这些配置是否正确? (Y/N) ")
    if not ok:
        print("请重新配置")
        print()
        _configure_env()
        return

    env_path.write_text("\n".join(env_file), encoding="u8")


def configure_env() -> bool:
    try:
        _configure_env()
    except Exception:
        traceback.print_exc()
        return False
    return True


def check_configured():
    if any(x.exists() for x in ENVIRON_PATHS):
        clear()
        print("虚拟环境文件夹 或 环境配置 已存在")
        print("看起来你已经配置过 NoneBot 了")
        print()

        ok = check("是否要删除现有环境并重新配置？\n如果之前配置失败请按 Y 继续 (Y/N) ")
        if not ok:
            print("取消配置")
            return True

    del_path(*ENVIRON_PATHS)
    return None


def main():
    if check_configured():
        return

    if not IS_WIN:
        clear()
        if not check_python_ver():
            return

        # set_use_sudo()

    if IS_WIN:
        clear()
        global python_path
        python_path = get_win_python_path()

    clear()
    global pypi_mirror
    pypi_mirror = get_pypi_mirror()

    if configure_pip_mirror():
        return print("设置 pip 镜像源失败！")

    clear()
    print("安装必要依赖中……")
    if install_pre_reqs():
        return print("安装必要依赖失败！")

    clear()
    print("配置项目中，请稍候……")
    if configure_proj():
        return print("配置项目失败！")

    clear()
    if setup_gocq():
        return print("安装 GoCQ 启动器失败！")

    clear()
    if not configure_env():
        return print("配置 .env 文件失败！")

    clear()
    print(
        "恭喜！你的 NoneBot2 已配置完毕\n"
        "\n"
        "接下来，你可以：\n"
        "- 打开 .env.prod 文件，编辑 NoneBot2 的配置\n"
        "- 进入虚拟环境，输入 nb 命令安装你需要的插件、适配器等\n"
        "想启动你的机器人，运行 #启动.bat 即可~\n"
        "\n"
        "本包内置了一个测试部署用的插件，\n"
        "设置好 SUPERUSER 后，试试向机器人发送命令 ping，\n"
        "看看你的机器人会不会回应吧！\n"
        "\n"
        "如果有 NoneBot2 的相关问题想提问，欢迎加入下面的群\n"
        "我的个人交流群：1105946125\n"
        "NoneBot 官方群：768887710"
        "\n"
        "祝使用愉快 ♡"
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception:
        traceback.print_exc()
    input("\n\n请按回车键退出")

import os
import platform
import traceback
from typing import Iterable, List, Optional, Tuple, TypeVar, Union


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

HEADER = "欢迎使用 NoneBot2 一键包配置向导\n按下 Ctrl+C 退出\n"

is_win = "Windows" in platform.system()
clear_cmd = "cls" if is_win else "clear"
use_sudo = False
no_clear = False
pypi_mirror = PYPI_MIRROR_KEEP
python_path = "python3"

T = TypeVar("T")


def clear():
    if no_clear:
        return

    os.system(clear_cmd)
    print(HEADER)


def system(cmd: Union[str, Iterable[str]]) -> int:
    if isinstance(cmd, str):
        cmd = [cmd]

    if use_sudo:
        cmd = [f"sudo {x}" for x in cmd]

    for c in cmd:
        print(f"> {c}")
        res = os.system(c)
        if res:
            print(f"! 返回代码 {res} ❌")
            return res

    return 0


def set_use_sudo():
    ok = input('接下来的操作是否要使用 "sudo"? (Y/N) ').strip().lower()
    if ok == "y":
        global use_sudo
        use_sudo = True


def select(list: List[T]) -> T:
    while True:
        try:
            index = int(input(f"请输入 (1 - {len(list)}): ").strip())
            index -= 1
            return list[index]
        except (ValueError, IndexError):
            print("选择错误，请重新输入！")


def get_win_python_path() -> str:
    env_path = os.environ["PATH"].split(";")

    founded = []
    for p in env_path:
        p = os.path.join(p, "python.exe")
        if os.path.exists(p):
            founded.append(p)
    founded = list(set(founded))
    founded.sort()

    if len(founded) == 1:
        return founded[0]

    print("你想要使用哪个 Python ？")
    for i, p in enumerate(founded):
        print(f"{i+1}. {p}")
    return select(founded)


def input_pypi_mirror() -> str:
    while True:
        url = input("请输入你要使用的镜像源地址：").strip()
        ok = input("请检查你输入的 URL 是否正确 (Y/N) ").strip().lower()
        if ok == "y":
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

    if pypi_mirror:
        return system(
            f'{python_path} -m pip config set global.index-url "{pypi_mirror}"'
        )

    system(f"{python_path} -m pip config unset global.index-url")
    return 0


def install_pre_reqs() -> int:
    return system(f"{python_path} -m pip install pdm nb-cli -U")


def configure_proj() -> int:
    # 如果有更好的方法欢迎提供
    venv_path = os.path.abspath(
        ".venv/Scripts/python.exe" if is_win else ".venv/bin/python"
    )
    cmd = [
        "pdm config -l python.use_venv True",
        "pdm config -l venv.in_project True",
        f'pdm use "{python_path}"',
        "pdm venv create --force",
        f'pdm use "{venv_path}"',
        "pdm install --no-self",
    ]

    if not pypi_mirror:
        cmd.insert(0, "pdm config -l -d pypi.url")
    elif pypi_mirror != PYPI_MIRROR_KEEP:
        cmd.insert(0, f"pdm config -l pypi.url {pypi_mirror}")

    cmd = [f"{python_path} -m {x}" for x in cmd]
    return system(cmd)


def setup_gocq() -> int:
    ok = input("你想要在 NoneBot 中内置 GoCQ 启动器吗？(Y/N) ").strip().lower()

    if ok != "y":
        return 0

    return system(f"{python_path} -m pdm run nb plugin install nonebot-plugin-gocqhttp")


def main():
    if not is_win:
        clear()
        set_use_sudo()

    if is_win:
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
    print(
        "恭喜！你的 NoneBot2 已配置完毕 🎉\n"
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
        "祝使用愉快 ❤️"
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except:  # noqa: E722
        traceback.print_exc()
    input("\n\n请按回车键退出")

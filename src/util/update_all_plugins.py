# pyright: reportGeneralTypeIssues=false

import subprocess
import traceback
from pathlib import Path

from tomlkit import parse


def update(name: str) -> bool:
    proc = subprocess.run(
        ["pip", "install", name, "-U"],
        capture_output=True,
        encoding="u8",
    )

    out = proc.stdout
    ok = proc.returncode == 0

    ver = None
    if "Successfully installed " in out:
        index = out.rfind(name) + len(name) + 1
        ver = out[index : out.find(" ", index)].strip()

    if ok:
        if not ver:
            print(f"插件 {name} 已经是最新版本了")
        else:
            print(f"插件 {name} 已更新到版本 {ver}")
    else:
        print(f"更新插件 {name} 失败！！")
        print(proc.stderr)

    return ok


def main():
    pyproject = parse((Path.cwd() / "pyproject.toml").read_text(encoding="u8"))
    nb_config = pyproject["tool"]["nonebot"]

    preload_plugins = set(nb_config.get("preload_plugins", []))
    plugins = set(nb_config["plugins"])
    plugins |= preload_plugins

    if not plugins:
        print("你还没有安装过商店插件，没有需要更新的插件")
        return

    print(
        "一键更新所有插件有可能会导致插件间不兼容报错\n"
        "请问您是否真的要继续？\n"
        "\n"
        "如果你真的要继续，请按下回车开始操作\n"
        "如果你不想继续，请按下 Ctrl+C 或者关闭窗口"
    )
    input()

    total_num = len(plugins)
    print(f"已发现 {total_num} 个插件，准备更新")
    print()

    success = []
    fail = []
    for i, pl in enumerate(plugins):
        pl = pl.replace("_", "-")
        print(f"正在更新插件 {pl} ({i + 1}/{total_num})")

        if update(pl):
            success.append(pl)
        else:
            fail.append(pl)
        print()

    print(f"更新完毕，成功 {len(success)} 个，失败 {len(fail)} 个")
    if fail:
        fail_list = "\n".join([f"- {x}" for x in fail])
        print(f"更新失败的插件列表：\n{fail_list}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception:
        traceback.print_exc()
    input("\n\n请按回车键退出")

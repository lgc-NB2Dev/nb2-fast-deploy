from pathlib import Path
import subprocess
from typing import List

from tomlkit import parse


def update(name: str) -> bool:
    print(f"正在更新插件 {name}")
    proc = subprocess.run(
        ["pip", "install", name, "-U"],
        shell=True,
        capture_output=True,
        encoding="u8",
    )

    ok = proc.returncode == 0
    print(f"更新插件 {name} {'成功' if ok else '失败！！'}")

    if not ok:
        print(proc.stderr)

    return ok


def main():
    pyproject = parse((Path.cwd() / "pyproject.toml").read_text(encoding="u8"))
    plugins: List[str] = pyproject["tool"]["nonebot"]["plugins"]  # type: ignore

    if not plugins:
        print("你还没有安装过商店插件，没有需要更新的插件")
        return

    print(f"已发现 {len(plugins)} 个插件，准备更新")
    print()

    success = []
    fail = []
    for pl in plugins:
        pl = pl.replace("_", "-")
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
    main()

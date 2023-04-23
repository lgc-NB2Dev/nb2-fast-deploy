from contextlib import suppress
import subprocess

from utils import ENVIRON_PATHS


def main():
    if not all(x.exists() for x in ENVIRON_PATHS):
        print("看起来你还没有配置过 NoneBot")
        print("请先运行 #配置向导.bat 来配置环境")
        input()
        return

    while True:
        print("启动 NoneBot ...\n")

        subprocess.run(["nb", "run"])

        print("\nNoneBot 已停止运行\n如果需要重新运行，请按下回车")
        input()


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        main()

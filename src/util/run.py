import os
import subprocess

from const import TIMEOUT_CMD


def main():
    while True:
        print("启动 NoneBot ...\n")

        proc = subprocess.run(["nb", "run"])

        if not proc.returncode:
            print("\nNoneBot 已停止运行\n如果需要重新运行，请按下回车")
            input()

        else:
            print(
                "\n"
                "NoneBot 意外停止运行！\n"
                "10 秒后 NoneBot 将重新运行\n"
                "如果你不想重启，请手动关掉窗口\n"
                "如果你想立即重启，请按任意键"
            )
            os.system(TIMEOUT_CMD)


if __name__ == "__main__":
    main()

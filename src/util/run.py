import os
import platform
import subprocess


is_win = "Windows" in platform.system()
timeout_cmd = "timeout /t 10" if is_win else "read -t 10"


def main():
    while True:
        print("启动 NoneBot ...\n")

        proc = subprocess.run(["pdm", "run", "nb", "run"])

        if not proc.returncode:
            return

        print(
            "\n"
            "NoneBot 意外停止运行！\n"
            "10 秒后 NoneBot 将重新运行\n"
            "如果你不想重启，请手动关掉窗口\n"
            "如果你想立即重启，请按任意键"
        )
        os.system(timeout_cmd)


if __name__ == "__main__":
    main()

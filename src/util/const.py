import platform

IS_WIN = "Windows" in platform.system()
CLEAR_CMD = "cls" if IS_WIN else "clear"
TIMEOUT_CMD = "timeout /t 10" if IS_WIN else "read -t 10"

import platform
from pathlib import Path

IS_WIN = "Windows" in platform.system()
CLEAR_CMD = "cls" if IS_WIN else "clear"

ENVIRON_PATHS = Path(".venv"), Path(".pdm-python"), Path("pdm.toml"), Path("pdm.lock")

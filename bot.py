#!/usr/bin/env python3
# pyright: reportGeneralTypeIssues=false

import importlib
from pathlib import Path

import nonebot
from nonebot.log import default_format, logger
from tomlkit import parse


nonebot.init()
driver = nonebot.get_driver()


# region 自定义 Logger
# 自动将 bot 报错记录到文件
logger.add(
    "logs/error.log",
    rotation="1 MB",
    diagnose=True,
    level="ERROR",
    format=default_format,
    compression="zip",
)
# endregion


# region 读取项目信息
pyproject = parse((Path(__file__).parent / "pyproject.toml").read_text(encoding="u8"))

adapters = pyproject["tool"]["nonebot"]["adapters"]

preload_plugins = set(pyproject["tool"]["nonebot"]["preload_plugins"])

plugins = set(pyproject["tool"]["nonebot"]["plugins"])
plugins.difference_update(preload_plugins)

plugin_dirs = set(pyproject["tool"]["nonebot"]["plugin_dirs"])
# endregion


# region 加载适配器 & 插件
for ad in adapters:
    driver.register_adapter(
        importlib.import_module(ad["module_name"]).Adapter,
    )

for pl in preload_plugins:
    nonebot.load_plugin(pl)

nonebot.load_all_plugins(plugins, plugin_dirs)
# endregion


nonebot.run()

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
ERROR_LOG = True

if ERROR_LOG:
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
try:
    pyproject = parse(
        (Path(__file__).parent / "pyproject.toml").read_text(encoding="u8")
    )
    nb_config = pyproject["tool"]["nonebot"]

    adapters = nb_config["adapters"]

    preload_plugins = set(nb_config.get("preload_plugins", []))

    plugins = set(nb_config["plugins"])
    plugins.difference_update(preload_plugins)

    plugin_dirs = set(nb_config["plugin_dirs"])

except Exception:
    logger.exception("读取 NoneBot 项目信息失败")
    exit(1)
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

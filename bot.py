#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import nonebot
from tomlkit import parse

# 自定义 Logger
# 这里示范添加一个每日 0 点重新生成的 error.log 日志
#
# from nonebot.log import logger, default_format
#
# logger.add(
#     "error.log",
#     rotation="00:00",
#     diagnose=False,
#     level="ERROR",
#     format=default_format
# )


# 可以在init函数中添加 .env 配置，优先级高于 .env
nonebot.init(
    # var1=True
)


pyproject = parse((Path(__file__).parent / "pyproject.toml").read_text(encoding="u8"))

# 根据 pyproject.toml 注册 Adapter
import importlib

driver = nonebot.get_driver()
for adapter in pyproject["tool"]["nonebot"]["adapters"]:  # type: ignore
    driver.register_adapter(importlib.import_module(adapter["module_name"]).Adapter)


# 在加载其他插件之前加载前置插件
# 详见 pyproject.toml [tool.nonebot-one-click] 项的注释
for p in pyproject["tool"]["nonebot"]["oneclick"]["preload_plugins"]:  # type: ignore
    nonebot.load_plugin(p)


# 如果你不知道你在干什么，请不要动此文件
# 你可以 使用nb脚手架 或者 修改`pyproject.toml` 来加载插件
# 下面的几行代码会自动加载 pyproject.toml [tool.nonebot] 项里的插件和插件目录
nonebot.load_all_plugins(
    set(pyproject["tool"]["nonebot"]["plugins"]),  # type: ignore
    set(pyproject["tool"]["nonebot"]["plugin_dirs"]),  # type: ignore
)


# 在已加载配置的基础上修改配置
#
# config = driver.config
# config.var1 = False


if __name__ == "__main__":
    nonebot.run()

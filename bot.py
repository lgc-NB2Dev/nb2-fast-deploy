#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot

# 自定义 Logger
#
# from nonebot.log import logger, default_format
#
# 添加一个每日0点重新生成的error.log日志
# logger.add(
#     "error.log", rotation="00:00", diagnose=False, level="ERROR", format=default_format
# )


# 可以在init函数中添加.env环境变量，优先级高于.env
nonebot.init(
    # var1=True
)

driver = nonebot.get_driver()

### 注册 Adapter ###
# 有需要请自行取消注释

## OneBot V11
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

driver.register_adapter(ONEBOT_V11Adapter)

## OneBot V12
# from nonebot.adapters.onebot.v12 import Adapter as ONEBOT_V12Adapter
# driver.register_adapter(ONEBOT_V12Adapter)

## 钉钉
# from nonebot.adapters.ding import Adapter as DingAdapter
# driver.register_adapter(DingAdapter)

## 飞书
# from nonebot.adapters.feishu import Adapter as FeiShuAdapter
# driver.register_adapter(FeiShuAdapter)

## Telegram
# from nonebot.adapters.telegram import Adapter as TGAdapter
# driver.register_adapter(TGAdapter)

## QQ 官方频道 Bot
# from nonebot.adapters.qqguild import Adapter as QQGuildAdapter
# driver.register_adapter(QQGuildAdapter)

## 开黑啦（不支持2.0.0b5）
# from nonebot.adapters.kaiheila import Adapter as KaiHeiLaAdapter
# driver.register_adapter(KaiHeiLaAdapter)

## MiraiApiHttp 2.x
# from nonebot.adapters.mirai2 import Adapter as MiraiAdapter
# driver.register_adapter(MiraiAdapter)

## 控制台
# from nonebot.adapters.console import Adapter as ConsoleAdapter
# driver.register_adapter(ConsoleAdapter)

## Github
# from nonebot.adapters.github import Adapter as GithubAdapter
# driver.register_adapter(GithubAdapter)

## NtChat 微信（不支持2.0.0b5）
# from nonebot.adapters.ntchat import Adapter as NTChatAdapter
# driver.register_adapter(NTChatAdapter)


# 如果出现插件require报错，请在这里加上load_plugin代码使被require的插件先加载
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugin("nonebot_plugin_htmlrender")
nonebot.load_plugin("nonebot_plugin_imageutils")
nonebot.load_plugin("nonebot_plugin_guild_patch")


# 如果你不知道你在干什么，请不要动此文件
# 你可以 使用nb脚手架 或者 修改`pyproject.toml` 来加载插件
# 下面的一行代码会自动加载 pyproject.toml [tool.nonebot] 项里的插件和插件目录
nonebot.load_from_toml("pyproject.toml")


# 在已加载配置的基础上修改配置
#
# config = driver.config
# config.var1 = False


if __name__ == "__main__":
    nonebot.run()

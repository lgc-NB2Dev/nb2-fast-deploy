"""超级用户 Ping 指令回复，可以用来检查 Bot 部署状态"""

from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.internal.adapter import MessageEvent

h_ping = on_command("ping", aliases={"Ping", "PING"}, permission=SUPERUSER)


@h_ping.handle()
async def _(matcher: Matcher, _: MessageEvent):
    await matcher.finish("Pong~")

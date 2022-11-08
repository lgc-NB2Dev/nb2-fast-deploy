@echo off
chcp 65001

:start
echo 启动 NoneBot……
py -3.10 -m poetry run nb run

echo.
echo NoneBot已停止运行！
echo 10 秒后NoneBot将重新运行
echo 如果你不想重启，请手动关掉窗口
echo 如果你想立即重启，请按任意键

timeout /t 10
goto start
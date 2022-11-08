@echo off
chcp 65001

goto finish

py -3.10 -V > nul
if not %errorlevel%==0 (
    echo 你还没有安装 Python 3.10 或你的 Python 3.10 不在 PATH 中，请检查安装
    goto end
)

set needset=0
choice /m "是否想要使用清华 pypi 镜像源？（Y 同意，N 拒绝）"
if %errorlevel%==1 (
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    echo.
    echo 请手动查看 pyproject.toml 文件的第 59 行是否被注释
) else (
    pip config unset global.index-url
    echo.
    echo 请手动注释 pyproject.toml 文件的第 59 行
)

echo.
echo 默认会安装 OneBot 适配器与适用于反向 ws 的驱动器
echo 可以编辑 pyproject.toml 文件来安装其他的适配器和驱动器
echo 准备好了吗？按下回车继续配置与安装依赖~
pause > nul

echo.
echo 安装Poetry，请稍等
py -3.10 -m pip install poetry -U
if not %errorlevel%==0 (
    echo 安装 Poetry 失败！
    goto end
)

echo.
echo 安装项目依赖，请稍等
py -3.10 -m poetry install
if not %errorlevel%==0 (
    echo 安装项目依赖失败！
    goto end
)

echo.
echo 更新项目依赖，请稍等
py -3.10 -m poetry update
if not %errorlevel%==0 (
    echo 更新项目依赖失败！
    goto end
)

:finish
echo.
echo 恭喜！执行成功~ 接下来你可以：
echo.
echo - 打开 .env 文件来编辑一些配置项，比如超级用户与 Bot 昵称等
echo - 打开 .env.prod 文件编辑 NoneBot 监听的 IP 与端口
echo - 如果使用了 ForwardDriver，请注释 bot.py 的第 23 行
echo - 如果安装了其他适配器，请取消 bot.py 对应注释
echo.
echo 完成上面这些操作后，以后只需要打开 #启动.bat 就可以启动 NoneBot 啦！
echo 安装插件等操作可以看 README.md 文档！
echo.
echo 本整合内包含了一个测试部署状态用的 ping 插件
echo 设置好超级用户配置之后，启动 GoCQ 与 NoneBot
echo 试试向 Bot 发送指令 ping ，如果 Bot 回复了就代表配置没有问题啦~
echo 想删掉这个插件的话，删除 src/plugins/ping.py 就可以了
echo.
echo 祝使用愉快~
echo.

:end
echo 按任意键关闭
pause > nul
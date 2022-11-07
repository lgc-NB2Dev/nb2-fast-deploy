# NoneBot2 Windows 一键部署

## 要求

- Python `3.10.x`（安装时记得勾选 `Add Python 3.10 to PATH` !!!）

## 简单教程

1. 克隆本仓库 / 打包下载本仓库
2. 如果只需要使用 `OneBot V11` 适配器，请直接运行 `#配置环境.bat`  
   否则请看完 [这个](#切换连接方式--使用其他适配器--使用其他驱动器) 再运行
3. 依你喜好修改 `.env` 文件 `常用配置项` 里的 `SUPERUSERS` 与 `NICKNAME` 项
4. 依你喜好修改 `.env.prod` 文件 里的 IP 与端口配置
5. 设置 GoCQ 反向 ws universal URL 为 `ws://127.0.0.1:8080/onebot/v11/ws/`  
   其中，`127.0.0.1` 和 `8080` 分别对应 `.env.prod` 配置的 HOST 和 PORT。
6. 运行 `#启动.bat`
7. 用 `SUPERUSERS` 里的帐号向 Bot 发送 `ping`，Bot 如果回复 `Pong~` 就代表部署成功  
   如果你不想要这个功能，请删除 `src/plugins/ping.py` 文件
8. 之后每次启动运行 `#启动.bat` 即可，直接关掉窗口即可关闭 NoneBot

## 进阶使用

### 切换连接方式 / 使用其他适配器 / 使用其他驱动器

我已经在 `pyproject.toml`、`.env`、`bot.py` 文件里写好了注释，修改好后再按照简单教程做即可

### 安装 / 卸载插件

#### 安装商店插件

1. 运行 `#进入虚拟环境.bat`
2. 粘贴从插件市场里复制下来的 `nb plugin install 插件名` 格式的指令，按下回车
3. 根据插件文档在 `.env` 文件里纂写配置项
4. 如果 NoneBot 正在运行，关掉 NoneBot 后重新开启即可

#### 卸载商店插件

1. 运行 `#进入虚拟环境.bat`
2. 输入 `nb plugin uninstall 插件名`，插件名支持模糊检索
3. 如果卸载报错 `拒绝访问` ，请关掉 NoneBot 后重试
4. 如果 NoneBot 正在运行，关掉 NoneBot 后重新开启即可

#### 安装第三方插件

1. 在 `src/plugins` 文件夹放入第三方插件
2. 运行 `#进入虚拟环境.bat`
3. 安装插件依赖
4. 如果 NoneBot 正在运行，关掉 NoneBot 后重新开启即可

#### 卸载第三方插件

1. 从 `src/plugins` 文件夹删除对应插件
2. 如果 NoneBot 正在运行，关掉 NoneBot 后重新开启即可

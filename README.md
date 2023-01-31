# NoneBot2 Windows 一键部署

## 要求

- Python `3.10.x`（安装时记得勾选 `Add Python 3.10 to PATH` !!!）

## 如何使用

### [点这里 -----> \[视频介绍\] <----- 点这里](https://www.bilibili.com/video/BV11P411F7XM/)

运行 `#配置环境.bat` ，按照指引即可

## 进阶使用

### 切换连接方式 / 使用其他适配器 / 使用其他驱动器

我已经在 `pyproject.toml`、`.env`、`bot.py` 文件里写好了注释，按照对应文档稍微编辑一下即可

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

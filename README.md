<!-- markdownlint-disable MD031 -->

# NoneBot2 快速部署包

[![wakatime](https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/11088243-4834-4b8d-91c3-5b765bd053d4.svg)](https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/11088243-4834-4b8d-91c3-5b765bd053d4)

## 要求

- 默认 Python `>=3.8` ( `python3 -V` )

## 如何使用

1. 克隆存储库到本地（ `nb2` 可以换成你喜欢的文件夹名字）
   ```bash
   git clone --depth=1 -b linux https://github.com/lgc-NB2Dev/nb2-fast-deploy nb2
   cd nb2
   ```
2. 赋予快速部署包内脚本可执行权限
   ```bash
   chmod 777 ./_*
   ```
3. 运行配置环境脚本
   ```bash
   ./_configure
   ```

### 部署包脚本

- 启动 `NoneBot`
  ```bash
  ./_run
  ```
- 更新全部插件
  ```bash
  ./_upd-plugin
  ```
- 打印虚拟环境进入方式
  ```bash
  ./_venv
  ```
- 在虚拟环境中运行命令
  ```bash
  pdm run <命令>
  ```

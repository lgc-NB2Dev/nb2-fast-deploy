@echo off

chcp 65001

:: 设置镜像源，不想使用镜像源的请将下面一行前面加 :: 注释掉，pyproject.toml 文件那里也有镜像源设置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

echo 安装Poetry，请稍等
py -3.10 -m pip install poetry -U

echo 安装项目依赖，请稍等
py -3.10 -m poetry install

pause
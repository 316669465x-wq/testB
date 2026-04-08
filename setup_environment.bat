@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo   AI Programming Tool - 环境安装脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] 检测 Python 版本...
for /f "tokens=2" %%i in ('python --version') do set pyver=%%i
echo       当前版本：%pyver%

REM 检查虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo [2/4] 发现已有虚拟环境，跳过创建
) else (
    echo [2/4] 正在创建虚拟环境 (venv)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [错误] 创建虚拟环境失败，请确保安装了 python3-venv 模块
        pause
        exit /b 1
    )
    echo       虚拟环境创建成功
)

REM 激活虚拟环境
echo [3/4] 激活虚拟环境...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [错误] 激活虚拟环境失败
    pause
    exit /b 1
)

REM 升级 pip
echo       正在升级 pip...
python -m pip install --upgrade pip --quiet

REM 安装依赖
echo [4/4] 正在安装项目依赖 (requirements.txt)...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [警告] 部分依赖安装失败，请检查网络连接或 requirements.txt
    ) else (
        echo       依赖安装完成
    )
) else (
    echo [警告] 未找到 requirements.txt，跳过依赖安装
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 下一步操作：
echo 1. 激活环境：venv\Scripts\activate
echo 2. 运行程序：python ai_programming_tool.py
echo.
pause

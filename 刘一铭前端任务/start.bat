@echo off
chcp 65001 > nul
echo 🚀 DiffProtect Pro - 前端启动脚本
echo ==================================
echo.

REM 检查 Python 是否安装
where python >nul 2>nul
if %errorlevel% == 0 (
    echo ✅ 检测到 Python
    echo 📡 启动本地服务器: http://localhost:8080
    echo 💡 按 Ctrl+C 停止服务器
    echo.
    python -m http.server 8080
) else (
    where python3 >nul 2>nul
    if %errorlevel% == 0 (
        echo ✅ 检测到 Python3
        echo 📡 启动本地服务器: http://localhost:8080
        echo 💡 按 Ctrl+C 停止服务器
        echo.
        python3 -m http.server 8080
    ) else (
        echo ❌ 未检测到 Python
        echo.
        echo 请选择以下方式之一：
        echo 1. 安装 Python: https://www.python.org/downloads/
        echo 2. 使用 Node.js: npx http-server -p 8080
        echo 3. 直接用浏览器打开 index.html
        echo.
        pause
    )
)

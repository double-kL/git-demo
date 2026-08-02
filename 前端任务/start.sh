#!/bin/bash

# DiffProtect Pro 前端快速启动脚本

echo "🚀 DiffProtect Pro - 前端启动脚本"
echo "=================================="
echo ""

# 检查是否安装了 Python
if command -v python3 &> /dev/null; then
    echo "✅ 检测到 Python3"
    echo "📡 启动本地服务器: http://localhost:8080"
    echo "💡 按 Ctrl+C 停止服务器"
    echo ""
    python3 -m http.server 8080
elif command -v python &> /dev/null; then
    echo "✅ 检测到 Python"
    echo "📡 启动本地服务器: http://localhost:8080"
    echo "💡 按 Ctrl+C 停止服务器"
    echo ""
    python -m http.server 8080
else
    echo "❌ 未检测到 Python"
    echo ""
    echo "请选择以下方式之一："
    echo "1. 安装 Python: https://www.python.org/downloads/"
    echo "2. 使用 Node.js: npx http-server -p 8080"
    echo "3. 直接用浏览器打开 index.html"
    echo ""
fi

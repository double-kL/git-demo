#!/bin/bash

echo "========================================"
echo "  DiffProtect Pro - Mock后端启动脚本"
echo "========================================"
echo ""

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 未检测到 Node.js"
    echo ""
    echo "请先安装 Node.js: https://nodejs.org/"
    echo ""
    exit 1
fi

echo "✅ 检测到 Node.js"
echo ""

# 检查是否已安装依赖
if [ ! -d "node_modules" ]; then
    echo "📦 首次运行，正在安装依赖..."
    echo ""
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
    echo ""
fi

echo "🚀 启动 Mock 后端服务器..."
echo ""
node mock-server.js

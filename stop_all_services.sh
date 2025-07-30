#!/bin/bash

# 停止所有服务的脚本
echo "🛑 停止冥想助手项目的所有服务..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 创建logs目录（如果不存在）
mkdir -p logs

# 停止 my_project 服务
echo -e "${BLUE}停止 my_project 服务...${NC}"
if [ -f "logs/my_project.pid" ]; then
    MY_PROJECT_PID=$(cat logs/my_project.pid)
    if kill -0 $MY_PROJECT_PID 2>/dev/null; then
        kill $MY_PROJECT_PID
        echo -e "${GREEN}✅ my_project 服务已停止 (PID: $MY_PROJECT_PID)${NC}"
    else
        echo -e "${YELLOW}⚠️  my_project 服务未运行${NC}"
    fi
    rm -f logs/my_project.pid
else
    echo -e "${YELLOW}⚠️  未找到 my_project PID 文件${NC}"
fi

# 停止 Spring Boot 后端服务
echo -e "${BLUE}停止 Spring Boot 后端服务...${NC}"
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo -e "${GREEN}✅ 后端服务已停止 (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠️  后端服务未运行${NC}"
    fi
    rm -f logs/backend.pid
else
    echo -e "${YELLOW}⚠️  未找到后端 PID 文件${NC}"
fi

# 停止前端代理服务器
echo -e "${BLUE}停止前端代理服务器...${NC}"
if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo -e "${GREEN}✅ 前端代理服务器已停止 (PID: $FRONTEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠️  前端代理服务器未运行${NC}"
    fi
    rm -f logs/frontend.pid
else
    echo -e "${YELLOW}⚠️  未找到前端 PID 文件${NC}"
fi

# 额外清理：杀死可能遗留的进程
echo -e "${BLUE}清理可能遗留的进程...${NC}"

# 清理可能的Flask进程
pkill -f "python3 service.py" 2>/dev/null && echo -e "${GREEN}✅ 清理了遗留的Flask进程${NC}"

# 清理可能的Spring Boot进程
pkill -f "spring-boot:run" 2>/dev/null && echo -e "${GREEN}✅ 清理了遗留的Spring Boot进程${NC}"

# 清理可能的代理服务器进程
pkill -f "proxy_server.py" 2>/dev/null && echo -e "${GREEN}✅ 清理了遗留的代理服务器进程${NC}"

echo -e "${GREEN}🎉 所有服务已停止！${NC}"

# 检查端口是否仍被占用
echo -e "${BLUE}检查端口状态...${NC}"
if lsof -i :8008 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  端口8008仍被占用${NC}"
else
    echo -e "${GREEN}✅ 端口8008已释放${NC}"
fi

if lsof -i :8081 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  端口8081仍被占用${NC}"
else
    echo -e "${GREEN}✅ 端口8081已释放${NC}"
fi

if lsof -i :8080 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  端口8080仍被占用${NC}"
else
    echo -e "${GREEN}✅ 端口8080已释放${NC}"
fi

echo -e "${BLUE}停止完成！${NC}" 
#!/bin/bash

# 登录演示项目停止脚本
echo "🛑 正在停止登录演示项目..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 停止后端服务
echo -e "${BLUE}停止后端服务...${NC}"
if [ -f backend.pid ]; then
    BACKEND_PID=$(cat backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo -e "${GREEN}✅ 后端服务已停止 (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠️  后端服务已经停止${NC}"
    fi
    rm -f backend.pid
else
    echo -e "${YELLOW}⚠️  未找到后端服务PID文件${NC}"
fi

# 停止前端服务
echo -e "${BLUE}停止前端代理服务器...${NC}"
if [ -f frontend.pid ]; then
    FRONTEND_PID=$(cat frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo -e "${GREEN}✅ 前端代理服务器已停止 (PID: $FRONTEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠️  前端代理服务器已经停止${NC}"
    fi
    rm -f frontend.pid
else
    echo -e "${YELLOW}⚠️  未找到前端代理服务器PID文件${NC}"
fi

# 清理可能残留的进程
echo -e "${BLUE}清理残留进程...${NC}"
pkill -f "spring-boot:run" 2>/dev/null
pkill -f "proxy_server.py" 2>/dev/null
pkill -f "vue-cli-service serve" 2>/dev/null

# 检查端口是否被占用
echo -e "${BLUE}检查端口状态...${NC}"
if lsof -i :8080 >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  端口8080仍被占用${NC}"
    echo "如需强制停止，请运行: lsof -ti:8080 | xargs kill -9"
fi

if lsof -i :8081 >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  端口8081仍被占用${NC}"
    echo "如需强制停止，请运行: lsof -ti:8081 | xargs kill -9"
fi

echo -e "${GREEN}🎉 项目停止完成！${NC}"
echo ""
echo -e "${BLUE}日志文件已保留:${NC}"
echo -e "  后端日志: ${GREEN}backend.log${NC}"
echo -e "  前端日志: ${GREEN}frontend.log${NC} (代理服务器日志)"
echo ""
echo -e "${YELLOW}如需重新启动项目，请运行: ${GREEN}./run_project.sh${NC}" 
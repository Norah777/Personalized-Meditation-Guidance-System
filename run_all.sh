#!/bin/bash

# =============================================================================
# Meditation Assistant - 统一启动脚本
# =============================================================================

echo "🚀 启动冥想助手项目..."
echo "=" * 60

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 项目根目录: $SCRIPT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查必要的命令
echo -e "\n${BLUE}📋 检查依赖...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

if ! command -v java &> /dev/null; then
    echo -e "${RED}❌ Java 未安装${NC}"
    exit 1
fi

if ! command -v mvn &> /dev/null && ! [ -f "$SCRIPT_DIR/logindemo/springboot-login-demo-master/mvnw" ]; then
    echo -e "${RED}❌ Maven 未安装且项目中没有mvnw${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 依赖检查通过${NC}"

# 创建日志目录
mkdir -p "$SCRIPT_DIR/logs"

# 函数：启动AI服务
start_ai_service() {
    echo -e "\n${BLUE}🤖 启动AI服务...${NC}"
    cd "$SCRIPT_DIR/my_project"
    
    # 检查配置文件
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠️  .env文件不存在，请确保已配置API密钥${NC}"
    fi
    
    # 激活虚拟环境并设置PYTHONPATH
    if [ -d "venv" ]; then
        source venv/bin/activate
        export PYTHONPATH=.
    fi
    
    # 启动服务
    python3 service.py > "$SCRIPT_DIR/logs/ai_service.log" 2>&1 &
    AI_PID=$!
    echo $AI_PID > "$SCRIPT_DIR/logs/ai_service.pid"
    echo -e "${GREEN}✅ AI服务已启动 (PID: $AI_PID)${NC}"
    echo -e "   📄 日志文件: logs/ai_service.log"
    echo -e "   🌐 服务地址: http://localhost:8008"
}

# 函数：启动Spring Boot后端
start_spring_boot() {
    echo -e "\n${BLUE}☕ 启动Spring Boot后端...${NC}"
    cd "$SCRIPT_DIR/logindemo/springboot-login-demo-master"
    
    # 使用项目自带的mvnw或系统的mvn
    if [ -f "./mvnw" ]; then
        MAVEN_CMD="./mvnw"
    else
        MAVEN_CMD="mvn"
    fi
    
    # 启动Spring Boot
    $MAVEN_CMD spring-boot:run > "$SCRIPT_DIR/logs/spring_boot.log" 2>&1 &
    SPRING_PID=$!
    echo $SPRING_PID > "$SCRIPT_DIR/logs/spring_boot.pid"
    echo -e "${GREEN}✅ Spring Boot后端已启动 (PID: $SPRING_PID)${NC}"
    echo -e "   📄 日志文件: logs/spring_boot.log"
    echo -e "   🌐 服务地址: http://localhost:8081"
}

# 函数：启动前端代理服务器
start_proxy_server() {
    echo -e "\n${BLUE}🌐 启动前端代理服务器...${NC}"
    cd "$SCRIPT_DIR/logindemo"
    
    # 启动代理服务器
    python3 proxy_server.py > "$SCRIPT_DIR/logs/proxy_server.log" 2>&1 &
    PROXY_PID=$!
    echo $PROXY_PID > "$SCRIPT_DIR/logs/proxy_server.pid"
    echo -e "${GREEN}✅ 前端代理服务器已启动 (PID: $PROXY_PID)${NC}"
    echo -e "   📄 日志文件: logs/proxy_server.log"
    echo -e "   🌐 前端地址: http://localhost:8080"
}

# 函数：等待服务启动
wait_for_services() {
    echo -e "\n${YELLOW}⏳ 等待服务启动...${NC}"
    
    # 等待AI服务
    echo -n "等待AI服务启动..."
    for i in {1..30}; do
        if curl -s http://localhost:8008/health > /dev/null 2>&1; then
            echo -e " ${GREEN}✅${NC}"
            break
        fi
        echo -n "."
        sleep 2
    done
    
    # 等待Spring Boot
    echo -n "等待Spring Boot启动..."
    for i in {1..60}; do
        if curl -s http://localhost:8081/actuator/health > /dev/null 2>&1; then
            echo -e " ${GREEN}✅${NC}"
            break
        fi
        echo -n "."
        sleep 2
    done
    
    # 等待代理服务器
    echo -n "等待代理服务器启动..."
    for i in {1..30}; do
        if curl -s http://localhost:8080 > /dev/null 2>&1; then
            echo -e " ${GREEN}✅${NC}"
            break
        fi
        echo -n "."
        sleep 2
    done
}

# 函数：显示服务状态
show_status() {
    echo -e "\n${BLUE}📊 服务状态检查${NC}"
    echo "=" * 40
    
    # AI服务状态
    if curl -s http://localhost:8008/health > /dev/null 2>&1; then
        echo -e "🤖 AI服务:        ${GREEN}✅ 运行中${NC}"
    else
        echo -e "🤖 AI服务:        ${RED}❌ 未运行${NC}"
    fi
    
    # Spring Boot状态
    if curl -s http://localhost:8081/actuator/health > /dev/null 2>&1; then
        echo -e "☕ Spring Boot:   ${GREEN}✅ 运行中${NC}"
    else
        echo -e "☕ Spring Boot:   ${RED}❌ 未运行${NC}"
    fi
    
    # 代理服务器状态
    if curl -s http://localhost:8080 > /dev/null 2>&1; then
        echo -e "🌐 代理服务器:    ${GREEN}✅ 运行中${NC}"
    else
        echo -e "🌐 代理服务器:    ${RED}❌ 未运行${NC}"
    fi
}

# 函数：停止所有服务
stop_all_services() {
    echo -e "\n${YELLOW}🛑 停止所有服务...${NC}"
    
    # 停止AI服务
    if [ -f "$SCRIPT_DIR/logs/ai_service.pid" ]; then
        AI_PID=$(cat "$SCRIPT_DIR/logs/ai_service.pid")
        if ps -p $AI_PID > /dev/null; then
            kill $AI_PID
            echo -e "${GREEN}✅ AI服务已停止${NC}"
        fi
        rm -f "$SCRIPT_DIR/logs/ai_service.pid"
    fi
    
    # 停止Spring Boot
    if [ -f "$SCRIPT_DIR/logs/spring_boot.pid" ]; then
        SPRING_PID=$(cat "$SCRIPT_DIR/logs/spring_boot.pid")
        if ps -p $SPRING_PID > /dev/null; then
            kill $SPRING_PID
            echo -e "${GREEN}✅ Spring Boot已停止${NC}"
        fi
        rm -f "$SCRIPT_DIR/logs/spring_boot.pid"
    fi
    
    # 停止代理服务器
    if [ -f "$SCRIPT_DIR/logs/proxy_server.pid" ]; then
        PROXY_PID=$(cat "$SCRIPT_DIR/logs/proxy_server.pid")
        if ps -p $PROXY_PID > /dev/null; then
            kill $PROXY_PID
            echo -e "${GREEN}✅ 代理服务器已停止${NC}"
        fi
        rm -f "$SCRIPT_DIR/logs/proxy_server.pid"
    fi
}

# 主逻辑
case "${1:-start}" in
    "start")
        echo -e "${GREEN}🚀 启动所有服务...${NC}"
        start_ai_service
        sleep 3
        start_spring_boot
        sleep 3
        start_proxy_server
        wait_for_services
        show_status
        echo -e "\n${GREEN}🎉 所有服务已启动完成！${NC}"
        echo -e "\n${BLUE}📱 使用指南:${NC}"
        echo -e "   🌐 访问前端: http://localhost:8080"
        echo -e "   👤 测试账号: 用户名=123, 密码=123"
        echo -e "   📄 查看日志: tail -f logs/*.log"
        echo -e "   🛑 停止服务: $0 stop"
        ;;
    "stop")
        stop_all_services
        echo -e "${GREEN}✅ 所有服务已停止${NC}"
        ;;
    "status")
        show_status
        ;;
    "restart")
        stop_all_services
        sleep 3
        echo -e "${GREEN}🔄 重新启动所有服务...${NC}"
        start_ai_service
        sleep 3
        start_spring_boot
        sleep 3
        start_proxy_server
        wait_for_services
        show_status
        ;;
    "logs")
        echo -e "${BLUE}📄 查看实时日志...${NC}"
        echo "按 Ctrl+C 退出"
        tail -f "$SCRIPT_DIR/logs"/*.log
        ;;
    *)
        echo "使用方法: $0 {start|stop|status|restart|logs}"
        echo ""
        echo "命令说明:"
        echo "  start   - 启动所有服务 (默认)"
        echo "  stop    - 停止所有服务"
        echo "  status  - 查看服务状态"
        echo "  restart - 重启所有服务"
        echo "  logs    - 查看实时日志"
        exit 1
        ;;
esac 
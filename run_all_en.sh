#!/bin/bash

# =============================================================================
# Meditation Assistant - Unified Startup Script
# =============================================================================

# English version

echo "🚀 Starting Meditation Assistant Project..."
echo "=" * 60

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Project root: $SCRIPT_DIR"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check required commands
echo -e "\n${BLUE}📋 Checking dependencies...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed${NC}"
    exit 1
fi

if ! command -v java &> /dev/null; then
    echo -e "${RED}❌ Java is not installed${NC}"
    exit 1
fi

if ! command -v mvn &> /dev/null && ! [ -f "$SCRIPT_DIR/logindemo/springboot-login-demo-master/mvnw" ]; then
    echo -e "${RED}❌ Maven is not installed and mvnw is not found in the project${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependency check passed${NC}"

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"

# Function: Start AI service
start_ai_service() {
    echo -e "\n${BLUE}🤖 Starting AI service...${NC}"
    cd "$SCRIPT_DIR/my_project"
    
    # Check config file
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠️  .env file not found, please make sure API keys are configured${NC}"
    fi
    
    # Activate virtual environment and set PYTHONPATH
    if [ -d "venv" ]; then
        source venv/bin/activate
        export PYTHONPATH=.
    fi
    
    # Start service
    python3 service.py > "$SCRIPT_DIR/logs/ai_service.log" 2>&1 &
    AI_PID=$!
    echo $AI_PID > "$SCRIPT_DIR/logs/ai_service.pid"
    echo -e "${GREEN}✅ AI service started (PID: $AI_PID)${NC}"
    echo -e "   📄 Log file: logs/ai_service.log"
    echo -e "   🌐 Service URL: http://localhost:8008"
}

# Function: Start Spring Boot backend
start_spring_boot() {
    echo -e "\n${BLUE}☕ Starting Spring Boot backend...${NC}"
    cd "$SCRIPT_DIR/logindemo/springboot-login-demo-master"
    
    # Use project mvnw or system mvn
    if [ -f "./mvnw" ]; then
        MAVEN_CMD="./mvnw"
    else
        MAVEN_CMD="mvn"
    fi
    
    # Start Spring Boot
    $MAVEN_CMD spring-boot:run > "$SCRIPT_DIR/logs/spring_boot.log" 2>&1 &
    SPRING_PID=$!
    echo $SPRING_PID > "$SCRIPT_DIR/logs/spring_boot.pid"
    echo -e "${GREEN}✅ Spring Boot backend started (PID: $SPRING_PID)${NC}"
    echo -e "   📄 Log file: logs/spring_boot.log"
    echo -e "   🌐 Service URL: http://localhost:8081"
}

# Function: Start frontend proxy server
start_proxy_server() {
    echo -e "\n${BLUE}🌐 Starting frontend proxy server...${NC}"
    cd "$SCRIPT_DIR/logindemo"
    
    # Start proxy server
    python3 proxy_server.py > "$SCRIPT_DIR/logs/proxy_server.log" 2>&1 &
    PROXY_PID=$!
    echo $PROXY_PID > "$SCRIPT_DIR/logs/proxy_server.pid"
    echo -e "${GREEN}✅ Frontend proxy server started (PID: $PROXY_PID)${NC}"
    echo -e "   📄 Log file: logs/proxy_server.log"
    echo -e "   🌐 Frontend URL: http://localhost:8080"
}

# Function: Wait for services to start
wait_for_services() {
    echo -e "\n${YELLOW}⏳ Waiting for services to start...${NC}"
    
    # Wait for AI service
    echo -n "Waiting for AI service to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8008/health > /dev/null 2>&1; then
            echo -e " ${GREEN}✅${NC}"
            break
        fi
        echo -n "."
        sleep 2
    done
    
    # Wait for Spring Boot
    echo -n "Waiting for Spring Boot to start..."
    for i in {1..60}; do
        if curl -s http://localhost:8081/actuator/health > /dev/null 2>&1; then
            echo -e " ${GREEN}✅${NC}"
            break
        fi
        echo -n "."
        sleep 2
    done
    
    # Wait for proxy server
    echo -n "Waiting for proxy server to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8080 > /dev/null 2>&1; then
            echo -e " ${GREEN}✅${NC}"
            break
        fi
        echo -n "."
        sleep 2
    done
}

# Function: Show service status
show_status() {
    echo -e "\n${BLUE}📊 Service Status${NC}"
    echo "=" * 40
    
    # AI service status
    if curl -s http://localhost:8008/health > /dev/null 2>&1; then
        echo -e "🤖 AI Service:        ${GREEN}✅ Running${NC}"
    else
        echo -e "🤖 AI Service:        ${RED}❌ Not running${NC}"
    fi
    
    # Spring Boot status
    if curl -s http://localhost:8081/actuator/health > /dev/null 2>&1; then
        echo -e "☕ Spring Boot:       ${GREEN}✅ Running${NC}"
    else
        echo -e "☕ Spring Boot:       ${RED}❌ Not running${NC}"
    fi
    
    # Proxy server status
    if curl -s http://localhost:8080 > /dev/null 2>&1; then
        echo -e "🌐 Proxy Server:      ${GREEN}✅ Running${NC}"
    else
        echo -e "🌐 Proxy Server:      ${RED}❌ Not running${NC}"
    fi
}

# Function: Stop all services
stop_all_services() {
    echo -e "\n${YELLOW}🛑 Stopping all services...${NC}"
    
    # Stop AI service
    if [ -f "$SCRIPT_DIR/logs/ai_service.pid" ]; then
        AI_PID=$(cat "$SCRIPT_DIR/logs/ai_service.pid")
        if ps -p $AI_PID > /dev/null; then
            kill $AI_PID
            echo -e "${GREEN}✅ AI service stopped${NC}"
        fi
        rm -f "$SCRIPT_DIR/logs/ai_service.pid"
    fi
    
    # Stop Spring Boot
    if [ -f "$SCRIPT_DIR/logs/spring_boot.pid" ]; then
        SPRING_PID=$(cat "$SCRIPT_DIR/logs/spring_boot.pid")
        if ps -p $SPRING_PID > /dev/null; then
            kill $SPRING_PID
            echo -e "${GREEN}✅ Spring Boot stopped${NC}"
        fi
        rm -f "$SCRIPT_DIR/logs/spring_boot.pid"
    fi
    
    # Stop proxy server
    if [ -f "$SCRIPT_DIR/logs/proxy_server.pid" ]; then
        PROXY_PID=$(cat "$SCRIPT_DIR/logs/proxy_server.pid")
        if ps -p $PROXY_PID > /dev/null; then
            kill $PROXY_PID
            echo -e "${GREEN}✅ Proxy server stopped${NC}"
        fi
        rm -f "$SCRIPT_DIR/logs/proxy_server.pid"
    fi
}

# Main logic
case "${1:-start}" in
    "start")
        echo -e "${GREEN}🚀 Starting all services...${NC}"
        start_ai_service
        sleep 3
        start_spring_boot
        sleep 3
        start_proxy_server
        wait_for_services
        show_status
        echo -e "\n${GREEN}🎉 All services started!${NC}"
        echo -e "\n${BLUE}📱 Usage Guide:${NC}"
        echo -e "   🌐 Frontend: http://localhost:8080"
        echo -e "   👤 Test account: username=123, password=123"
        echo -e "   📄 View logs: tail -f logs/*.log"
        echo -e "   🛑 Stop services: $0 stop"
        ;;
    "stop")
        stop_all_services
        echo -e "${GREEN}✅ All services stopped${NC}"
        ;;
    "status")
        show_status
        ;;
    "restart")
        stop_all_services
        sleep 3
        echo -e "${GREEN}🔄 Restarting all services...${NC}"
        start_ai_service
        sleep 3
        start_spring_boot
        sleep 3
        start_proxy_server
        wait_for_services
        show_status
        ;;
    "logs")
        echo -e "${BLUE}📄 Viewing real-time logs...${NC}"
        echo "Press Ctrl+C to exit"
        tail -f "$SCRIPT_DIR/logs"/*.log
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start all services (default)"
        echo "  stop    - Stop all services"
        echo "  status  - Show service status"
        echo "  restart - Restart all services"
        echo "  logs    - View real-time logs"
        exit 1
        ;;
esac 
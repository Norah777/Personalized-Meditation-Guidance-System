#!/bin/bash

# 登录演示项目运行脚本
echo "🚀 开始配置和运行登录演示项目..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查MySQL服务是否运行
echo -e "${BLUE}步骤1: 检查MySQL服务状态...${NC}"
if ! brew services list | grep mysql | grep started > /dev/null; then
    echo -e "${YELLOW}启动MySQL服务...${NC}"
    brew services start mysql
    sleep 3
fi

# 创建数据库和用户
echo -e "${BLUE}步骤2: 设置数据库...${NC}"
mysql -u root -p123456 <<EOF
CREATE DATABASE IF NOT EXISTS logindemo;
USE logindemo;
SOURCE logindemo.sql;
SHOW TABLES;
SELECT * FROM user;
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 数据库配置成功！${NC}"
else
    echo -e "${RED}❌ 数据库配置失败，请检查MySQL配置${NC}"
    exit 1
fi

# 构建和启动后端
echo -e "${BLUE}步骤3: 构建和启动Spring Boot后端...${NC}"
cd springboot-login-demo-master

# 更新数据库配置（如果需要）
echo -e "${YELLOW}检查数据库配置...${NC}"
if ! grep -q "spring.datasource.password=123456" src/main/resources/application.properties; then
    echo "请确认MySQL root密码是否为123456，如果不是，请修改 src/main/resources/application.properties 文件"
fi

# 构建项目
echo -e "${YELLOW}构建Maven项目...${NC}"
./mvnw clean package -DskipTests

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 后端构建成功！${NC}"
    
    # 启动后端服务
    echo -e "${YELLOW}启动后端服务 (端口8081)...${NC}"
    nohup ./mvnw spring-boot:run > ../backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../backend.pid
    echo -e "${GREEN}✅ 后端服务已启动 (PID: $BACKEND_PID)${NC}"
    
    # 等待后端启动
    sleep 10
    
    # 检查后端是否正常运行
    if curl -s http://localhost:8081 > /dev/null; then
        echo -e "${GREEN}✅ 后端服务运行正常！${NC}"
    else
        echo -e "${YELLOW}⚠️  后端服务可能还在启动中，请稍等...${NC}"
    fi
else
    echo -e "${RED}❌ 后端构建失败${NC}"
    exit 1
fi

# 回到根目录
cd ..

# 安装和启动前端
echo -e "${BLUE}步骤4: 安装和启动Vue前端...${NC}"
cd vue-login-demo-master

# 检查node_modules是否存在
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}安装前端依赖...${NC}"
    npm install --legacy-peer-deps
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 前端依赖安装成功！${NC}"
    else
        echo -e "${RED}❌ 前端依赖安装失败${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ 前端依赖已存在${NC}"
fi

# 构建前端项目
echo -e "${YELLOW}构建前端项目...${NC}"
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 前端构建成功！${NC}"
else
    echo -e "${RED}❌ 前端构建失败${NC}"
    exit 1
fi

# 回到根目录
cd ..

# 启动支持代理的前端服务器
echo -e "${YELLOW}启动前端代理服务器...${NC}"
nohup python3 proxy_server.py > frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > frontend.pid
echo -e "${GREEN}✅ 前端代理服务器已启动 (PID: $FRONTEND_PID)${NC}"

# 等待前端启动
sleep 5

# 检查前端是否正常运行
if curl -s http://localhost:8080 > /dev/null; then
    echo -e "${GREEN}✅ 前端服务运行正常！${NC}"
else
    echo -e "${YELLOW}⚠️  前端服务可能还在启动中，请稍等...${NC}"
fi

echo -e "${GREEN}🎉 项目启动完成！${NC}"
echo -e "${BLUE}访问地址:${NC}"
echo -e "  前端: ${GREEN}http://localhost:8080${NC}"
echo -e "  后端: ${GREEN}http://localhost:8081${NC}"
echo ""
echo -e "${YELLOW}测试用户:${NC}"
echo -e "  用户名: ${GREEN}123${NC}"
echo -e "  密码: ${GREEN}123${NC}"
echo ""
echo -e "${BLUE}日志文件:${NC}"
echo -e "  后端日志: ${GREEN}backend.log${NC}"
echo -e "  前端日志: ${GREEN}frontend.log${NC} (代理服务器日志)"
echo ""
echo -e "${BLUE}服务说明:${NC}"
echo -e "  前端: ${GREEN}构建后的静态文件 + Python代理服务器${NC}"
echo -e "  后端: ${GREEN}Spring Boot应用${NC}"
echo ""
echo -e "${YELLOW}停止服务:${NC}"
echo -e "  运行: ${GREEN}./stop_project.sh${NC}"
echo ""
echo -e "${BLUE}如果遇到问题，请检查日志文件${NC}" 
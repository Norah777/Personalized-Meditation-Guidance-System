#!/bin/bash

# 合并项目启动脚本
echo "🚀 启动冥想助手项目的所有服务..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}当前工作目录: $(pwd)${NC}"

# 检查必要的目录和文件
echo -e "${BLUE}步骤1: 检查项目结构...${NC}"
if [ ! -d "my_project" ]; then
    echo -e "${RED}❌ my_project 目录不存在${NC}"
    exit 1
fi

if [ ! -d "logindemo" ]; then
    echo -e "${RED}❌ logindemo 目录不存在${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 项目结构检查完成${NC}"

# 创建必要的目录
echo -e "${BLUE}步骤2: 创建必要的目录...${NC}"
mkdir -p logindemo/uploads/images
mkdir -p logindemo/uploads/videos
mkdir -p logindemo/springboot-login-demo-master/uploads/images
mkdir -p logindemo/springboot-login-demo-master/uploads/videos

echo -e "${GREEN}✅ 目录创建完成${NC}"

# 检查MySQL服务
echo -e "${BLUE}步骤3: 检查MySQL服务...${NC}"
if ! brew services list | grep mysql | grep started > /dev/null; then
    echo -e "${YELLOW}启动MySQL服务...${NC}"
    brew services start mysql
    sleep 3
fi

# 设置数据库
echo -e "${BLUE}步骤4: 设置数据库...${NC}"
cd logindemo
mysql -u root -p123456 <<EOF
CREATE DATABASE IF NOT EXISTS logindemo;
USE logindemo;
SOURCE logindemo.sql;
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 数据库配置成功！${NC}"
else
    echo -e "${RED}❌ 数据库配置失败${NC}"
    exit 1
fi

cd ..

# 启动 my_project 服务
echo -e "${BLUE}步骤5: 启动 my_project 服务...${NC}"
cd my_project

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}创建虚拟环境...${NC}"
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
source venv/bin/activate
pip install -r requirements.txt

# 启动 my_project 服务
echo -e "${YELLOW}启动 my_project 服务 (端口8008)...${NC}"
nohup python3 service.py > ../logs/my_project.log 2>&1 &
MY_PROJECT_PID=$!
echo $MY_PROJECT_PID > ../logs/my_project.pid
echo -e "${GREEN}✅ my_project 服务已启动 (PID: $MY_PROJECT_PID)${NC}"

cd ..

# 启动 Spring Boot 后端
echo -e "${BLUE}步骤6: 启动 Spring Boot 后端...${NC}"
cd logindemo/springboot-login-demo-master

# 构建项目
echo -e "${YELLOW}构建 Spring Boot 项目...${NC}"
./mvnw clean package -DskipTests

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 后端构建成功！${NC}"
    
    # 启动后端服务
    echo -e "${YELLOW}启动后端服务 (端口8081)...${NC}"
    nohup ./mvnw spring-boot:run > ../../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../../logs/backend.pid
    echo -e "${GREEN}✅ 后端服务已启动 (PID: $BACKEND_PID)${NC}"
else
    echo -e "${RED}❌ 后端构建失败${NC}"
    exit 1
fi

cd ../..

# 构建和启动前端
echo -e "${BLUE}步骤7: 构建和启动前端...${NC}"
cd logindemo/vue-login-demo-master

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}安装前端依赖...${NC}"
    npm install --legacy-peer-deps
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 前端依赖安装失败${NC}"
        exit 1
    fi
fi

# 构建前端
echo -e "${YELLOW}构建前端项目...${NC}"
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 前端构建成功！${NC}"
else
    echo -e "${RED}❌ 前端构建失败${NC}"
    exit 1
fi

cd ..

# 启动前端代理服务器
echo -e "${YELLOW}启动前端代理服务器 (端口8080)...${NC}"
nohup python3 proxy_server.py > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
echo -e "${GREEN}✅ 前端代理服务器已启动 (PID: $FRONTEND_PID)${NC}"

cd ..

# 等待所有服务启动
echo -e "${BLUE}步骤8: 等待服务启动...${NC}"
sleep 10

# 检查服务状态
echo -e "${BLUE}步骤9: 检查服务状态...${NC}"

# 检查 my_project 服务
if curl -s http://localhost:8008/health > /dev/null; then
    echo -e "${GREEN}✅ my_project 服务运行正常！${NC}"
else
    echo -e "${YELLOW}⚠️  my_project 服务可能还在启动中...${NC}"
fi

# 检查后端服务
if curl -s http://localhost:8081 > /dev/null; then
    echo -e "${GREEN}✅ 后端服务运行正常！${NC}"
else
    echo -e "${YELLOW}⚠️  后端服务可能还在启动中...${NC}"
fi

# 检查前端服务
if curl -s http://localhost:8080 > /dev/null; then
    echo -e "${GREEN}✅ 前端服务运行正常！${NC}"
else
    echo -e "${YELLOW}⚠️  前端服务可能还在启动中...${NC}"
fi

echo -e "${GREEN}🎉 所有服务启动完成！${NC}"
echo -e "${BLUE}访问地址:${NC}"
echo -e "  前端应用: ${GREEN}http://localhost:8080${NC}"
echo -e "  后端API: ${GREEN}http://localhost:8081${NC}"
echo -e "  my_project服务: ${GREEN}http://localhost:8008${NC}"
echo ""
echo -e "${YELLOW}测试用户:${NC}"
echo -e "  用户名: ${GREEN}123${NC}"
echo -e "  密码: ${GREEN}123${NC}"
echo ""
echo -e "${BLUE}日志文件:${NC}"
echo -e "  my_project日志: ${GREEN}logs/my_project.log${NC}"
echo -e "  后端日志: ${GREEN}logs/backend.log${NC}"
echo -e "  前端日志: ${GREEN}logs/frontend.log${NC}"
echo ""
echo -e "${YELLOW}停止服务:${NC}"
echo -e "  运行: ${GREEN}./stop_all_services.sh${NC}"
echo ""
echo -e "${BLUE}如果遇到问题，请检查日志文件${NC}" 
# 🧘 Meditation Assistant - 冥想助手

一个完整的全栈冥想助手项目，包含用户登录、心情记录和AI驱动的冥想内容生成功能。

## 🏗️ 项目结构

```
meditation-assistant/
├── 📁 logindemo/                               # 前端和Spring Boot后端
│   ├── 📁 springboot-login-demo-master/       # Spring Boot后端服务
│   ├── 📁 vue-login-demo-master/              # Vue.js前端源码
│   ├── 📁 uploads/                            # 生成的媒体文件存储
│   │   ├── 📁 images/                         # 生成的图片
│   │   └── 📁 videos/                         # 生成的视频
│   ├── 📄 proxy_server.py                     # 前端代理服务器
│   └── 📄 test_*.py                           # 测试脚本
├── 📁 my_project/                             # AI服务
│   ├── 📁 pipeline/                           # AI处理流水线
│   ├── 📁 config/                             # 配置文件
│   ├── 📄 service.py                          # Flask AI服务
│   └── 📄 .env                                # 环境变量配置
├── 📁 logs/                                   # 服务日志文件
├── 📄 run_all.sh                              # 统一启动脚本
└── 📄 README.md                               # 项目说明文档
```

## 🚀 快速开始

### 1. 一键启动所有服务

```bash
# 进入项目目录
cd ./meditation-assistant

# 给启动脚本执行权限
chmod +x run_all.sh

# 启动所有服务
./run_all.sh
```

### 2. 访问应用

启动完成后，访问：
- **前端应用**: http://localhost:8080
- **测试账号**: 用户名=`123`, 密码=`123`

### 3. 使用冥想功能

1. 登录后点击"开始冥想"
2. 选择当前心情
3. 描述你的感受或想法
4. 点击发送生成个性化冥想文本
5. 可选择生成配套图片或视频

## 🔧 其他命令

```bash
# 查看服务状态
./run_all.sh status

# 停止所有服务
./run_all.sh stop

# 重启所有服务
./run_all.sh restart

# 查看实时日志
./run_all.sh logs
```

## 🛠️ 技术栈

### 后端
- **Spring Boot 2.3.12** - REST API服务
- **Java 8+** - 编程语言
- **Maven** - 依赖管理
- **MySQL 8.0+** - 数据库
- **JPA/Hibernate** - ORM框架

### 前端
- **Vue.js 2.6.11** - 前端框架
- **Element UI 2.15.6** - UI组件库
- **Vue Router** - 路由管理
- **Axios** - HTTP客户端

### AI服务
- **Python 3.8+** - 编程语言
- **Flask** - Web框架
- **OpenAI API** - 文本生成
- **DashScope API** - 图片生成
- **MiniMax API** - 语音合成
- **FFmpeg** - 视频处理

## ⚙️ 配置说明

### 1. AI服务配置

在 `my_project/.env` 文件中配置API密钥：

```env
# 文本生成API (DeepSeek)
TEXT_API_KEY=your_deepseek_api_key
TEXT_BASE_URL=https://api.deepseek.com
TEXT_MODEL_NAME=deepseek-chat

# 图片生成API (DashScope)
DASHSCOPE_API_KEY=your_dashscope_api_key

# 语音合成API (MiniMax)
TTS_API_KEY=your_minimax_api_key
TTS_GROUP_ID=your_group_id
```

### 2. 数据库配置

确保MySQL服务运行，并创建数据库：

```sql
CREATE DATABASE logindemo;
USE logindemo;
-- 运行项目中的SQL初始化脚本
```

## 🔍 服务详情

### AI服务 (端口 8008)
- **健康检查**: `GET /health`
- **生成文本**: `POST /generate-text`
- **生成图片**: `POST /generate-image`
- **生成视频**: `POST /generate-video`
- **完整流水线**: `POST /process`

### Spring Boot后端 (端口 8081)
- **用户登录**: `POST /user/login`
- **用户注册**: `POST /user/register`
- **生成文本**: `POST /mood-logs/generateText`
- **生成图片**: `POST /mood-logs/generateImage`
- **生成视频**: `POST /mood-logs/generateVideoFromText`

### 前端代理服务器 (端口 8080)
- **静态文件服务**: Vue.js构建文件
- **API代理**: 转发请求到Spring Boot
- **媒体文件服务**: 提供生成的图片和视频

## 📋 新功能特性

### ✨ 分步骤生成
- **快速文本生成** (2-5秒) - 立即获得冥想指导
- **可选图片生成** (10-15秒) - 根据文本生成视觉内容
- **可选视频生成** (30-45秒) - 创建完整的冥想体验

### ✨ 智能路径管理
- **统一项目结构** - 所有组件在同一目录下
- **自动路径配置** - 无需手动配置复杂路径
- **智能文件处理** - 自动检测和复制生成的媒体文件

### ✨ 便捷运维
- **一键启动** - 单个命令启动所有服务
- **日志管理** - 集中的日志文件管理
- **服务监控** - 实时服务状态检查
- **优雅停止** - 安全停止所有服务

## 🐛 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 检查端口占用
   lsof -i :8008 :8080 :8081
   
   # 查看详细日志
   ./run_all.sh logs
   ```

2. **API密钥问题**
   ```bash
   # 检查.env文件
   cat my_project/.env
   
   # 确保所有必需的API密钥都已配置
   ```

3. **数据库连接问题**
   ```bash
   # 检查MySQL服务
   brew services list | grep mysql
   
   # 启动MySQL服务
   brew services start mysql
   ```

4. **文件权限问题**
   ```bash
   # 给启动脚本执行权限
   chmod +x run_all.sh
   
   # 检查uploads目录权限
   ls -la logindemo/uploads/
   ```

### 日志查看

```bash
# 查看所有服务日志
tail -f logs/*.log

# 查看特定服务日志
tail -f logs/ai_service.log
tail -f logs/spring_boot.log
tail -f logs/proxy_server.log
```

## 🤝 开发指南

### 开发模式启动

```bash
# 分别启动各个服务进行开发
cd my_project && python3 service.py          # AI服务
cd logindemo/springboot-login-demo-master && ./mvnw spring-boot:run  # 后端
cd logindemo && python3 proxy_server.py      # 前端代理
```

### 测试

```bash
# 运行路径测试
cd logindemo && python3 test_path_fix.py

# 运行功能测试
cd logindemo && python3 test_image_fix.py
```

## 📄 许可证

本项目仅供学习和研究使用。

## 🙏 致谢

感谢所有开源项目和API服务提供商的支持。

---

**享受你的冥想之旅！** 🧘‍♀️✨ 
# 🧘 Meditation Assistant

A full-stack meditation assistant project featuring user login, mood tracking, and AI-powered meditation content generation.

## 🏗️ Project Structure

```
meditation-assistant/
├── 📁 logindemo/                               # Frontend and Spring Boot backend
│   ├── 📁 springboot-login-demo-master/       # Spring Boot backend service
│   ├── 📁 vue-login-demo-master/              # Vue.js frontend source code
│   ├── 📁 uploads/                            # Generated media file storage
│   │   ├── 📁 images/                         # Generated images
│   │   └── 📁 videos/                         # Generated videos
│   ├── 📄 proxy_server.py                     # Frontend proxy server
│   └── 📄 test_*.py                           # Test scripts
├── 📁 my_project/                             # AI service
│   ├── 📁 pipeline/                           # AI processing pipeline
│   ├── 📁 config/                             # Configuration files
│   ├── 📄 service.py                          # Flask AI service
│   └── 📄 .env                                # Environment variable configuration
├── 📁 logs/                                   # Service log files
├── 📄 run_all.sh                              # Unified startup script
└── 📄 README.md                               # Project documentation
```

## 🚀 Quick Start

### 1. Start All Services with One Command

```bash
# Enter the project directory
cd ./meditation-assistant

# Grant execute permission to the startup script
chmod +x run_all.sh

# Start all services
./run_all_en.sh
```

### 2. (For Development) Start AI Service Manually

If you want to run the AI service manually for development or debugging:

```bash
cd my_project
source venv/bin/activate      # Activate the Python virtual environment (if applicable)
export PYTHONPATH=.           # Set PYTHONPATH if required
python3 service.py
```

### 3. Access the Application

After startup, visit:
- **Frontend App**: http://localhost:8080
- **Test Account**: Username=`123`, Password=`123`

### 3. Using the Meditation Feature

1. Log in and click "Start Meditation"
2. Select your current mood
3. Describe your feelings or thoughts
4. Click send to generate personalized meditation text
5. Optionally, generate a matching image or video

## 🔧 Other Commands

```bash
# Check service status
./run_all.sh status

# Stop all services
./run_all.sh stop

# Restart all services
./run_all.sh restart

# View real-time logs
./run_all.sh logs
```

## 🛠️ Tech Stack

### Backend
- **Spring Boot 2.3.12** - REST API service
- **Java 8+** - Programming language
- **Maven** - Dependency management
- **MySQL 8.0+** - Database
- **JPA/Hibernate** - ORM framework

### Frontend
- **Vue.js 2.6.11** - Frontend framework
- **Element UI 2.15.6** - UI component library
- **Vue Router** - Routing management
- **Axios** - HTTP client

### AI Service
- **Python 3.8+** - Programming language
- **Flask** - Web framework
- **OpenAI API** - Text generation
- **DashScope API** - Image generation
- **MiniMax API** - Speech synthesis
- **FFmpeg** - Video processing

## ⚙️ Configuration

### 1. AI Service Configuration

Configure API keys in `my_project/.env`:

```env
# Text Generation API (DeepSeek)
TEXT_API_KEY=your_deepseek_api_key
TEXT_BASE_URL=https://api.deepseek.com
TEXT_MODEL_NAME=deepseek-chat

# Image Generation API (DashScope)
DASHSCOPE_API_KEY=your_dashscope_api_key

# Speech Synthesis API (MiniMax)
TTS_API_KEY=your_minimax_api_key
TTS_GROUP_ID=your_group_id
```

### 2. Database Configuration

Make sure MySQL is running and create the database:

```sql
CREATE DATABASE logindemo;
USE logindemo;
-- Run the SQL initialization script from the project
```

## 🔍 Service Details

### AI Service (Port 8008)
- **Health Check**: `GET /health`
- **Generate Text**: `POST /generate-text`
- **Generate Image**: `POST /generate-image`
- **Generate Video**: `POST /generate-video`
- **Full Pipeline**: `POST /process`

### Spring Boot Backend (Port 8081)
- **User Login**: `POST /user/login`
- **User Registration**: `POST /user/register`
- **Generate Text**: `POST /mood-logs/generateText`
- **Generate Image**: `POST /mood-logs/generateImage`
- **Generate Video**: `POST /mood-logs/generateVideoFromText`

### Frontend Proxy Server (Port 8080)
- **Static File Service**: Vue.js build files
- **API Proxy**: Forwards requests to Spring Boot
- **Media File Service**: Serves generated images and videos

## 📋 New Features

### ✨ Step-by-Step Generation
- **Quick Text Generation** (2-5 seconds) - Get meditation guidance instantly
- **Optional Image Generation** (10-15 seconds) - Visual content based on text
- **Optional Video Generation** (30-45 seconds) - Create a complete meditation experience

### ✨ Intelligent Path Management
- **Unified Project Structure** - All components in one directory
- **Automatic Path Configuration** - No need for manual path setup
- **Smart File Handling** - Automatically detects and copies generated media files

### ✨ Easy Operations
- **One-Click Startup** - Start all services with a single command
- **Log Management** - Centralized log file management
- **Service Monitoring** - Real-time service status checks
- **Graceful Shutdown** - Safely stop all services

## 🐛 Troubleshooting

### Common Issues

1. **Service Startup Failure**
   ```bash
   # Check for port conflicts
   lsof -i :8008 :8080 :8081
   
   # View detailed logs
   ./run_all.sh logs
   ```

2. **API Key Issues**
   ```bash
   # Check .env file
   cat my_project/.env
   
   # Make sure all required API keys are set
   ```

3. **Database Connection Issues**
   ```bash
   # Check MySQL service
   brew services list | grep mysql
   
   # Start MySQL service
   brew services start mysql
   ```

4. **File Permission Issues**
   ```bash
   # Grant execute permission to the startup script
   chmod +x run_all.sh
   
   # Check uploads directory permissions
   ls -la logindemo/uploads/
   ```

### Viewing Logs

```bash
# View all service logs
tail -f logs/*.log

# View specific service logs
tail -f logs/ai_service.log
tail -f logs/spring_boot.log
tail -f logs/proxy_server.log
```

## 🤝 Development Guide

### Start in Development Mode

```bash
# Start each service separately for development
cd my_project && python3 service.py          # AI service
cd logindemo/springboot-login-demo-master && ./mvnw spring-boot:run  # Backend
cd logindemo && python3 proxy_server.py      # Frontend proxy
```

### Testing

```bash
# Run path tests
cd logindemo && python3 test_path_fix.py

# Run feature tests
cd logindemo && python3 test_image_fix.py
```

## 📄 License

This project is for learning and research purposes only.

## 🙏 Acknowledgements

Thanks to all open-source projects and API service providers for their support.

---

**Enjoy your meditation journey!** 🧘‍♀️✨ 
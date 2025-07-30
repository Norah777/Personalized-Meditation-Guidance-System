# Login Demo with Meditation Assistant

This is a complete full-stack login demo project with an integrated meditation assistant, including Spring Boot backend, Vue.js frontend, and an AI-powered meditation content generation service.

## 🚀 New Feature: Step-by-Step Meditation Generation

The meditation assistant now supports a new step-by-step generation approach:

1. **Generate Text** → Users receive personalized meditation text first
2. **Generate Image** → Optional image generation based on the text
3. **Generate Video** → Optional video generation with narration and visuals

This provides a better user experience with faster initial responses and more control over the generation process.

## 🏗️ Project Structure

```
logindemo/
├── springboot-login-demo-master/    # Spring Boot backend
├── vue-login-demo-master/           # Vue.js frontend
├── my_project/                      # AI meditation generation service
├── uploads/                         # Generated content storage
│   ├── videos/                      # Generated videos
│   └── images/                      # Generated images
├── proxy_server.py                  # Frontend proxy server
├── run_project.sh                   # Project startup script
├── stop_project.sh                  # Project shutdown script
└── README.md                        # This file
```

## 🔧 Technology Stack

### Backend
- **Spring Boot 2.3.12**
- **Java 1.8+**
- **Maven 3.6+**
- **MySQL 8.0+**
- **JPA/Hibernate**

### Frontend
- **Vue.js 2.6.11**
- **Element UI 2.15.6**
- **Vue Router 3.5.3**
- **Axios 0.25.0**

### AI Service
- **Python 3.8+**
- **Flask**
- **OpenAI API**
- **FFmpeg** (for video generation)

## 🚀 Quick Start

### 1. Prerequisites

Make sure you have the following installed:
- **Java 1.8+** ✅
- **Maven 3.6+** ✅
- **Node.js 14+** ✅
- **MySQL 8.0+** ✅
- **Python 3.8+** ✅

### 2. One-Click Startup

```bash
# Grant execute permissions to scripts
chmod +x run_project.sh stop_project.sh

# Start the project
./run_project.sh
```

### 3. Configure AI Service

Before using the meditation assistant, configure the AI service:

```bash
# Navigate to the AI service directory
cd my_project

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cp config_example.env .env
# Edit .env with your API keys

# Start the AI service
python service.py
```

### 4. Access the Application

After successful startup, access:
- **Frontend**: http://localhost:8080
- **Backend**: http://localhost:8081
- **AI Service**: http://localhost:8008

### 5. Test Account

- **Username**: `123`
- **Password**: `123`

## 🧘 How to Use the Meditation Assistant

### Step 1: Login and Navigate
1. Log in with the test account
2. Navigate to "Start Meditation" from the main menu

### Step 2: Generate Meditation Text
1. Select your current mood (Happy, Sad, Angry, Calm, Excited, Tired)
2. Describe your feelings or thoughts in the text area
3. Click "Send" to generate personalized meditation text

### Step 3: Generate Additional Content (Optional)
After receiving the meditation text, you can:
- Click "Generate Image" to create a visual representation
- Click "Generate Video" to create a complete meditation video with narration

### Step 4: Enjoy Your Meditation
- Read the generated text for guidance
- View the generated image for visual inspiration
- Watch the video for a complete meditation experience

## 🔧 Manual Setup (If Needed)

### 1. Database Setup

```bash
# Start MySQL service
brew services start mysql

# Create database
mysql -u root -p
CREATE DATABASE logindemo;
USE logindemo;
SOURCE logindemo.sql;
```

### 2. Backend Setup

```bash
cd springboot-login-demo-master
./mvnw clean package -DskipTests
./mvnw spring-boot:run
```

### 3. Frontend Setup

```bash
cd vue-login-demo-master
npm install
npm run build
```

### 4. AI Service Setup

```bash
cd my_project
pip install -r requirements.txt
python service.py
```

## 🛑 Stop Services

```bash
./stop_project.sh
```

## 📋 API Endpoints

### Authentication
- `POST /api/user/login` - User login
- `POST /api/user/register` - User registration

### Meditation Generation
- `POST /api/mood-logs/generateText` - Generate meditation text
- `POST /api/mood-logs/generateImage` - Generate meditation image
- `POST /api/mood-logs/generateVideoFromText` - Generate meditation video

### AI Service (Direct Access)
- `POST /generate-text` - Generate text only
- `POST /generate-image` - Generate image from text
- `POST /generate-video` - Generate video from text and image
- `POST /process` - Complete pipeline (legacy)

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check MySQL service: `brew services list | grep mysql`
   - Verify database password (default: 123456)

2. **Port Already in Use**
   - Check port usage: `lsof -i :8080` or `lsof -i :8081`
   - Force stop: `lsof -ti:8080 | xargs kill -9`

3. **AI Service Not Working**
   - Check API keys in `.env` file
   - Verify Python dependencies are installed
   - Ensure FFmpeg is installed for video generation

4. **Frontend Dependencies Installation Failed**
   - Clear cache: `npm cache clean --force`
   - Delete node_modules: `rm -rf node_modules`
   - Reinstall: `npm install`

### View Logs

```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log

# AI service logs
tail -f proxy.log
```

## 📚 Features

- ✅ User registration and login
- ✅ Password validation
- ✅ Session management
- ✅ Responsive design
- ✅ Error handling
- ✅ **NEW**: Step-by-step meditation generation
- ✅ **NEW**: AI-powered text generation
- ✅ **NEW**: Image generation from text
- ✅ **NEW**: Video generation with narration
- ✅ **NEW**: Real-time user feedback

## 🔒 Security Notice

⚠️ **Warning**: This is a demo project and should not be used in production without proper security measures:

- Passwords are not encrypted
- No input validation
- No rate limiting
- No authentication tokens

## 📖 Documentation

- [AI Service Usage Guide](my_project/SERVICE_USAGE.md)
- [Configuration Guide](my_project/CONFIG_GUIDE.md)

## 🎯 Future Enhancements

- [ ] Streaming text generation for real-time feedback
- [ ] Multiple meditation styles and themes
- [ ] User preference learning
- [ ] Meditation history tracking
- [ ] Social sharing features
- [ ] Mobile app version

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is for educational purposes only. 
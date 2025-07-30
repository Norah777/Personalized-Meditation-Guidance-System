<template>
  <div class="meditation-container">
    <div class="chat-container">
      <!-- Chat message area -->
      <div class="messages" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.role]"
        >
          <div class="avatar">
            <el-avatar
              :icon="
                message.role === 'user' ? 'el-icon-user' : 'el-icon-chat-round'
              "
            />
          </div>
          <div class="content">
            <div class="meta">
              <span class="role">{{
                message.role === "user" ? "You" : "Meditation Assistant"
              }}</span>
              <span class="time">{{ formatTime(message.timestamp) }}</span>
              <span v-if="message.mood" class="mood-tag">
                <el-tag :type="getMoodType(message.mood)" size="mini">
                  {{ getMoodEmoji(message.mood) }}
                  {{ getMoodText(message.mood) }}
                </el-tag>
              </span>
            </div>
            <div class="text">
              <!-- Show loading animation when generating text -->
              <div v-if="message.isGenerating" class="generating-text">
                <el-icon class="loading"><el-icon-loading /></el-icon>
                {{ message.content }}
              </div>
              <!-- Normal message content -->
              <div v-else v-html="renderMessage(message.content)"></div>
            </div>
            
            <!-- Action buttons for generated text -->
            <div v-if="message.role === 'assistant' && message.generatedText && !message.isGenerating" class="action-buttons">
              <el-button 
                type="primary" 
                size="small" 
                @click="generateImage(message, index)"
                :loading="message.isGeneratingImage"
                :disabled="message.isGeneratingVideo"
              >
                <i class="el-icon-picture"></i>
                Generate Image
              </el-button>
              <el-button 
                type="success" 
                size="small" 
                @click="generateVideo(message, index)"
                :loading="message.isGeneratingVideo"
                :disabled="message.isGeneratingImage"
              >
                <i class="el-icon-video-camera"></i>
                Generate Video
              </el-button>
            </div>
            
            <!-- Show generated image -->
            <div v-if="message.imageUrl" class="image-container">
              <img 
                :src="message.imageUrl" 
                alt="Generated meditation image"
                style="width: 100%; max-width: 400px; border-radius: 12px; margin-top: 10px;"
                @load="scrollToBottom"
              />
            </div>
            
            <!-- Show generated video -->
            <div v-if="message.videoUrl" class="video-container">
              <video
                :src="message.videoUrl"
                controls
                style="width: 100%; max-width: 400px; border-radius: 12px; margin-top: 10px;"
                @loadstart="console.log('Video loading started:', message.videoUrl)"
                @loadedmetadata="console.log('Video metadata loaded')"
                @error="console.error('Video loading error:', $event)"
                @canplay="console.log('Video ready to play')"
                @ended="handleVideoEnded(message)"
              ></video>
            </div>
          </div>
        </div>
        
        <!-- Loading indicator -->
        <div v-if="isLoading" class="message assistant">
          <div class="avatar">
            <el-avatar icon="el-icon-chat-round" />
          </div>
          <div class="content">
            <div class="meta">
              <span class="role">Meditation Assistant</span>
            </div>
            <div class="text">
              <el-icon class="loading"><el-icon-loading /></el-icon>
              Thinking...
            </div>
          </div>
        </div>
      </div>

      <!-- Input area -->
      <div class="input-area">
        <div class="mood-selector">
          <span class="label">Current mood:</span>
          <el-radio-group v-model="currentMood" size="small">
            <el-radio-button
              v-for="mood in moods"
              :key="mood.value"
              :label="mood.value"
            >
              <el-tooltip :content="mood.label" placement="top">
                <div class="mood-option">
                  <span class="mood-emoji">{{ mood.emoji }}</span>
                  <span class="mood-label">{{ mood.label }}</span>
                </div>
              </el-tooltip>
            </el-radio-button>
          </el-radio-group>
        </div>

        <div class="input-box">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="Tell me your current feelings or thoughts..."
            @keyup.enter.native="sendMessage"
            resize="none"
          />
          <el-button
            class="send-btn"
            type="primary"
            :disabled="!inputMessage.trim() || isLoading"
            @click="sendMessage"
          >
            Send
            <i class="el-icon-s-promotion"></i>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      currentMood: "happy",
      inputMessage: "", // 修复变量名，与模板保持一致
      isLoading: false, // 添加缺失的isLoading变量
      messages: [
        // 添加初始欢迎消息
        {
          role: "assistant",
          content: "Hello! I'm your personal Meditation Assistant. I'm here to help you find inner peace and tranquility through personalized meditation experiences. I can generate custom meditation text, soothing images, and even create meditation videos tailored to your needs. Please share your current feelings, thoughts, or what you'd like to focus on during your meditation session today.",
          timestamp: new Date(),
          isGenerating: false,
        }
      ],
      sessionId: null, // 添加会话ID字段
      playingVideoUrl: null,
      moods: [
        { value: "happy", label: "Happy", emoji: "😊" },
        { value: "sad", label: "Sad", emoji: "😢" },
        { value: "angry", label: "Angry", emoji: "😠" },
        { value: "calm", label: "Calm", emoji: "😌" },
        { value: "excited", label: "Excited", emoji: "🤩" },
        { value: "tired", label: "Tired", emoji: "😴" },
      ],
    };
  },
  computed: {
    userId() {
      const user = JSON.parse(localStorage.getItem("user")) || {};
      return user?.uid;
    },
  },
  methods: {
    async sendMessage() {
      if (!this.inputMessage.trim() || this.isLoading) return;

      this.isLoading = true; // 设置加载状态

      const userMessage = {
        role: "user",
        content: this.inputMessage,
        mood: this.currentMood,
        timestamp: new Date(),
      };

      this.messages.push(userMessage);
      this.inputMessage = "";
      this.scrollToBottom();

      try {
        // Generate meditation text
        await this.generateMeditationText(userMessage);
      } finally {
        this.isLoading = false; // 确保加载状态被重置
      }
    },

    async generateMeditationText(userMessage) {
      // Add assistant message for text generation in progress
      const generatingMessage = {
        role: "assistant",
        content: "Generating personalized meditation text for you...",
        timestamp: new Date(),
        isGenerating: true,
      };

      this.messages.push(generatingMessage);
      this.scrollToBottom();

      try {
        // Call text generation API
        const generatedText = await this.requestGenerateText(userMessage.content);

        // Validate text validity
        if (!generatedText || typeof generatedText !== "string") {
          throw new Error("Invalid text returned from backend");
        }

        // Update message, remove generating state, add text and action buttons
        const messageIndex = this.messages.length - 1;
        this.$set(this.messages, messageIndex, {
          role: "assistant",
          content: generatedText,
          timestamp: new Date(),
          isGenerating: false,
          generatedText: generatedText, // Store the text for later use
          isGeneratingImage: false,
          isGeneratingVideo: false,
        });

        console.log("Generated text:", generatedText);
        this.$nextTick(() => this.scrollToBottom());
        this.$message.success("Meditation text generated successfully");
      } catch (error) {
        console.error("Text generation failed:", {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
        });

        // Update message to show error
        const messageIndex = this.messages.length - 1;
        this.$set(this.messages, messageIndex, {
          role: "assistant",
          content: "Sorry, text generation failed. Please try again later or resend your thoughts.",
          timestamp: new Date(),
          isGenerating: false,
          hasError: true,
        });

        this.$message.error(`Text generation failed: ${error.message || "Unknown error"}`);
      }
    },

    async generateImage(message, messageIndex) {
      this.$set(this.messages[messageIndex], 'isGeneratingImage', true);
      
      try {
        const imageUrl = await this.requestGenerateImage(message.generatedText);
        
        if (!imageUrl || typeof imageUrl !== "string") {
          throw new Error("Invalid image URL returned from backend");
        }
        
        this.$set(this.messages[messageIndex], 'imageUrl', imageUrl);
        this.$set(this.messages[messageIndex], 'isGeneratingImage', false);
        
        this.$message.success("Image generated successfully");
        this.$nextTick(() => this.scrollToBottom());
      } catch (error) {
        console.error("Image generation failed:", error);
        this.$set(this.messages[messageIndex], 'isGeneratingImage', false);
        this.$message.error(`Image generation failed: ${error.message || "Unknown error"}`);
      }
    },

    async generateVideo(message, messageIndex) {
      this.$set(this.messages[messageIndex], 'isGeneratingVideo', true);
      
      try {
        // Use existing image if available
        const imagePath = message.imageUrl ? message.imageUrl : null;
        const videoUrl = await this.requestGenerateVideo(message.generatedText, imagePath);
        
        if (!videoUrl || typeof videoUrl !== "string") {
          throw new Error("Invalid video URL returned from backend");
        }
        
        this.$set(this.messages[messageIndex], 'videoUrl', videoUrl);
        this.$set(this.messages[messageIndex], 'isGeneratingVideo', false);
        
        this.$message.success("Video generated successfully");
        this.$nextTick(() => this.scrollToBottom());
      } catch (error) {
        console.error("Video generation failed:", error);
        this.$set(this.messages[messageIndex], 'isGeneratingVideo', false);
        this.$message.error(`Video generation failed: ${error.message || "Unknown error"}`);
      }
    },

    async requestGenerateText(userPrompt) {
      const params = new FormData();
      params.append("userId", this.userId);
      params.append("mood", this.currentMood);
      params.append("content", userPrompt);

      const response = await axios.post(
        "/api/mood-logs/generateText",
        params,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      return response.data.text;
    },

    async requestGenerateImage(textContent) {
      const params = new FormData();
      params.append("userId", this.userId);
      params.append("textContent", textContent);
      // 添加sessionId参数
      if (this.sessionId) {
        params.append("sessionId", this.sessionId);
      }

      const response = await axios.post(
        "/api/mood-logs/generateImage",
        params,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      
      // 保存返回的sessionId
      if (response.data.sessionId) {
        this.sessionId = response.data.sessionId;
      }
      
      return response.data.imageUrl;
    },

    async requestGenerateVideo(textContent, imagePath = null) {
      const params = new FormData();
      params.append("userId", this.userId);
      params.append("textContent", textContent);
      if (imagePath) {
        params.append("imagePath", imagePath);
      }
      // 添加sessionId参数
      if (this.sessionId) {
        params.append("sessionId", this.sessionId);
      }

      const response = await axios.post(
        "/api/mood-logs/generateVideoFromText",
        params,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      
      // 保存返回的sessionId
      if (response.data.sessionId) {
        this.sessionId = response.data.sessionId;
      }
      
      return response.data.videoUrl;
    },

    // Reset state after video playback ends
    handleVideoEnded(message) {
      if (this.playingVideoUrl === message.videoUrl) {
        this.playingVideoUrl = null;
      }
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },

    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    renderMessage(content) {
      // Simple text rendering with line breaks
      return content.replace(/\n/g, "<br>");
    },

    getMoodType(mood) {
      const moodMap = {
        happy: "success",
        sad: "info",
        angry: "warning",
        calm: "primary",
        excited: "danger",
        tired: "info",
      };
      return moodMap[mood] || "primary";
    },

    getMoodEmoji(mood) {
      const foundMood = this.moods.find(m => m.value === mood);
      return foundMood ? foundMood.emoji : "😊";
    },

    getMoodText(mood) {
      const foundMood = this.moods.find(m => m.value === mood);
      return foundMood ? foundMood.label : mood;
    },
  },
};
</script>

<style scoped>
.meditation-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
}

.message {
  display: flex;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease-in;
}

.message.user {
  flex-direction: row-reverse;
}

.message.user .content {
  background: #007bff;
  color: white;
  margin-right: 12px;
  margin-left: 0;
}

.message.assistant .content {
  background: white;
  color: #333;
  margin-left: 12px;
  margin-right: 0;
}

.avatar {
  flex-shrink: 0;
}

.content {
  max-width: 70%;
  padding: 15px;
  border-radius: 18px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  font-size: 12px;
  opacity: 0.7;
}

.role {
  font-weight: 600;
}

.time {
  color: #999;
}

.mood-tag {
  margin-left: auto;
}

.text {
  line-height: 1.6;
  word-wrap: break-word;
}

.generating-text {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #666;
  font-style: italic;
}

.action-buttons {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.action-buttons .el-button {
  border-radius: 20px;
}

.image-container, .video-container {
  margin-top: 15px;
  text-align: center;
}

.input-area {
  padding: 20px;
  background: white;
  border-top: 1px solid #e9ecef;
}

.mood-selector {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.label {
  font-weight: 600;
  color: #333;
  white-space: nowrap;
}

.mood-option {
  display: flex;
  align-items: center;
  gap: 5px;
}

.mood-emoji {
  font-size: 16px;
}

.mood-label {
  font-size: 12px;
}

.input-box {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.input-box .el-textarea {
  flex: 1;
}

.send-btn {
  border-radius: 20px;
  padding: 10px 20px;
  height: auto;
}

.loading {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .meditation-container {
    padding: 10px;
  }
  
  .content {
    max-width: 85%;
  }
  
  .mood-selector {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .input-box {
    flex-direction: column;
    gap: 10px;
  }
  
  .send-btn {
    width: 100%;
  }
}
</style>

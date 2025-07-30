<template>
  <div class="mood-container">
    <div class="mood-card">
      <h2 class="date-title">{{ formatDate(currentDate) }}</h2>
      <form @submit.prevent="saveMoodLog" class="mood-form">
        <div class="mood-options">
          <label v-for="mood in moods" :key="mood.value" 
                 :class="['mood-option', { 'selected': selectedMood === mood.value }]">
            <input type="radio" v-model="selectedMood" :value="mood.value" :disabled="loading">
            <span class="mood-icon">{{ mood.icon }}</span>
            <span class="mood-label">{{ mood.label }}</span>
          </label>
        </div>
        
        <textarea
          v-model="content"
          placeholder="Write your mood diary for today..."
          :disabled="loading"
          class="mood-textarea"
        ></textarea>
        
        <button type="submit" :disabled="loading" class="save-button">
          {{ loading ? 'Saving...' : 'Save Diary' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedMood: 'happy',
      content: '',
      currentDate: this.$route.params.date,
      loading: false,
      moods: [
        { value: 'happy', label: 'Happy', icon: '😊' },
        { value: 'sad', label: 'Sad', icon: '😢' },
        { value: 'angry', label: 'Angry', icon: '😠' },
        { value: 'calm', label: 'Calm', icon: '😌' },
        { value: 'excited', label: 'Excited', icon: '😃' },
        { value: 'tired', label: 'Tired', icon: '😴' }
      ]
    };
  },
  // Rest of script remains unchanged
  computed: {
    userId() {
      const user = JSON.parse(localStorage.getItem('user')) || {};
      return user?.uid;
    }
  },
  methods: {
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    async fetchMoodLog() {
      if (!this.userId) {
        this.$message.warning('Please log in first');
        this.$router.push('/login');
        return;
      }

      try {
        const response = await this.axios.get('/api/mood-logs/date', {
          params: {
            userId: this.userId,
            date: this.currentDate
          }
        });

        if (response.data?.mood || response.data?.content) {
          this.selectedMood = response.data.mood || 'happy';
          this.content = response.data.content || '';
        }
      } catch (error) {
        if (error.response?.status !== 404) {
          console.error('Failed to fetch log:', error);
          this.$message.error('Failed to load log');
        }
      }
    },
    async saveMoodLog() {
      console.log("Save button clicked");
      try {
        this.loading = true;
        const response = await this.axios.post('/api/mood-logs', {
          userId: this.userId,
          logDate: this.currentDate,
          mood: this.selectedMood,
          content: this.content
        });

        console.log("Save response:", response);
        
        if (response.data && response.data.id) {
          this.$message.success('Saved successfully');
          setTimeout(() => {
            this.$router.push('/mood-calendar');
          }, 1000);
        } else {
          this.$message.warning('Saved successfully, but response data is abnormal');
        }
      } catch (error) {
        console.error('Save failed:', error);
        const errorMsg = error.response?.data?.message || 
                        error.message || 
                        'Save failed';
        this.$message.error(errorMsg);
      } finally {
        this.loading = false;
      }
    }
  },
  created() {
    this.fetchMoodLog();
  }
};
</script>

<style scoped>
.mood-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-image: url('https://images.unsplash.com/photo-1444080748397-f442aa95c3e5?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  padding: 20px;


}

.mood-card {
  background-color: rgba(255, 255, 255, 0.85);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  padding: 30px;
  width: 100%;
  max-width: 600px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.date-title {
  color: #333;
  text-align: center;
  margin-bottom: 30px;
  font-size: 1.8rem;
  font-weight: 500;
}

.mood-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mood-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.mood-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: rgba(255, 255, 255, 0.7);
  border: 2px solid transparent;
}

.mood-option:hover {
  background-color: rgba(240, 240, 240, 0.9);
}

.mood-option.selected {
  border-color: #409eff;
  background-color: rgba(64, 158, 255, 0.1);
}

.mood-icon {
  font-size: 2.5rem;
  margin-bottom: 8px;
}

.mood-label {
  font-size: 0.9rem;
  color: #555;
}

.mood-textarea {
  width: 100%;
  min-height: 200px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  resize: vertical;
  font-size: 1rem;
  line-height: 1.6;
  transition: border-color 0.3s;
  background-color: rgba(255, 255, 255, 0.8);
}

.mood-textarea:focus {
  border-color: #409eff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.save-button {
  padding: 12px 24px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  align-self: center;
  width: 50%;
}

.save-button:hover:not(:disabled) {
  background-color: #66b1ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.save-button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
  opacity: 0.7;
}

input[type="radio"] {
  display: none;
}
</style>
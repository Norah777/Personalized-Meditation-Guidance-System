<template>
  <div class="mood-calendar-container">
    <h1 class="calendar-title">Mood Calendar</h1>
    <div v-loading="loading" class="calendar-wrapper">
      <el-calendar ref="calendar" v-if="!loading">
        <template #dateCell="{ date }">
          <div 
            class="calendar-day-cell"
            @click.stop="handleDayClick(date)"
            :class="{ 
              'has-mood': getMoodForDate(date),
              'has-content': hasContentForDate(date)
            }"
          >
            <div class="day-number">{{ date.getDate() }}</div>
            <div 
              v-if="getMoodForDate(date)"
              :class="['mood-indicator', getMoodForDate(date)]"
            >
              {{ moodDisplayText[getMoodForDate(date)] }}
            </div>
            <div v-if="hasContentForDate(date)" class="content-indicator">📝</div>
          </div>
        </template>
      </el-calendar>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      moodEvents: [],
      moodDisplayText: {
        happy: '😊',
        sad: '😢',
        angry: '😠',
        calm: '😌',
        excited: '😃',
        tired: '😴'
      }
    }
  },
  computed: {
    userId() {
      const user = JSON.parse(localStorage.getItem('user')) || {};
      return user?.uid;
    }
  },
  methods: {
    async handleDayClick(date) {
      const dateStr = this.formatDate(date);
      const existingMood = this.getMoodForDate(date);

      try {
        await this.$router.push({
          name: 'MoodLogEditor',
          params: { date: dateStr },
          query: { mood: existingMood || '' }
        });
      } catch (error) {
        console.error('Route navigation failed:', error);
        this.$message.error('Cannot open edit page');
      }
    },

    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },

    getMoodForDate(date) {
      const dateStr = this.formatDate(date);
      const event = this.moodEvents.find(e => e.logDate === dateStr || e.date === dateStr);
      return event ? event.mood : null;
    },

    hasContentForDate(date) {
      const dateStr = this.formatDate(date);
      const event = this.moodEvents.find(e => e.logDate === dateStr || e.date === dateStr);
      return event && event.content && event.content.trim().length > 0;
    },

    async fetchCalendarData() {
      if (!this.userId) {
        this.$message.error('Please log in first');
        await this.$router.push('/login');
        return;
      }

      this.loading = true;
      try {
        const response = await this.axios.get('/api/mood-logs/calendar', {
          params: {
            userId: this.userId,
            year: new Date().getFullYear(),
            month: new Date().getMonth() + 1
          }
        });

        if (response.data.code === '0' || response.status === 200) {
          this.moodEvents = response.data.days || [];

        }
      } catch (error) {
        console.error('Failed to fetch calendar data:', error);
        this.$message.error('Failed to load calendar data');
      } finally {
        this.loading = false;
      }
    }
  },
  async created() {
    await this.fetchCalendarData();
  }
}
</script>

<style scoped>
.mood-calendar-container {
  padding: 30px;
  max-width: 1000px;
  margin: 20px auto;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.calendar-title {
  text-align: center;
  margin-bottom: 30px;
  color: #3a3a3a;
  font-size: 2rem;
  font-weight: 600;
  background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.calendar-wrapper {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.el-calendar {
  height: 650px;
  border-radius: 12px;
  border: none;
}

.el-calendar /deep/ .el-calendar__header {
  padding: 0 0 20px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 15px;
}

.el-calendar /deep/ .el-calendar__body {
  padding: 0;
}

.calendar-day-cell {
  height: 100%;
  padding: 8px;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  border-radius: 8px;
}

.calendar-day-cell:hover {
  background-color: rgba(100, 149, 237, 0.1);
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.calendar-day-cell.has-mood {
  background-color: rgba(100, 149, 237, 0.05);
}

.day-number {
  font-weight: bold;
  text-align: right;
  margin-bottom: 4px;
  font-size: 14px;
  color: #4a4a4a;
}

.mood-indicator {
  font-size: 20px;
  color: black;
  background: none;
  width: auto;
  height: auto;
  box-shadow: none;
}

.content-indicator {
  position: absolute;
  bottom: 4px;
  right: 4px;
  font-size: 12px;
  color: #6a11cb;
}

.happy { background-color: #67C23A; }
.sad { background-color: #909399; }
.angry { background-color: #F56C6C; }
.calm { background-color: #409EFF; }
.excited { background-color: #E6A23C; }
.tired { background-color: #8E44AD; }

/* Special styles for current date */
.el-calendar /deep/ .el-calendar-table td.is-today .calendar-day-cell {
  background-color: rgba(106, 17, 203, 0.1);
}

.el-calendar /deep/ .el-calendar-table td.is-today .day-number {
  color: #6a11cb;
  font-weight: 700;
}

/* Special styles for weekends */
.el-calendar /deep/ .el-calendar-table td.is-weekend .day-number {
  color: #F56C6C;
}
</style>
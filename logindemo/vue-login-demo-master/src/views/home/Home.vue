<template>
  <div>
    <!-- Add navigation menu -->
    <el-menu 
      :default-active="activeMenu" 
      mode="horizontal" 
      @select="handleMenuSelect"
      background-color="#f5f7fa"
      active-text-color="#409EFF">
      <el-menu-item index="home">Personal Home</el-menu-item>
      <el-menu-item index="mood-calendar">Mood Calendar</el-menu-item>
      <el-menu-item index="start-meditation">Start Meditation</el-menu-item>
    </el-menu>
     <h2>Welcome {{ user.uname }}! Your UID is {{ user.uid }}</h2>
    <el-button @click="logout" type="danger">Logout</el-button>
  </div>
  
</template>

<script>
export default {
  data() {
     return {
      user: {
        uname: "",
        uid: null,
      },
      activeMenu: 'home' // Default active menu item
    };
  },
  methods: {
    logout() {
      // 1. Clear user information from localStorage
      localStorage.removeItem('user');
      // 2. Navigate to login page
      this.$router.push('/login');
      // 3. Show logout success message (optional)
      this.$message.success('Logged out successfully');
    },
       // Menu selection handler
    handleMenuSelect(index) {
      if (index === 'mood-calendar') {
        this.$router.push('/mood-calendar');
      } 
      else if (index === 'start-meditation'){
        this.$router.push('/start-meditation');
      }
      else if (index === 'home') {
        this.$router.push('/home');
      }
    },
  },
  mounted() {
    // Load user information from localStorage
    const storedUser = JSON.parse(localStorage.getItem('user'));
    if (storedUser && storedUser.uid) {
      this.user = storedUser;
    } else {
      // If not logged in, force redirect to login page
      this.$router.push('/login');
      this.$message.warning('Please log in first!');
    }
    // Set active menu item based on current route
    const routePath = this.$route.path;
    if (routePath.includes('mood-calendar')) {
      this.activeMenu = 'mood-calendar';
    }
    else if(routePath.includes('start-meditation')) {
      this.activeMenu = 'start-meditation';
    } else {
      this.activeMenu = 'home';
    }
  }
};
</script>

<style scoped>
/* Add some basic styles */
h2 {
  color: #409EFF;
  margin-bottom: 10px;
}

.button-group .el-button {
  margin-right: 10px;
}

/* Menu style adjustments */
.el-menu {
  margin-bottom: 40px;
}
</style>
<template>
  <div>
    <el-card class="box-card">
      <h2>Login</h2>
      <el-form
        :model="ruleForm"
        status-icon
        :rules="rules"
        ref="ruleForm"
        label-position="left"
        label-width="70px"
        class="login-from"
      >
        <el-form-item label="Username" prop="uname">
          <el-input v-model="ruleForm.uname"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input
            type="password"
            v-model="ruleForm.password"
            autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <div class="btnGroup">
        <el-button
          type="primary"
          @click="submitForm('ruleForm')"
          v-loading="loading"
          >Login</el-button
        >
        <el-button @click="resetForm('ruleForm')">Reset</el-button>
        <router-link to="/register">
          <el-button style="margin-left: 10px">Register</el-button>
        </router-link>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ruleForm: {
        uname: "",
        password: "",
      },
      rules: {
        uname: [
          { required: true, message: "Username cannot be empty!", trigger: "blur" },
        ],
        password: [
          { required: true, message: "Password cannot be empty!", trigger: "blur" },
        ],
      },
      loading: false, // Whether to show loading animation
    };
  },
  methods: {
    async submitForm(formName) {
  this.$refs[formName].validate(async valid => {
    if (!valid) return;

    this.loading = true;
    try {
      const params = new URLSearchParams();
      params.append('uname', this.ruleForm.uname);
      params.append('password', this.ruleForm.password);

      const res = await this.axios({
        url: '/api/user/login',
        method: 'post',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: params
      });

      if (res.data.code === '0') {
        // ✅ Login successful, save user info and redirect
        const user = {
          uid: res.data.data.uid,
          uname: res.data.data.uname
        };
        localStorage.setItem('user', JSON.stringify(user));
        this.$router.push('/home');
      } else {
        this.$message.error(res.data.msg || 'Login failed');
      }
    } catch (error) {
      console.error('Login failed:', error);
      this.$message.error('Network or server error');
    } finally {
      this.loading = false;
    }
  });
}



}
};
</script>

<style scoped>
/* Center login panel with 400px width */
.box-card {
  margin: auto auto;
  width: 400px;
}
/* Center the form within login panel */
.login-from {
  margin: auto auto;
}
</style>
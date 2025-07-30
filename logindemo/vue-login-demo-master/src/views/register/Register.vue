<template>
  <div>
    <el-card class="box-card">
      <h2>Register</h2>
      <el-form
        :model="ruleForm"
        status-icon
        :rules="rules"
        ref="ruleForm"
        label-position="left"
        label-width="80px"
        class="demo-ruleForm"
      >
        <el-form-item label="Username" prop="uname">
          <el-input v-model="ruleForm.uname"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="pass">
          <el-input
            type="password"
            v-model="ruleForm.pass"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="Confirm Password" prop="password">
          <el-input
            type="password"
            v-model="ruleForm.password"
            autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <div class="btnGroup">
        <el-button type="primary" @click="submitForm('ruleForm')"  v-loading="loading"
          >Submit</el-button
        >
        <el-button @click="resetForm('ruleForm')">Reset</el-button>
        <el-button @click="goBack">Back</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please enter password"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please enter password again"));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error("Password confirmation does not match!"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        uname: "",
        pass: "",
        password: "",
      },
      rules: {
        uname: [
          { required: true, message: "Username cannot be empty!", trigger: "blur" },
        ],
        pass: [{ required: true, validator: validatePass, trigger: "blur" }],
        password: [
          { required: true, validator: validatePass2, trigger: "blur" },
        ],
      },
      loading: false
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        this.loading = true;  // Show loading animation on submit button
        if (valid) {
          let _this = this;
          this.axios({     // axios makes request to backend
            url: "/api/user/register",  // Request URL
            method: "post",             // Request method
            headers: {                  // Request headers
              "Content-Type": "application/json",
            },
            data: { // Request parameters, using data, different from login params
              uname: _this.ruleForm.uname,
              password: _this.ruleForm.password,
            },
          }).then((res) => { // Execute code in brackets when receiving backend response, res is response info
            if (res.data.code === '0') {  // When response code is 0, registration successful
              // Display backend success message
              this.$message({
                message: res.data.msg,
                type: "success",
              });
            }else{  // When response code is not 0, registration failed
              // Display backend failure message
              this.$message({
                message: res.data.msg,
                type: "warning",
              });
            }
            // Whether success or failure, stop loading animation after receiving backend response
            _this.loading = false;
            console.log(res);
          });
        } else { // If username or password is empty, show required message without backend request
          console.log("error submit!!");
          this.loading = false;
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    goBack() {
      this.$router.go(-1);
    },
  },
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
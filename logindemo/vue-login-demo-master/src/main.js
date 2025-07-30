import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import VueRouter from 'vue-router'
import router from './router'  // 你的路由配置
import axios from 'axios'
import VueAxios from 'vue-axios'


Vue.prototype.$axios = axios
// 关闭生产提示
Vue.config.productionTip = false

// 注册插件
Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(VueAxios, axios)

// 初始化用户状态（可选）
const user = JSON.parse(localStorage.getItem('user'))
if (user) {
  console.log('检测到已登录用户:', user)  // 调试用
}

// 创建 Vue 实例
new Vue({
  render: h => h(App),
  router,  // 注入路由
  // 不再需要 store
}).$mount('#app')
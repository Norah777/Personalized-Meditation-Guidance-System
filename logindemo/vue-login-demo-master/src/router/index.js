// 此文件专门负责项目的路由

import VueRouter from "vue-router"

// 引入组件
import Login from '../views/login/Login'
import Register from '../views/register/Register'
import Home from '../views/home/Home'
import { Message } from "element-ui";
import MoodCalendar from '../views/mood-calendar/MoodCalendar.vue';  // @表示src目录
import MoodLogEditor from '../views/mood-log/MoodLogEditor.vue';
import StartMeditation from '../views/start-meditation/StartMeditation.vue';
// 创建并暴露一个路由器
const router = new VueRouter({
    mode: 'history',    // 路由模式，该模式不会在地址中显示井号#
    routes: [
        {
            path: '/',          // 路径
            redirect: '/login'  // 重定向
        },
        {
            path: '/login',     // 路径
            component: Login    // 跳转到的组件
        },
        {
            path: '/register',     // 路径
            component: Register    // 跳转到的组件
        },
        {
            path: '/home',     // 路径
            component: Home    // 跳转到的组件
        },
        {
            path: '/mood-calendar',
            name: 'MoodCalendar',
            component: MoodCalendar
        },
        {
            path: '/mood-log/:date',  // :date是动态参数
            name: 'MoodLogEditor',
            component: MoodLogEditor,
            props: true  // 将路由参数作为props传递给组件
        },
        {
            path: '/start-meditation',
            name: 'StartMeditation',
            component: StartMeditation
        },
    ]
})

// 路由守卫：仅依赖 localStorage
router.beforeEach((to, from, next) => {
    const user = JSON.parse(localStorage.getItem('user')) // 直接读 localStorage
    const isAuthenticated = !!user?.uid // 检查 uid 是否存在
  
    if (to.matched.some(route => route.meta.requiresAuth) && !isAuthenticated) {
      next('/login')
      Message.warning('请先登录！')
    } else {
      next()
    }
  })
  
export default router;
import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import ChatView from '../views/ChatView.vue'
import SecretView from '../views/SecretView.vue'

const router = createRouter({
  // 使用 HTML5 历史模式，URL 中没有丑陋的 #
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      // :secretCode 是动态路由参数，这样就能通过 URL 传递彩蛋密码了
      path: '/secret/:secretCode',
      name: 'secret',
      component: SecretView,
      props: true // 允许将 secretCode 作为 prop 直接传给 SecretView
    }
  ]
})

export default router
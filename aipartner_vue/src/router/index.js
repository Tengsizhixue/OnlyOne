import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import ChatView from '../views/ChatView.vue'
import SecretView from '../views/SecretView.vue'
import FinalView from '../views/secrets/FinalView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView
    },
    {
      // 🌟 核心修复：还原成单层路由，彻底消除缺失 component 的黄色警告
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/secret/:secretCode',
      name: 'secret',
      component: SecretView,
      props: true
    },
    {
      path: '/final',
      name: 'final',
      component: FinalView
    }
  ]
})

export default router
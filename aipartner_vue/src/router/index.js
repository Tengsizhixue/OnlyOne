import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import ChatView from '../views/ChatView.vue'
import SecretView from '../views/SecretView.vue'
import FinalView from '../views/secrets/FinalView.vue' // 💡 引入终局页面

const router = createRouter({
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
      path: '/secret/:secretCode',
      name: 'secret',
      component: SecretView,
      props: true
    },
    {
      // 💡 注册终局路由
      path: '/final',
      name: 'final',
      component: FinalView
    }
  ]
})

export default router
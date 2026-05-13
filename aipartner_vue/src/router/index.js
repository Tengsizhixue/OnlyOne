import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      // 🌟 优化：使用动态 import() 实现路由懒加载，极大缩小首屏 JS 体积
      component: () => import('../views/LandingView.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/ChatView.vue')
    },
    {
      path: '/secret/:secretCode',
      name: 'secret',
      component: () => import('../views/SecretView.vue'),
      props: true
    },
    {
      path: '/final',
      name: 'final',
      component: () => import('../views/secrets/FinalView.vue')
    }
  ]
})

export default router
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 1. 引入 Element Plus 组件库
import ElementPlus from 'element-plus'
// 2. 【最关键的一步】引入 Element Plus 的全局 CSS 样式表！
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(router)
// 3. 告诉 Vue 使用 Element Plus
app.use(ElementPlus)

app.mount('#app')
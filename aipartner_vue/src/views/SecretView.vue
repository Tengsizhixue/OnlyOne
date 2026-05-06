<template>
  <div class="secret-root-container">

    <!-- Vue 提供的高级动态组件特性：根据 currentComponent 自动加载对应文件 -->
    <component
      v-if="currentComponent"
      :is="currentComponent"
      @back="handleBack"
    />

    <!-- 兜底页面：当代码是 111111 或找不到对应页面时，显示默认界面 -->
    <div v-else class="secret-page glass-panel shadow-2xl">
      <div class="secret-content">
        <h1 class="highlight-text">🎉 恭喜你找到了特殊页面！</h1>
        <p>但是这里什么都没有，如果你后面发现了其他特殊的数字，可以试一试在对话框里输入</p>
        <br/>
        <button class="enter-btn shimmer-btn" @click="handleBack">返回聊天</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

// 1. 引入我们刚刚分离出去的独立组件
import LiHongBaoView from './secrets/LiHongBaoView.vue'
import GameMemoryView from './secrets/GameMemoryView.vue'
import AstlibraView from './secrets/AstlibraView.vue'
import VioletLetterView from './secrets/VioletLetterView.vue'
import MusicView from './secrets/MusicView.vue'
import GameView from './secrets/GameView.vue'

const props = defineProps({
  secretCode: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['back'])

// 💡 规范化事件传递，确保必定触发外层的返回动作
const handleBack = () => {
  emit('back')
}

// 2. 核心路由表：密码对应的页面
const viewMap = {
  '260315': LiHongBaoView,
  '251027': GameMemoryView,
  '260410': AstlibraView,
  '19xxxx': VioletLetterView,
  '240802': MusicView,
  '180818': GameView
}

// 3. 计算当前应该渲染哪一个组件
const currentComponent = computed(() => {
  return viewMap[props.secretCode] || null
})
</script>

<style scoped>
/* 💡 核心修复：添加根容器样式，确保不会影响内部元素的绝对居中与排版，且动画执行时不会挤压空间 */
.secret-root-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  position: absolute; /* 防止切换时占据文档流 */
  top: 0;
  left: 0;
}

/* 兜底界面的独立样式 */
.secret-page {
  width: 90vw; max-width: 800px; padding: 60px;
  text-align: center; border-radius: 24px; z-index: 100;
  color: white;
}
.secret-content {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.highlight-text { color: #a78bfa; margin-bottom: 20px; }
</style>
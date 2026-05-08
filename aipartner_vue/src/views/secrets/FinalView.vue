<template>
  <div class="final-container">
    <div class="final-content glass-panel shadow-2xl">
      <h1 class="highlight-text">🎉 终局之门</h1>

      <div class="story-box">
        <p>恭喜你，沿着这些神秘的数字，找齐了所有失落的记忆拼图。</p>
        <p>（这是结尾页面的示例，你可以后续自由设计这里的排版、动画、甚至放一段通关视频......）</p>
      </div>

      <button class="enter-btn shimmer-btn" @click="goHome">
        返回现实 (主页)
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.final-container {
  width: 100vw; height: 100vh; display: flex; justify-content: center; align-items: center;
  position: absolute; top: 0; left: 0; z-index: 1000;
  background-color: rgba(15, 23, 42, 0.9);
}
.final-content {
  width: 90vw; max-width: 800px; padding: 60px; text-align: center; border-radius: 24px;
}
.highlight-text {
  color: #fbbf24; font-size: 42px; margin-bottom: 30px; text-shadow: 0 0 20px rgba(251, 191, 36, 0.4);
}
.story-box {
  background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 30px; border-radius: 16px; margin-bottom: 40px; color: #f8fafc;
  font-size: 18px; line-height: 2;
}
@media (max-width: 768px) {
  .final-content { padding: 40px 20px; }
  .highlight-text { font-size: 32px; }
  .story-box { font-size: 15px; }
}
</style>
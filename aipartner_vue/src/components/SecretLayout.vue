<template>
  <div class="secret-view-container">
    <div class="secret-bg" :style="{ backgroundImage: `url(${bgImage})` }"></div>

    <!-- 💡 新增的浮动任务面板 -->
    <div class="quest-floating-widget glass-panel shadow-lg">
      <div class="quest-header">
        <el-icon><Compass /></el-icon> 命运的指引
      </div>
      <div class="quest-body">
        <p v-if="currentQuest" class="quest-text">{{ currentQuest.question }}</p>
        <p v-else class="quest-text success">✨ 所有的拼图已集齐...</p>
      </div>
    </div>

    <div class="secret-page shadow-2xl">
      <div class="secret-content">
        <h1 class="highlight-text" :style="{ color: titleColor }">{{ title }}</h1>
        <p class="subtitle">恭喜你找到：{{ code }}</p>

        <slot :openImage="openImage"></slot>

        <!-- 💡 动态按钮文案：如果全通关了，按钮变成前往结局 -->
        <button class="enter-btn shimmer-btn" @click="$emit('back')">
          {{ isAllUnlocked ? '开启终局之门 ✨' : '返回聊天' }}
        </button>
      </div>
    </div>

    <transition name="fade">
      <div v-if="previewImage" class="image-preview-overlay" @click="closeImage">
        <el-icon class="close-preview-btn"><Close /></el-icon>
        <img :src="previewImage" class="preview-img" />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Close, Compass } from '@element-plus/icons-vue'
// 💡 引入解密状态
import { currentQuest, isAllUnlocked } from '../store/questState.js'

defineProps({
  bgImage: { type: String, required: true },
  title: { type: String, required: true },
  titleColor: { type: String, default: '#f8fafc' },
  code: { type: String, required: true }
})

defineEmits(['back'])

const previewImage = ref('')
const openImage = (url) => { previewImage.value = url }
const closeImage = () => { previewImage.value = '' }
</script>

<style scoped>
/* ========== 原有样式保持不变 ========== */
.secret-view-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
.secret-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: #050505; background-size: cover; background-position: center; filter: brightness(0.65); z-index: -1; pointer-events: none; }
.secret-page { width: 95vw; max-width: 1200px; height: 90vh; padding: 40px 60px; text-align: center; border-radius: 24px; z-index: 1; color: #f8fafc; background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.3); display: flex; flex-direction: column; }
.secret-content { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; }
.highlight-text { margin-bottom: 10px; font-size: 32px; font-weight: bold; flex-shrink: 0; }
.subtitle { color: #94a3b8; font-family: monospace; margin-bottom: 20px; letter-spacing: 2px; flex-shrink: 0; }
.enter-btn { flex-shrink: 0; }
.image-preview-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); z-index: 9999; display: flex; justify-content: center; align-items: center; cursor: zoom-out; }
.preview-img { max-width: 90%; max-height: 90%; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.close-preview-btn { position: absolute; top: 30px; right: 30px; font-size: 36px; color: rgba(255, 255, 255, 0.7); cursor: pointer; transition: all 0.3s; }
.close-preview-btn:hover { transform: scale(1.1); color: #fff; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* 💡 新增的悬浮任务面板样式 */
.quest-floating-widget {
  position: absolute; top: 30px; right: 30px; width: 300px; padding: 16px 20px;
  border-radius: 16px; z-index: 50; background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px); border: 1px solid rgba(167, 139, 250, 0.4); color: #f8fafc;
}
.quest-header { font-size: 14px; font-weight: bold; color: #a78bfa; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;}
.quest-text { font-size: 15px; margin: 0; line-height: 1.5; }
.quest-text.success { color: #34d399; font-weight: bold;}

@media (max-width: 768px) {
  .secret-page { width: 100vw; height: 100dvh; border-radius: 0; padding: 90px 20px 80px; border: none; background: rgba(15, 23, 42, 0.3); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
  .highlight-text { font-size: 24px; margin-bottom: 6px; }
  .subtitle { font-size: 12px; margin-bottom: 16px; }

  /* 移动端悬浮框置顶 */
  .quest-floating-widget {
    top: 10px; left: 10px; right: 10px; width: auto; padding: 12px 16px;
  }
}
</style>
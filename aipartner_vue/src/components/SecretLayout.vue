<template>
  <div class="secret-view-container">
    <div class="secret-bg" :style="{ backgroundImage: `url(${bgImage})` }"></div>

    <div class="secret-page shadow-2xl">
      <div class="secret-content">
        <h1 class="highlight-text" :style="{ color: titleColor }">{{ title }}</h1>
        <p class="subtitle">恭喜你找到：{{ code }}</p>

        <!-- 💡 核心修复：使用作用域插槽，将 openImage 方法暴露给父组件 -->
        <slot :openImage="openImage"></slot>

        <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
      </div>
    </div>

    <!-- 公共的图片预览功能 -->
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
import { Close } from '@element-plus/icons-vue'

defineProps({
  bgImage: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  titleColor: {
    type: String,
    default: '#f8fafc'
  },
  code: {
    type: String,
    required: true
  }
})

defineEmits(['back'])

// 统一管理图片预览逻辑
const previewImage = ref('')
const openImage = (url) => { previewImage.value = url }
const closeImage = () => { previewImage.value = '' }
</script>

<style scoped>
/* ========== 这里集中了所有彩蛋页面的公共样式 ========== */
.secret-view-container {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; justify-content: center; align-items: center;
}
.secret-bg {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background-color: #050505;
  background-size: cover; background-position: center;
  filter: brightness(0.65); z-index: -1; pointer-events: none;
}
.secret-page {
  width: 95vw; max-width: 1200px; height: 90vh;
  padding: 40px 60px; text-align: center; border-radius: 24px; z-index: 1; color: #f8fafc;
  background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.3);
  display: flex; flex-direction: column;
}
.secret-content { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; }
.highlight-text { margin-bottom: 10px; font-size: 32px; font-weight: bold; flex-shrink: 0; }
.subtitle { color: #94a3b8; font-family: monospace; margin-bottom: 20px; letter-spacing: 2px; flex-shrink: 0; }
.enter-btn { flex-shrink: 0; }

/* 💡 图片预览遮罩与动画样式 */
.image-preview-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px);
  z-index: 9999; display: flex; justify-content: center; align-items: center;
  cursor: zoom-out;
}
.preview-img {
  max-width: 90%; max-height: 90%; border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.close-preview-btn {
  position: absolute; top: 30px; right: 30px; font-size: 36px;
  color: rgba(255, 255, 255, 0.7); cursor: pointer; transition: all 0.3s;
}
.close-preview-btn:hover { transform: scale(1.1); color: #fff; }

.fade-enter-active,
.fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }

/* 💡 移动端公共排版 */
@media (max-width: 768px) {
  .secret-page {
    width: 100vw; height: 100dvh; border-radius: 0;
    padding: 50px 20px 80px; border: none;
    background: rgba(15, 23, 42, 0.3);
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  }
  .highlight-text { font-size: 24px; margin-bottom: 6px; }
  .subtitle { font-size: 12px; margin-bottom: 16px; }
}
</style>
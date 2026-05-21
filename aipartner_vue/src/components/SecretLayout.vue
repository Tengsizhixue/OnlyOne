<template>
  <div class="secret-view-container">
    <div class="secret-bg" :style="{ backgroundImage: `url(${bgImage})` }"></div>

    <div class="secret-page shadow-2xl">
      <div class="secret-content">
        <h1 class="highlight-text" :style="{ color: titleColor }">{{ title }}</h1>
        <p class="subtitle">恭喜你找到：{{ code }}</p>

        <!-- 将控制逻辑下放到插槽中，以便在每个文本的最末尾使用按钮 -->
        <slot :openImage="openImage" :back="() => $emit('back')"></slot>
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
import { Close } from '@element-plus/icons-vue'

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
.secret-view-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
.secret-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: #050505; background-size: cover; background-position: center; filter: brightness(0.65); z-index: -1; pointer-events: none; }

.secret-page {
  width: 95vw; max-width: 1200px; height: 90vh; padding: 40px 60px; text-align: center; border-radius: 24px; z-index: 1; color: #f8fafc;
  background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.3);
  display: flex; flex-direction: column; box-sizing: border-box;
}

.secret-content {
  flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; width: 100%; overflow: hidden;
}

.highlight-text { margin-bottom: 10px; font-size: 32px; font-weight: bold; flex-shrink: 0; }
.subtitle { color: #94a3b8; font-family: monospace; margin-bottom: 20px; letter-spacing: 2px; flex-shrink: 0; }

.image-preview-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); z-index: 9999; display: flex; justify-content: center; align-items: center; cursor: zoom-out; }
.preview-img { max-width: 90%; max-height: 90%; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.close-preview-btn { position: absolute; top: 30px; right: 30px; font-size: 36px; color: rgba(255, 255, 255, 0.7); cursor: pointer; transition: all 0.3s; }
.close-preview-btn:hover { transform: scale(1.1); color: #fff; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .secret-page {
    width: 100%; height: 100dvh; border-radius: 0;
    padding: 1px 20px 20px; border: none; background: rgba(15, 23, 42, 0.3); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  }
  .highlight-text { font-size: 22px; margin-bottom: 6px; }
  .subtitle { font-size: 12px; margin-bottom: 16px; }
}
</style>
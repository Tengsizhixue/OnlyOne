<template>
  <div class="background-container">
    <!-- 独立出背景图片层，平滑预加载防闪屏 -->
    <div class="bg-image-layer" :style="customBgStyle" :class="{ 'show-bg': !isLanding && hasCustomBg }"></div>

    <!-- 🚀 全局动态极光流体背景 (在没有静态壁纸时显示) 🚀 -->
    <div class="dynamic-bg" :class="{ 'hide-bg': !isLanding && hasCustomBg }">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="orb orb-4"></div>
      <!-- 添加一层细腻的噪点纹理，提升高级质感 -->
      <div class="noise-overlay"></div>
    </div>
  </div>
</template>

<script setup>
// 接收父组件 App.vue 传过来的状态
defineProps({
  isLanding: {
    type: Boolean,
    default: true
  },
  hasCustomBg: {
    type: Boolean,
    default: false
  },
  customBgStyle: {
    type: Object,
    default: () => ({})
  }
})
</script>

<style scoped>
.background-container {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  z-index: 0; pointer-events: none;
}
.bg-image-layer {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background-size: cover; background-position: center; background-repeat: no-repeat;
  opacity: 0; z-index: 0; pointer-events: none;
  transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
.bg-image-layer.show-bg {
  opacity: 1;
}

.dynamic-bg {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  overflow: hidden; z-index: 0;
  transition: opacity 1.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.dynamic-bg.hide-bg {
  opacity: 0;
}

.noise-overlay {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.04; z-index: 1; pointer-events: none;
}
.orb {
  position: absolute; border-radius: 50%;
  filter: blur(80px); opacity: 0.7;
  animation: aurora 20s infinite alternate ease-in-out;
  transition: background 1.5s ease;
  will-change: transform;
}
.orb-1 { width: 50vw; height: 50vw; top: -10%; left: -10%; animation-duration: 25s; }
.orb-2 { width: 45vw; height: 45vw; bottom: -20%; right: -10%; animation-duration: 22s; animation-delay: -5s; }
.orb-3 { width: 35vw; height: 35vw; top: 40%; left: 60%; animation-duration: 28s; animation-delay: -10s; }
.orb-4 { width: 40vw; height: 40vw; bottom: 20%; left: -20%; animation-duration: 30s; animation-delay: -15s; }

@keyframes aurora {
  0% { transform: translate(0, 0) scale(1) rotate(0deg); }
  33% { transform: translate(15%, -10%) scale(1.1) rotate(45deg); }
  66% { transform: translate(-10%, 15%) scale(0.9) rotate(-30deg); }
  100% { transform: translate(5%, -5%) scale(1.15) rotate(15deg); }
}
</style>
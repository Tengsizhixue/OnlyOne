<template>
  <!-- 新增：最外层包裹容器，建立独立的层级上下文 -->
  <div class="secret-view-container">

    <!-- 修改：全屏背景层被提取到了卡片外面，不再受毛玻璃属性的约束 -->
    <div class="secret-bg"></div>

    <div class="secret-page shadow-2xl">
      <div class="secret-content">
        <h1 class="highlight-text" style="color: #fbbf24;">⚖️ 神之天平的隐秘画卷</h1>
        <p class="subtitle">特殊代码认证：260410</p>
        <div class="content-box">
          <p>这里是《神之天平》的专属展示页面。</p>
          <p>（后续内容待设计：留给这款让你印象深刻的游戏...）</p>
        </div>
        <button class="enter-btn shimmer-btn" @click="handleBack">返回聊天</button>
      </div>
    </div>

  </div>
</template>

<script setup>
const emit = defineEmits(['back'])

const handleBack = () => {
  emit('back')
}
</script>

<style scoped>
/* ================= 新增：外层容器样式 ================= */
.secret-view-container {
  position: relative; /* 建立全新的堆叠上下文 */
  z-index: 10;        /* 确保这整个页面完全盖住外面的 App.vue 角色背景 */
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* ================= 修改：背景层样式 ================= */
.secret-bg {
  position: absolute; /* 相对于充满全屏的父容器 */
  top: 0; left: 0; width: 100%; height: 100%;
  /* 神之天平主题临时占位图：天平/奇幻/天空 */
  background-image: url('https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?auto=format&fit=crop&w=2000&q=80');
  background-size: cover; background-position: center;
  filter: brightness(0.35);
  z-index: -1; /* 垫底，但只在当前界面的上下文里垫底 */
  pointer-events: none;
}

/* ================= 原有：卡片样式 (去掉了 z-index: 100，因为外层已经接管) ================= */
.secret-page {
  width: 90vw; max-width: 800px; padding: 40px 60px; text-align: center; border-radius: 24px;
  z-index: 1; color: #f8fafc; max-height: 90dvh; overflow-y: auto;
  background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
.secret-page::-webkit-scrollbar { width: 6px; }
.secret-page::-webkit-scrollbar-track { background: transparent; }
.secret-page::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 4px; }
.secret-content { display: flex; flex-direction: column; align-items: center; justify-content: center; }
.highlight-text { margin-bottom: 10px; font-size: 28px; }
.subtitle { color: #94a3b8; font-family: monospace; margin-bottom: 30px; letter-spacing: 2px; }
.content-box { background: rgba(0, 0, 0, 0.35); border: 1px solid rgba(255, 255, 255, 0.1); padding: 40px; border-radius: 16px; margin-bottom: 40px; width: 100%; min-height: 200px; display: flex; flex-direction: column; justify-content: center; }
</style>
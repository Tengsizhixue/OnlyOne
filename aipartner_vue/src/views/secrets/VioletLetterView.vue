<template>
  <div class="secret-page shadow-2xl">
    <div class="secret-bg"></div>

    <div class="secret-content">
      <h1 class="highlight-text" style="color: #c084fc;">✉️ 无名信件的归宿</h1>
      <p class="subtitle">特殊代码认证：19xxxx</p>
      <div class="content-box">
        <p>这里是薇尔莉特为你寄来的专属信件空间。</p>
        <p>（后续内容待设计：可以放入你想展示的动漫截图、感人信件文本等...）</p>
      </div>
      <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
    </div>
  </div>
</template>

<script setup>
defineEmits(['back'])
</script>

<style scoped>
.secret-bg {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  /* 信件主题临时占位图：复古信件/打字机 */
  background-image: url('https://images.unsplash.com/photo-1577401239170-897942555fb3?auto=format&fit=crop&w=2000&q=80');
  background-size: cover; background-position: center;
  filter: brightness(0.35);
  z-index: -1; pointer-events: none;
}
.secret-page {
  width: 90vw; max-width: 800px; padding: 40px 60px; text-align: center; border-radius: 24px;
  z-index: 100; color: #f8fafc; max-height: 90dvh; overflow-y: auto;
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
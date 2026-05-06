<template>
  <div class="secret-view-container">
    <div class="secret-bg"></div>

    <div class="secret-page shadow-2xl">
      <div class="secret-content">
        <h1 class="highlight-text" style="color: #fbbf24;">⚔️ 游戏冒险的彼岸</h1>
        <p class="subtitle">特殊代码认证：180818</p>
        <div class="content-box">
          <p>这里是游戏的专属展示页面。</p>
          <p>（后续内容待设计：留给这款让你印象深刻的游戏...）</p>
        </div>
        <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(['back'])
</script>

<style scoped>
.secret-view-container {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; justify-content: center; align-items: center;
}
.secret-bg {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background-color: #050505;
  background-image: url('https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=2000&q=80');
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
.content-box {
  background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 40px; border-radius: 16px; margin-bottom: 30px; width: 100%;
  flex: 1; overflow-y: auto;
  display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
  font-size: 16px; line-height: 1.8;
}
.content-box::-webkit-scrollbar { width: 8px; }
.content-box::-webkit-scrollbar-track { background: transparent; }
.content-box::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 4px; }
.content-box::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }
.enter-btn { flex-shrink: 0; }

@media (max-width: 768px) {
  .secret-page {
    width: 100vw;
    height: 100dvh; /* 适配手机的动态高度 */
    border-radius: 0;
    /* 增加顶部的呼吸空间，底部留白更自然 */
    padding: 50px 20px 80px;
    border: none;
    /* 手机端进一步调低背景板透明度 */
    background: rgba(20, 10, 25, 0.3);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }
  .music-room .story-box {
    /* 缩小文字框内边距、优化行高、加大圆角让其更像一个浮窗卡片 */
    padding: 18px;
    font-size: 14px;
    margin-bottom: 20px;
    border-radius: 12px;
    line-height: 1.8;
  }
  .highlight-text { font-size: 24px; margin-bottom: 6px; }
  .subtitle { font-size: 12px; margin-bottom: 16px; }
}
</style>
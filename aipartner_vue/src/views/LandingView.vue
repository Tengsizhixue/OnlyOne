<template>
  <div class="landing-page">
    <el-scrollbar class="landing-scrollbar">
      <div class="landing-content glass-panel shadow-2xl floating-panel">
        <div class="landing-header">
          <div class="landing-icon pulse-icon">
            <img src="https://api.dicebear.com/9.x/bottts-neutral/svg?seed=AI" alt="AI Logo" class="landing-img" />
          </div>
          <h1 class="landing-title">正在开发，未完成</h1>
        </div>

        <div class="features-grid">
          <div class="feature-card glass-card hover-lift">
            <el-icon class="feature-icon"><User /></el-icon>
            <h3>角色丰富</h3>
            <p>这次的每个人物我都设计了特殊问答，问对问题会带有独特身份码</p>
          </div>
          <div class="feature-card glass-card hover-lift">
            <el-icon class="feature-icon"><ColdDrink /></el-icon>
            <h3>特殊会话</h3>
            <p>我会把以前我没删掉并且也没发过的内容放进特殊会话里</p>
          </div>
          <div class="feature-card glass-card hover-lift">
            <el-icon class="feature-icon"><Sugar /></el-icon>
            <h3>ui优化</h3>
            <p>换了个前端，这次的ui设计会比上次稍微好看些</p>
          </div>
        </div>

        <div class="scenario-section">
          <h3 class="scenario-title">我的一些想法</h3>
          <div class="scenario-tags">
            <span class="scenario-tag">后面不一定更</span>
            <span class="scenario-tag">太耗时间</span>
            <span class="scenario-tag">没什么更好的想法</span>
            <span class="scenario-tag">功能多了代码太复杂</span>
            <span class="scenario-tag">没什么能分享的</span>
          </div>
        </div>

        <!-- 点击后触发事件，通知外层 App.vue 切换页面 -->
        <button class="enter-btn shimmer-btn" @click="$emit('enter-chat')">
          <span class="btn-text">打开交流界面</span>
          <el-icon class="enter-icon"><ArrowRight /></el-icon>
        </button>
      </div>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { User, ColdDrink, Sugar, ArrowRight } from '@element-plus/icons-vue'

// 声明对外暴露的事件
defineEmits(['enter-chat'])
</script>

<style scoped>
.landing-page { position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: center; z-index: 100; overflow: hidden; }
.landing-scrollbar { height: 100%; width: 100%; z-index: 10; }
:deep(.el-scrollbar__wrap) { display: flex; align-items: center; justify-content: center; }
.floating-panel { animation: float-panel 6s ease-in-out infinite; }
@keyframes float-panel { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
.landing-content { text-align: center; padding: 50px 60px; border-radius: 30px; max-width: 800px; margin: 40px auto; transition: all 0.6s ease; }
.landing-header { margin-bottom: 40px; }
.pulse-icon { animation: pulse-ring 2.5s infinite cubic-bezier(0.215, 0.61, 0.355, 1); }
@keyframes pulse-ring { 0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); } 70% { box-shadow: 0 0 0 20px rgba(99, 102, 241, 0); } 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); } }
.landing-icon { font-size: 54px; color: #6366f1; margin-bottom: 20px; background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto; overflow: hidden; }
.landing-img { width: 100%; height: 100%; object-fit: contain; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 40px; }
.feature-card { padding: 24px 20px; border-radius: 20px; text-align: center; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: default; }
.hover-lift:hover { transform: translateY(-8px) scale(1.02); }
.feature-icon { font-size: 28px; color: #6366f1; margin-bottom: 16px; transition: transform 0.3s; }
.hover-lift:hover .feature-icon { transform: scale(1.2); }
.feature-card h3 { font-size: 16px; font-weight: 700; margin: 0 0 8px 0; transition: color 0.6s ease; }
.feature-card p { font-size: 13px; margin: 0; line-height: 1.5; transition: color 0.6s ease; }
.scenario-section { margin-bottom: 40px; text-align: center; }
.scenario-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; letter-spacing: 1px; transition: color 0.6s ease; }
.scenario-tags { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
.scenario-tag { padding: 8px 16px; border-radius: 20px; font-size: 13px; transition: all 0.2s; box-shadow: 0 2px 6px rgba(0,0,0,0.02); cursor: default; }
.scenario-tag:hover { transform: scale(1.05); }

@media (max-width: 768px) {
  :deep(.el-scrollbar__wrap) { align-items: flex-start; }
  .landing-content { padding: 30px 20px; margin: 30px 20px 60px 20px; width: auto; border-radius: 24px; }
  .features-grid { grid-template-columns: 1fr; gap: 16px; }
  .landing-title { font-size: 28px; }
}
</style>
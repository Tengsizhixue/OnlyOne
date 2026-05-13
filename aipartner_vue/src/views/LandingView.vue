<template>
  <div class="landing-page tech-theme">
    <!-- 🌟 核心修复：抽出单独的一层 wrapper 运行开机动画，避免与 Vue Router 的切换事件产生冲突锁死 -->
    <div class="tv-crt-wrapper">
      <!-- 科技风背景层 -->
      <div class="tech-bg-layer">
        <div class="cyber-grid"></div>
        <div class="glowing-orb orb-1"></div>
        <div class="glowing-orb orb-2"></div>
        <div class="scanlines"></div>
        <div class="vignette"></div>
      </div>

      <el-scrollbar class="landing-scrollbar">
        <div class="landing-content hud-panel sys-boot-seq">

          <!-- 四角瞄准星装饰 (HUD风格) -->
          <div class="hud-corner top-left"></div>
          <div class="hud-corner top-right"></div>
          <div class="hud-corner bottom-left"></div>
          <div class="hud-corner bottom-right"></div>

          <div class="landing-header stagger-1">
            <div class="landing-icon holo-icon">
              <div class="icon-ring inner-ring"></div>
              <div class="icon-ring outer-ring"></div>
              <img src="https://api.dicebear.com/9.x/bottts-neutral/svg?seed=AI" alt="AI Logo" class="landing-img" />
            </div>
            <h1 class="landing-title glitch-text" data-text="正在开发，未完成">正在开发，未完成</h1>
            <div class="sys-status">
              <span class="status-dot"></span>
              <span>SYSTEM STATUS: ONLINE_</span>
            </div>
          </div>

          <div class="features-grid stagger-2">
            <div class="feature-card cyber-card">
              <div class="card-border-trace desktop-only"></div>
              <el-icon class="feature-icon neon-glow"><User /></el-icon>
              <div class="card-text">
                <h3>角色优化</h3>
                <p>这次的每个人物我都进行了特殊的设计</p>
              </div>
            </div>
            <div class="feature-card cyber-card">
              <div class="card-border-trace desktop-only"></div>
              <el-icon class="feature-icon neon-glow"><ColdDrink /></el-icon>
              <div class="card-text">
                <h3>额外内容</h3>
                <p>加的内容已经完全脱离了我最开始的初衷</p>
              </div>
            </div>
            <div class="feature-card cyber-card">
              <div class="card-border-trace desktop-only"></div>
              <el-icon class="feature-icon neon-glow"><Sugar /></el-icon>
              <div class="card-text">
                <h3>ui优化</h3>
                <p>ui设计会比上次好看，但是我不确定会有什么bug，我一个人测试是不会卡的</p>
              </div>
            </div>
          </div>

          <div class="scenario-section stagger-3">
            <h3 class="scenario-title">[ 我想说的 ]</h3>
            <div class="scenario-tags">
              <span class="scenario-tag holo-tag">全都是AI做的，但很耗时间</span>
              <span class="scenario-tag holo-tag">想不到还能加什么</span>
              <span class="scenario-tag holo-tag">有的浏览器可能会很卡</span>
              <span class="scenario-tag holo-tag">没什么能分享的了</span>
              <span class="scenario-tag holo-tag">电脑和手机页面我都做了优化</span>
              <span class="scenario-tag holo-tag">如果你会看源码，就能直接看到我加了什么</span>
              <span class="scenario-tag holo-tag alert-tag">不推荐直接看源码</span>
              <span class="scenario-tag holo-tag alert-tag">后面没时间，不会再改了</span>
            </div>
          </div>

          <!-- 科技感启动按钮 -->
          <div class="action-wrapper stagger-4">
            <button class="enter-btn cyber-btn" @click="goToChat">
              <span class="btn-text">WELCOME</span>
              <el-icon class="enter-icon"><ArrowRight /></el-icon>
              <div class="btn-glitch-layer"></div>
            </button>
          </div>

        </div>
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup>
import { User, ColdDrink, Sugar, ArrowRight } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToChat = () => {
  router.push('/chat')
}
</script>

<style scoped>
/* 定义科技风主色调和变量 */
.tech-theme {
  --primary-cyan: #00f3ff;
  --primary-blue: #0284c7;
  --dark-bg: #030712;
  --panel-bg: rgba(10, 15, 30, 0.6);
  --text-main: #e2e8f0;
  --text-muted: #94a3b8;
  --neon-shadow: 0 0 10px rgba(0, 243, 255, 0.5), 0 0 20px rgba(0, 243, 255, 0.3);
}

.landing-page {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background-color: var(--dark-bg);
  color: var(--text-main);
  overflow: hidden;
  font-family: 'SF Pro Display', -apple-system, Roboto, Helvetica, sans-serif;
}

/* ================= 📺 老式 CRT 电视开机特效 (移至内层) ================= */
.tv-crt-wrapper {
  width: 100%;
  height: 100%;
  position: absolute;
  inset: 0;
  animation: turn-on 0.8s cubic-bezier(0.23, 1, 0.32, 1) forwards;
  transform-origin: center center;
}

@keyframes turn-on {
  0% {
    transform: scale(0, 0) translate3d(0, 0, 0);
    filter: brightness(0);
  }
  30% {
    transform: scale(0.1, 0.002) translate3d(0, 0, 0);
    filter: brightness(10); /* 收缩成高亮的一条线 */
  }
  60% {
    transform: scale(1, 0.002) translate3d(0, 0, 0);
    filter: brightness(10); /* 横向撑开的高亮线 */
  }
  100% {
    transform: scale(1, 1) translate3d(0, 0, 0);
    filter: brightness(1); /* 垂直撑开，恢复正常亮度 */
  }
}

/* ================= 背景系统 ================= */
.tech-bg-layer { position: absolute; inset: 0; z-index: 1; pointer-events: none; overflow: hidden; }

/* 动态透视网格 */
.cyber-grid {
  position: absolute; inset: -50%;
  background-image:
    linear-gradient(rgba(0, 243, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 243, 255, 0.05) 1px, transparent 1px);
  background-size: 40px 40px;
  transform: perspective(1000px) rotateX(60deg) translateY(-100px) translateZ(-200px);
  animation: grid-move 15s linear infinite;
}
@keyframes grid-move {
  0% { transform: perspective(1000px) rotateX(60deg) translateY(0) translateZ(-200px); }
  100% { transform: perspective(1000px) rotateX(60deg) translateY(40px) translateZ(-200px); }
}

/* 背景呼吸光晕 */
.glowing-orb {
  position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.4;
  animation: orb-float 10s ease-in-out infinite alternate;
}
.orb-1 { width: 400px; height: 400px; background: var(--primary-cyan); top: -100px; left: -100px; }
.orb-2 { width: 500px; height: 500px; background: #3b82f6; bottom: -150px; right: -100px; animation-delay: -5s; }
@keyframes orb-float {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(50px, 50px) scale(1.2); }
}

/* 屏幕复古扫描线 & 暗角 */
.scanlines {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.1) 50%, rgba(0,0,0,0.1));
  background-size: 100% 4px;
  opacity: 0.3; pointer-events: none;
}
.vignette { position: absolute; inset: 0; background: radial-gradient(circle, transparent 50%, #000000 120%); }

/* ================= 布局 & 滚动 ================= */
.landing-scrollbar { height: 100%; width: 100%; z-index: 10; position: relative; }
:deep(.el-scrollbar__view) {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 15px;
  box-sizing: border-box;
}

/* ================= HUD 主面板 ================= */
.hud-panel {
  position: relative;
  background: var(--panel-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 243, 255, 0.15);
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(0, 243, 255, 0.05);
  clip-path: polygon(
    30px 0, 100% 0, 100% calc(100% - 30px), calc(100% - 30px) 100%, 0 100%, 0 30px
  );
  text-align: center; padding: 60px 70px; max-width: 850px; width: 100%; margin: 0 auto;
  box-sizing: border-box;
}

/* HUD 四角瞄准星 */
.hud-corner { position: absolute; width: 20px; height: 20px; border: 2px solid var(--primary-cyan); opacity: 0.5; }
.top-left { top: 15px; left: 15px; border-right: none; border-bottom: none; }
.top-right { top: 15px; right: 15px; border-left: none; border-bottom: none; }
.bottom-left { bottom: 15px; left: 15px; border-right: none; border-top: none; }
.bottom-right { bottom: 15px; right: 15px; border-left: none; border-top: none; }

/* ================= 头部元素 ================= */
.landing-header { margin-bottom: 50px; }

/* 全息头像框 */
.holo-icon {
  position: relative; width: 110px; height: 110px; margin: 0 auto 20px auto;
  display: flex; align-items: center; justify-content: center;
}
.icon-ring { position: absolute; inset: 0; border-radius: 50%; border: 1px solid transparent; }
.inner-ring { border-top-color: var(--primary-cyan); border-bottom-color: var(--primary-cyan); animation: spin 4s linear infinite; }
.outer-ring { inset: -10px; border-left-color: var(--primary-blue); border-right-color: var(--primary-blue); animation: spin-reverse 6s linear infinite; opacity: 0.5; }
.landing-img { width: 70%; height: 70%; object-fit: contain; filter: drop-shadow(0 0 8px var(--primary-cyan)); }
@keyframes spin { 100% { transform: rotate(360deg); } }
@keyframes spin-reverse { 100% { transform: rotate(-360deg); } }

/* 故障风标题 */
.glitch-text {
  font-size: 32px; font-weight: 800; letter-spacing: 2px;
  color: #fff; text-shadow: var(--neon-shadow); margin-bottom: 12px;
  position: relative;
}

/* 系统状态打字机效果 */
.sys-status { font-family: monospace; font-size: 13px; color: var(--primary-cyan); display: flex; align-items: center; justify-content: center; gap: 8px; opacity: 0.8; }
.status-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px #10b981; animation: blink 1.5s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

/* ================= 功能卡片 ================= */
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 50px; }
.cyber-card {
  background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 30px 20px; text-align: center; position: relative;
  transition: all 0.4s ease; overflow: hidden; cursor: crosshair;
}
.cyber-card::before {
  content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, transparent, rgba(0, 243, 255, 0.1) 100%);
  transform: translateY(100%); transition: transform 0.4s ease;
}
.cyber-card:hover { border-color: rgba(0, 243, 255, 0.4); box-shadow: 0 5px 20px rgba(0, 243, 255, 0.1); transform: translateY(-5px); }
.cyber-card:hover::before { transform: translateY(0); }

.card-border-trace { position: absolute; inset: 0; pointer-events: none; }
.card-border-trace::before, .card-border-trace::after {
  content: ''; position: absolute; width: 0; height: 1px; background: var(--primary-cyan); transition: all 0.4s ease;
}
.cyber-card:hover .card-border-trace::before { width: 100%; top: 0; left: 0; box-shadow: var(--neon-shadow); }
.cyber-card:hover .card-border-trace::after { width: 100%; bottom: 0; right: 0; box-shadow: var(--neon-shadow); }

.feature-icon { font-size: 32px; color: var(--primary-cyan); margin-bottom: 16px; transition: all 0.3s; z-index: 2; position: relative; }
.cyber-card:hover .feature-icon { transform: scale(1.1); color: #fff; filter: drop-shadow(0 0 10px var(--primary-cyan)); }
.card-text { z-index: 2; position: relative; }
.cyber-card h3 { font-size: 17px; font-weight: 600; color: #fff; margin: 0 0 10px 0; }
.cyber-card p { font-size: 13px; color: var(--text-muted); line-height: 1.6; margin: 0; }

/* ================= 标签区 ================= */
.scenario-section { margin-bottom: 50px; }
.scenario-title { font-family: monospace; font-size: 14px; color: var(--text-muted); margin-bottom: 20px; letter-spacing: 2px; }
.scenario-tags { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
.holo-tag {
  background: rgba(0, 243, 255, 0.05); border: 1px solid rgba(0, 243, 255, 0.2);
  padding: 8px 16px; font-size: 12px; color: var(--primary-cyan);
  clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
  transition: all 0.3s ease; cursor: default;
}
.holo-tag:hover { background: rgba(0, 243, 255, 0.15); box-shadow: var(--neon-shadow); transform: translateY(-2px); }
.alert-tag { border-color: rgba(244, 63, 94, 0.4); color: #f43f5e; }
.alert-tag:hover { background: rgba(244, 63, 94, 0.15); box-shadow: 0 0 10px rgba(244, 63, 94, 0.4); }

/* ================= 动作按钮 ================= */
.action-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  width: 100%;
  z-index: 20;
}
.cyber-btn {
  background: transparent; border: 1px solid var(--primary-cyan);
  color: var(--primary-cyan); padding: 16px 40px; font-size: 16px; font-weight: 700; font-family: monospace;
  letter-spacing: 2px; display: flex; align-items: center; justify-content: center; gap: 12px; cursor: pointer;
  position: relative; overflow: hidden; transition: all 0.3s;
  clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px);
}
.cyber-btn::before {
  content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.4), transparent);
  transition: all 0.5s ease;
}
.cyber-btn:hover { background: rgba(0, 243, 255, 0.1); color: #fff; box-shadow: 0 0 20px rgba(0, 243, 255, 0.4) inset; }
.cyber-btn:hover::before { left: 100%; }
.enter-icon { font-size: 20px; transition: transform 0.3s; }
.cyber-btn:hover .enter-icon { transform: translateX(5px); }

/* ================= 入场启动动画序列 ================= */
.sys-boot-seq .stagger-1 { opacity: 0; animation: bootUp 0.8s ease forwards 0.7s; }
.sys-boot-seq .stagger-2 { opacity: 0; animation: bootUp 0.8s ease forwards 0.9s; }
.sys-boot-seq .stagger-3 { opacity: 0; animation: bootUp 0.8s ease forwards 1.1s; }
.sys-boot-seq .stagger-4 { opacity: 0; animation: bootUp 0.8s ease forwards 1.3s; }

@keyframes bootUp {
  0% { opacity: 0; transform: translateY(30px) scale(0.98); filter: blur(5px); }
  100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}

/* ================= 移动端适配 ================= */
@media (max-width: 768px) {
  :deep(.el-scrollbar__view) {
    align-items: flex-start;
    padding: 20px 10px;
  }

  .hud-panel {
    padding: 30px 15px;
    clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px);
  }

  .hud-corner { display: none; }

  .landing-header { margin-bottom: 30px; }
  .holo-icon { width: 80px; height: 80px; margin-bottom: 12px; }
  .glitch-text { font-size: 22px; }

  .features-grid {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 30px;
  }

  .cyber-card {
    display: flex;
    flex-direction: row;
    align-items: center;
    text-align: left;
    padding: 14px 16px;
    background: linear-gradient(90deg, rgba(0, 243, 255, 0.08) 0%, rgba(0, 0, 0, 0) 100%);
    border: none;
    border-left: 3px solid var(--primary-cyan);
    transform: none !important;
  }
  .cyber-card::before, .desktop-only { display: none; }
  .cyber-card:hover { box-shadow: none; }

  .feature-icon {
    margin-bottom: 0;
    margin-right: 16px;
    font-size: 26px;
    flex-shrink: 0;
  }
  .card-text {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .cyber-card h3 { font-size: 15px; margin-bottom: 4px; }
  .cyber-card p { font-size: 12px; }

  .scenario-section { margin-bottom: 40px; }
  .scenario-tags { gap: 8px; }
  .holo-tag { padding: 6px 10px; font-size: 11px; }

  .action-wrapper { display: block; width: 100%; }
  .cyber-btn { width: 100%; padding: 16px 20px; font-size: 15px; }
}
</style>
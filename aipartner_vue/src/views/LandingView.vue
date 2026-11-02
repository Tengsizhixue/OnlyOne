<template>
  <div class="landing-page tech-theme">
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

          <!-- 四角瞄准星装饰 -->
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
            <h1 class="landing-title glitch-text" data-text="呆呆的非智能伙伴">呆呆的非智能伙伴</h1>
            <div class="sys-status">
              <span class="status-dot"></span>
              <span>SYSTEM STATUS: ONLINE</span>
            </div>
          </div>

          <!-- 🌟 核心重构：高级系统模块化的卡片设计 -->
          <div class="features-grid stagger-2">

            <div class="feature-card cyber-card">
              <div class="card-border-trace desktop-only"></div>
              <div class="icon-wrapper">
                <!-- 科技感图标：身份生物识别/目标锁定 -->
                <svg class="custom-tech-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <circle cx="12" cy="10" r="3" stroke-dasharray="2 2"></circle>
                  <path d="M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662"></path>
                  <line x1="12" y1="2" x2="12" y2="4"></line>
                  <line x1="12" y1="20" x2="12" y2="22"></line>
                  <line x1="2" y1="12" x2="4" y2="12"></line>
                  <line x1="20" y1="12" x2="22" y2="12"></line>
                </svg>
              </div>
              <div class="card-text">
                <div class="sys-label">BETTER_CHARACTER_DESIGN </div>
                <h3>角色优化</h3>
                <p>这次的每个人物我都进行了特殊的设计</p>
              </div>
            </div>

            <div class="feature-card cyber-card">
              <div class="card-border-trace desktop-only"></div>
              <div class="icon-wrapper">
                <!-- 科技感图标：3D等距数据魔方/资料库 -->
                <svg class="custom-tech-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                  <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                  <line x1="12" y1="22.08" x2="12" y2="12"></line>
                  <polygon points="12 7 8 9.5 8 14.5 12 17 16 14.5 16 9.5 12 7" stroke-dasharray="1 2"></polygon>
                </svg>
              </div>
              <div class="card-text">
                <div class="sys-label">EXTRA_CONTENT</div>
                <h3>额外内容</h3>
                <p>加的内容已经完全脱离了我最开始的初衷</p>
              </div>
            </div>

            <div class="feature-card cyber-card">
              <div class="card-border-trace desktop-only"></div>
              <div class="icon-wrapper">
                <!-- 科技感图标：UI显示器蓝图 -->
                <svg class="custom-tech-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                  <line x1="8" y1="21" x2="16" y2="21"></line>
                  <line x1="12" y1="17" x2="12" y2="21"></line>
                  <rect x="6" y="7" width="12" height="6" stroke-dasharray="2 2"></rect>
                  <line x1="2" y1="10" x2="22" y2="10" stroke-width="0.5" stroke-dasharray="1 3"></line>
                </svg>
              </div>
              <div class="card-text">
                <div class="sys-label">BETTER_UI</div>
                <h3>UI优化</h3>
                <p>ui设计会比上次好看，但是我不确定会有什么bug，我一个人测试是不会卡的</p>
              </div>
            </div>

          </div>

          <div class="scenario-section stagger-3">
            <h3 class="scenario-title">[ 前言 ]</h3>
            <div class="scenario-tags">
              <span class="scenario-tag holo-tag">想不到还能加什么</span>
              <span class="scenario-tag holo-tag">有的浏览器可能会很卡</span>
              <span class="scenario-tag holo-tag">电脑和手机页面我都做了优化</span>
              <span class="scenario-tag holo-tag alert-tag">后面没时间，不会再改了</span>
            </div>
          </div>

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
// 移除了 User, ColdDrink, Sugar 这些不协调的图标，只保留必要的箭头
import { ArrowRight } from '@element-plus/icons-vue'
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
  0% { transform: scale(0, 0) translate3d(0, 0, 0); filter: brightness(0); }
  30% { transform: scale(0.1, 0.002) translate3d(0, 0, 0); filter: brightness(10); }
  60% { transform: scale(1, 0.002) translate3d(0, 0, 0); filter: brightness(10); }
  100% { transform: scale(1, 1) translate3d(0, 0, 0); filter: brightness(1); }
}

/* ================= 背景系统 ================= */
.tech-bg-layer { position: absolute; inset: 0; z-index: 1; pointer-events: none; overflow: hidden; }

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

.hud-corner { position: absolute; width: 20px; height: 20px; border: 2px solid var(--primary-cyan); opacity: 0.5; }
.top-left { top: 15px; left: 15px; border-right: none; border-bottom: none; }
.top-right { top: 15px; right: 15px; border-left: none; border-bottom: none; }
.bottom-left { bottom: 15px; left: 15px; border-right: none; border-top: none; }
.bottom-right { bottom: 15px; right: 15px; border-left: none; border-top: none; }

/* ================= 头部元素 ================= */
.landing-header { margin-bottom: 50px; }

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

.glitch-text {
  font-size: 32px; font-weight: 800; letter-spacing: 2px;
  color: #fff; text-shadow: var(--neon-shadow); margin-bottom: 12px;
  position: relative;
}

.sys-status { font-family: monospace; font-size: 13px; color: var(--primary-cyan); display: flex; align-items: center; justify-content: center; gap: 8px; opacity: 0.8; }
.status-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px #10b981; animation: blink 1.5s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

/* ================= 🌟 模块化功能卡片 ================= */
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 50px; }
.cyber-card {
  background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 30px 20px; text-align: center; position: relative;
  transition: all 0.4s ease; overflow: hidden; cursor: crosshair;
  display: flex; flex-direction: column; align-items: center;
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

/* 🌟 高级定制：带扫描线动画的图标盒子 */
.icon-wrapper {
  position: relative;
  width: 54px; height: 54px; margin-bottom: 18px;
  display: flex; align-items: center; justify-content: center;
  background: rgba(0, 243, 255, 0.05); border: 1px solid rgba(0, 243, 255, 0.2);
  border-radius: 12px; box-shadow: inset 0 0 15px rgba(0, 243, 255, 0.05);
  transition: all 0.4s ease; z-index: 2; overflow: hidden;
}
.cyber-card:hover .icon-wrapper {
  background: rgba(0, 243, 255, 0.15); border-color: rgba(0, 243, 255, 0.6);
  box-shadow: 0 0 20px rgba(0, 243, 255, 0.2), inset 0 0 15px rgba(0, 243, 255, 0.2);
  transform: scale(1.1);
}
/* HUD 上下扫描雷达线 */
.icon-wrapper::after {
  content: ''; position: absolute; top: -10%; left: 0; right: 0; height: 2px;
  background: var(--primary-cyan); box-shadow: 0 0 10px var(--primary-cyan);
  animation: scan-line 2.5s cubic-bezier(0.4, 0, 0.2, 1) infinite; opacity: 0.6;
}
@keyframes scan-line {
  0% { top: -10%; opacity: 0; }
  20% { opacity: 1; }
  80% { opacity: 1; }
  100% { top: 110%; opacity: 0; }
}

.custom-tech-icon { width: 28px; height: 28px; color: var(--primary-cyan); filter: drop-shadow(0 0 5px var(--primary-cyan)); transition: all 0.4s ease; }
.cyber-card:hover .custom-tech-icon { color: #fff; filter: drop-shadow(0 0 12px var(--primary-cyan)); }

.card-text { z-index: 2; position: relative; }
/* 增加系统模块号标签，强化科技专业感 */
.sys-label { font-family: monospace; font-size: 10px; color: var(--primary-blue); letter-spacing: 1px; margin-bottom: 8px; font-weight: bold; }
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
  position: relative; display: flex; justify-content: center; width: 100%; z-index: 20;
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
  :deep(.el-scrollbar__view) { align-items: flex-start; padding: 20px 10px; }

  .hud-panel {
    padding: 30px 15px;
    clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px);
  }
  .hud-corner { display: none; }
  .landing-header { margin-bottom: 30px; }
  .holo-icon { width: 80px; height: 80px; margin-bottom: 12px; }
  .glitch-text { font-size: 22px; }

  /* 🌟 移动端：将系统模块改为带有左侧粗边的列阵排版，让它看起来像数据终端的选项卡 */
  .features-grid { display: flex; flex-direction: column; gap: 12px; margin-bottom: 30px; }

  .cyber-card {
    flex-direction: row; align-items: stretch; text-align: left;
    padding: 16px; background: linear-gradient(90deg, rgba(0, 243, 255, 0.08) 0%, rgba(0, 0, 0, 0) 100%);
    border: none; border-left: 3px solid var(--primary-cyan); transform: none !important;
  }
  .cyber-card::before, .desktop-only { display: none; }
  .cyber-card:hover { box-shadow: none; }

  .icon-wrapper {
    margin-bottom: 0; margin-right: 16px; flex-shrink: 0;
    width: 48px; height: 48px; border-radius: 8px;
  }
  .cyber-card:hover .icon-wrapper { transform: none; }

  .card-text { display: flex; flex-direction: column; justify-content: center; }
  .sys-label { font-size: 9px; margin-bottom: 2px; }
  .cyber-card h3 { font-size: 15px; margin-bottom: 4px; }
  .cyber-card p { font-size: 12px; }

  .scenario-section { margin-bottom: 40px; }
  .scenario-tags { gap: 8px; }
  .holo-tag { padding: 6px 10px; font-size: 11px; }

  .action-wrapper { display: block; width: 100%; }
  .cyber-btn { width: 100%; padding: 16px 20px; font-size: 15px; }
}
</style>
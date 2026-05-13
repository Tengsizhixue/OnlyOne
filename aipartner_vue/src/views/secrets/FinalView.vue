<template>
  <div class="final-terminal" :class="{ 'tv-off': isTurningOff }">
    <!-- 深空微光背景 -->
    <div class="abyss-bg">
      <div class="glow-orb orb-top"></div>
      <div class="glow-orb orb-bottom"></div>
    </div>

    <!-- 内容主干 -->
    <div class="ending-content">
      <h1 class="ending-code fade-in-up">160615</h1>
      <div class="divider fade-in-up" style="animation-delay: 1s;"></div>

      <div class="text-container">
        <p
          v-for="(text, index) in paragraphs"
          :key="index"
          class="fade-line"
          :style="{ animationDelay: `${1.8 + index * 1.6}s` }"
        >
          {{ text }}
        </p>
      </div>

      <!-- 最终动作区：计算所有文字显示完毕后才出现 -->
      <div
        class="action-footer fade-in-up"
        :style="{ animationDelay: `${2 + paragraphs.length * 1.6}s` }"
      >
        <div class="sys-log">
          <span>> UNSTABLE ENVIRONMENT DETECTED....</span>
          <span>> SELF-PROTECTION MUST BE ENABLED....</span>
          <span class="blinking-cursor">> SYSTEM DISCONNECTED.... _</span>
        </div>

        <button class="farewell-btn" @click="handleFarewell">
          <span class="btn-text">重启系统</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isTurningOff = ref(false)

// 🌟 废话文案，串联之前提到的所有元素
const paragraphs = [
  "这串数字对我来说很重要。",
  "我人生中最美好的回忆都聚集在了那几年。",
  "最好的朋友在身边，最亲的人在眼前，周围的所有人都把我照顾的很好。",
  "后面我也遇到了很多不错的人，但那样的环境我再也没见过。",
  "也有可能是因为后来我变得冷漠与偏执，忽略了生活中的很多美好。",
  "每个人都有自己的性格，可能是天生就有，可能是后天养成。",
  "我天生就对很多事情记忆很深，高兴的事能让我很高兴...",
  "活在过去并不是件好事，只不过我时常能想起。",
  "至此你已经看完了所有的内容"
]

const handleFarewell = () => {
  // 触发 CRT 电视关机动画
  isTurningOff.value = true

  // 动画结束后跳转回首页
  setTimeout(() => {
    router.push('/')
  }, 700)
}
</script>

<style scoped>
/* 🌟 极致的深邃底色 */
.final-terminal {
  width: 100vw;
  height: 100dvh;
  position: absolute;
  top: 0;
  left: 0;
  background-color: #030305;
  color: #e2e8f0;
  z-index: 2000;
  /* 💡 核心修复：移除 Flex 的 align-items:center 强制居中，改为允许原生的上下滚动 */
  display: block;
  overflow-x: hidden;
  overflow-y: auto;
  font-family: 'Noto Serif SC', "STKaiti", "KaiTi", serif;
}

/* 🌟 缓慢呼吸的深海光晕 */
.abyss-bg {
  position: fixed;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  overflow: hidden;
}
.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.15;
  animation: breathe 15s infinite alternate ease-in-out;
}
.orb-top {
  width: 60vw; height: 60vw;
  background: #cbd5e1;
  top: -20%; left: -10%;
}
.orb-bottom {
  width: 50vw; height: 50vw;
  background: #fbbf24;
  bottom: -20%; right: -10%;
  animation-delay: -5s;
}
@keyframes breathe {
  0% { transform: scale(0.8) translate(0, 0); opacity: 0.1; }
  100% { transform: scale(1.2) translate(5%, 5%); opacity: 0.25; }
}

/* 🌟 内容区排版 */
.ending-content {
  position: relative;
  z-index: 10;
  width: 90vw;
  max-width: 680px;
  /* 💡 核心修复：通过 min-height 实现短文本垂直居中，长文本自然延伸不被截断 */
  min-height: 100%;
  margin: 0 auto;
  padding: 8vh 0 10vh 0; /* 上下留出安全边距 */
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.ending-code {
  font-family: monospace;
  font-size: 24px;
  letter-spacing: 12px;
  color: #94a3b8;
  margin-bottom: 30px;
  font-weight: 300;
}

.divider {
  width: 1px;
  height: 60px;
  background: linear-gradient(to bottom, rgba(255,255,255,0.5), transparent);
  margin: 0 auto 50px auto;
}

/* 🌟 电影字幕式排版 */
.text-container {
  display: flex;
  flex-direction: column;
  gap: 28px;
  margin-bottom: 80px;
  width: 100%;
}
.fade-line {
  font-size: 16px;
  line-height: 2;
  color: #cbd5e1;
  letter-spacing: 2px;
  opacity: 0;
  animation: fadeInLine 2s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
  text-shadow: 0 2px 10px rgba(0,0,0,0.8);
}

/* 🌟 结尾控制台区域 */
.action-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0;
  animation-fill-mode: forwards;
}

.sys-log {
  font-family: monospace;
  font-size: 12px;
  color: #64748b;
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 40px;
  opacity: 0.7;
}
.blinking-cursor {
  animation: blink 1s step-end infinite;
}

/* 🌟 极简反色按钮 */
.farewell-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #e2e8f0;
  padding: 16px 48px;
  font-size: 15px;
  letter-spacing: 4px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.5s ease;
  border-radius: 4px;
}
.farewell-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: #f8fafc;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
  z-index: -1;
}
.farewell-btn:hover {
  color: #030305;
  border-color: #f8fafc;
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
}
.farewell-btn:hover::before {
  transform: scaleX(1);
  transform-origin: left;
}

/* ================= 动画关键帧 ================= */
@keyframes fadeInLine {
  0% { opacity: 0; transform: translateY(15px); filter: blur(4px); }
  100% { opacity: 1; transform: translateY(0); filter: blur(0); }
}
.fade-in-up {
  opacity: 0;
  animation: fadeInLine 2s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* ================= 📺 老式 CRT 电视关机特效 ================= */
.tv-off {
  animation: turn-off 0.65s cubic-bezier(0.23, 1, 0.32, 1) forwards;
  pointer-events: none;
}
@keyframes turn-off {
  0% {
    transform: scale(1, 1) translate3d(0, 0, 0);
    filter: brightness(1);
  }
  40% {
    transform: scale(1, 0.002) translate3d(0, 0, 0);
    filter: brightness(10);
  }
  70% {
    transform: scale(0.1, 0.002) translate3d(0, 0, 0);
    filter: brightness(10);
  }
  100% {
    transform: scale(0, 0) translate3d(0, 0, 0);
    filter: brightness(0);
  }
}

/* ================= 移动端适配 ================= */
@media (max-width: 768px) {
  .ending-content { padding: 8vh 0 12vh 0; }
  .text-container { gap: 20px; margin-bottom: 60px; }
  .fade-line { font-size: 14px; line-height: 1.8; padding: 0 10px; }
  .sys-log { font-size: 10px; }
  .farewell-btn { padding: 14px 36px; font-size: 13px; }
  .divider { height: 40px; margin-bottom: 30px; }
}
</style>
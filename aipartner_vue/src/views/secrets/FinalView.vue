<template>
  <div class="final-terminal" :class="{ 'tv-off': isTurningOff, 'hacked-mode': isHacked }">
    <!-- 📺 复古 CRT 扫描线遮罩 -->
    <div class="scanlines"></div>

    <!-- 深空微光背景 -->
    <div class="abyss-bg">
      <div class="glow-orb orb-top"></div>
      <div class="glow-orb orb-bottom"></div>
    </div>

    <!-- 内容主干 -->
    <div class="ending-content" ref="contentRef">
      <!-- 动态解码的数字 -->
      <h1 class="ending-code fade-in-up">{{ displayCode }}</h1>
      <div class="divider fade-in-up" style="animation-delay: 1s;"></div>

      <div class="text-container">
        <p
          v-for="(text, index) in paragraphs"
          :key="index"
          class="fade-line"
          :style="{ animationDelay: `${1.8 + index * 2.0}s` }"
          @animationend="handleLineShow(index)"
        >
          {{ text }}
        </p>
      </div>

      <!-- 最终动作区：计算所有文字显示完毕后才出现 -->
      <div
        class="action-footer"
        :class="{ 'show-footer': isHacked }"
      >
        <div class="sys-log">
          <span class="typewriter">> 检测到李蓝宝的攻击....</span>
          <span class="typewriter" style="animation-delay: 0.8s;">> 正在启动驱魔音乐....</span>
          <span class="typewriter blinking-cursor" style="animation-delay: 1.6s;">> 需要最高权限....</span>
        </div>

        <button
          class="farewell-btn"
          :class="{ 'glitch-btn': isHacked }"
          :disabled="isTurningOff"
          @click="handleFarewell"
        >
          <span class="btn-text">播放音乐并重启系统</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isTurningOff = ref(false)
const isHacked = ref(false) // 控制画风突变的开关
const contentRef = ref(null)

// 🌟 160615 解码特效
const targetCode = "160615"
const displayCode = ref("000000")
const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"

const decodeText = () => {
  let iterations = 0;
  const interval = setInterval(() => {
    displayCode.value = displayCode.value.split("").map((letter, index) => {
      if (index < iterations) return targetCode[index];
      return chars[Math.floor(Math.random() * chars.length)];
    }).join("");

    if (iterations >= targetCode.length) clearInterval(interval);
    iterations += 1 / 5; // 控制解码速度
  }, 30);
}

// 🌟 废话文案
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

// 监听每一行文字出现，实现自动向下滚动
const handleLineShow = (index) => {
  if (contentRef.value) {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    });
  }

  // 当最后一行文字播放完毕，触发“被黑”状态
  if (index === paragraphs.length - 1) {
    setTimeout(() => {
      isHacked.value = true;
      // 再次滚动到底部确保按钮可见
      setTimeout(() => {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      }, 100);
    }, 1500);
  }
}

onMounted(() => {
  setTimeout(decodeText, 500); // 延迟半秒开始解码数字
})

const handleFarewell = () => {
  if (isTurningOff.value) return; // 防抖，防止重复点击
  isTurningOff.value = true

  // ================= 🌟 跨页面音乐引擎 🌟 =================
  const audioUrl = 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E6%9C%80%E7%BB%88%E7%9A%84%E6%90%9E%E7%AC%91%E9%9F%B3%E4%B9%90.mp3'
  const bgAudio = new Audio(audioUrl)
  bgAudio.loop = true

  setTimeout(() => {
    bgAudio.play().catch(e => console.warn('音频播放被拦截:', e))
    window.__exorcism_audio = bgAudio

    const unregisterGuard = router.beforeEach((to, from) => {
      if (from.path === '/' && to.path !== '/') {
        if (window.__exorcism_audio) {
          window.__exorcism_audio.pause()
          window.__exorcism_audio.currentTime = 0
          window.__exorcism_audio = null
        }
        unregisterGuard()
      }
    })

    router.push('/')
  }, 700)
}
</script>

<style scoped>
/* 保持原有基础样式 */
.final-terminal {
  width: 100vw;
  height: 100dvh;
  position: absolute;
  top: 0;
  left: 0;
  background-color: #030305;
  color: #e2e8f0;
  z-index: 2000;
  display: block;
  overflow-x: hidden;
  overflow-y: auto;
  font-family: 'Noto Serif SC', "STKaiti", "KaiTi", serif;
  transition: background-color 0.5s ease;
}

/* 📺 增加复古扫描线 */
.scanlines {
  position: fixed;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(255,255,255,0),
    rgba(255,255,255,0) 50%,
    rgba(0,0,0,0.1) 50%,
    rgba(0,0,0,0.1)
  );
  background-size: 100% 4px;
  z-index: 100;
  pointer-events: none;
  opacity: 0.3;
}

/* 🚨 黑客入侵模式（画风突变） */
.final-terminal.hacked-mode {
  background-color: #1a0505; /* 变成暗红色调 */
}
.hacked-mode .orb-top { background: #ef4444; filter: blur(150px); }
.hacked-mode .orb-bottom { background: #b91c1c; }
.hacked-mode .fade-line { opacity: 0.5; } /* 让前面的文字变暗 */

/* 原有光晕动画 */
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
  transition: all 1.5s ease;
  animation: breathe 15s infinite alternate ease-in-out;
}
.orb-top { width: 60vw; height: 60vw; background: #cbd5e1; top: -20%; left: -10%; }
.orb-bottom { width: 50vw; height: 50vw; background: #fbbf24; bottom: -20%; right: -10%; animation-delay: -5s; }

@keyframes breathe {
  0% { transform: scale(0.8) translate(0, 0); opacity: 0.1; }
  100% { transform: scale(1.2) translate(5%, 5%); opacity: 0.25; }
}

.ending-content {
  position: relative;
  z-index: 10;
  width: 90vw;
  max-width: 680px;
  min-height: 100%;
  margin: 0 auto;
  padding: 8vh 0 10vh 0;
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
  transition: opacity 1s ease;
}

/* 🌟 控制台打字机效果 */
.action-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  display: none; /* 初始隐藏 */
}
.action-footer.show-footer {
  display: flex;
}

.sys-log {
  font-family: monospace;
  font-size: 12px;
  color: #ef4444; /* 警告红 */
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 40px;
  width: 100%;
  max-width: 300px;
}

.typewriter {
  overflow: hidden;
  white-space: nowrap;
  width: 0;
  animation: typing 1s steps(30, end) forwards;
}

.blinking-cursor::after {
  content: '_';
  animation: blink 1s step-end infinite;
}

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
  opacity: 0;
  animation: fadeInLine 1s ease forwards;
  animation-delay: 2.5s; /* 等打字机打完再出现 */
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
.farewell-btn:hover:not(:disabled) {
  color: #030305;
  border-color: #f8fafc;
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
}
.farewell-btn:hover:not(:disabled)::before {
  transform: scaleX(1);
  transform-origin: left;
}
/* 被黑客入侵后的按钮样式 */
.glitch-btn {
  border-color: #ef4444;
  color: #ef4444;
}
.glitch-btn::before {
  background: #ef4444;
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
@keyframes typing {
  from { width: 0 }
  to { width: 100% }
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
  0% { transform: scale(1, 1) translate3d(0, 0, 0); filter: brightness(1); }
  40% { transform: scale(1, 0.002) translate3d(0, 0, 0); filter: brightness(10); }
  70% { transform: scale(0.1, 0.002) translate3d(0, 0, 0); filter: brightness(10); }
  100% { transform: scale(0, 0) translate3d(0, 0, 0); filter: brightness(0); }
}

/* ================= 移动端适配 ================= */
@media (max-width: 768px) {
  .ending-content { padding: 8vh 0 12vh 0; }
  .text-container { gap: 20px; margin-bottom: 60px; }
  .fade-line { font-size: 14px; line-height: 1.8; padding: 0 10px; }
  .sys-log { font-size: 11px; }
  .farewell-btn { padding: 14px 36px; font-size: 13px; }
  .divider { height: 40px; margin-bottom: 30px; }
}
</style>
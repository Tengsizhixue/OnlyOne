<template>
  <div class="secret-root-container">

    <!-- 1. 具体的彩蛋子页面渲染区 (完全独立，互不干扰) -->
    <component
      v-if="currentComponent"
      :is="currentComponent"
      @back="handleBack"
    />

    <!-- 2. 160615 记忆总目录页 (当你没有匹配到特定子组件时显示) -->
    <div v-else class="gallery-view-container">

      <!-- 🌟 极简高级感背景：深渊暗房与流动的胶片光斑 -->
      <div class="gallery-bg">
        <div class="ambient-light light-1"></div>
        <div class="ambient-light light-2"></div>
        <div class="noise-overlay"></div>
      </div>

      <div class="gallery-scroll-area custom-scrollbar">
        <div class="gallery-content">

          <!-- 头部序言区 -->
          <header class="gallery-header">
            <h1 class="gallery-title">真正的前言</h1>
            <p class="gallery-subtitle">160615</p>
            <div class="elegant-divider"></div>
          </header>

          <section class="gallery-prose">
            <p>这个数字是我网址的一级域名，文章的最后会说这个数字是怎么来的。顶级域名 .xyz 单纯是因为便宜，一年就一刀乐。</p>
            <p>回到侧边框后，你会看到其他的一些问题，你可以尝试着去问 AI 里面的问题。如果问的角色没错，AI 的回复中会有其他的 6 位数字；如果 AI 没给你正确的答案，可能是它抽风了，你可以多问几遍。</p>
            <p>内容太多，如果感兴趣可以看看后面的内容，也有很多的废话，但这应该是最后一次在网上讨论以前的事。</p>
            <p>如果看完后也不要问我关于这里面的任何事情，我不想再讨论。</p>
          </section>

          <!-- 🌟 记忆碎片列表 -->
          <section class="fragments-section">
            <div class="section-title">
              <span class="diamond"></span>
              <span>如果你懒得一个个去问，可以翻阅下方的记录：</span>
              <span class="diamond"></span>
            </div>

            <div class="fragment-list">
              <div
                v-for="(quest, index) in SECRET_QUESTS"
                :key="quest.code"
                class="fragment-item"
                :class="{
                  'is-current': quest.code === '160615',
                  'is-visited': quest.code !== '160615' && unlockedCodes.includes(quest.code)
                }"
                @click="jumpToSecret(quest.code)"
              >
                <!-- 左侧：章节序号 -->
                <div class="frag-index">
                  <span>碎片</span>
                  <span class="num">{{ String(index + 1).padStart(2, '0') }}</span>
                </div>

                <!-- 中间：执念/问题 -->
                <div class="frag-text">
                  {{ quest.question }}
                </div>

                <!-- 右侧：密钥 -->
                <div class="frag-code">
                  {{ quest.code }}
                </div>

                <!-- 悬停时的光泽流转 -->
                <div class="frag-hover-glow"></div>
              </div>
            </div>
          </section>

          <!-- 底部归宿 -->
          <footer class="gallery-footer">
            <button class="quiet-btn back-btn" @click="handleBack">
              合上展卷
            </button>
            <button v-if="isAllUnlocked" class="quiet-btn forward-btn" @click="goToFinal">
              走向终点
            </button>
          </footer>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
// 🌟 引入 unlockedCodes 状态，用来判断用户是否点开过这个碎片
import { unlockCode, isAllUnlocked, SECRET_QUESTS, unlockedCodes } from '../store/questState.js'

import LiHongBaoView from './secrets/LiHongBaoView.vue'
import GameMemoryView from './secrets/GameMemoryView.vue'
import AstlibraView from './secrets/AstlibraView.vue'
import VioletLetterView from './secrets/VioletLetterView.vue'
import MusicView from './secrets/MusicView.vue'
import GameView from './secrets/GameView.vue'
import QQdisappearView from './secrets/QQdisappearView.vue'

const props = defineProps({
  secretCode: {
    type: String,
    default: ''
  }
})

const router = useRouter()
const route = useRoute()

onMounted(() => {
  if (props.secretCode) unlockCode(props.secretCode)
})
watch(() => props.secretCode, (newCode) => {
  if (newCode) unlockCode(newCode)
})

const handleBack = () => {
  router.push({
    name: 'chat',
    query: {
      view: 'room',
      role: route.query.role,
      session: route.query.session
    }
  })
}

const goToFinal = () => {
  router.push('/final')
}

// 快捷跃迁功能
const jumpToSecret = (code) => {
  if (code === '160615') return
  unlockCode(code) // 🌟 每次点击就会被记录到 unlockedCodes 中
  router.push({
    name: 'secret',
    params: { secretCode: code },
    query: {
      role: route.query.role,
      session: route.query.session
    }
  })
}

const viewMap = {
  '260315': LiHongBaoView,
  '251027': GameMemoryView,
  '260410': AstlibraView,
  '191001': VioletLetterView,
  '240802': MusicView,
  '180818': GameView,
  '240619': QQdisappearView
}

const currentComponent = computed(() => {
  return viewMap[props.secretCode] || null
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');

.secret-root-container { display: flex; justify-content: center; align-items: center; width: 100%; height: 100dvh; position: fixed; top: 0; left: 0; z-index: 999; overflow: hidden; }

/* ================= 🌟 背景：安静的记忆放映室 ================= */
.gallery-view-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: #030305; }
.gallery-bg { position: absolute; inset: 0; z-index: 0; overflow: hidden; pointer-events: none; }

.ambient-light { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.15; animation: drift 20s infinite alternate ease-in-out; }
.light-1 { width: 50vw; height: 50vw; background: #64748b; top: -10%; left: -10%; }
.light-2 { width: 60vw; height: 60vw; background: #78716c; bottom: -20%; right: -10%; animation-delay: -10s; }
.noise-overlay { position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E"); z-index: 1; }

@keyframes drift { 0% { transform: translate(0, 0) scale(1); } 100% { transform: translate(5%, 5%) scale(1.1); } }

/* ================= 🌟 滚动与排版容器 ================= */
.gallery-scroll-area {
  position: relative; z-index: 10; width: 100%; height: 100%;
  overflow-y: auto; overflow-x: hidden;
}
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }

.gallery-content {
  max-width: 800px; margin: 0 auto; padding: 10vh 40px 10vh 40px;
  display: flex; flex-direction: column; align-items: center;
}

/* ================= 🌟 头部与序言 ================= */
.gallery-header { text-align: center; margin-bottom: 50px; width: 100%; animation: fade-in-up 1s ease-out; }
.gallery-title { font-family: 'Noto Serif SC', serif; font-size: 42px; font-weight: 700; color: #f8fafc; letter-spacing: 12px; margin: 0 0 16px 12px; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
.gallery-subtitle { font-family: monospace; font-size: 13px; color: #94a3b8; letter-spacing: 4px; margin: 0; }
.elegant-divider { width: 1px; height: 60px; background: linear-gradient(to bottom, rgba(255,255,255,0.3), transparent); margin: 30px auto 0 auto; }

.gallery-prose { width: 100%; margin-bottom: 60px; animation: fade-in-up 1.2s ease-out forwards; opacity: 0; }
.gallery-prose p {
  font-family: 'Noto Serif SC', serif; font-size: 15px; line-height: 2.2; color: #cbd5e1;
  text-indent: 2em; margin-bottom: 16px; text-align: justify;
}

/* ================= 🌟 记忆列表项 (List Design) ================= */
.fragments-section { width: 100%; animation: fade-in-up 1.4s ease-out forwards; opacity: 0; }
.section-title { display: flex; align-items: center; justify-content: center; gap: 16px; margin-bottom: 30px; font-family: 'Noto Serif SC', serif; font-size: 14px; color: #64748b; font-style: italic; }
.diamond { width: 4px; height: 4px; background: #64748b; transform: rotate(45deg); }

.fragment-list { display: flex; flex-direction: column; gap: 12px; }

.fragment-item {
  position: relative; display: flex; align-items: center; padding: 20px 24px;
  background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px; overflow: hidden; cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.fragment-item:hover {
  background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.frag-index { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 60px; border-right: 1px solid rgba(255,255,255,0.1); margin-right: 20px; padding-right: 20px; flex-shrink: 0; }
.frag-index span { font-size: 10px; color: #64748b; letter-spacing: 2px; }
.frag-index .num { font-family: 'Noto Serif SC', serif; font-size: 20px; color: #94a3b8; font-weight: bold; margin-top: 4px; transition: color 0.3s;}

.frag-text { flex: 1; font-family: 'Noto Serif SC', serif; font-size: 15px; color: #e2e8f0; line-height: 1.6; padding-right: 20px; transition: color 0.3s;}
.frag-code { font-family: monospace; font-size: 14px; letter-spacing: 2px; color: #cbd5e1; background: rgba(0,0,0,0.3); padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05); flex-shrink: 0; transition: all 0.3s; }
.fragment-item:hover .frag-code { background: rgba(255,255,255,0.1); color: #fff; }

.frag-hover-glow { position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent); transform: skewX(-20deg); transition: none; pointer-events: none; }
.fragment-item:hover .frag-hover-glow { animation: shine 1s ease-out; }
@keyframes shine { 100% { left: 200%; } }

/* ================= 🌟 视觉探索反馈状态 ================= */
/* 1. 当前所在页 (160615) - 彻底置灰，不可点击 */
.fragment-item.is-current { opacity: 0.3; pointer-events: none; border-color: transparent; }

/* 2. 已浏览过的碎片 - 整体变暗，但依旧保留细微的可点击感知 */
.fragment-item.is-visited {
  opacity: 0.55;
  background: rgba(255, 255, 255, 0.01);
  border-color: rgba(255, 255, 255, 0.02);
}
.fragment-item.is-visited .frag-text { color: #94a3b8; }
.fragment-item.is-visited .frag-index .num { color: #64748b; }
.fragment-item.is-visited .frag-code { color: #64748b; background: rgba(0,0,0,0.15); border-color: transparent; }

/* 悬停时稍微点亮，方便再次阅读 */
.fragment-item.is-visited:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.03);
  border-color: rgba(255, 255, 255, 0.1);
}
.fragment-item.is-visited:hover .frag-text { color: #e2e8f0; }

/* ================= 🌟 底部按钮 ================= */
.gallery-footer { margin-top: 60px; display: flex; gap: 24px; animation: fade-in-up 1.6s ease-out forwards; opacity: 0; }

.quiet-btn {
  background: transparent; border: 1px solid rgba(255, 255, 255, 0.2);
  color: #94a3b8; padding: 12px 36px; border-radius: 50px;
  font-family: 'Noto Serif SC', serif; font-size: 15px; letter-spacing: 2px;
  cursor: pointer; transition: all 0.4s ease;
}
.quiet-btn:hover { background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.6); color: #fff; transform: translateY(-2px); }
.forward-btn { border-color: rgba(255, 255, 255, 0.4); color: #e2e8f0; }

@keyframes fade-in-up {
  0% { opacity: 0; transform: translateY(20px); filter: blur(5px); }
  100% { opacity: 1; transform: translateY(0); filter: blur(0); }
}

/* ================= 📱 移动端适配 ================= */
@media (max-width: 768px) {
  .gallery-content { padding: 8vh 20px 8vh 20px; }

  .gallery-title { font-size: 32px; letter-spacing: 8px; margin-left: 8px; }
  .elegant-divider { height: 40px; margin-top: 20px; }

  .gallery-prose { margin-bottom: 40px; }
  .gallery-prose p { font-size: 14px; line-height: 2; margin-bottom: 12px; }

  .section-title { font-size: 12px; margin-bottom: 20px; }

  .fragment-item { padding: 16px; flex-direction: column; align-items: flex-start; gap: 12px; }

  .frag-index { width: 100%; border-right: none; border-bottom: 1px solid rgba(255,255,255,0.05); margin-right: 0; padding-right: 0; padding-bottom: 12px; flex-direction: row; justify-content: flex-start; align-items: baseline; gap: 8px; }
  .frag-index span { font-size: 12px; }
  .frag-index .num { margin-top: 0; font-size: 16px; }

  .frag-text { padding-right: 0; font-size: 14px; line-height: 1.7; width: 100%; }

  .frag-code { width: 100%; text-align: center; margin-top: 4px; padding: 8px; box-sizing: border-box; background: rgba(255,255,255,0.03); }

  .gallery-footer { flex-direction: column; width: 100%; gap: 16px; margin-top: 40px; }
  .quiet-btn { width: 100%; }
}
</style>
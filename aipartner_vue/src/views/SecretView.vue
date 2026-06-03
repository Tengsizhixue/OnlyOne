<template>
  <div class="secret-root-container">

    <component
      v-if="currentComponent"
      :is="currentComponent"
      @back="handleBack"
    />

    <div v-else class="gallery-view-container">

      <div class="gallery-bg">
        <div class="ambient-light light-1"></div>
        <div class="ambient-light light-2"></div>
        <div class="noise-overlay"></div>
      </div>

      <div class="gallery-scroll-area custom-scrollbar">
        <div class="gallery-content">

          <header class="gallery-header">
            <h1 class="gallery-title">真正的前言</h1>
            <p class="gallery-subtitle">160615</p>
            <div class="elegant-divider"></div>
          </header>

          <section class="gallery-prose">
            <p>这个数字是我网址的二级域名，后面会说这个数字是怎么来的。顶级域名 .xyz 单纯是因为便宜，一年就一刀乐。</p>
             <p><del>回到侧边框后，你会看到其他的一些问题，你可以尝试着去问 AI 里面的问题。如果问的角色没错，AI 的回复中会有其他的 6 位数字；如果 AI 没给你正确的答案，可能是它抽风了，你可以多问几遍。</del></p>
            <p>现在不需要再问ai了，内容在下面已经列出</p>
            <p>内容太多，有很多的废话，如果感兴趣可以看看后面的内容</p>
            <p>如果你真的闲着没事干看完了，也不要问我关于这里面的任何事情，我不想讨论。因为很多事情都是很久以前的，聊着没意义</p>
          </section>

          <!-- 🌟 常规记忆碎片列表 -->
          <section class="fragments-section">
            <div class="section-title">
              <span class="diamond"></span>
              <span>点击翻阅下方的记录：</span>
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
                <div class="frag-index">
                  <span>碎片</span>
                  <span class="num">{{ String(index + 1).padStart(2, '0') }}</span>
                </div>
                <div class="frag-text">{{ quest.question }}</div>
                <div class="frag-code">{{ quest.code }}</div>
                <div class="frag-hover-glow"></div>
              </div>

              <!-- 最终的废话结局 -->
              <div 
                class="fragment-item extra-item" 
                :class="{ 'is-visited': visitedExtras.final }"
                @click="goToFinalFromList"
              >
                <div class="frag-index">
                  <span>终章</span>
                  <span class="num">00</span>
                </div>
                <div class="frag-text">结局</div>
                <div class="frag-code">FINAL</div>
                <div class="frag-hover-glow"></div>
              </div>
            </div>
          </section>

          <!-- 🌟 新增附加目录：不隐藏，直接展示，并提示拦截 -->
          <section class="fragments-section extra-section">
            <div class="section-title">
              <span class="diamond"></span>
              <span>附加目录（不建议阅读）：</span>
              <span class="diamond"></span>
            </div>

            <div class="fragment-list">
              <!-- 其他隐藏随笔 -->
              <div
                v-for="(extra, index) in EXTRA_LIST"
                :key="extra.realCode"
                class="fragment-item extra-item"
                :class="{ 'is-visited': visitedExtras['extra' + extra.realCode] }"
                @click="handleExtraClick(extra)"
              >
                <div class="frag-index">
                  <span>附加</span>
                  <span class="num">??</span>
                </div>
                <div class="frag-text">{{ extra.name }}</div>
                <div class="frag-code">{{ extra.code }}</div>
                <div class="frag-hover-glow"></div>
              </div>
            </div>
          </section>

          <!-- 底部归宿 -->
          <footer class="gallery-footer">
            <button class="quiet-btn back-btn" @click="handleBack">
              合上展卷
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
import { ElMessageBox } from 'element-plus'
import { unlockCode, SECRET_QUESTS, unlockedCodes, visitedExtras, markExtraAsVisited } from '../store/questState.js'

import LiHongBaoView from './secrets/LiHongBaoView.vue'
import GameMemoryView from './secrets/GameMemoryView.vue'
import AstlibraView from './secrets/AstlibraView.vue'
import VioletLetterView from './secrets/VioletLetterView.vue'
import MusicView from './secrets/MusicView.vue'
import GameView from './secrets/GameView.vue'

// 🌟 新增的附加页面引用
import Extra200326View from './secrets/Extra200326View.vue'
import Extra210318View from './secrets/Extra210318View.vue'
import Extra230602View from './secrets/Extra230602View.vue'

const props = defineProps({
  secretCode: { type: String, default: '' }
})

const router = useRouter()
const route = useRoute()

onMounted(() => { if (props.secretCode) unlockCode(props.secretCode) })
watch(() => props.secretCode, (newCode) => { if (newCode) unlockCode(newCode) })

const handleBack = () => {
  // 返回到 160615 主界面
  router.push({
    name: 'secret',
    params: { secretCode: '160615' },
    query: {
      role: route.query.role,
      session: route.query.session
    }
  })
}

// 🌟 附加目录的数据配置
const EXTRA_LIST = [
  { name: '附加1', code: '？？？？', realCode: '200326' },
  { name: '附加2', code: '？？？？', realCode: '210318' },
  { name: '附加3', code: '？？？？', realCode: '230602' },
]

const goToFinalFromList = () => {
  markExtraAsVisited('final')
  router.push('/final')
}

const handleExtraClick = (item) => {
  ElMessageBox.confirm('这些内容我虽然写了，但是不推荐你看', '附加内容', {
    confirmButtonText: '执意要看',
    cancelButtonText: '还是算了',
    type: 'warning',
    center: true,
    customClass: 'custom-extra-msgbox'
  }).then(() => {
    // 标记为已访问
    markExtraAsVisited('extra' + item.realCode)
    router.push({
      name: 'secret',
      params: { secretCode: item.realCode },
      query: {
        role: route.query.role,
        session: route.query.session
      }
    })
  }).catch(() => {})
}

const jumpToSecret = (code) => {
  if (code === '160615') return
  unlockCode(code)
  router.push({
    name: 'secret',
    params: { secretCode: code },
    query: {
      role: route.query.role,
      session: route.query.session
    }
  })
}

// 移除了 QQdisappearView 的映射
const viewMap = {
  '260315': LiHongBaoView,
  '251027': GameMemoryView,
  '260410': AstlibraView,
  '191001': VioletLetterView,
  '240802': MusicView,
  '180818': GameView,
  '200326': Extra200326View,
  '210318': Extra210318View,
  '230602': Extra230602View
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

.gallery-scroll-area { position: relative; z-index: 10; width: 100%; height: 100%; overflow-y: auto; overflow-x: hidden; }
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }

.gallery-content { max-width: 800px; margin: 0 auto; padding: 10vh 40px 10vh 40px; display: flex; flex-direction: column; align-items: center; }

.gallery-header { text-align: center; margin-bottom: 50px; width: 100%; animation: fade-in-up 1s ease-out; }
.gallery-title { font-family: 'Noto Serif SC', serif; font-size: 42px; font-weight: 700; color: #f8fafc; letter-spacing: 12px; margin: 0 0 16px 12px; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
.gallery-subtitle { font-family: monospace; font-size: 13px; color: #94a3b8; letter-spacing: 4px; margin: 0; }
.elegant-divider { width: 1px; height: 60px; background: linear-gradient(to bottom, rgba(255,255,255,0.3), transparent); margin: 30px auto 0 auto; }

.gallery-prose { width: 100%; margin-bottom: 60px; animation: fade-in-up 1.2s ease-out forwards; opacity: 0; }
.gallery-prose p { font-family: 'Noto Serif SC', serif; font-size: 15px; line-height: 2.2; color: #cbd5e1; text-indent: 2em; margin-bottom: 16px; text-align: justify; }

.fragments-section { width: 100%; animation: fade-in-up 1.4s ease-out forwards; opacity: 0; }
.section-title { display: flex; align-items: center; justify-content: center; gap: 16px; margin-bottom: 30px; font-family: 'Noto Serif SC', serif; font-size: 14px; color: #64748b; font-style: italic; }
.diamond { width: 4px; height: 4px; background: #64748b; transform: rotate(45deg); }

.fragment-list { display: flex; flex-direction: column; gap: 12px; }

.fragment-item { position: relative; display: flex; align-items: center; padding: 20px 24px; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; overflow: hidden; cursor: pointer; transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); }
.fragment-item:hover { background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.15); transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }

.frag-index { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 60px; border-right: 1px solid rgba(255,255,255,0.1); margin-right: 20px; padding-right: 20px; flex-shrink: 0; }
.frag-index span { font-size: 10px; color: #64748b; letter-spacing: 2px; }
.frag-index .num { font-family: 'Noto Serif SC', serif; font-size: 20px; color: #94a3b8; font-weight: bold; margin-top: 4px; transition: color 0.3s;}

.frag-text { flex: 1; font-family: 'Noto Serif SC', serif; font-size: 15px; color: #e2e8f0; line-height: 1.6; padding-right: 20px; transition: color 0.3s;}
.frag-code { font-family: monospace; font-size: 14px; letter-spacing: 2px; color: #cbd5e1; background: rgba(0,0,0,0.3); padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05); flex-shrink: 0; transition: all 0.3s; }
.fragment-item:hover .frag-code { background: rgba(255,255,255,0.1); color: #fff; }

.frag-hover-glow { position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent); transform: skewX(-20deg); transition: none; pointer-events: none; }
.fragment-item:hover .frag-hover-glow { animation: shine 1s ease-out; }
@keyframes shine { 100% { left: 200%; } }

.fragment-item.is-current { opacity: 0.3; pointer-events: none; border-color: transparent; }
.fragment-item.is-visited { opacity: 0.55; background: rgba(255, 255, 255, 0.01); border-color: rgba(255, 255, 255, 0.02); }
.fragment-item.is-visited .frag-text { color: #94a3b8; }
.fragment-item.is-visited .frag-index .num { color: #64748b; }
.fragment-item.is-visited .frag-code { color: #64748b; background: rgba(0,0,0,0.15); border-color: transparent; }
.fragment-item.is-visited:hover { opacity: 1; background: rgba(255, 255, 255, 0.03); border-color: rgba(255, 255, 255, 0.1); }
.fragment-item.is-visited:hover .frag-text { color: #e2e8f0; }

/* 🌟 附加目录特定样式 */
.extra-section { margin-top: 50px; animation: fade-in-up 1.6s ease-out forwards; opacity: 0; }
.extra-item { border: 1px dashed rgba(255, 255, 255, 0.1) !important; background: rgba(0, 0, 0, 0.2) !important; }
.extra-item:hover { border-color: rgba(255, 255, 255, 0.3) !important; background: rgba(255, 255, 255, 0.05) !important; }

.gallery-footer { margin-top: 60px; display: flex; gap: 24px; animation: fade-in-up 1.8s ease-out forwards; opacity: 0; }
.quiet-btn { background: transparent; border: 1px solid rgba(255, 255, 255, 0.2); color: #94a3b8; padding: 12px 36px; border-radius: 50px; font-family: 'Noto Serif SC', serif; font-size: 15px; letter-spacing: 2px; cursor: pointer; transition: all 0.4s ease; }
.quiet-btn:hover { background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.6); color: #fff; transform: translateY(-2px); }

@keyframes fade-in-up { 0% { opacity: 0; transform: translateY(20px); filter: blur(5px); } 100% { opacity: 1; transform: translateY(0); filter: blur(0); } }

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

/* 自定义 MsgBox 的样式可以通过覆盖 Element Plus 类名实现，这里只做基础保证 */
:global(.custom-extra-msgbox) {
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}
:global(.custom-extra-msgbox .el-message-box__title) { color: #f8fafc; }
:global(.custom-extra-msgbox .el-message-box__content) { color: #cbd5e1; }
</style>
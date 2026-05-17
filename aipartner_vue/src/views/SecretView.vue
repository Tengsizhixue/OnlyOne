<template>
  <div class="secret-root-container">

    <!-- 1. 具体的彩蛋子页面渲染区 (完全独立，互不干扰) -->
    <component
      v-if="currentComponent"
      :is="currentComponent"
      @back="handleBack"
    />

    <!-- 2. 160615 记忆总目录页 (当你没有匹配到特定子组件时显示) -->
    <div v-else class="archive-view-container">
      <div class="archive-bg">
        <div class="cyber-grid"></div>
        <div class="bg-glow"></div>
      </div>

      <div class="archive-panel glass-panel shadow-2xl">
        <!-- 头部标题区 -->
        <div class="archive-header">
          <div class="status-indicator">
            <span class="pulse-dot"></span>
            <span class="status-text">ARCHIVE_NODE // 160615</span>
          </div>
          <h1 class="archive-title">记忆索引目录</h1>
          <p class="archive-subtitle">所有散落的碎片，都在这里汇聚。</p>
        </div>

        <!-- 核心内容滚动区 -->
        <div class="archive-body custom-scrollbar">
          <div class="intro-box">
            <p>这个数字是我网址的一级域名，文章的最后会说这个数字是怎么来的。顶级域名 .xyz 单纯是因为便宜，1年就1刀乐。</p>
            <p>回到侧边框后，你会看到其他的一些问题，你可以尝试着去问 AI 里面的问题。如果问的角色没错，AI 的回复中会有其他的 6 位数字；如果 AI 没给你正确的答案，可能是它抽风了，你可以多问几遍。</p>
            <p>内容太多了，如果感兴趣可以看看后面的内容，也有很多的废话，这应该是最后一次在网上讨论以前的事了。</p>
          </div>

          <div class="divider">
            <span class="divider-line"></span>
            <span class="divider-text">MEMORY_FRAGMENTS</span>
            <span class="divider-line"></span>
          </div>

          <p class="hint-text">如果你懒得一个个去问，可以直接点击下方的档案卡片跃迁：</p>

          <!-- 🌟 动态生成的档案卡片网格 -->
          <div class="quest-grid">
            <div
              v-for="(quest, index) in SECRET_QUESTS"
              :key="quest.code"
              class="quest-card"
              :class="{ 'current-node': quest.code === '160615' }"
              @click="jumpToSecret(quest.code)"
            >
              <div class="card-glare"></div>
              <div class="quest-id">NO. 0{{ index + 1 }}</div>
              <div class="quest-q">{{ quest.question }}</div>
              <div class="quest-code-wrapper">
                <span class="code-label">ACCESS_CODE</span>
                <span class="code-value">{{ quest.code }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部操作区 -->
        <div class="archive-footer">
          <button class="action-btn back-btn" @click="handleBack">
             返回聊天
          </button>
          <button v-if="isAllUnlocked" class="action-btn forward-btn" @click="goToFinal">
            前往终点
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// 🌟 核心修复：删除了不存在的 resetQuestProgress，只保留你文件里真实存在的三个变量
import { unlockCode, isAllUnlocked, SECRET_QUESTS } from '../store/questState.js'

import LiHongBaoView from './secrets/LiHongBaoView.vue'
import GameMemoryView from './secrets/GameMemoryView.vue'
import AstlibraView from './secrets/AstlibraView.vue'
import VioletLetterView from './secrets/VioletLetterView.vue'
import MusicView from './secrets/MusicView.vue'
import GameView from './secrets/GameView.vue'
import QQdisappearView from './secrets/QQdisappearView.vue' // 确保使用相对路径

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

// 🌟 快捷跃迁功能：点击卡片直接前往对应的彩蛋页
const jumpToSecret = (code) => {
  if (code === '160615') return // 已经是当前页了，不跳
  unlockCode(code) // 确保解锁
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
.secret-root-container { display: flex; justify-content: center; align-items: center; width: 100%; height: 100dvh; position: fixed; top: 0; left: 0; z-index: 999; overflow: hidden; }

/* ================= 🌟 160615 专属背景 ================= */
.archive-view-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
.archive-bg { position: absolute; inset: 0; background-color: #050505; z-index: -1; overflow: hidden; }
.cyber-grid {
  position: absolute; inset: -50%;
  background-image: linear-gradient(rgba(167, 139, 250, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(167, 139, 250, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
  transform: perspective(1000px) rotateX(60deg) translateY(-100px) translateZ(-200px);
  animation: grid-move 20s linear infinite;
}
.bg-glow {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 80vw; height: 80vw; background: radial-gradient(circle, rgba(124, 58, 237, 0.15) 0%, transparent 70%);
  filter: blur(60px); pointer-events: none;
}
@keyframes grid-move {
  0% { transform: perspective(1000px) rotateX(60deg) translateY(0) translateZ(-200px); }
  100% { transform: perspective(1000px) rotateX(60deg) translateY(50px) translateZ(-200px); }
}

/* ================= 🌟 档案面板主框架 ================= */
.archive-panel {
  width: 95vw; max-width: 1100px; height: 90vh;
  background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(139, 92, 246, 0.2); box-shadow: 0 30px 60px rgba(0,0,0,0.6), inset 0 0 20px rgba(139, 92, 246, 0.05);
  border-radius: 20px;
  display: flex; flex-direction: column; overflow: hidden;
}

/* 头部 */
.archive-header {
  padding: 30px 40px 20px 40px; border-bottom: 1px solid rgba(139, 92, 246, 0.2);
  background: linear-gradient(180deg, rgba(139, 92, 246, 0.05) 0%, transparent 100%);
  text-align: center; position: relative; flex-shrink: 0;
}
.status-indicator { display: inline-flex; align-items: center; gap: 8px; margin-bottom: 12px; background: rgba(0,0,0,0.4); padding: 4px 12px; border-radius: 12px; border: 1px solid rgba(167, 139, 250, 0.3); }
.pulse-dot { width: 8px; height: 8px; border-radius: 50%; background: #a78bfa; box-shadow: 0 0 10px #a78bfa; animation: pulse 2s infinite; }
.status-text { font-family: monospace; font-size: 12px; color: #c4b5fd; letter-spacing: 1px; }
.archive-title { font-size: 32px; font-weight: 800; color: #f3e8ff; margin: 0 0 8px 0; letter-spacing: 2px; text-shadow: 0 0 15px rgba(167, 139, 250, 0.4); }
.archive-subtitle { font-size: 14px; color: #a78bfa; margin: 0; letter-spacing: 1px; }

/* 内容滚动区 */
.archive-body { flex: 1; overflow-y: auto; overflow-x: hidden; padding: 30px 40px; }
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.3); border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(139, 92, 246, 0.6); }

.intro-box { background: rgba(0, 0, 0, 0.3); border-left: 3px solid #8b5cf6; padding: 24px; border-radius: 0 12px 12px 0; margin-bottom: 30px; }
.intro-box p { font-size: 15px; color: #e2e8f0; line-height: 1.8; margin: 0 0 12px 0; text-align: left; }
.intro-box p:last-child { margin-bottom: 0; }

.divider { display: flex; align-items: center; gap: 16px; margin: 40px 0 20px 0; }
.divider-line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, rgba(167, 139, 250, 0.4), transparent); }
.divider-text { font-family: monospace; color: #c4b5fd; font-size: 13px; letter-spacing: 2px; }

.hint-text { text-align: center; color: #94a3b8; font-size: 14px; margin-bottom: 24px; font-style: italic; }

/* ================= 🌟 档案卡片网格 ================= */
.quest-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  padding-bottom: 20px;
}

.quest-card {
  position: relative; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 12px; padding: 20px; text-align: left; overflow: hidden; cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex; flex-direction: column; gap: 12px;
}
.quest-card::before {
  content: ''; position: absolute; inset: 0; background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), transparent);
  opacity: 0; transition: opacity 0.4s;
}
.quest-card:hover {
  transform: translateY(-4px); border-color: rgba(167, 139, 250, 0.6);
  box-shadow: 0 10px 20px rgba(0,0,0,0.4), 0 0 15px rgba(139, 92, 246, 0.2);
}
.quest-card:hover::before { opacity: 1; }

.current-node { pointer-events: none; border-color: rgba(255, 255, 255, 0.1); opacity: 0.5; filter: grayscale(1); }

.card-glare { position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%); opacity: 0; transform: scale(0.5); transition: all 0.6s; pointer-events: none; }
.quest-card:hover .card-glare { opacity: 1; transform: scale(1) translate(10%, 10%); }

.quest-id { font-family: monospace; font-size: 12px; color: #a78bfa; font-weight: bold; letter-spacing: 1px; }
.quest-q { font-size: 15px; color: #f8fafc; line-height: 1.6; flex: 1; font-weight: 500;}
.quest-code-wrapper { display: flex; align-items: center; justify-content: space-between; background: rgba(0,0,0,0.4); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(139, 92, 246, 0.15); margin-top: auto;}
.code-label { font-family: monospace; font-size: 11px; color: #94a3b8; }
.code-value { font-family: monospace; font-size: 16px; font-weight: bold; color: #d8b4fe; letter-spacing: 2px; }

/* 底部按钮 */
.archive-footer {
  padding: 20px 40px; border-top: 1px solid rgba(139, 92, 246, 0.2);
  background: rgba(0, 0, 0, 0.2); display: flex; justify-content: center; gap: 20px; flex-shrink: 0;
}
.action-btn {
  padding: 12px 30px; border-radius: 50px; font-size: 15px; font-weight: 600; cursor: pointer;
  display: flex; align-items: center; gap: 8px; transition: all 0.3s;
}
.back-btn { background: transparent; border: 1px solid rgba(167, 139, 250, 0.4); color: #c4b5fd; }
.back-btn:hover { background: rgba(167, 139, 250, 0.1); color: #fff; transform: translateX(-3px); }
.forward-btn { background: #8b5cf6; border: none; color: white; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); }
.forward-btn:hover { background: #7c3aed; transform: translateX(3px); box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6); }

@keyframes pulse { 0% { opacity: 1; box-shadow: 0 0 10px #a78bfa; } 50% { opacity: 0.4; box-shadow: 0 0 2px #a78bfa; } 100% { opacity: 1; box-shadow: 0 0 10px #a78bfa; } }

/* ================= 📱 移动端适配 ================= */
@media (max-width: 768px) {
  .archive-panel { width: 100%; height: 100dvh; border-radius: 0; border: none; }
  .archive-header { padding: 24px 20px 16px 20px; }
  .archive-title { font-size: 24px; }
  .archive-subtitle { font-size: 12px; }

  .archive-body { padding: 20px 16px; }
  .intro-box { padding: 16px; margin-bottom: 24px; }
  .intro-box p { font-size: 14px; }

  .quest-grid { grid-template-columns: 1fr; gap: 16px; }
  .quest-card { padding: 16px; }
  .quest-q { font-size: 14px; }
  .code-value { font-size: 14px; }

  .archive-footer { padding: 16px 20px; flex-direction: column; gap: 12px; }
  .action-btn { justify-content: center; width: 100%; }
}
</style>
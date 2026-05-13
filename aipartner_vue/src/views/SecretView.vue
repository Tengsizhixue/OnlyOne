<template>
  <div class="secret-root-container">
    <component
      v-if="currentComponent"
      :is="currentComponent"
      @back="handleBack"
    />
    <div v-else class="secret-view-container">
      <div class="secret-bg fallback-bg"></div>
      <div class="secret-page glass-panel shadow-2xl">
        <div class="secret-content">
          <h1 class="highlight-text">🎉 恭喜你找到了特殊页面！</h1>
          <div class="content-box">
            <p>这个数字是我网址的一级域名。顶级域名.xyz单纯是因为便宜，1年就1刀乐。</p>
            <p>回到侧边框后，你会看到其他的一些问题，你可以尝试着去问ai里面的问题，
              如果你觉得问的角色没错，但是ai却没给你正确的答案</p>
            <p>要么是ai抽风了，你可以多问几遍，如果还是没反应那就是你在瞎**问</p>

            <div class="bottom-action">
              <button class="shimmer-btn" @click="handleBack">
                {{ isAllUnlocked ? '点击查看最后的废话' : '返回聊天' }}
              </button>
              <!-- 🐛 临时调试按钮：重置所有进度 -->
              <button class="debug-reset-btn" @click="handleReset" title="重置所有谜题进度">
                🔄 重置进度
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { unlockCode, isAllUnlocked, resetQuestProgress } from '../store/questState.js'

import LiHongBaoView from './secrets/LiHongBaoView.vue'
import GameMemoryView from './secrets/GameMemoryView.vue'
import AstlibraView from './secrets/AstlibraView.vue'
import VioletLetterView from './secrets/VioletLetterView.vue'
import MusicView from './secrets/MusicView.vue'
import GameView from './secrets/GameView.vue'

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
  if (isAllUnlocked.value) {
    router.push('/final')
  } else {
    router.push({
      name: 'chat',
      query: {
        view: 'room',
        role: route.query.role,
        session: route.query.session
      }
    })
  }
}

const handleReset = () => {
  if (confirm('确定要重置所有谜题进度吗？')) {
    resetQuestProgress()
    alert('✅ 已重置！页面将刷新...')
    window.location.reload()
  }
}

const viewMap = {
  '260315': LiHongBaoView,
  '251027': GameMemoryView,
  '260410': AstlibraView,
  '191001': VioletLetterView,
  '240802': MusicView,
  '180818': GameView
}

const currentComponent = computed(() => {
  return viewMap[props.secretCode] || null
})
</script>

<style scoped>
/* 💡 核心修复：使用 100dvh 而不是 100vh，这样可以自适应浏览器地址栏高度 */
.secret-root-container { display: flex; justify-content: center; align-items: center; width: 100%; height: 100dvh; position: fixed; top: 0; left: 0; z-index: 999; overflow: hidden; }
.secret-view-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
.fallback-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: #0f172a; z-index: -1; }

.secret-page {
  width: 95vw; max-width: 1200px; height: 90vh; padding: 40px 60px; text-align: center; border-radius: 24px; z-index: 1; color: #f8fafc;
  background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.3);
  display: flex; flex-direction: column;
  box-sizing: border-box; /* 💡 核心修复：防止 padding 撑破高度 */
}

.secret-content { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%; overflow: hidden; }
.highlight-text { color: #a78bfa; margin-bottom: 20px; font-size: 32px; font-weight: bold; flex-shrink: 0;}

.content-box {
  background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 40px; border-radius: 16px; margin-bottom: 20px; width: 100%;
  flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
  font-size: 18px; overflow-y: auto;
}
.bottom-action { margin-top: 30px; display: flex; justify-content: center; }

@media (max-width: 768px) {
  .secret-page {
    width: 100%; height: 100dvh; border-radius: 0;
    padding: 70px 20px 20px; /* 💡 缩小 padding */
    border: none; background: rgba(15, 23, 42, 0.3); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  }
  .content-box { padding: 18px; font-size: 14px; margin-bottom: 16px; border-radius: 12px; line-height: 1.8; }
  .highlight-text { font-size: 24px; margin-bottom: 6px; }
  .bottom-action { margin-top: 20px; }
}
</style>
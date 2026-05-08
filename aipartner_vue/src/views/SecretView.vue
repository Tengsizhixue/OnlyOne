<!-- Template 保持不变 -->
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
            <p>但是这里什么都没有，如果你后面发现了其他特殊的数字，可以试一试在对话框里输入</p>
          </div>
          <!-- 💡 兜底页面也支持去往终局 -->
          <button class="enter-btn shimmer-btn" @click="handleBack">
             {{ isAllUnlocked ? '开启终局之门 ✨' : '返回聊天' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue' // 💡 引入生命周期
import { useRouter } from 'vue-router'
// 💡 引入解密状态
import { unlockCode, isAllUnlocked } from '../store/questState.js'

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

// 💡 核心逻辑：当页面加载，或者密码变化时，将该密码记录为已解锁！
onMounted(() => {
  if (props.secretCode) unlockCode(props.secretCode)
})
watch(() => props.secretCode, (newCode) => {
  if (newCode) unlockCode(newCode)
})

// 💡 核心逻辑：接管返回按钮，如果所有拼图凑齐，去结局！
const handleBack = () => {
  if (isAllUnlocked.value) {
    router.push('/final')
  } else {
    router.push('/chat')
  }
}

const viewMap = {
  '260315': LiHongBaoView,
  '251027': GameMemoryView,
  '260410': AstlibraView,
  '19xxxx': VioletLetterView,
  '240802': MusicView,
  '180818': GameView
}

const currentComponent = computed(() => {
  return viewMap[props.secretCode] || null
})
</script>

<style scoped>
/* ========== CSS 原封不动 ========== */
.secret-root-container { display: flex; justify-content: center; align-items: center; width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; z-index: 999; }
.secret-view-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
.fallback-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: #0f172a; z-index: -1; }
.secret-page { width: 95vw; max-width: 1200px; height: 90vh; padding: 40px 60px; text-align: center; border-radius: 24px; z-index: 1; color: #f8fafc; background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.3); display: flex; flex-direction: column; }
.secret-content { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; }
.highlight-text { color: #a78bfa; margin-bottom: 20px; font-size: 32px; font-weight: bold; flex-shrink: 0;}
.content-box { background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.1); padding: 40px; border-radius: 16px; margin-bottom: 30px; width: 100%; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 18px; }
.enter-btn { flex-shrink: 0; }
@media (max-width: 768px) {
  .secret-page { width: 100vw; height: 100dvh; border-radius: 0; padding: 50px 20px 30px; border: none; background: rgba(15, 23, 42, 0.3); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
  .content-box { padding: 18px; font-size: 14px; margin-bottom: 20px; border-radius: 12px; line-height: 1.8; }
  .highlight-text { font-size: 24px; margin-bottom: 6px; }
}
</style>
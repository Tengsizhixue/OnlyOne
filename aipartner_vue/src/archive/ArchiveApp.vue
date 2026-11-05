<template>
  <div class="archive-page">
    <div aria-hidden="true" class="bg" :class="{ 'is-lit': lit }">
      <span class="warm"></span>
      <span class="lamp"></span>
      <span class="noise"></span>
    </div>

    <main class="wrap">
      <div v-if="loading" class="board skel-board" v-cloak>
        <div v-for="n in 3" :key="n" class="col skel">
          <div class="skel-line skel-w55"></div>
          <div class="skel-line skel-w85"></div>
          <div class="skel-line skel-w40"></div>
          <div class="skel-line skel-w70"></div>
          <div class="skel-line skel-w30"></div>
        </div>
      </div>
      <div v-else-if="loadError" class="archive-status error">{{ loadError }}</div>

      <div v-else class="board">
        <p v-if="stateError" class="archive-inline-error">{{ stateError }}</p>

        <ArchiveStage
          v-for="(stage, index) in content.stages"
          :key="stage.id"
          :stage="stage"
          :names="names"
          :unlocked="!!unlockedStages[stage.id]"
          :revealing="!!revealingStages[stage.id]"
          :order="index"
          :feedback="stageFeedback[stage.id]"
          @unlock="onUnlockStage"
        />
      </div>

      <div class="foot"></div>
    </main>

    <button
      class="to-top"
      :class="{ 'is-show': showToTop }"
      type="button"
      aria-label="回到顶部"
      @click="toTop"
    >
      <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">
        <path
          d="M12 20V6M6 12l6-6 6 6"
          fill="none"
          stroke="currentColor"
          stroke-width="1.7"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import ArchiveStage from './components/ArchiveStage.vue'
import { getContent, getState, unlockStage } from './api.js'
import { initAmbientLight, initTouchFeedback } from './fx.js'

const content = ref(null)
const names = ref({})
const unlockedStages = ref({})
const revealingStages = reactive({})
const stageFeedback = reactive({})

// 只要揭开过任意一栏，环境光就从冷灰缓缓转暖（纯视觉，不加任何文字）
const lit = computed(() => Object.keys(unlockedStages.value).length > 0)

const loading = ref(true)
const loadError = ref('')
const stateError = ref('')

// 回到顶部：向下滚过一屏再淡入；显隐只切 class，位移/淡入交给 CSS
const showToTop = ref(false)
let toTopRaf = 0

onMounted(async () => {
  initAmbientLight()
  initTouchFeedback()

  window.addEventListener('scroll', onScrollToTop, { passive: true })
  window.addEventListener('resize', onScrollToTop, { passive: true })
  updateToTop()

  const [contentResult, stateResult] = await Promise.allSettled([getContent(), getState()])

  if (contentResult.status === 'rejected') {
    loadError.value = contentResult.reason?.message || '档案读取失败，请稍后再试。'
    loading.value = false
    return
  }

  content.value = contentResult.value

  if (stateResult.status === 'fulfilled') {
    const state = stateResult.value
    names.value = state.names || {}
    for (const id of state.stages || []) {
      unlockedStages.value[id] = true
    }
  } else {
    stateError.value = '进度读取失败，本次解锁可能无法保存。'
  }

  loading.value = false
})

async function onUnlockStage(stageId, value) {
  const name = (value || '').trim()
  if (!name) return
  stageFeedback[stageId] = { text: '核对中…', ok: false, busy: true }
  try {
    const res = await unlockStage(stageId, name)
    names.value = { ...names.value, ...(res.names || {}) }
    unlockedStages.value[stageId] = true
    revealingStages[stageId] = true
    stageFeedback[stageId] = { text: '本阶段已解锁。', ok: true, busy: false }
  } catch (e) {
    stageFeedback[stageId] = { text: e.message, ok: false, busy: false }
  }
}

function updateToTop() {
  toTopRaf = 0
  showToTop.value = window.scrollY > window.innerHeight
}

function onScrollToTop() {
  if (!toTopRaf) toTopRaf = requestAnimationFrame(updateToTop)
}

function toTop() {
  const reduce =
    window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches
  window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' })
}

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScrollToTop)
  window.removeEventListener('resize', onScrollToTop)
  if (toTopRaf) cancelAnimationFrame(toTopRaf)
})
</script>

<style>
.archive-inline-error {
  grid-column: 1 / -1;
  margin: 0 0 12px;
  color: #c9a0a0;
  font-size: 12px;
  letter-spacing: 0.04em;
}
</style>

<template>
  <div class="archive-page">
    <div aria-hidden="true" class="bg" :class="{ 'is-lit': lit }">
      <span class="warm"></span>
      <span class="lamp"></span>
      <span class="noise"></span>
    </div>

    <main class="wrap">
      <div v-if="loading" class="archive-status" v-cloak>正在调取档案…</div>
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

        <ExtraSection
          :items="content.extras"
          :intro="content.extraIntro"
          :names="names"
          :states="extraStates"
          :texts="extraTexts"
          :all="extrasAll"
          :ranking="ranking"
          @unlock="onUnlockExtra"
        />
      </div>

      <div class="foot"></div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import ArchiveStage from './components/ArchiveStage.vue'
import ExtraSection from './components/ExtraSection.vue'
import { getContent, getState, unlockExtra, unlockStage } from './api.js'
import { initAmbientLight } from './fx.js'

const content = ref(null)
const names = ref({})
const unlockedStages = ref({})
const revealingStages = reactive({})
const stageFeedback = reactive({})
const extraStates = reactive({})
const extraTexts = ref({})
const extrasAll = ref(false)
const ranking = ref(null)

// 只要揭开过任意一栏，环境光就从冷灰缓缓转暖（纯视觉，不加任何文字）
const lit = computed(() => Object.keys(unlockedStages.value).length > 0)

const loading = ref(true)
const loadError = ref('')
const stateError = ref('')

onMounted(async () => {
  initAmbientLight()

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
    for (const id of state.extras || []) {
      extraStates[id] = { answered: true, feedback: '', busy: false }
    }
    // 三题全对时后端才会把内容发下来
    if (state.extraTexts && Object.keys(state.extraTexts).length) {
      extraTexts.value = state.extraTexts
      extrasAll.value = true
      ranking.value = state.ranking || null
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

async function onUnlockExtra(id, value) {
  const answer = (value || '').trim()
  if (!answer) return
  extraStates[id] = {
    ...(extraStates[id] || {}),
    feedback: '核对中…',
    busy: true,
  }
  try {
    const res = await unlockExtra(id, answer)
    extraStates[id] = { answered: true, feedback: '', busy: false }
    for (const eid of res.answered || []) {
      if (eid !== id) extraStates[eid] = { ...(extraStates[eid] || {}), answered: true, busy: false }
    }
    if (res.all && res.texts) {
      extraTexts.value = res.texts
      extrasAll.value = true
      ranking.value = res.ranking || null
    }
  } catch (e) {
    extraStates[id] = {
      ...(extraStates[id] || {}),
      feedback: e.message,
      busy: false,
    }
  }
}
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

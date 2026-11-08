<template>
  <div class="archive-page">
    <!-- 顶部提醒：有人留言 / 有人回复了你的留言，点一下直接跳到那条 -->
    <NotifyBar ref="notifyRef" :names="names" />

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

        <template v-for="(stage, index) in content.stages" :key="stage.id">
          <!-- 纯文字阶段（只有一段介绍，没有名单）走单独组件 -->
          <StageInterlude v-if="stage.lines" :stage="stage" />
          <ArchiveStage
            v-else
            :stage="stage"
            :names="names"
            :just-revealed="justRevealed"
            :order="index"
            :feedback="stageFeedback[stage.id]"
            :extras-unlocked="extraUnlocked"
            @unlock="onUnlockPerson"
            @extra-unlocked="onExtraUnlocked"
            @author-changed="onAuthorChanged"
          />
        </template>
      </div>

      <PhotoSection
        v-if="photoAlbums.length"
        :albums="photoAlbums"
        :unlocked="photoUnlocked"
      />

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
import StageInterlude from './components/StageInterlude.vue'
import PhotoSection from './components/PhotoSection.vue'
import NotifyBar from './components/NotifyBar.vue'
import { getContent, getState, unlockPerson } from './api.js'
import { initAmbientLight, initTouchFeedback } from './fx.js'

const content = ref(null)
const names = ref({})
const photoUnlocked = ref({})
// 已答过题的附加内容（按栏 id）；刷新后不用再答一遍
const extraUnlocked = ref([])
const justRevealed = ref(null)
const stageFeedback = reactive({})
// 顶部提醒条：作者模式切换后要让它按新口径立刻重算
const notifyRef = ref(null)

// 相册横跨两栏，挂在页面底部整行显示
const photoAlbums = computed(() => content.value?.photos?.albums || [])

// 只要揭示过任意一个人，环境光就从冷灰缓缓转暖（纯视觉，不加任何文字）
const lit = computed(() => Object.keys(names.value).length > 0)

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
    // names 里只有已经揭示过的人，没揭示的一律没有键
    names.value = state.names || {}
    photoUnlocked.value = state.photos || {}
    extraUnlocked.value = state.extras || []
  } else {
    stateError.value = '进度读取失败，本次解锁可能无法保存。'
  }

  loading.value = false
})

// 附加内容答完三题：把这一栏记下来，条目立刻展开，刷新也还在
function onExtraUnlocked(stageId) {
  if (!extraUnlocked.value.includes(stageId)) {
    extraUnlocked.value = [...extraUnlocked.value, stageId]
  }
}

// 进 / 出作者模式后重新问一次进度：作者模式下服务端会把所有人名一起给回来，
// 退出后又要变回「只显示已经揭示过的人」，所以必须整份重取，不能只加不减。
async function onAuthorChanged() {
  try {
    const state = await getState()
    names.value = state.names || {}
    photoUnlocked.value = state.photos || {}
    extraUnlocked.value = state.extras || {}
    stateError.value = ''
  } catch (e) {
    // 静默：cookie 已经生效，刷新页面就能拿到正确状态
  }
  notifyRef.value?.refresh?.()
}

async function onUnlockPerson(stageId, value) {  const name = (value || '').trim()
  if (!name) return
  stageFeedback[stageId] = { text: '核对中…', ok: false, busy: true }
  try {
    const res = await unlockPerson(stageId, name)
    // 后端只返回输对的那一个人，其余人名依然不显示
    names.value = { ...names.value, ...(res.names || {}) }
    justRevealed.value = { stage: stageId, person: res.person }
    stageFeedback[stageId] = { text: `已揭示「${res.name}」`, ok: true, busy: false }
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

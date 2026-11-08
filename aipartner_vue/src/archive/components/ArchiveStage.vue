<template>
  <section class="col" :class="{ 'is-lit': lit }" :data-stage="stage.id">
    <div class="col-head">
      <span aria-hidden="true" class="cdot"></span>
      <h2 class="col-title">{{ stage.title }}</h2>
    </div>

    <form autocomplete="off" class="phase-unlock-form" @submit.prevent="submit">
      <input
        v-model="input"
        :aria-label="'输入' + stage.title + '任意人物的姓名或拼音'"
        autocomplete="off"
        class="phase-unlock-input"
        :disabled="busy"
        placeholder="输入本阶段任意姓名或拼音"
        type="text"
      />
      <button class="phase-unlock-btn" type="submit" :disabled="busy">
        {{ busy ? '核对中…' : '揭示' }}
      </button>
    </form>
    <p class="phase-unlock-feedback" :class="{ ok: feedbackOk }">{{ feedbackText }}</p>

    <div v-for="group in stage.groups" :key="group.id" class="group">
      <button
        :aria-expanded="!!openGroups[group.id]"
        class="cnt"
        type="button"
        @click="toggleGroup(group.id)"
      >
        <span class="cnt-t"><span aria-hidden="true" class="tick"></span>{{ group.title }}</span>
        <span class="cnt-n">{{ shownCount[group.id] }}</span>
      </button>

      <div v-show="openGroups[group.id]" class="roster">
        <PersonRow
          v-for="person in group.people"
          :key="person.id"
          :person="person"
          :display-name="displayName(person)"
          :open="!!openPeople[person.id]"
          :desc-html="descFor(person)"
          :revealing="person.id === flashId"
          :reveal-index="person.id === flashId ? 0 : revealIndexMap[person.id] || 0"
          @toggle="togglePerson"
          @author-changed="emit('author-changed', $event)"
        />
      </div>
    </div>

    <!-- 附加内容挂在本阶段里：答对三道题才展开那几个人 -->
    <ExtraSection
      v-if="hasExtras"
      :section="stage.extras"
      :stage-id="stage.id"
      :unlocked="extrasUnlocked.includes(stage.id)"
      :names="names"
      @unlocked="emit('extra-unlocked', stage.id)"
    />
  </section>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import PersonRow from './PersonRow.vue'
import ExtraSection from './ExtraSection.vue'
import { renderTokens } from '../render.js'

const props = defineProps({
  stage: { type: Object, required: true },
  names: { type: Object, default: () => ({}) },
  feedback: { type: Object, default: null },
  // 父级刚揭示的人：{ stage, person }，只给那一行播一次翻牌动画
  justRevealed: { type: Object, default: null },
  order: { type: Number, default: 0 },
  // 已答过题的附加内容（按栏 id）
  extrasUnlocked: { type: Array, default: () => [] },
})

const emit = defineEmits(['unlock', 'extra-unlocked', 'author-changed'])

const REDUCED =
  typeof window !== 'undefined' &&
  window.matchMedia &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

const input = ref('')
const openGroups = reactive({})
const openPeople = reactive({})

// 分组人数：入场时从 0 滚到实际值，像清点一遍档案
const shownCount = reactive({})

function targetCount(group) {
  return group.people.filter((person) => !person.deleted).length
}

// 初值直接给真实人数：rAF 第一帧会立刻把它覆盖成 0 再数上去（那一帧肉眼看不见）。
// 万一 rAF 不跑，页面显示的就是正确人数，绝不会停在 0。
for (const group of props.stage.groups) {
  shownCount[group.id] = targetCount(group)
}

// 兜底一旦落地，就锁住计数，避免残余的 rAF 再把数字写回 0
let countSettled = false

function countUp(id, target, delay) {
  const duration = 460
  let startAt = 0
  let frames = 0
  function frame(now) {
    if (countSettled) return
    frames += 1
    // 先空转两帧再开始计数：万一 rAF 只被调度了一两次就断掉，
    // 数字会停在初始的真实人数上，而不是被改成 0。
    if (frames < 3) {
      requestAnimationFrame(frame)
      return
    }
    if (!startAt) startAt = now + delay
    const progress = Math.min(1, Math.max(0, (now - startAt) / duration))
    shownCount[id] = Math.round(target * (1 - Math.pow(1 - progress, 3)))
    if (progress < 1) requestAnimationFrame(frame)
    else shownCount[id] = target
  }
  requestAnimationFrame(frame)
}

onMounted(() => {
  if (REDUCED) return
  props.stage.groups.forEach((group, groupIndex) => {
    countUp(group.id, targetCount(group), 220 + props.order * 130 + groupIndex * 90)
  })
  // 兜底：rAF 万一没跑起来（后台标签页、省电模式等），1.6 秒后直接落到真实人数，
  // 绝不让计数停在一个错的数字上。
  setTimeout(() => {
    countSettled = true
    for (const group of props.stage.groups) {
      if (shownCount[group.id] !== targetCount(group)) {
        shownCount[group.id] = targetCount(group)
      }
    }
  }, 1600)
})

// 本阶段是否已揭示过至少一个人：只影响卡片点亮，不参与解锁判断
const lit = computed(() =>
  props.stage.groups.some((group) => group.people.some((person) => !!props.names[person.id]))
)

// 父级刚揭示的那一行挂一次动画，其他人不动
const flashId = computed(() => {
  const just = props.justRevealed
  return just && just.stage === props.stage.id ? just.person : ''
})

// 渐显错位索引：按组内序号，展开哪一组就从哪一组的第一行开始依次出现
const revealIndexMap = {}
for (const group of props.stage.groups) {
  group.people.forEach((person, index) => {
    revealIndexMap[person.id] = index
  })
}

const allPeople = computed(() =>
  props.stage.groups.flatMap((group) =>
    group.people.map((person) => ({ ...person, groupId: group.id }))
  )
)

const busy = computed(() => !!(props.feedback && props.feedback.busy))
const hasExtras = computed(
  () => !!(props.stage.extras && props.stage.extras.items && props.stage.extras.items.length)
)
const feedbackOk = computed(() => !!(props.feedback && props.feedback.ok))
const feedbackText = computed(() => {
  if (props.feedback && props.feedback.text) return props.feedback.text
  return '逐个人输入你记得的姓名或拼音，输对谁就显示谁'
})

function displayName(person) {
  return props.names[person.id] || '***'
}

function descFor(person) {
  return openPeople[person.id] ? renderTokens(person.desc, props.names) : ''
}

// 揭示成功后清空输入框，方便接着输下一个
watch(
  () => props.feedback,
  (feedback) => {
    if (feedback && feedback.ok) input.value = ''
  },
)

function submit() {
  if (busy.value) return
  const value = input.value.trim()
  if (!value) return
  emit('unlock', props.stage.id, value)
}

function toggleGroup(id) {
  openGroups[id] = !openGroups[id]
}

// 手机上同时只留一个人展开：描述是整幅宽的，同时开两条会把旁边那个人名
// 顶到很远的地方，看着就像「点开一个，另一个不见了」。桌面端保持可同时展开。
const COMPACT =
  typeof window !== 'undefined' && window.matchMedia
    ? window.matchMedia('(max-width: 820px)')
    : null

function openOnly(id) {
  if (COMPACT && COMPACT.matches) {
    for (const key of Object.keys(openPeople)) openPeople[key] = false
  }
  openPeople[id] = true
}

function togglePerson(person) {
  // 划去的人：如果同阶段存在同名且未划去的条目，跳过去
  if (person.deleted && props.names[person.id]) {
    const target = allPeople.value.find(
      (item) =>
        !item.deleted &&
        item.id !== person.id &&
        props.names[item.id] === props.names[person.id]
    )
    if (target) {
      openGroups[target.groupId] = true
      openOnly(target.id)
      nextTick(() => {
        const el = document.getElementById('person-' + target.id)
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      })
      return
    }
  }
  if (openPeople[person.id]) {
    openPeople[person.id] = false
    // 收起长文时把人名拉回视口：否则内容一收缩，刚才那行已经跑到屏幕外
    nextTick(() => {
      const el = document.getElementById('person-' + person.id)
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    })
    return
  }
  // 手机上换人时，上一条描述会塌掉，页面高度骤减，手指底下的内容会窜位；
  // 把新点开的这个名字顶到视口上方，位置就稳了。
  const hadOther =
    !!(COMPACT && COMPACT.matches) && Object.keys(openPeople).some((key) => openPeople[key])
  openOnly(person.id)
  if (hadOther) {
    nextTick(() => {
      const el = document.getElementById('person-' + person.id)
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  }
}

// 顶部提醒条点名「谁下面有新留言」：展开他所在的分组、点开这个人，滚到留言区并亮一下
function onJump(ev) {
  const person = ev && ev.detail ? ev.detail.person : ''
  if (!person) return
  const hit = allPeople.value.find((item) => item.id === person)
  if (!hit) return
  openGroups[hit.groupId] = true
  openOnly(hit.id)
  nextTick(() => {
    const cmt = document.querySelector(`.cmt[data-person="${person}"]`)
    const target = cmt || document.getElementById('person-' + person)
    if (!target) return
    let landed = false
    const land = () => {
      if (landed) return
      landed = true
      target.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth', block: 'center' })
      target.classList.add('is-flash')
      setTimeout(() => target.classList.remove('is-flash'), 1800)
    }
    // 定位前先把这块留言拉到最新再滚：提醒和列表虽已同节拍，点提醒的这一刻
    // 列表仍可能差半拍，刷完再滚才不会「跳过来却没看到那条」。
    if (cmt) {
      cmt.dispatchEvent(new CustomEvent('cmt-refresh', { detail: { then: land } }))
      // 万一没人接这个事件，也别把跳转卡住
      setTimeout(land, 700)
    } else {
      land()
    }
  })
}

onMounted(() => window.addEventListener('archive:jump', onJump))
onBeforeUnmount(() => window.removeEventListener('archive:jump', onJump))
</script>

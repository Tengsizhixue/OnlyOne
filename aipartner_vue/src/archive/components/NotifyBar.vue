<template>
  <div v-if="visible" class="notify-bar" role="status" aria-live="polite">
    <span aria-hidden="true" class="notify-dot"></span>
    <button class="notify-msg" type="button" @click="jump">{{ message }}</button>
    <button class="notify-go" type="button" @click="jump">{{ author ? '去看看' : '查看' }}</button>
    <button class="notify-x" type="button" aria-label="隐藏这条提醒" @click="dismiss">×</button>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { getNotifications } from '../api.js'
import { startAlignedPoll } from '../poll.js'

const props = defineProps({
  // 已解锁的人名；作者模式下这里是全部名字
  names: { type: Object, default: () => ({}) },
})

const SEEN_KEY = 'archive.notify.seen.v1'

const items = ref([])
const author = ref(false)
// 服务端当前最新的留言 id，用来推进「看到哪儿了」的游标
const lastId = ref(0)

function readSeen() {
  // -1 表示这台设备还没记录过：服务端只会把游标推到最新，不会弹出历史留言
  try {
    const raw = window.localStorage.getItem(SEEN_KEY)
    if (raw === null) return -1
    const value = Number(raw)
    return Number.isFinite(value) && value >= 0 ? value : -1
  } catch (e) {
    return -1
  }
}

function writeSeen(value) {
  try {
    window.localStorage.setItem(SEEN_KEY, String(value))
  } catch (e) {
    // 隐私模式下写不进去，最多每次进页面重新提醒一次
  }
}

function displayName(id) {
  return props.names[id] || '***'
}

const visible = computed(() => items.value.length > 0)

const message = computed(() => {
  const top = items.value[0]
  if (!top) return ''
  // 一次只讲一处，剩下的留在条上接着点；带个「还有几处」不让人以为只有一条
  const rest = items.value.length - 1
  const tail = rest > 0 ? `，还有 ${rest} 处` : ''
  // 访客只可能收到「回复」，措辞固定
  if (!author.value) {
    return rest > 0 ? `有人回复了你的留言（还有 ${rest} 处）` : '有人回复了你的留言，点击可快速查看'
  }
  const name = `「${displayName(top.person)}」`
  const head =
    top.count > 1
      ? `有人在${name}的下面留言了（${top.count} 条）`
      : `有人在${name}的下面留言了`
  return head + tail
})

async function refresh() {
  if (document.hidden) return
  try {
    const data = await getNotifications(readSeen())
    author.value = !!data.author
    lastId.value = Number(data.last) || 0
    // 服务端按「最新在前」给（MAX(id) DESC）。这里改成从旧到新依次消费：
    // 游标只能往前推，先跳最新的就会把更早的几处一起跨过去 —— 那正是漏消息的原因。
    const list = (data.items || [])
      .slice()
      .sort((a, b) => (Number(a.id) || 0) - (Number(b.id) || 0))
    if (list.length) {
      items.value = list
    } else if (!items.value.length && lastId.value) {
      // 真没有新东西了才把游标推到最新；本地还留着没点完的几处就不要动它
      writeSeen(lastId.value)
    }
  } catch (e) {
    // 提醒失败不打扰人，等下一轮
  }
}

function dismiss() {
  if (lastId.value) writeSeen(lastId.value)
  items.value = []
}

function jump() {
  const top = items.value[0]
  if (!top) return
  // 只把这一处记成看过，其余留在条上：点一次跳一处，三处都能看到，不会漏
  if (top.id) writeSeen(top.id)
  items.value = items.value.slice(1)
  if (!items.value.length && lastId.value) writeSeen(lastId.value)
  window.dispatchEvent(new CustomEvent('archive:jump', { detail: { person: top.person } }))
}

// 提醒条出现时把正文整体下移一条的高度，别让它压住第一行标题
watch(visible, (on) => {
  const root = document.documentElement
  if (on) root.classList.add('has-notify')
  else root.classList.remove('has-notify')
})

function onVisibility() {
  if (!document.hidden) refresh()
}

let stopPoll = null

onMounted(() => {
  refresh()
  // 和留言列表同一个节拍，避免提醒先到、列表后到
  stopPoll = startAlignedPoll(refresh)
  document.addEventListener('visibilitychange', onVisibility)
})

onBeforeUnmount(() => {
  if (stopPoll) stopPoll()
  document.removeEventListener('visibilitychange', onVisibility)
  document.documentElement.classList.remove('has-notify')
})

// 进入 / 退出作者模式后立刻按新的口径重算一次
defineExpose({ refresh })
</script>

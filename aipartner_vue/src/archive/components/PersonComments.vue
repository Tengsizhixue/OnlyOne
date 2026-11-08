<template>
  <div class="cmt" :data-person="personId" @cmt-refresh="onRefreshRequest">
    <div class="cmt-head">
      <span aria-hidden="true" class="cmt-line"></span>
      <span class="cmt-t">其他人的留言</span>
      <span v-if="count > 0" class="cmt-n">{{ count }}</span>
    </div>

    <p v-if="loading" class="cmt-tip">读取中…</p>
    <p v-else-if="loadError" class="cmt-tip bad">{{ loadError }}</p>
    <p v-else-if="!items.length" class="cmt-tip">这里还没有其他人的看法。</p>

    <ul v-if="items.length" class="cmt-list">
      <li
        v-for="item in items"
        :key="item.id"
        class="cmt-item"
        :class="{
          'is-new': freshIds.has(item.id),
          'is-author': item.role === 'author',
          'is-mine': item.mine && item.role !== 'author',
        }"
      >
        <div class="cmt-meta">
          <span class="cmt-who">{{ item.nick || '匿名' }}</span>
          <span v-if="item.role === 'author'" class="cmt-badge">作者</span>
          <span v-else-if="item.mine" class="cmt-mine-mark">我</span>
          <span v-if="item.pinned" class="cmt-pin-mark">置顶</span>
          <span class="cmt-time">{{ when(item.created) }}</span>
          <span class="cmt-ops">
            <button class="cmt-reply-btn" type="button" @click="openReply(item)">
              回复
            </button>
            <button v-if="isAuthor" class="cmt-reply-btn" type="button" @click="togglePin(item)">
              {{ item.pinned ? '取消置顶' : '置顶' }}
            </button>
            <button v-if="item.mine || isAuthor" class="cmt-del" type="button" @click="remove(item)">
              删除
            </button>
          </span>
        </div>
        <p class="cmt-body">{{ item.body }}</p>

        <!-- 内联回复框：回复目标是这条顶层留言 -->
        <div v-if="replyTarget && replyTarget.id === item.id" class="cmt-reply-form">
          <p class="cmt-reply-hint">回复 @{{ replyTarget.nick }}「{{ replyTarget.snippet }}」</p>
          <textarea
            ref="replyInput"
            v-model="replyDraft"
            class="cmt-input"
            maxlength="300"
            placeholder="写下你的回复…"
            rows="2"
          ></textarea>
          <div class="cmt-acts">
            <button class="cmt-btn cmt-btn-sm" type="button" :disabled="busy" @click="submitReply(item)">
              {{ busy ? '发送中…' : '发送' }}
            </button>
            <button class="cmt-cancel" type="button" @click="closeReply">取消</button>
          </div>
        </div>

        <!-- 回复区：这一楼下的讨论 -->
        <ul v-if="item.replies && item.replies.length" class="cmt-replies">
          <li
            v-for="r in item.replies"
            :key="r.id"
            class="cmt-reply"
            :class="{
              'is-new': freshIds.has(r.id),
              'is-author': r.role === 'author',
              'is-mine': r.mine && r.role !== 'author',
            }"
          >
            <div class="cmt-meta">
              <span class="cmt-who">{{ r.nick || '匿名' }}</span>
              <span v-if="r.role === 'author'" class="cmt-badge">作者</span>
              <span v-else-if="r.mine" class="cmt-mine-mark">我</span>
              <span class="cmt-time">{{ when(r.created) }}</span>
              <span class="cmt-ops">
                <button class="cmt-reply-btn" type="button" @click="openReply(r)">
                  回复
                </button>
                <button v-if="r.mine || isAuthor" class="cmt-del" type="button" @click="removeReply(item, r)">
                  删除
                </button>
              </span>
            </div>
            <p v-if="r.replyTo" class="cmt-ref">
              ↳ 回复 @{{ r.replyTo }}「{{ r.replyToSnippet }}」
            </p>
            <p class="cmt-body">{{ r.body }}</p>

            <!-- 内联回复框：回复目标是这条回复 -->
            <div v-if="replyTarget && replyTarget.id === r.id" class="cmt-reply-form">
              <p class="cmt-reply-hint">回复 @{{ replyTarget.nick }}「{{ replyTarget.snippet }}」</p>
              <textarea
                ref="replyInput"
                v-model="replyDraft"
                class="cmt-input"
                maxlength="300"
                placeholder="写下你的回复…"
                rows="2"
              ></textarea>
              <div class="cmt-acts">
                <button class="cmt-btn cmt-btn-sm" type="button" :disabled="busy" @click="submitReply(item)">
                  {{ busy ? '发送中…' : '发送' }}
                </button>
                <button class="cmt-cancel" type="button" @click="closeReply">取消</button>
              </div>
            </div>
          </li>
        </ul>
      </li>
    </ul>

    <div class="cmt-form">
      <p class="cmt-form-head">
        发表新留言
        <span v-if="isAuthor" class="cmt-mode">
          作者模式 ·
          <button class="cmt-mode-out" type="button" @click="exitAuthor">退出</button>
        </span>
      </p>
      <input
        v-model="nick"
        class="cmt-nick"
        maxlength="12"
        placeholder="昵称（填不填无所谓，默认匿名）"
        type="text"
      />
      <textarea
        v-model="draft"
        class="cmt-input"
        maxlength="300"
        placeholder="你也可以随便写，其他人可见。有问题也可以说，只要不是太离谱的我看到都会回"
        rows="2"
      ></textarea>
      <div class="cmt-acts">
        <button class="cmt-btn" type="button" :disabled="busy" @click="submit">
          {{ busy ? '发送中…' : '发表留言' }}
        </button>
        <span class="cmt-count">{{ draft.length }}/300</span>
      </div>
      <p v-if="tip" class="cmt-tip" :class="{ bad: tipBad }">{{ tip }}</p>
    </div>
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import {
  addComment,
  authorLogin,
  authorLogout,
  authorStatus,
  deleteComment,
  listComments,
  pinComment,
} from '../api.js'
import { startAlignedPoll } from '../poll.js'
import { askConfirm, settleConfirm } from '../confirm.js'

const props = defineProps({
  personId: { type: String, required: true },
})

const emit = defineEmits(['author-changed'])

const NICK_KEY = 'archive.nick.v1'
// 留言框里以这句开头是口令，不是留言；口令本身由服务端校验
const AUTHOR_CMD = '#作者'
// 暗号本身就是口令：整条只有 6 位数字时先试着当暗号（失败仍然当普通留言发出去）
const CODE_RE = /^\d{6}$/

const items = ref([])
const count = ref(0)
const loading = ref(true)
const loadError = ref('')
const busy = ref(false)
const tip = ref('')
const tipBad = ref(false)
const draft = ref('')
const nick = ref(readNick())
// 作者模式：是否已用口令换到签名 cookie（状态由服务端 /author/status 确认）
const isAuthor = ref(false)

// 删除确认走全页共用那个弹窗：不用 window.confirm（微信内置浏览器会把它
// 降级成「是否关闭网页」，或者干脆吞掉不返回）。实现见 ../confirm.js。

// 回复相关
const replyTarget = ref(null)     // 被回复留言的 {id, nick, snippet}
const replyDraft = ref('')
const replyInput = ref(null)

// 轮询停止函数（节拍与提醒条共用，见 poll.js）
let stopPoll = null
// 首次加载的 promise：从提醒条跳过来时要等它，别在空列表上定位
let firstLoad = null

// 轮询拉到或刚发出的新留言 id，播一次入场动画后清除
const freshIds = ref(new Set())

function readNick() {
  try {
    return window.localStorage.getItem(NICK_KEY) || ''
  } catch (e) {
    return ''
  }
}

function writeNick(value) {
  try {
    window.localStorage.setItem(NICK_KEY, value)
  } catch (e) {
    // 隐私模式下写不进去也不影响发留言
  }
}

function when(seconds) {
  const now = Date.now() / 1000
  const diff = Math.max(0, now - seconds)
  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)} 分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)} 小时前`
  if (diff < 86400 * 7) return `${Math.floor(diff / 86400)} 天前`
  const d = new Date(seconds * 1000)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

/** 把留言正文压成单行短引用，用于引用行与回复框标题 */
function snippetOf(text) {
  const flat = (text || '').replace(/\s+/g, ' ').trim()
  return flat.length > 15 ? `${flat.slice(0, 15)}…` : flat
}

/** 收集列表里所有留言与回复的 id */
function idsOf(list) {
  const s = new Set()
  for (const i of list) {
    s.add(i.id)
    for (const r of i.replies || []) s.add(r.id)
  }
  return s
}

/** 把不在 oldIds 里的条目标记为新，播一次浮入动画 */
function markFresh(list, oldIds) {
  const fresh = new Set()
  for (const i of list) {
    if (!oldIds.has(i.id)) fresh.add(i.id)
    for (const r of i.replies || []) if (!oldIds.has(r.id)) fresh.add(r.id)
  }
  if (!fresh.size) return
  freshIds.value = fresh
  setTimeout(() => {
    freshIds.value = new Set()
  }, 900)
}

async function load() {
  loading.value = true
  loadError.value = ''
  try {
    const data = await listComments(props.personId)
    items.value = data.items || []
    count.value = data.count || 0
  } catch (e) {
    loadError.value = e.message || '留言读取失败'
  } finally {
    loading.value = false
  }
}

/** 拉一次并落到界面上 */
async function fetchAndApply() {
  const data = await listComments(props.personId)
  const next = data.items || []
  count.value = data.count || 0
  // 只在数据真正变化时更新，避免不必要的 DOM 重排
  if (JSON.stringify(next) !== JSON.stringify(items.value)) {
    const oldIds = idsOf(items.value)
    items.value = next
    markFresh(next, oldIds)
  }
}

/** 轮询：静默刷新，不影响用户正在输入的内容 */
async function pollRefresh() {
  // 用户正在写留言或回复时跳过，标签页隐藏时也跳过
  if (draft.value.trim() || replyDraft.value.trim() || document.hidden) return
  try {
    await fetchAndApply()
  } catch (e) {
    // 轮询失败不提示，等下一轮
  }
}

/**
 * 从提醒条跳过来时：先把这块的留言拉到最新，再让调用方去滚动定位，
 * 否则会出现「提醒说有新留言，点进去却没看到」。
 * 首次 load 还在路上时直接采信它的结果，不重复发请求。
 */
async function onRefreshRequest(ev) {
  try {
    if (loading.value) {
      // 首次 load 还在路上：等它落地，别再发一次，也别在空列表上定位
      if (firstLoad) await firstLoad
    } else {
      await fetchAndApply()
    }
  } catch (e) {
    // 拉不到就按原样定位，提醒本身还有效
  }
  const then = ev && ev.detail ? ev.detail.then : null
  if (typeof then === 'function') then()
}

function startPolling() {
  stopPolling()
  stopPoll = startAlignedPoll(pollRefresh)
}

function stopPolling() {
  if (stopPoll) {
    stopPoll()
    stopPoll = null
  }
}

// -------- 作者模式 --------
async function checkAuthor() {
  try {
    const data = await authorStatus()
    isAuthor.value = !!data.author
  } catch (e) {
    // 取不到就按访客处理，不影响留言本身
    isAuthor.value = false
  }
}

/**
 * 留言框里直接输暗号就进作者模式（暗号配在服务器 .env，不进仓库）；
 * 也保留「#作者 暗号」的写法，方便换成更长的口令。
 * 返回 true 表示已经被当成命令处理掉，不要再发出去。
 */
async function handleCommand(text) {
  const isCmd = text.startsWith(AUTHOR_CMD)
  if (!isCmd && !CODE_RE.test(text)) return false
  const key = isCmd ? text.slice(AUTHOR_CMD.length).trim() : text
  if (!key) {
    tip.value = '口令呢？'
    tipBad.value = true
    return true
  }
  try {
    await authorLogin(key)
    isAuthor.value = true
    draft.value = ''
    replyDraft.value = ''
    closeReply()
    tip.value = '已进入作者模式：所有人名都会显示，之后发的留言带「作者」标记，30 天内有效。'
    tipBad.value = false
    emit('author-changed', true)
  } catch (e) {
    // 6 位数字只是「可能是暗号」，验不过就当普通留言继续发，别把内容吞了
    if (!isCmd) return false
    tip.value = e.message || '这条不能发。'
    tipBad.value = true
  }
  return true
}

async function exitAuthor() {
  try {
    await authorLogout()
  } catch (e) {
    // 请求失败也先在本地按访客显示，下次刷新会重新问服务端
  }
  isAuthor.value = false
  tip.value = '已退出作者模式。'
  tipBad.value = false
  emit('author-changed', false)
}

async function togglePin(item) {
  if (busy.value) return
  busy.value = true
  tip.value = ''
  tipBad.value = false
  try {
    await pinComment(item.id, !item.pinned)
    // 本地按「置顶在前、其余保持原顺序」重排，避免整列表闪烁
    item.pinned = !item.pinned
    const pinned = items.value.filter((i) => i.pinned)
    const rest = items.value.filter((i) => !i.pinned)
    items.value = [...pinned, ...rest]
  } catch (e) {
    tip.value = e.message || '置顶失败，请稍后再试。'
    tipBad.value = true
  } finally {
    busy.value = false
  }
}

// -------- 发表顶层留言 --------
async function submit() {
  if (busy.value) return
  const text = draft.value.trim()
  tip.value = ''
  tipBad.value = false
  if (!text) {
    tip.value = '写点什么再发表吧。'
    tipBad.value = true
    return
  }
  // 口令命令：走登录，不写留言
  if (await handleCommand(text)) return
  busy.value = true
  try {
    const res = await addComment(props.personId, nick.value.trim(), text)
    // 按发表时间正序，新的接在最后
    const oldIds = idsOf(items.value)
    items.value = [...items.value, res.item]
    count.value += 1
    markFresh(items.value, oldIds)
    draft.value = ''
    writeNick(nick.value.trim())
    tip.value = '已发表，其他人刷新页面就能看到。'
  } catch (e) {
    tip.value = e.message || '发表失败，请稍后再试。'
    tipBad.value = true
  } finally {
    busy.value = false
  }
}

// -------- 回复 --------
function openReply(target) {
  replyTarget.value = {
    id: target.id,
    nick: target.nick || '匿名',
    snippet: snippetOf(target.body),
  }
  replyDraft.value = ''
  nextTick(() => {
    if (replyInput.value) {
      const el = Array.isArray(replyInput.value) ? replyInput.value[0] : replyInput.value
      el && el.focus()
    }
  })
}

function closeReply() {
  replyTarget.value = null
  replyDraft.value = ''
}

async function submitReply(parentItem) {
  if (busy.value) return
  const text = replyDraft.value.trim()
  if (!text) return
  // 回复框里输的也可能是口令，别把它当回复发出去
  if (await handleCommand(text)) return
  busy.value = true
  tip.value = ''
  tipBad.value = false
  try {
    const res = await addComment(props.personId, nick.value.trim(), text, replyTarget.value.id)
    // 插入到对应的顶层留言的 replies 里
    const newItem = res.item
    const oldIds = idsOf(items.value)
    const target = items.value.find((i) => i.id === (newItem.rootId || parentItem.id))
    if (target) {
      if (!target.replies) target.replies = []
      target.replies.push(newItem)
    }
    count.value += 1
    markFresh(items.value, oldIds)
    writeNick(nick.value.trim())
    closeReply()
  } catch (e) {
    tip.value = e.message || '回复失败，请稍后再试。'
    tipBad.value = true
  } finally {
    busy.value = false
  }
}

// -------- 删除 --------
async function remove(item) {
  const replyCount = (item.replies || []).length
  let msg
  if (!item.mine && isAuthor) {
    msg = replyCount
      ? `以作者身份删掉这条留言？其下 ${replyCount} 条回复也会一起隐藏。`
      : '以作者身份删掉这条留言？对方将看不到它。'
  } else if (replyCount) {
    msg = `删除这条留言？其下 ${replyCount} 条回复也会被删除，不能恢复。`
  } else {
    msg = '删除这条留言？删除后不能恢复。'
  }
  if (!(await askConfirm(msg))) return
  busy.value = true
  tip.value = ''
  tipBad.value = false
  try {
    const res = await deleteComment(item.id)
    const deleted = new Set(res.deleted || [item.id])
    items.value = items.value.filter((row) => !deleted.has(row.id))
    count.value = Math.max(0, count.value - deleted.size)
  } catch (e) {
    tip.value = e.message || '删除失败，请稍后再试。'
    tipBad.value = true
  } finally {
    busy.value = false
  }
}

async function removeReply(parentItem, reply) {
  const msg = !reply.mine && isAuthor ? '以作者身份隐藏这条回复？' : '删除这条回复？'
  if (!(await askConfirm(msg))) return
  busy.value = true
  tip.value = ''
  tipBad.value = false
  try {
    const res = await deleteComment(reply.id)
    const deleted = new Set(res.deleted || [reply.id])
    parentItem.replies = (parentItem.replies || []).filter((r) => !deleted.has(r.id))
    count.value = Math.max(0, count.value - deleted.size)
  } catch (e) {
    tip.value = e.message || '删除失败，请稍后再试。'
    tipBad.value = true
  } finally {
    busy.value = false
  }
}

function onVisibility() {
  if (!document.hidden) pollRefresh()
}

onMounted(() => {
  firstLoad = load()
  checkAuthor()
  startPolling()
  // 切回标签页立刻补一次，不用等下一个刻度
  document.addEventListener('visibilitychange', onVisibility)
})

onBeforeUnmount(() => {
  stopPolling()
  document.removeEventListener('visibilitychange', onVisibility)
  // 组件被卸载时确认框还挂着的话，让 await 立即结束
  settleConfirm(false)
})
</script>

<template>
  <div class="cmt" :data-person="personId">
    <div class="cmt-head">
      <span aria-hidden="true" class="cmt-line"></span>
      <span class="cmt-t">其他人的留言</span>
      <span v-if="count > 0" class="cmt-n">{{ count }}</span>
    </div>

    <p v-if="loading" class="cmt-tip">读取中…</p>
    <p v-else-if="loadError" class="cmt-tip bad">{{ loadError }}</p>
    <p v-else-if="!items.length" class="cmt-tip">这里还没有其他人的看法。</p>

    <ul v-if="items.length" class="cmt-list">
      <li v-for="item in items" :key="item.id" class="cmt-item">
        <div class="cmt-meta">
          <span class="cmt-who">{{ item.nick || '匿名' }}</span>
          <span class="cmt-time">{{ when(item.created) }}</span>
          <span class="cmt-ops">
            <button class="cmt-reply-btn" type="button" @click="openReply(item)">
              回复
            </button>
            <button v-if="item.mine" class="cmt-del" type="button" @click="remove(item)">
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
          <li v-for="r in item.replies" :key="r.id" class="cmt-reply">
            <div class="cmt-meta">
              <span class="cmt-who">{{ r.nick || '匿名' }}</span>
              <span class="cmt-time">{{ when(r.created) }}</span>
              <span class="cmt-ops">
                <button class="cmt-reply-btn" type="button" @click="openReply(r)">
                  回复
                </button>
                <button v-if="r.mine" class="cmt-del" type="button" @click="removeReply(item, r)">
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
      <p class="cmt-form-head">发表新留言</p>
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
import { addComment, deleteComment, listComments } from '../api.js'

const props = defineProps({
  personId: { type: String, required: true },
})

const NICK_KEY = 'archive.nick.v1'
const POLL_INTERVAL = 30000 // 30 秒轮询一次

const items = ref([])
const count = ref(0)
const loading = ref(true)
const loadError = ref('')
const busy = ref(false)
const tip = ref('')
const tipBad = ref(false)
const draft = ref('')
const nick = ref(readNick())

// 回复相关
const replyTarget = ref(null)     // 被回复留言的 {id, nick, snippet}
const replyDraft = ref('')
const replyInput = ref(null)

// 轮询定时器
let pollTimer = null

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

/** 轮询：静默刷新，不影响用户正在输入的内容 */
async function pollRefresh() {
  // 用户正在写留言或回复时跳过，标签页隐藏时也跳过
  if (draft.value.trim() || replyDraft.value.trim() || document.hidden) return
  try {
    const data = await listComments(props.personId)
    const newItems = data.items || []
    // 只在数据真正变化时更新，避免不必要的 DOM 重排
    if (JSON.stringify(newItems) !== JSON.stringify(items.value)) {
      items.value = newItems
      count.value = data.count || 0
    }
  } catch (e) {
    // 轮询失败不提示，等下一轮
  }
}

function startPolling() {
  stopPolling()
  pollTimer = setInterval(pollRefresh, POLL_INTERVAL)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
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
  busy.value = true
  try {
    const res = await addComment(props.personId, nick.value.trim(), text)
    items.value = [res.item, ...items.value]
    count.value += 1
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
  busy.value = true
  tip.value = ''
  tipBad.value = false
  try {
    const res = await addComment(props.personId, nick.value.trim(), text, replyTarget.value.id)
    // 插入到对应的顶层留言的 replies 里
    const newItem = res.item
    const target = items.value.find((i) => i.id === (newItem.rootId || parentItem.id))
    if (target) {
      if (!target.replies) target.replies = []
      target.replies.push(newItem)
    }
    count.value += 1
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
  const msg = replyCount
    ? `删除这条留言？其下 ${replyCount} 条回复也会被删除，不能恢复。`
    : '删除这条留言？删除后不能恢复。'
  if (!window.confirm(msg)) return
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
  if (!window.confirm('删除这条回复？')) return
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

onMounted(() => {
  load()
  startPolling()
})

onBeforeUnmount(() => {
  stopPolling()
})
</script>

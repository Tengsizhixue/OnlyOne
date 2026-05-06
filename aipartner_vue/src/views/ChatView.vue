<template>
  <el-container class="main-layout glass-panel">
    <div class="sidebar-overlay" v-show="isMobileMenuOpen" @click="isMobileMenuOpen = false"></div>

    <!-- 左侧边栏 -->
    <el-aside width="280px" class="sidebar" :class="{ 'mobile-open': isMobileMenuOpen }">
      <div class="mobile-close-btn" @click="isMobileMenuOpen = false">
        <el-icon><Close /></el-icon>
      </div>

      <div class="sidebar-header">
        <div class="logo-wrapper">
          <img src="https://api.dicebear.com/9.x/bottts-neutral/svg?seed=AI" alt="AI Logo" class="logo-img" />
          <h2 class="logo">不智能伙伴</h2>
        </div>
        <div class="uid-box" title="点击复制身份码" @click="copyUid">
          <span class="uid-label">身份码</span>
          <span class="uid-value">
            {{ uid }}
            <el-icon class="copy-icon"><DocumentCopy /></el-icon>
          </span>
        </div>
      </div>

      <button class="new-chat-btn" @click="createNewSession">
        <el-icon class="btn-icon"><Plus /></el-icon>
        <span>新建对话</span>
      </button>

      <div class="history-list">
        <div class="list-title">记忆宝匣</div>
        <el-scrollbar height="calc(100vh - 320px)" class="custom-scrollbar">
          <div
            v-for="session in sessions"
            :key="session.session_id"
            :class="['history-item', { active: currentSessionId === session.session_id }]"
            @click="loadSession(session.session_id)"
          >
            <div class="session-info">
              <span class="session-name">{{ session.name }}</span>
              <span class="session-time">{{ session.display_time }}</span>
            </div>
            <div class="delete-btn-wrapper">
              <el-icon class="delete-icon" @click.stop="deleteSession(session.session_id)"><Delete /></el-icon>
            </div>
          </div>
        </el-scrollbar>
      </div>

      <div class="sidebar-footer">
        <el-input v-model="recoverUid" placeholder="输入8位恢复码..." class="recover-input">
          <template #append>
            <el-button class="recover-btn" @click="recoverHistory">同步</el-button>
          </template>
        </el-input>
      </div>
    </el-aside>

    <!-- 右侧聊天区域 -->
    <el-container class="chat-container">
      <el-header class="chat-header">
        <button class="mobile-menu-btn" @click="isMobileMenuOpen = true">
          <el-icon><Menu /></el-icon>
        </button>

        <div class="role-settings" v-if="messages.length === 0">
          <el-select v-model="roleConfig.role_type" placeholder="选择伙伴" class="glass-select" style="width: 150px">
            <el-option v-for="role in availableRoles" :key="role.role_type" :label="role.name" :value="role.role_type" />
          </el-select>
          <transition name="fade">
            <div class="custom-inputs" v-if="roleConfig.role_type === '自定义'">
              <el-input v-model="roleConfig.name" placeholder="伙伴的称呼" class="glass-input" style="width: 140px" />
              <el-input v-model="roleConfig.nature" placeholder="设定TA的性格与世界观..." class="glass-input" style="width: 240px; max-width: 100%;" />
            </div>
          </transition>
        </div>
        <div class="locked-status" v-else>
          <div class="status-badge">
            <span class="dot connected"></span>
            当前角色: <span class="badge-text">{{ roleConfig.name }}</span>
          </div>
          <span class="lock-tip mobile-hide"><el-icon><Lock /></el-icon> 记忆已锁定，需新建以更改</span>
        </div>

        <button class="exit-btn" @click="$emit('go-home')" title="返回首页">
           <el-icon><House /></el-icon>
        </button>
      </el-header>

      <el-main class="chat-main" ref="chatMainRef">
        <div class="chat-inner">
          <div class="message-wrapper" v-for="(msg, index) in messages" :key="index" :class="msg.role">
            <div class="avatar-container">
              <el-avatar :src="msg.avatar" class="avatar" />
            </div>
            <div class="bubble">
              <div class="text-content" v-html="formatText(msg.content)"></div>
              <span v-if="msg.role === 'assistant' && isGenerating && index === messages.length - 1" class="cursor-blink"></span>
            </div>
          </div>

          <div v-if="messages.length === 0" class="empty-state">
            <div class="empty-icon-wrapper">
              <el-avatar :src="getRoleInfo().avatar" class="empty-avatar" />
            </div>
            <h3 class="empty-title">{{ getRoleInfo().welcomeTitle }}</h3>
            <p class="empty-subtext">{{ getRoleInfo().welcomeText }}</p>
          </div>
          <div style="height: 140px;"></div>
        </div>
      </el-main>

      <div class="fixed-footer">
        <div class="input-container">
          <el-input
            v-model="inputText"
            type="textarea"
            :rows="1"
            :autosize="{ minRows: 1, maxRows: 4 }"
            placeholder="输入你想说的话..."
            @keydown.enter.prevent="handleEnter"
            :disabled="isGenerating"
            class="glass-textarea"
          />
          <button class="send-btn" :class="{ 'is-loading': isGenerating }" @click="sendMessage" :disabled="isGenerating || !inputText.trim()">
            <el-icon v-if="!isGenerating"><Position /></el-icon>
            <div v-else class="loader-dots"><span></span><span></span><span></span></div>
          </button>
        </div>
      </div>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, reactive, nextTick, watch, onMounted } from 'vue'
import { Plus, Delete, Position, Lock, DocumentCopy, House, Menu, Close } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { USER_AVATAR, getCurrentRoleConfig } from '../config/constants.js'

const emit = defineEmits(['go-home', 'enter-secret', 'update:roleType'])

const isMobileMenuOpen = ref(false)
const uid = ref(localStorage.getItem('chat_uid') || generateUid())
const recoverUid = ref('')
const sessions = ref([])
const currentSessionId = ref('')
const messages = ref([])
const inputText = ref('')
const isGenerating = ref(false)
const chatMainRef = ref(null)

const roleConfig = reactive({
  role_type: '自定义',
  name: '李蓝宝',
  nature: '幽默风趣'
})

// ★★★ 在这里新增了两位新助手角色
const availableRoles = ref([
  { role_type: '自定义', name: '李蓝宝' },
  { role_type: '誊思致雪', name: '誊思致雪' },
  { role_type: '薇尔莉特', name: '薇尔莉特' },
  { role_type: '音乐推荐助手', name: '音乐推荐助手' },
  { role_type: '游戏聊天助手', name: '游戏聊天助手' }
])

const getRoleInfo = () => getCurrentRoleConfig(roleConfig.role_type)

const fetchRoles = async () => {
  try {
    const res = await fetch('/api/roles')
    if (res.ok) {
      const data = await res.json()
      if (data && data.length > 0) {
        availableRoles.value = data
      }
    }
  } catch (error) {
    console.warn("无法从后端获取角色列表，使用本地默认配置", error)
  }
}

onMounted(() => {
  fetchRoles()
  fetchSessions()
})

function generateUid() {
  const newUid = Math.random().toString(36).substring(2, 10)
  localStorage.setItem('chat_uid', newUid)
  return newUid
}

const copyUid = async () => {
  try {
    await navigator.clipboard.writeText(uid.value)
    ElMessage.success('身份码已灵动复制至剪贴板 ✨')
  } catch (err) {
    const input = document.createElement('input')
    input.value = uid.value
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
    ElMessage.success('身份码已灵动复制至剪贴板 ✨')
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatMainRef.value) {
    const el = chatMainRef.value.$el
    el.scrollTop = el.scrollHeight
  }
}

const formatText = (text) => text ? text.replace(/\n/g, '<br/>') : ''

const fetchSessions = async () => {
  try {
    const res = await fetch(`/api/sessions?uid=${uid.value}`)
    if (!res.ok) throw new Error("请求失败")
    const data = await res.json()
    sessions.value = data
  } catch (error) {
    console.error("获取历史记录失败", error)
  }
}

const loadSession = async (id) => {
  if (isGenerating.value) return ElMessage.warning("伙伴正在回复，请稍后再切换")
  try {
    const res = await fetch(`/api/sessions/${id}?uid=${uid.value}`)
    if (!res.ok) throw new Error("获取详情失败")
    const data = await res.json()

    currentSessionId.value = id
    isMobileMenuOpen.value = false

    const savedName = data.name || '李蓝宝'
    const savedNature = data.nature || ''

    let detectedRoleType = '自定义'
    const matchedRole = availableRoles.value.find(r => r.name === savedName)
    if (matchedRole && matchedRole.role_type !== '自定义') {
      detectedRoleType = matchedRole.role_type
    }

    roleConfig.role_type = detectedRoleType
    roleConfig.name = savedName
    roleConfig.nature = savedNature
    emit('update:roleType', detectedRoleType)

    const currentAiAvatar = getRoleInfo().avatar

    messages.value = (data.message || []).map(msg => ({
      ...msg,
      avatar: msg.avatar || (msg.role === 'user' ? USER_AVATAR : currentAiAvatar)
    }))

    scrollToBottom()
  } catch (error) {
    ElMessage.error("获取回忆失败，请检查网络联接")
  }
}

const createNewSession = () => {
  currentSessionId.value = ''
  messages.value = []
  roleConfig.role_type = '自定义'

  const customRole = availableRoles.value.find(r => r.role_type === '自定义')
  roleConfig.name = customRole ? customRole.name : '李蓝宝'
  roleConfig.nature = '幽默风趣'

  emit('update:roleType', '自定义')
  isMobileMenuOpen.value = false
}

watch(() => roleConfig.role_type, (newVal) => {
  const selectedRole = availableRoles.value.find(r => r.role_type === newVal)

  if (newVal === '自定义') {
    roleConfig.name = selectedRole?.name || '李蓝宝'
    roleConfig.nature = '幽默风趣'
  } else {
    roleConfig.name = selectedRole?.name || newVal
    roleConfig.nature = ''
  }
  emit('update:roleType', newVal)
})

const recoverHistory = async () => {
  const targetUid = recoverUid.value.trim()
  if (targetUid.length !== 8) return ElMessage.warning("请输入完整、正确的8位身份码")
  try {
    const res = await fetch(`/api/sessions?uid=${targetUid}`)
    if (!res.ok) throw new Error("请求失败")
    const data = await res.json()
    if (data.length === 0) return ElMessage.warning("未找到该身份码的记忆痕迹，请检查是否输入正确")
    uid.value = targetUid
    localStorage.setItem('chat_uid', uid.value)
    createNewSession()
    sessions.value = data
    ElMessage.success("记忆同步成功")
  } catch (error) {
    ElMessage.error("同步失败，请检查网络联接")
  }
}

const deleteSession = (id) => {
  ElMessageBox.confirm('确定要抹除这段对话记忆吗？此操作将无法挽回。', '抹除确认', {
    type: 'warning', confirmButtonText: '确定抹除', cancelButtonText: '再想一下'
  }).then(async () => {
    try {
      await fetch(`/api/sessions/${id}?uid=${uid.value}`, { method: 'DELETE' })
      sessions.value = sessions.value.filter(s => s.session_id !== id)
      if (currentSessionId.value === id) createNewSession()
      ElMessage.success('记忆已抹除')
    } catch (e) {
      ElMessage.error('清理失败，网络出现波动')
    }
  }).catch(() => {})
}

const handleEnter = (e) => {
  if (!e.shiftKey) sendMessage()
  else inputText.value += '\n'
}

const sendMessage = async () => {
  if (!inputText.value.trim() || isGenerating.value) return
  const userText = inputText.value.trim()

  // ★★★ 在这里新增了 薇尔莉特、音乐助手 和 游戏助手 的暗号验证拦截
  const secretCodes = ['260315', '251027', '260410', '19xxxx', '240802', '180818','111111']
  if (secretCodes.includes(userText)) {
    inputText.value = ''
    emit('enter-secret', userText)
    return
  }

  inputText.value = ''
  if (!currentSessionId.value) {
    const now = new Date()
    const pad = n => n.toString().padStart(2, '0')
    currentSessionId.value = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}_${pad(now.getHours())}-${pad(now.getMinutes())}-${pad(now.getSeconds())}`
  }

  messages.value.push({ role: 'user', content: userText, avatar: USER_AVATAR })
  scrollToBottom()

  const aiAvatar = getRoleInfo().avatar
  messages.value.push({ role: 'assistant', content: '', avatar: aiAvatar })
  isGenerating.value = true
  scrollToBottom()

  try {
    const response = await fetch(`/api/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/octet-stream' },
      body: JSON.stringify({
        uid: uid.value, session_id: currentSessionId.value,
        role_config: roleConfig, content: userText,
        user_avatar: USER_AVATAR, ai_avatar: aiAvatar
      })
    })

    if (!response.ok) throw new Error("服务端异常")
    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')

    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      messages.value[messages.value.length - 1].content += decoder.decode(value, { stream: true })
      scrollToBottom()
    }
  } catch (error) {
    messages.value[messages.value.length - 1].content = "（伙伴似乎走神了，没听到你说的话。请检查网络或后端服务）"
  } finally {
    isGenerating.value = false
    fetchSessions()
  }
}
</script>

<style scoped>
/* 此文件已彻底清除了所有默认色。由 App.vue 负责提供多主题颜色和背景！ */
.main-layout { width: 95vw; max-width: 1400px; height: 92dvh; border-radius: 24px; overflow: hidden; z-index: 10; position: relative; }
.sidebar { display: flex; flex-direction: column; padding: 24px 20px; transition: all 0.5s ease; border-right-style: solid; border-right-width: 1px; border-right-color: transparent;}
.mobile-close-btn { display: none; }
.sidebar-overlay { display: none; }
.sidebar-header { margin-bottom: 28px; }
.logo-wrapper { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.logo-img { width: 15%; height: 15%; object-fit: cover; }
.logo { font-size: 20px; font-weight: 700; margin: 0; letter-spacing: 1px; }

.uid-box { border-radius: 8px; display: inline-flex; align-items: center; overflow: hidden; cursor: pointer; border-style: solid; border-width: 1px; border-color: transparent; transition: all 0.2s; }
.uid-box:hover { transform: translateY(-1px); }
.uid-label { font-size: 12px; font-weight: 600; padding: 6px 10px; }
.uid-value { font-size: 13px; padding: 6px 12px; font-family: monospace; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.copy-icon { transition: color 0.2s; }

.new-chat-btn { width: 100%; border-radius: 12px; height: 46px; margin-bottom: 24px; font-weight: 600; font-size: 15px; display: flex; align-items: center; justify-content: center; gap: 8px; cursor: pointer; transition: all 0.2s; border-style: solid; border-width: 1px; border-color: transparent;}
.new-chat-btn:hover { transform: translateY(-1px); }

.history-list { flex: 1; overflow: hidden; }
.list-title { font-size: 13px; font-weight: 600; margin-bottom: 12px; letter-spacing: 1px; }
.history-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-radius: 12px; cursor: pointer; transition: all 0.2s; margin-bottom: 6px; border-style: solid; border-width: 1px; border-color: transparent;}
.session-info { display: flex; flex-direction: column; overflow: hidden; }
.session-name { font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.session-time { font-size: 12px; margin-top: 4px; }

.delete-btn-wrapper { opacity: 0; display: flex; align-items: center; justify-content: center; width: 30px; height: 30px; border-radius: 8px; transition: all 0.2s; }
.delete-icon { font-size: 15px; }
.history-item:hover .delete-btn-wrapper { opacity: 1; }
.sidebar-footer { margin-top: 24px; }
:deep(.recover-input .el-input__wrapper) { border-radius: 10px 0 0 10px; }
:deep(.recover-input .el-input-group__append) { border-radius: 0 10px 10px 0; font-weight: 600; border-left: none; }

.chat-container { display: flex; flex-direction: column; position: relative; background: transparent; }
.chat-header { height: 70px; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; border-bottom-style: solid; border-bottom-width: 1px; border-bottom-color: transparent; z-index: 20; transition: all 0.5s ease; }
.mobile-menu-btn { display: none; }
.role-settings { display: flex; gap: 12px; }
.custom-inputs { display: flex; gap: 12px; }
.locked-status { display: flex; align-items: center; }
.status-badge { display: flex; align-items: center; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; white-space: nowrap; transition: all 0.5s ease; border-style: solid; border-width: 1px; border-color: transparent;}
.dot.connected { width: 8px; height: 8px; border-radius: 50%; margin-right: 10px; flex-shrink: 0; }
.badge-text { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px; }
.lock-tip { font-size: 13px; margin-left: 20px; display: flex; align-items: center; gap: 6px; }
.exit-btn { width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer; transition: all 0.2s; flex-shrink: 0; border-style: solid; border-width: 1px; border-color: transparent;}
.exit-btn:hover { transform: scale(1.05); }

.chat-main { flex: 1; overflow-y: auto; scroll-behavior: smooth; padding: 0; }
.chat-inner { max-width: 840px; margin: 0 auto; padding: 40px 24px; }
.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 15vh; text-align: center; }
.empty-icon-wrapper { width: 88px; height: 88px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 24px; border-style: solid; border-width: 3px; border-color: transparent; transition: all 0.3s ease; }
.empty-avatar { width: 72px; height: 72px; border-radius: 50%; }
.empty-title { font-size: 24px; font-weight: 600; margin: 0 0 12px 0; }
.empty-subtext { font-size: 15px; margin: 0; max-width: 400px; line-height: 1.6; }

.message-wrapper { display: flex; margin-bottom: 36px; align-items: flex-start; }
.message-wrapper.user { flex-direction: row-reverse; }
.avatar-container { border-radius: 14px; padding: 2px; flex-shrink: 0; }
.avatar { width: 42px; height: 42px; border-radius: 12px; display: block; }
.message-wrapper.user .avatar-container { margin-left: 18px; }
.message-wrapper.assistant .avatar-container { margin-right: 18px; }

.bubble { max-width: 75%; padding: 16px 22px; font-size: 15px; line-height: 1.7; word-wrap: break-word; backdrop-filter: blur(10px); transition: background-color 0.5s ease; border-style: solid; border-width: 1px; border-color: transparent;}
.message-wrapper.user .bubble { border-radius: 20px 4px 20px 20px; }
.message-wrapper.assistant .bubble { border-radius: 4px 20px 20px 20px; }

.cursor-blink { display: inline-block; width: 8px; height: 16px; margin-left: 6px; vertical-align: text-bottom; animation: blink 1s step-end infinite; }

.fixed-footer { position: absolute; bottom: 32px; left: 0; right: 0; display: flex; justify-content: center; padding: 0 24px; pointer-events: none; }
.input-container { pointer-events: auto; width: 100%; max-width: 800px; display: flex; align-items: flex-end; border-radius: 24px; padding: 8px 16px 8px 20px; transition: all 0.3s; border-style: solid; border-width: 1px; border-color: transparent;}
.input-container:focus-within { transform: translateY(-2px); }

.send-btn { margin-left: 12px; margin-bottom: 0px; width: 40px; height: 40px; border-radius: 14px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; font-size: 18px; flex-shrink: 0; border: none; }
.send-btn:hover:not(:disabled) { transform: scale(1.05) rotate(-5deg); }
.send-btn:disabled { cursor: not-allowed; }

.loader-dots { display: flex; gap: 3px; }
.loader-dots span { width: 4px; height: 4px; background-color: #fff; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; }
.loader-dots span:nth-child(1) { animation-delay: -0.32s; }
.loader-dots span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }

@media (max-width: 768px) {
  .main-layout { width: 100%; height: 100%; border-radius: 0; border: none; }
  .mobile-menu-btn { display: flex; align-items: center; justify-content: center; background: transparent; border: none; font-size: 24px; padding: 8px; margin-right: 12px; cursor: pointer; }
  .sidebar { position: fixed; left: 0; top: 0; bottom: 0; z-index: 1000; transform: translateX(-100%); width: 85vw !important; max-width: 320px; border-right: none;}
  .sidebar.mobile-open { transform: translateX(0); }
  .sidebar-overlay { display: block; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 999; }
  .mobile-close-btn { display: flex; position: absolute; right: 16px; top: 16px; font-size: 24px; cursor: pointer; }
  .chat-header { padding: 10px 16px; height: auto; min-height: 64px; }
  .role-settings { flex-wrap: wrap; gap: 10px; width: 100%; }
  .role-settings .el-select { width: 100% !important; }
  .custom-inputs { width: 100%; flex-direction: column; gap: 10px; margin-top: 4px; }
  .custom-inputs .el-input { width: 100% !important; }
  .mobile-hide { display: none !important; }
  .chat-inner { padding: 20px 16px; }
  .bubble { max-width: 85%; padding: 12px 16px; }
  .message-wrapper.user .avatar-container { margin-left: 10px; }
  .message-wrapper.assistant .avatar-container { margin-right: 10px; }
  .fixed-footer { bottom: 16px; padding: 0 16px; }
  .input-container { border-radius: 20px; padding: 6px 12px 6px 16px; }
}
</style>




<template>
  <div class="chat-view-root">

    <transition name="fade-hall">
      <RoleSelectionHall
        v-if="isSelectingRole"
        :available-roles="availableRoles"
        :role-config="roleConfig"
        @update-role="handleRoleUpdate"
        @enter-chat="enterChat"
      />
    </transition>

    <transition name="fade-transform">
      <el-container v-show="!isSelectingRole" class="main-layout glass-panel">

        <ChatSidebar
          :is-mobile-menu-open="isMobileMenuOpen"
          :uid="uid"
          :sessions="sessions"
          :current-session-id="currentSessionId"
          @close-mobile-menu="isMobileMenuOpen = false"
          @create-session="createNewSession"
          @load-session="loadSession"
          @delete-session="deleteSession"
          @sync-history="recoverHistory"
        />

        <ChatBoard
          :messages="messages"
          :is-generating="isGenerating"
          :role-config="roleConfig"
          @open-mobile-menu="isMobileMenuOpen = true"
          @back-to-hall="backToSelection"
          @send-message="handleSendMessage"
        />

      </el-container>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { USER_AVATAR, getCurrentRoleConfig } from '../config/constants.js'
import { SECRET_QUESTS } from '../store/questState.js'

import RoleSelectionHall from '../components/RoleSelectionHall.vue'
import ChatSidebar from '../components/ChatSidebar.vue'
import ChatBoard from '../components/ChatBoard.vue'

const emit = defineEmits(['update:roleType'])
const router = useRouter()
const route = useRoute()

// 🌟 核心修复：使用 Query 参数（?view=room）来判断页面状态 🌟
// 这样就不会触发 Vue Router 的组件缺失警告，且同样完美支持浏览器返回键！
const isSelectingRole = computed(() => route.query.view !== 'room')

const isMobileMenuOpen = ref(false)
const uid = ref(localStorage.getItem('chat_uid') || generateUid())
const sessions = ref([])
const currentSessionId = ref('')
const messages = ref([])
const isGenerating = ref(false)
const availableRoles = ref([])

const roleConfig = reactive({
  role_type: '',
  name: '',
  nature: ''
})

function generateUid() {
  const newUid = Math.random().toString(36).substring(2, 10)
  localStorage.setItem('chat_uid', newUid)
  return newUid
}

const fetchRoles = async () => {
  try {
    const res = await fetch('/api/roles')
    if (res.ok) {
      const data = await res.json()
      if (data && data.length > 0) {
        const liLanbaoIndex = data.findIndex(r => r.role_type === '李蓝宝')
        if (liLanbaoIndex > 0) {
          const liLanbao = data.splice(liLanbaoIndex, 1)[0]
          data.unshift(liLanbao)
        }
        availableRoles.value = data
        if (!roleConfig.role_type) roleConfig.role_type = '李蓝宝'
      }
    }
  } catch (error) {
    console.warn("无法从后端获取角色列表，使用本地默认配置", error)
  }
}

const fetchSessions = async () => {
  try {
    const res = await fetch(`/api/sessions?uid=${uid.value}`)
    if (res.ok) sessions.value = await res.json()
  } catch (error) {
    console.error("获取历史记录失败", error)
  }
}

const handleRoleUpdate = (newType) => {
  const selectedRole = availableRoles.value.find(r => r.role_type === newType)
  if (selectedRole && newType !== '自定义') {
    roleConfig.name = selectedRole.name
    roleConfig.nature = ''
  }
  roleConfig.role_type = newType
  emit('update:roleType', newType)
}

const enterChat = () => {
  // 🌟 点击进入聊天，追加 query 参数 ?view=room
  router.push({ name: 'chat', query: { view: 'room' } })
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
    if (matchedRole && matchedRole.role_type !== '自定义') detectedRoleType = matchedRole.role_type

    roleConfig.role_type = detectedRoleType
    roleConfig.name = savedName
    roleConfig.nature = savedNature
    emit('update:roleType', detectedRoleType)

    const currentAiAvatar = getCurrentRoleConfig(detectedRoleType)?.avatar || USER_AVATAR
    messages.value = (data.message || []).map(msg => ({
      ...msg,
      avatar: msg.avatar || (msg.role === 'user' ? USER_AVATAR : currentAiAvatar),
      isThinking: false
    }))

    // 🌟 加载记忆后，如果是从大厅进来的，追加 query 进入房间
    if (route.query.view !== 'room') {
      router.push({ name: 'chat', query: { view: 'room' } })
    }
  } catch (error) {
    ElMessage.error("获取回忆失败，请检查网络联接")
  }
}

const createNewSession = () => {
  currentSessionId.value = ''
  messages.value = []
  isMobileMenuOpen.value = false
  // 🌟 返回大厅，去掉 URL 里的 ?view=room
  if (route.query.view === 'room') {
    router.push({ name: 'chat' })
  }
}

const recoverHistory = async (targetUid) => {
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

const backToSelection = () => {
  if (messages.value.length > 0) {
    ElMessageBox.confirm('返回选择大厅将暂时离开当前对话，你可以在左侧边栏找到它。确定返回吗？', '提示', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'info'
    }).then(() => {
      createNewSession()
    }).catch(() => {})
  } else {
    createNewSession()
  }
}

const handleSendMessage = async (userText) => {
  const validCodes = [...SECRET_QUESTS.map(q => q.code), '160615']
  if (validCodes.includes(userText)) {
    router.push({ name: 'secret', params: { secretCode: userText } })
    return
  }

  if (!currentSessionId.value) {
    const now = new Date()
    const pad = n => n.toString().padStart(2, '0')
    currentSessionId.value = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}_${pad(now.getHours())}-${pad(now.getMinutes())}-${pad(now.getSeconds())}`
  }

  messages.value.push({ role: 'user', content: userText, avatar: USER_AVATAR })

  const aiAvatar = getCurrentRoleConfig(roleConfig.role_type)?.avatar || USER_AVATAR
  messages.value.push({ role: 'assistant', content: '', avatar: aiAvatar, isThinking: true })
  isGenerating.value = true

  const controller = new AbortController()
  const timeoutId = setTimeout(() => { controller.abort() }, 10000)

  try {
    const response = await fetch(`/api/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/octet-stream' },
      body: JSON.stringify({
        uid: uid.value, session_id: currentSessionId.value,
        role_config: roleConfig, content: userText,
        user_avatar: USER_AVATAR, ai_avatar: aiAvatar
      }),
      signal: controller.signal
    })

    if (!response.ok) throw new Error("服务端异常")
    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let isFirstChunk = true

    while (true) {
      const { value, done } = await reader.read()
      if (done) break

      if (isFirstChunk) {
        messages.value[messages.value.length - 1].isThinking = false
        clearTimeout(timeoutId)
        isFirstChunk = false
      }

      messages.value[messages.value.length - 1].content += decoder.decode(value, { stream: true })
    }
  } catch (error) {
    messages.value[messages.value.length - 1].isThinking = false
    if (error.name === 'AbortError') {
      messages.value[messages.value.length - 1].content = "（大脑烧坏了...等得太久没有回应，连线已断开，请稍后重试）"
    } else {
      messages.value[messages.value.length - 1].content = "（伙伴似乎走神了，没听到你说的话。请检查网络或后端服务）"
    }
  } finally {
    messages.value[messages.value.length - 1].isThinking = false
    isGenerating.value = false
    clearTimeout(timeoutId)
    fetchSessions()
  }
}

onMounted(() => {
  fetchRoles()
  fetchSessions()
})
</script>

<style scoped>
.chat-view-root { width: 100vw; height: 100dvh; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }
.main-layout { width: 95vw; max-width: 1400px; height: 92dvh; border-radius: 24px; overflow: hidden; z-index: 10; position: relative; }

.fade-transform-enter-active, .fade-transform-leave-active { transition: opacity 0.6s ease, transform 0.6s ease; transition-delay: 0.1s;}
.fade-transform-enter-from, .fade-transform-leave-to { opacity: 0; transform: translateY(20px); }

@media (max-width: 768px) {
  .main-layout { width: 100%; height: 100%; border-radius: 0; border: none; }
}
</style>
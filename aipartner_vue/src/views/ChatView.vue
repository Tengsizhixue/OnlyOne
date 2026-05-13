<template>
  <div class="chat-view-root">

    <!-- 🌟 核心优化：彻底移除 mode="out-in"，启用动态的双向 Cross-fade (淡入淡出堆叠) 动画！ -->
    <transition :name="transitionName">

      <!-- 场景 A：角色选择大厅（套上绝对定位外壳，确保在动画期间它和聊天室完美重叠而不破坏布局） -->
      <div v-if="isSelectingRole" class="scene-wrapper">
        <RoleSelectionHall
          :available-roles="availableRoles"
          :role-config="roleConfig"
          @update-role="handleRoleUpdate"
          @enter-chat="enterChat"
        />
      </div>

      <!-- 场景 B：聊天室主界面 -->
      <div v-else class="scene-wrapper">
        <el-container class="main-layout glass-panel">

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
      </div>

    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, onUnmounted } from 'vue'
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

const isSelectingRole = computed(() => route.query.view !== 'room')

// 🌟 动态控制场景动画方向 (进聊天 / 退回大厅)
const transitionName = ref('fade-zoom-in')

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

let activeStreamController = null

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
  transitionName.value = 'fade-zoom-in' // 触发“推近”动画
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

    if (route.query.view !== 'room') {
      transitionName.value = 'fade-zoom-in'
      router.push({ name: 'chat', query: { view: 'room' } })
    }
  } catch (error) {
    ElMessage.error("获取回忆失败，请检查网络联接")
  }
}

const createNewSession = () => {
  if (activeStreamController) {
    activeStreamController.abort()
    activeStreamController = null
  }

  currentSessionId.value = ''
  messages.value = []
  isMobileMenuOpen.value = false
  if (route.query.view === 'room') {
    transitionName.value = 'fade-zoom-out' // 触发“后退”动画
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
  ElMessageBox.confirm('确定要删除吗？此操作将无法挽回。', '抹除确认', {
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
  createNewSession()
}

const handleSendMessage = async (userText) => {
  const validCodes = [...SECRET_QUESTS.map(q => q.code), '160615']
  if (validCodes.includes(userText)) {
    // 💡 修复：将当前的会话ID和角色配置通过 query 参数传递给彩蛋页面
    router.push({
      name: 'secret',
      params: { secretCode: userText },
      query: {
        role: roleConfig.role_type,
        session: currentSessionId.value || undefined
      }
    })
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

  activeStreamController = new AbortController()
  const timeoutId = setTimeout(() => { activeStreamController.abort() }, 10000)

  try {
    const response = await fetch(`/api/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/octet-stream' },
      body: JSON.stringify({
        uid: uid.value, session_id: currentSessionId.value,
        role_config: roleConfig, content: userText,
        user_avatar: USER_AVATAR, ai_avatar: aiAvatar
      }),
      signal: activeStreamController.signal
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

      if (messages.value.length === 0) break;
      messages.value[messages.value.length - 1].content += decoder.decode(value, { stream: true })
    }
  } catch (error) {
    if (messages.value.length > 0) {
      messages.value[messages.value.length - 1].isThinking = false
      if (error.name === 'AbortError') {
        messages.value[messages.value.length - 1].content += "\n[对话已中断]"
      } else {
        messages.value[messages.value.length - 1].content = "（伙伴似乎走神了，没听到你说的话。请检查网络或后端服务）"
      }
    }
  } finally {
    if (messages.value.length > 0) {
      messages.value[messages.value.length - 1].isThinking = false
    }
    isGenerating.value = false
    clearTimeout(timeoutId)
    activeStreamController = null
    fetchSessions()
  }
}

onUnmounted(() => {
  if (activeStreamController) {
    activeStreamController.abort()
  }
})

onMounted(() => {
  fetchRoles()
  fetchSessions()
})

onMounted(async () => {
  await fetchRoles()
  await fetchSessions()

  // 🌟 返回聊天室时：根据 URL 参数自动恢复刚才的对话现场
  if (route.query.view === 'room') {
    if (route.query.session) {
      await loadSession(route.query.session)
    } else if (route.query.role) {
      handleRoleUpdate(route.query.role)
    }
  }
})
</script>

<style scoped>
.chat-view-root { width: 100vw; height: 100dvh; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }

/* 🌟 新增的过渡包装层：绝对定位确保大厅和聊天室能够在切换期间重叠不挤压！ */
.scene-wrapper {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-layout { width: 95vw; max-width: 1400px; height: 92dvh; border-radius: 24px; overflow: hidden; z-index: 10; position: relative; }

/* 🌟 电影级无缝动画 1：推入聊天室
   - 聊天室从远端(0.9) 推向正常视角(1.0) 并淡入
   - 大厅从正常视角(1.0) 被迫扑向脸部(1.15) 并淡出，完美配合大厅内部发起的 3D 动画
*/
.fade-zoom-in-enter-active,
.fade-zoom-in-leave-active {
  transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.fade-zoom-in-enter-from {
  opacity: 0;
  transform: scale(0.9);
  filter: blur(10px);
}
.fade-zoom-in-leave-to {
  opacity: 0;
  transform: scale(1.15);
  filter: blur(5px);
}

/* 🌟 电影级无缝动画 2：退回大厅
   - 聊天室向后方远遁(0.9) 并淡出
   - 大厅从贴脸处(1.1) 平滑退回到正常视角(1.0) 并淡入
*/
.fade-zoom-out-enter-active,
.fade-zoom-out-leave-active {
  transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.fade-zoom-out-enter-from {
  opacity: 0;
  transform: scale(1.1);
  filter: blur(10px);
}
.fade-zoom-out-leave-to {
  opacity: 0;
  transform: scale(0.9);
  filter: blur(5px);
}

@media (max-width: 768px) {
  .main-layout { width: 100%; height: 100%; border-radius: 0; border: none; }
}
</style>
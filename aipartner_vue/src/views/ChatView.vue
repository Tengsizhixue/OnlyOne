<template>
  <div class="chat-view-root">

    <!-- 🌟 阶段一：沉浸式 3D 角色选择大厅 (全屏显示) 🌟 -->
    <transition name="fade-hall">
      <div v-if="isSelectingRole" class="selection-hall" @touchstart="handleTouchStart" @touchend="handleTouchEnd">

        <!-- 返回首页按钮 -->
        <button class="top-exit-btn" @click="router.push('/')" title="返回首页">
          <el-icon><House /></el-icon>
        </button>

        <div class="carousel-3d">
          <div
            v-for="(role, index) in availableRoles"
            :key="role.role_type"
            class="carousel-card glass-panel"
            :class="{ active: index === activeCarouselIndex }"
            :style="getCardStyle(index)"
            @click="handleCardClick(index)"
          >
            <!-- 卡片反光遮罩 -->
            <div class="card-glare"></div>

            <img :src="getRoleAvatar(role.role_type)" class="card-avatar" />
            <h3 class="card-name">{{ role.name }}</h3>
            <p class="card-desc">{{ getRoleDescription(role.role_type) }}</p>

            <!-- 激活状态提示文字 -->
            <div class="click-hint" :class="{ visible: index === activeCarouselIndex }">
              <span class="shimmer-text">点击卡片进入</span>
            </div>
          </div>
        </div>

        <!-- 轮播控制按钮 -->
        <div class="carousel-controls">
          <button class="nav-btn" @click.stop="prevRole" :disabled="activeCarouselIndex === 0">
            <el-icon><ArrowLeft/></el-icon>
          </button>
          <button class="nav-btn" @click.stop="nextRole" :disabled="activeCarouselIndex === availableRoles.length - 1">
            <el-icon><ArrowRight/></el-icon>
          </button>
        </div>

        <!-- 自定义角色的输入框，平滑过渡 -->
        <transition name="fade-hall">
          <div class="custom-inputs-center" v-if="roleConfig.role_type === '自定义'">
            <el-input v-model="roleConfig.name" placeholder="设定伙伴的称呼" class="glass-input custom-name-input" />
            <el-input v-model="roleConfig.nature" type="textarea" placeholder="设定TA的性格与世界观..." class="glass-textarea" />
          </div>
        </transition>

      </div>
    </transition>


    <!-- 🌟 阶段二：聊天主界面 (点击卡片后出现) 🌟 -->
    <transition name="fade-transform">
      <el-container v-show="!isSelectingRole" class="main-layout glass-panel">
        <div class="sidebar-overlay" v-show="isMobileMenuOpen" @click="isMobileMenuOpen = false"></div>

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

          <!-- 点击新建对话时，返回 3D 选择大厅 -->
          <button class="new-chat-btn" @click="createNewSession">
            <el-icon class="btn-icon"><Plus /></el-icon>
            <span>新建对话</span>
          </button>

          <div class="quest-section">
            <div class="list-title">神秘指引</div>
            <div class="quest-card glass-panel">
              <p v-if="currentQuest" class="quest-text">{{ currentQuest.question }}</p>
              <p v-else class="quest-text success">所有谜题已解开！</p>
            </div>
          </div>

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

        <el-container class="chat-container">
          <el-header class="chat-header">
            <button class="mobile-menu-btn" @click="isMobileMenuOpen = true">
              <el-icon><Menu /></el-icon>
            </button>

            <!-- 聊天框顶部的状态展示 -->
            <div class="locked-status">
              <div class="status-badge">
                <span class="dot connected"></span>
                正在与 <span class="badge-text">{{ roleConfig.name || '伙伴' }}</span> 对话
              </div>
            </div>

            <!-- 右上角退出大厅按钮 -->
            <button class="exit-btn" @click="backToSelection" title="返回角色选择">
               <el-icon><ArrowLeft /></el-icon>
            </button>
          </el-header>

          <el-main class="chat-main" ref="chatMainRef">
            <div class="chat-inner">

              <!-- 聊天内容区域 -->
              <div class="message-wrapper" v-for="(msg, index) in messages" :key="index" :class="msg.role">
                <div class="avatar-container">
                  <el-avatar :src="msg.avatar" class="avatar" />
                </div>
                <div class="bubble">
                  <div v-if="msg.isThinking" class="thinking-state">
                    <el-icon class="is-loading"><Loading /></el-icon> 大脑正在烧烤，请稍后...
                  </div>
                  <div v-else class="text-content" v-html="formatText(msg.content)"></div>
                  <span v-if="msg.role === 'assistant' && isGenerating && index === messages.length - 1 && !msg.isThinking" class="cursor-blink"></span>
                </div>
              </div>

              <!-- 刚刚进入聊天且没有聊天记录时的欢迎语 -->
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
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Delete, Position, Lock, DocumentCopy, House, Menu, Close, Loading, Compass, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { USER_AVATAR, DEFAULT_AI_AVATAR, getCurrentRoleConfig } from '../config/constants.js'
import { SECRET_QUESTS, currentQuest } from '../store/questState.js'

const emit = defineEmits(['update:roleType'])
const router = useRouter()

// 🌟 核心状态：是否处于全屏角色选择大厅阶段 🌟
const isSelectingRole = ref(true)

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
  role_type: '',
  name: '',
  nature: ''
})

const availableRoles = ref([])
const isMobile = ref(false)

// ======== 3D 轮播控制逻辑 ========
const activeCarouselIndex = ref(0)
let touchStartX = 0

// 获取卡片展示的基础信息
const getRoleAvatar = (type) => getCurrentRoleConfig(type)?.avatar || DEFAULT_AI_AVATAR
const getRoleDescription = (type) => getCurrentRoleConfig(type)?.welcomeText || '你好，我是你的伙伴'

// 轮播操作
const nextRole = () => { if (activeCarouselIndex.value < availableRoles.value.length - 1) activeCarouselIndex.value++ }
const prevRole = () => { if (activeCarouselIndex.value > 0) activeCarouselIndex.value-- }

// 用户点击 3D 卡片
const handleCardClick = (index) => {
  if (activeCarouselIndex.value === index) {
    // 💡 点击的是当前高亮的卡片 -> 正式进入聊天室！
    if (roleConfig.role_type === '自定义' && !roleConfig.name.trim()) {
      ElMessage.warning('请先为自定义伙伴设定称呼！')
      return
    }
    isSelectingRole.value = false
  } else {
    // 点击边缘卡片 -> 将其切换到中间展示
    activeCarouselIndex.value = index
  }
}

// 返回 3D 选择大厅
const backToSelection = () => {
  if (messages.length > 0) {
    ElMessageBox.confirm('返回选择大厅将暂时离开当前对话，你可以在左侧边栏找到它。确定返回吗？', '提示', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'info'
    }).then(() => {
      createNewSession()
    }).catch(() => {})
  } else {
    createNewSession()
  }
}

// 手机端手势滑动
const handleTouchStart = (e) => { touchStartX = e.touches[0].clientX }
const handleTouchEnd = (e) => {
  const touchEndX = e.changedTouches[0].clientX
  if (touchStartX - touchEndX > 50) nextRole() // 左滑
  else if (touchEndX - touchStartX > 50) prevRole() // 右滑
}

// 动态计算 3D 卡片的 CSS Style (适配全屏)
const getCardStyle = (index) => {
  const offset = index - activeCarouselIndex.value
  const absOffset = Math.abs(offset)
  const sign = Math.sign(offset)

  // 大厅变成全屏后，间距和深度要更大些以体现史诗感
  const xTranslate = isMobile.value ? 100 : 260
  const zTranslate = isMobile.value ? 80 : 150
  const rotate = isMobile.value ? 35 : 45
  const scaleDrop = isMobile.value ? 0.15 : 0.1

  let transform = ''
  let opacity = 1
  let zIndex = 100 - absOffset

  if (offset === 0) {
    transform = `translateX(0px) translateZ(50px) rotateY(0deg) scale(1)`
    opacity = 1
  } else {
    transform = `translateX(${sign * xTranslate * absOffset}px) translateZ(-${zTranslate * absOffset}px) rotateY(${-sign * rotate}deg) scale(${1 - absOffset * scaleDrop})`
    opacity = absOffset > 2 ? 0 : (1 - absOffset * 0.4)
  }

  return {
    transform,
    zIndex,
    opacity,
    pointerEvents: absOffset > 1 ? 'none' : 'auto'
  }
}

// 监听轮播改变，同步给角色配置
watch(activeCarouselIndex, (newIdx) => {
  if (availableRoles.value[newIdx]) {
    roleConfig.role_type = availableRoles.value[newIdx].role_type
  }
})

// 监听角色改变，同步背景、默认数据
watch(() => roleConfig.role_type, (newType) => {
  const idx = availableRoles.value.findIndex(r => r.role_type === newType)
  if (idx !== -1 && idx !== activeCarouselIndex.value) {
    activeCarouselIndex.value = idx
  }
  emit('update:roleType', newType)

  const selectedRole = availableRoles.value.find(r => r.role_type === newType)
  if (selectedRole && newType !== '自定义') {
    roleConfig.name = selectedRole.name
    roleConfig.nature = ''
  }
})
// ===================================


const checkMobile = () => { isMobile.value = window.innerWidth <= 768 }

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
  fetchRoles()
  fetchSessions()
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

const getRoleInfo = () => getCurrentRoleConfig(roleConfig.role_type)

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

        if (!roleConfig.role_type) {
          roleConfig.role_type = '李蓝宝'
        }
        // 初始化轮播位置
        const idx = availableRoles.value.findIndex(r => r.role_type === roleConfig.role_type)
        if (idx !== -1) activeCarouselIndex.value = idx
      }
    }
  } catch (error) {
    console.warn("无法从后端获取角色列表，使用本地默认配置", error)
  }
}

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
      avatar: msg.avatar || (msg.role === 'user' ? USER_AVATAR : currentAiAvatar),
      isThinking: false
    }))

    // 加载历史记录后，直接跳过选人环节进入对话
    isSelectingRole.value = false
    scrollToBottom()
  } catch (error) {
    ElMessage.error("获取回忆失败，请检查网络联接")
  }
}

const createNewSession = () => {
  currentSessionId.value = ''
  messages.value = []
  roleConfig.role_type = '李蓝宝'
  emit('update:roleType', '李蓝宝')
  isMobileMenuOpen.value = false
  // 🌟 点击新建对话时，重回选择人物大厅 🌟
  isSelectingRole.value = true
}

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

  const validCodes = [...SECRET_QUESTS.map(q => q.code), '160615']

  if (validCodes.includes(userText)) {
    inputText.value = ''
    router.push({ name: 'secret', params: { secretCode: userText } })
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
  messages.value.push({ role: 'assistant', content: '', avatar: aiAvatar, isThinking: true })
  isGenerating.value = true
  scrollToBottom()

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
      scrollToBottom()
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
</script>

<style scoped>
/* 根容器充当视窗 */
.chat-view-root {
  width: 100vw; height: 100dvh; display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
}

/* 🌟 ==================== 阶段一：全屏 3D 选择大厅 ==================== 🌟 */
.selection-hall {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  perspective: 1500px; z-index: 50; user-select: none;
}

/* 左上角退出按钮 */
.top-exit-btn {
  position: absolute; top: 30px; left: 30px; z-index: 60;
  width: 48px; height: 48px; border-radius: 50%;
  background: rgba(0, 0, 0, 0.2); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);
  color: white; font-size: 24px; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.3s;
}
.top-exit-btn:hover { background: rgba(0, 0, 0, 0.4); transform: scale(1.1); }

/* 3D 舞台 */
.carousel-3d {
  position: relative; width: 340px; height: 480px;
  transform-style: preserve-3d; display: flex; justify-content: center; align-items: center;
}

/* 独立卡片 */
.carousel-card {
  position: absolute; width: 100%; height: 100%;
  border-radius: 20px; padding: 40px 24px; text-align: center;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  transition: all 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); cursor: pointer;
  box-shadow: 0 15px 50px rgba(0,0,0,0.5);
  border: 1px solid rgba(255, 255, 255, 0.15); overflow: hidden;
  background: rgba(15, 23, 42, 0.3); /* 防止完全透明 */
  backdrop-filter: blur(2px); -webkit-backdrop-filter: blur(2px);
}

.card-glare {
  position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
  background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.25) 50%, rgba(255,255,255,0) 100%);
  transform: skewX(-20deg); transition: all 0.5s; pointer-events: none; z-index: 1;
}
.carousel-card.active .card-glare { animation: shimmer 4s infinite linear; }

.carousel-card.active {
  box-shadow: 0 0 60px rgba(255, 255, 255, 0.3), inset 0 0 30px rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.8);
}

.card-avatar {
  width: 140px; height: 140px; border-radius: 50%; margin-bottom: 30px;
  border: 4px solid rgba(255,255,255,0.4); object-fit: cover;
  transition: transform 0.4s ease, border-color 0.4s ease; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
  z-index: 2;
}
.carousel-card.active .card-avatar { transform: scale(1.1); border-color: rgba(255,255,255,1); }

.card-name { font-size: 28px; font-weight: bold; margin: 0 0 16px 0; transition: color 0.3s; z-index: 2; color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.5);}
.card-desc {
  font-size: 15px; line-height: 1.7; opacity: 0.9; z-index: 2; color: #e2e8f0;
  display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden;
}

/* 提示文字：点击进入对话 */
.click-hint {
  position: absolute; bottom: 30px; opacity: 0; transform: translateY(10px);
  transition: all 0.5s ease; font-size: 14px; font-weight: bold; color: rgba(255,255,255,0.9);
  z-index: 2; pointer-events: none; background: rgba(0,0,0,0.2); padding: 8px 20px; border-radius: 20px;
}
.click-hint.visible { opacity: 1; transform: translateY(0); }
.shimmer-text {
  background: linear-gradient(90deg, #fff 0%, #fbbf24 50%, #fff 100%);
  background-size: 200% auto; color: transparent; -webkit-background-clip: text; background-clip: text;
  animation: shine 3s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* 两侧切换按钮 */
.carousel-controls { display: flex; gap: 40px; margin-top: 40px; z-index: 10; }
.nav-btn {
  width: 56px; height: 56px; border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.4); background: rgba(0,0,0,0.3); backdrop-filter: blur(8px);
  color: white; font-size: 24px; display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.nav-btn:hover:not(:disabled) { background: rgba(255, 255, 255, 0.3); transform: scale(1.15); box-shadow: 0 0 20px rgba(255,255,255,0.4);}
.nav-btn:disabled { opacity: 0.2; cursor: not-allowed; }

.custom-inputs-center { display: flex; flex-direction: column; gap: 14px; margin-top: 24px; width: 100%; max-width: 400px; z-index: 10;}
:deep(.custom-name-input .el-input__inner) { text-align: center; font-weight: bold; font-size: 16px; }

/* 🌟 ==================== 阶段二：常规聊天界面 ==================== 🌟 */
.main-layout { width: 95vw; max-width: 1400px; height: 92dvh; border-radius: 24px; overflow: hidden; z-index: 10; position: relative; }
.sidebar { display: flex; flex-direction: column; padding: 24px 20px; transition: all 0.5s ease; border-right: 1px solid transparent;}
.mobile-close-btn, .sidebar-overlay { display: none; }
.sidebar-header { margin-bottom: 28px; }
.logo-wrapper { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.logo-img { width: 15%; height: 15%; object-fit: cover; }
.logo { font-size: 20px; font-weight: 700; margin: 0; letter-spacing: 1px; }

.uid-box { border-radius: 8px; display: inline-flex; align-items: center; overflow: hidden; cursor: pointer; border: 1px solid transparent; transition: all 0.2s; }
.uid-box:hover { transform: translateY(-1px); }
.uid-label { font-size: 12px; font-weight: 600; padding: 6px 10px; }
.uid-value { font-size: 13px; padding: 6px 12px; font-family: monospace; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.copy-icon { transition: color 0.2s; }

.new-chat-btn { width: 100%; border-radius: 12px; height: 46px; margin-bottom: 24px; font-weight: 600; font-size: 15px; display: flex; align-items: center; justify-content: center; gap: 8px; cursor: pointer; transition: all 0.2s; border: 1px solid transparent;}
.new-chat-btn:hover { transform: translateY(-1px); }

.history-list { flex: 1; overflow: hidden; }
.list-title { font-size: 13px; font-weight: 600; margin-bottom: 12px; letter-spacing: 1px; }

.quest-section { margin-bottom: 24px; }
.quest-card { background: rgba(99, 102, 241, 0.1) !important; border: 1px solid rgba(99, 102, 241, 0.3) !important; padding: 14px; border-radius: 12px; transition: all 0.3s; }
.quest-text { font-size: 13px; color: #e0e7ff; margin: 0; line-height: 1.5; }
.quest-text.success { color: #34d399; font-weight: bold; }

.history-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-radius: 12px; cursor: pointer; transition: all 0.2s; margin-bottom: 6px; border: 1px solid transparent;}
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
.chat-header { height: 70px; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; border-bottom: 1px solid transparent; z-index: 20; transition: all 0.5s ease; }
.mobile-menu-btn { display: none; }
.locked-status { display: flex; align-items: center; }
.status-badge { display: flex; align-items: center; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; white-space: nowrap; transition: all 0.5s ease; border: 1px solid transparent;}
.dot.connected { width: 8px; height: 8px; border-radius: 50%; margin-right: 10px; flex-shrink: 0; background: #34d399; box-shadow: 0 0 8px #34d399;}
.badge-text { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px; margin-left: 6px;}

.exit-btn { width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer; transition: all 0.2s; flex-shrink: 0; border: 1px solid transparent;}
.exit-btn:hover { transform: scale(1.05); }

.chat-main { flex: 1; overflow-y: auto; scroll-behavior: smooth; padding: 0; }
.chat-inner { max-width: 840px; margin: 0 auto; padding: 40px 24px; position: relative; }

/* 聊天内容区 */
.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 10vh; text-align: center; animation: fade-in-up 0.8s ease-out forwards; }
@keyframes fade-in-up { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
.empty-icon-wrapper { width: 88px; height: 88px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 24px; border: 3px solid transparent; transition: all 0.3s ease; }
.empty-avatar { width: 72px; height: 72px; border-radius: 50%; }
.empty-title { font-size: 24px; font-weight: 600; margin: 0 0 12px 0; }
.empty-subtext { font-size: 15px; margin: 0; max-width: 400px; line-height: 1.6; }

.message-wrapper { display: flex; margin-bottom: 36px; align-items: flex-start; }
.message-wrapper.user { flex-direction: row-reverse; }
.avatar-container { border-radius: 14px; padding: 2px; flex-shrink: 0; }
.avatar { width: 42px; height: 42px; border-radius: 12px; display: block; }
.message-wrapper.user .avatar-container { margin-left: 18px; }
.message-wrapper.assistant .avatar-container { margin-right: 18px; }

.bubble { max-width: 75%; padding: 16px 22px; font-size: 15px; line-height: 1.7; word-wrap: break-word; backdrop-filter: blur(10px); transition: background-color 0.5s ease; border: 1px solid transparent;}
.message-wrapper.user .bubble { border-radius: 20px 4px 20px 20px; }
.message-wrapper.assistant .bubble { border-radius: 4px 20px 20px 20px; }

.thinking-state { display: flex; align-items: center; gap: 8px; font-size: 14px; font-style: italic; opacity: 0.7;}
.is-loading { animation: rotating 2s linear infinite; }
@keyframes rotating { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.cursor-blink { display: inline-block; width: 8px; height: 16px; margin-left: 6px; vertical-align: text-bottom; animation: blink 1s step-end infinite; background: currentColor; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

.fixed-footer { position: absolute; bottom: 32px; left: 0; right: 0; display: flex; justify-content: center; padding: 0 24px; pointer-events: none; z-index: 20; }
.input-container { pointer-events: auto; width: 100%; max-width: 800px; display: flex; align-items: flex-end; border-radius: 24px; padding: 8px 16px 8px 20px; transition: all 0.3s; border: 1px solid transparent;}
.input-container:focus-within { transform: translateY(-2px); }

.send-btn { margin-left: 12px; margin-bottom: 0px; width: 40px; height: 40px; border-radius: 14px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; font-size: 18px; flex-shrink: 0; border: none; }
.send-btn:hover:not(:disabled) { transform: scale(1.05) rotate(-5deg); }
.send-btn:disabled { cursor: not-allowed; }

.loader-dots { display: flex; gap: 3px; }
.loader-dots span { width: 4px; height: 4px; background-color: #fff; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; }
.loader-dots span:nth-child(1) { animation-delay: -0.32s; }
.loader-dots span:nth-child(2) { animation-delay: -0.16s; }

/* Vue 过渡动画 */
.fade-hall-enter-active, .fade-hall-leave-active { transition: opacity 0.6s ease, transform 0.6s ease; }
.fade-hall-enter-from { opacity: 0; transform: scale(1.05); }
.fade-hall-leave-to { opacity: 0; transform: scale(0.95); }

.fade-transform-enter-active, .fade-transform-leave-active { transition: opacity 0.6s ease, transform 0.6s ease; transition-delay: 0.1s;}
.fade-transform-enter-from { opacity: 0; transform: translateY(20px); }
.fade-transform-leave-to { opacity: 0; transform: translateY(20px); }

/* 📱 手机端适配 */
@media (max-width: 768px) {
  /* 轮播在手机端需要调整 */
  .carousel-3d { width: 240px; height: 380px; }
  .carousel-card { padding: 30px 20px; }
  .card-avatar { width: 100px; height: 100px; margin-bottom: 20px; }
  .card-name { font-size: 22px; margin-bottom: 12px; }
  .card-desc { font-size: 14px; -webkit-line-clamp: 4; }
  .carousel-controls { margin-top: 30px; gap: 30px; }
  .top-exit-btn { top: 20px; left: 20px; width: 40px; height: 40px; font-size: 20px; }

  /* 聊天布局 */
  .main-layout { width: 100%; height: 100%; border-radius: 0; border: none; }
  .mobile-menu-btn { display: flex; align-items: center; justify-content: center; background: transparent; border: none; font-size: 24px; padding: 8px; margin-right: 12px; cursor: pointer; }
  .sidebar { position: fixed; left: 0; top: 0; bottom: 0; z-index: 1000; transform: translateX(-100%); width: 85vw !important; max-width: 320px; border-right: none;}
  .sidebar.mobile-open { transform: translateX(0); }
  .sidebar-overlay { display: block; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 999; }
  .mobile-close-btn { display: flex; position: absolute; right: 16px; top: 16px; font-size: 24px; cursor: pointer; }
  .chat-header { padding: 10px 16px; height: auto; min-height: 64px; }
  .mobile-hide { display: none !important; }
  .chat-inner { padding: 20px 16px; }
  .bubble { max-width: 85%; padding: 12px 16px; }
  .message-wrapper.user .avatar-container { margin-left: 10px; }
  .message-wrapper.assistant .avatar-container { margin-right: 10px; }
  .fixed-footer { bottom: 16px; padding: 0 16px; }
  .input-container { border-radius: 20px; padding: 6px 12px 6px 16px; }
}
</style>
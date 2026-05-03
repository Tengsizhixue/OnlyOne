<template>
  <!-- 最外层容器，动态绑定主题 class，控制全局配色 -->
  <div class="app-wrapper" :class="themeClass">

    <!-- ================= 【修复 1】：独立出背景图片层，平滑预加载防闪屏 ================= -->
    <div class="bg-image-layer" :style="customBgStyle" :class="{ 'show-bg': !showLanding && hasCustomBg }"></div>

    <!-- 🚀 全局动态极光流体背景 (在没有静态壁纸时显示) 🚀 -->
    <div class="dynamic-bg" :class="{ 'hide-bg': !showLanding && hasCustomBg }">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="orb orb-4"></div>
      <!-- 添加一层细腻的噪点纹理，提升高级质感 -->
      <div class="noise-overlay"></div>
    </div>

    <!-- 合并路由动画，模式设置为 out-in，确保 DOM 节点平稳替换 -->
    <transition name="fade-transform" mode="out-in">

      <!-- ================= 欢迎首页 (Landing Page) ================= -->
      <div v-if="showLanding" class="landing-page" key="landing">
        <el-scrollbar class="landing-scrollbar">
          <div class="landing-content glass-panel shadow-2xl floating-panel">
            <div class="landing-header">
              <div class="landing-icon pulse-icon">
                <img src="https://api.dicebear.com/9.x/bottts-neutral/svg?seed=AI" alt="AI Logo" class="landing-img" />
              </div>
              <h1 class="landing-title">正在开发，未完成</h1>
            </div>

            <div class="features-grid">
              <div class="feature-card glass-card hover-lift">
                <el-icon class="feature-icon"><User /></el-icon>
                <h3>角色丰富</h3>
                <p>这次的每个人物我都设计了特殊问答，问对问题会带有独特身份码</p>
              </div>
              <div class="feature-card glass-card hover-lift">
                <el-icon class="feature-icon"><ColdDrink /></el-icon>
                <h3>特殊会话</h3>
                <p>我会把以前我没删掉并且也没发过的内容放进特殊会话里</p>
              </div>
              <div class="feature-card glass-card hover-lift">
                <el-icon class="feature-icon"><Sugar /></el-icon>
                <h3>ui优化</h3>
                <p>换了个前端，这次的ui设计会比上次稍微好看些</p>
              </div>
            </div>

            <div class="scenario-section">
              <h3 class="scenario-title">我的一些想法</h3>
              <div class="scenario-tags">
                <span class="scenario-tag">后面不一定更</span>
                <span class="scenario-tag">太耗时间</span>
                <span class="scenario-tag">没什么更好的想法</span>
                <span class="scenario-tag">功能多了代码太复杂</span>
                <span class="scenario-tag">没什么能分享的</span>
              </div>
            </div>

            <button class="enter-btn shimmer-btn" @click="enterChat">
              <span class="btn-text">打开交流界面</span>
              <el-icon class="enter-icon"><ArrowRight /></el-icon>
            </button>
          </div>
        </el-scrollbar>
      </div>

      <!-- ================= 聊天主界面 ================= -->
      <el-container v-else class="main-layout glass-panel shadow-2xl" key="chat">

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
              <el-select v-model="roleConfig.role_type" placeholder="选择伙伴" class="glass-select" style="width: 130px">
                <el-option label="自定义" value="自定义" />
                <el-option label="誊思致雪" value="誊思致雪" />
                <el-option label="薇尔莉特" value="薇尔莉特" />
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
                当前连接: <span class="badge-text">{{ roleConfig.name }}</span>
              </div>
              <span class="lock-tip mobile-hide"><el-icon><Lock /></el-icon> 记忆已锁定，需新建以更改</span>
            </div>

            <button class="exit-btn" @click="showLanding = true" title="返回首页">
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
                  <el-avatar :src="getCurrentRoleConfig().avatar" class="empty-avatar" />
                </div>
                <h3 class="empty-title">{{ getCurrentRoleConfig().welcomeTitle }}</h3>
                <p class="empty-subtext">{{ getCurrentRoleConfig().welcomeText }}</p>
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
import { ref, reactive, onMounted, nextTick, watch, computed } from 'vue'
import {
  Plus,
  Delete,
  Position,
  Lock,
  DocumentCopy,
  MagicStick,
  ArrowRight,
  ChatLineRound,
  CoffeeCup,
  House,
  User,
  Cloudy,
  Lightning,
  Menu,
  Close,
  ColdDrink, Sugar
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const showLanding = ref(true)
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

const USER_AVATAR = "https://api.dicebear.com/9.x/fun-emoji/svg?backgroundColor=fcbc34,059ff2&backgroundType=gradientLinear&seed=Emery"
const DEFAULT_AI_AVATAR = "https://api.dicebear.com/9.x/bottts-neutral/svg?seed=AI"
const VIOLET_AVATAR = "https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/IMG_20260426_121950.png"
const TENGSI_AVATAR = "https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/99525941faa37d77f54de15e9a0e3b8a.jpg"

// ==================== 角色配置中心 ====================
const ROLE_CONFIGS = {
  '薇尔莉特': {
    name: '薇尔莉特',
    nature: '温柔优雅的自动手记人偶',
    welcomeTitle: '你好，我是薇尔莉特',
    welcomeText: '曾经少佐说，要活下去，要自由地活下去。但我之前一直不知道那是什么意思，我终于知道，"我爱你"是一种想和对方在一起、想让对方幸福的心情',
    avatar: VIOLET_AVATAR
  },
  '誊思致雪': {
    name: '誊思致雪',
    nature: '神秘的替身使者',
    welcomeTitle: '很久不见，我叫誊思致雪',
    welcomeText: '你问我是谁？...我也不知道，我只是一个替身',
    avatar: TENGSI_AVATAR
  },
  '自定义': {
    name: '李蓝宝',
    nature: '幽默风趣',
    welcomeTitle: '你好，我是李蓝宝',
    welcomeText: '我是自定义角色，不代表任何人物，你可以随意修改我的性格与名称。我只有一个特殊设定：李红宝是我牢弟，关于他的问题你可以问我',
    avatar: DEFAULT_AI_AVATAR
  }
}


// 获取当前角色的配置
const getCurrentRoleConfig = () => {
  return ROLE_CONFIGS[roleConfig.role_type] || ROLE_CONFIGS['自定义']
}

// ==================== 动态计算全局主题类名 ====================
const themeClass = computed(() => {
  if (showLanding.value) return 'theme-landing'
  if (roleConfig.role_type === '薇尔莉特') return 'theme-violet'
  if (roleConfig.role_type === '誊思致雪') return 'theme-snow'
  return 'theme-default'
})

// 控制是否具有需要壁纸的特殊角色
const hasCustomBg = computed(() => {
  return roleConfig.role_type === '薇尔莉特' || roleConfig.role_type === '誊思致雪'
})

// 预加载配置好对应的壁纸，防闪现
const customBgStyle = computed(() => {
  if (roleConfig.role_type === '薇尔莉特') {
    return { backgroundImage: `url('https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=2000&q=80')` }
  } else if (roleConfig.role_type === '誊思致雪') {
    return { backgroundImage: `url('https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/1118416.jpg')` }
  }
  return {}
})

function generateUid() {
  const newUid = Math.random().toString(36).substring(2, 10)
  localStorage.setItem('chat_uid', newUid)
  return newUid
}

const enterChat = () => {
  showLanding.value = false
  fetchSessions()
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

const formatText = (text) => {
  if (!text) return ''
  return text.replace(/\n/g, '<br/>')
}

onMounted(() => {})

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
    roleConfig.name = savedName

    roleConfig.nature = data.nature || '系统内置设定'

    if (savedName === '薇尔莉特') roleConfig.role_type = '薇尔莉特'
    else if (savedName === '誊思致雪') roleConfig.role_type = '誊思致雪'
    else roleConfig.role_type = '自定义'

    const currentAiAvatar = getCurrentRoleConfig().avatar

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
  const defaultConfig = ROLE_CONFIGS['自定义']
  roleConfig.name = defaultConfig.name
  roleConfig.nature = defaultConfig.nature
  isMobileMenuOpen.value = false
}

watch(() => roleConfig.role_type, (newVal) => {
  const config = ROLE_CONFIGS[newVal]
  if (config) {
    roleConfig.name = config.name
    roleConfig.nature = config.nature
  }
})

const recoverHistory = async () => {
  const targetUid = recoverUid.value.trim()
  if (targetUid.length !== 8) {
    return ElMessage.warning("请输入完整、正确的8位身份码")
  }

  try {
    const res = await fetch(`/api/sessions?uid=${targetUid}`)
    if (!res.ok) throw new Error("请求失败")
    const data = await res.json()

    if (data.length === 0) {
      return ElMessage.warning("未找到该身份码的记忆痕迹，请检查是否输入正确")
    }

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
    type: 'warning',
    confirmButtonText: '确定抹除',
    cancelButtonText: '再想一下'
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
  if (!e.shiftKey) {
    sendMessage()
  } else {
    inputText.value += '\n'
  }
}

const sendMessage = async () => {
  if (!inputText.value.trim() || isGenerating.value) return

  const userText = inputText.value.trim()
  inputText.value = ''

  if (!currentSessionId.value) {
    const now = new Date()
    const pad = n => n.toString().padStart(2, '0')
    currentSessionId.value = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}_${pad(now.getHours())}-${pad(now.getMinutes())}-${pad(now.getSeconds())}`
  }

  messages.value.push({ role: 'user', content: userText, avatar: USER_AVATAR })
  scrollToBottom()

  const aiAvatar = getCurrentRoleConfig().avatar
  messages.value.push({ role: 'assistant', content: '', avatar: aiAvatar })
  isGenerating.value = true
  scrollToBottom()

  try {
    const response = await fetch(`/api/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/octet-stream'
      },
      body: JSON.stringify({
        uid: uid.value,
        session_id: currentSessionId.value,
        role_config: roleConfig,
        content: userText,
        user_avatar: USER_AVATAR,
        ai_avatar: aiAvatar
      })
    })

    if (!response.ok) throw new Error("服务端异常")

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')

    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value, { stream: true })
      messages.value[messages.value.length - 1].content += chunk
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

<style>
html, body, #app {
  margin: 0; padding: 0;
  height: 100dvh; width: 100vw;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  color: #334155;
  background-color: #0f172a;
}
</style>

<style scoped>
.app-wrapper {
  height: 100dvh; width: 100vw;
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
  background-color: #0f172a; /* 基础底色，防止透白 */
  transition: background-color 1s ease;
}

/* ==================== 🚀 背景图独立层 (防止闪屏核心) 🚀 ==================== */
.bg-image-layer {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background-size: cover; background-position: center; background-repeat: no-repeat;
  opacity: 0; z-index: 0; pointer-events: none;
  transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
.bg-image-layer.show-bg {
  opacity: 1;
}

.dynamic-bg {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  overflow: hidden; z-index: 0;
  transition: opacity 1.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.dynamic-bg.hide-bg {
  opacity: 0; /* 在有壁纸时淡出动态极光 */
}

.noise-overlay {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.04; z-index: 1; pointer-events: none;
}
.orb {
  position: absolute; border-radius: 50%;
  filter: blur(80px); opacity: 0.7;
  animation: aurora 20s infinite alternate ease-in-out;
  transition: background 1.5s ease;
  will-change: transform; /* 开启硬件加速，优化移动端极光渲染流畅度 */
}
.orb-1 { width: 50vw; height: 50vw; top: -10%; left: -10%; animation-duration: 25s; }
.orb-2 { width: 45vw; height: 45vw; bottom: -20%; right: -10%; animation-duration: 22s; animation-delay: -5s; }
.orb-3 { width: 35vw; height: 35vw; top: 40%; left: 60%; animation-duration: 28s; animation-delay: -10s; }
.orb-4 { width: 40vw; height: 40vw; bottom: 20%; left: -20%; animation-duration: 30s; animation-delay: -15s; }

@keyframes aurora {
  0% { transform: translate(0, 0) scale(1) rotate(0deg); }
  33% { transform: translate(15%, -10%) scale(1.1) rotate(45deg); }
  66% { transform: translate(-10%, 15%) scale(0.9) rotate(-30deg); }
  100% { transform: translate(5%, -5%) scale(1.15) rotate(15deg); }
}

/* ==================== 🎨 主题 1：自定义角色 (Default 聊天使用) ==================== */
/* 【重大修复】：从白色主题改为深色极光玻璃主题，彻底消除从首页进入时的违和感与强光闪屏 */
.theme-default .app-wrapper { background-color: #0f172a; }
.theme-default .orb-1 { background: #3b82f6; }
.theme-default .orb-2 { background: #8b5cf6; }
.theme-default .orb-3 { background: #06b6d4; }
.theme-default .orb-4 { background: #6366f1; }

.theme-default .main-layout.glass-panel {
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
.theme-default .chat-header { background-color: rgba(15, 23, 42, 0.4); border-bottom-color: rgba(255, 255, 255, 0.1); }
.theme-default .sidebar { background: rgba(15, 23, 42, 0.5); border-right-color: rgba(255, 255, 255, 0.1); }

.theme-default .logo, .theme-default .session-name, .theme-default .empty-title, .theme-default .list-title { color: #f8fafc; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
.theme-default .empty-subtext { color: #94a3b8; }

.theme-default .history-item:hover { background-color: rgba(255, 255, 255, 0.05); }
.theme-default .history-item.active { background-color: rgba(99, 102, 241, 0.2); border-color: rgba(99, 102, 241, 0.4); }
.theme-default .uid-box { background: rgba(0,0,0,0.3); border-color: rgba(255,255,255,0.1); }
.theme-default .uid-label { background: rgba(99, 102, 241, 0.6); color: #fff; }
.theme-default .uid-value { color: #e2e8f0; }
.theme-default .new-chat-btn { background: rgba(99, 102, 241, 0.15); border-color: rgba(99, 102, 241, 0.3); color: #c7d2fe; }
.theme-default .new-chat-btn:hover { background: rgba(99, 102, 241, 0.3); }

.theme-default .empty-icon-wrapper { background: rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.2); }
.theme-default .highlight-text { color: #a5b4fc; text-shadow: 0 0 10px rgba(99,102,241,0.3); }
.theme-default .status-badge { background-color: rgba(0, 0, 0, 0.4); color: #a5b4fc; border-color: rgba(99, 102, 241, 0.3); }
.theme-default .lock-tip { color: #94a3b8; }
.theme-default .exit-btn { background: rgba(0, 0, 0, 0.3); color: #cbd5e1; border-color: rgba(255, 255, 255, 0.15); }

.theme-default .input-container { background: rgba(15, 23, 42, 0.8); border-color: rgba(99, 102, 241, 0.3); }
.theme-default .input-container:focus-within { background: rgba(15, 23, 42, 0.95); border-color: rgba(99, 102, 241, 0.6); box-shadow: 0 15px 40px rgba(99, 102, 241, 0.2); }
.theme-default :deep(.glass-textarea .el-textarea__inner) { color: #f8fafc; }
.theme-default :deep(.glass-textarea .el-textarea__inner::placeholder) { color: #64748b; }
.theme-default .send-btn { background: #6366f1; }
.theme-default .send-btn:hover:not(:disabled) { background: #4f46e5; }

.theme-default .message-wrapper.user .bubble { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: #ffffff; border-color: transparent;}
.theme-default .message-wrapper.assistant .bubble { background-color: rgba(30, 41, 59, 0.8); border-color: rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0,0,0,0.2); color: #f8fafc; }

/* 🎨 主题 2：雪之主题 (Tengsi) - 冰雪剔透风格 */
.theme-snow .main-layout.glass-panel {
  background: rgba(255, 255, 255, 0.25) !important;
  backdrop-filter: blur(2px) !important;
  -webkit-backdrop-filter: blur(2px) !important;
  border-color: rgba(255, 255, 255, 0.6) !important;
  box-shadow: 0 25px 50px -12px rgba(125, 211, 252, 0.3);
}
.theme-snow .chat-header { background-color: rgba(255, 255, 255, 0.2); border-bottom-color: rgba(255, 255, 255, 0.4); }
.theme-snow .sidebar { background: rgba(240, 249, 255, 0.4); border-right-color: rgba(255, 255, 255, 0.5); }

.theme-snow .logo, .theme-snow .session-name, .theme-snow .empty-title, .theme-snow .list-title { color: #0f172a; text-shadow: 0 1px 3px rgba(255,255,255,0.9); }
.theme-snow .empty-subtext { color: #334155; text-shadow: 0 1px 2px rgba(255,255,255,0.9); }

.theme-snow .history-item:hover { background-color: rgba(255, 255, 255, 0.4); }
.theme-snow .history-item.active { background-color: rgba(255, 255, 255, 0.7); border-color: rgba(255, 255, 255, 0.9); }
.theme-snow .uid-box { background: rgba(255,255,255,0.6); border-color: rgba(255,255,255,0.8); }
.theme-snow .uid-label { background: rgba(56, 189, 248, 0.7); color: #fff; }
.theme-snow .uid-value { color: #0f172a; }
.theme-snow .new-chat-btn { background: rgba(255, 255, 255, 0.7); border-color: rgba(255, 255, 255, 0.9); color: #0284c7; }
.theme-snow .new-chat-btn:hover { background: rgba(255, 255, 255, 0.9); }

.theme-snow .empty-icon-wrapper { background: rgba(255, 255, 255, 0.5); border-color: rgba(255, 255, 255, 0.8); }
.theme-snow .highlight-text { color: #0284c7; text-shadow: 0 0 10px rgba(255,255,255,0.8); }
.theme-snow .status-badge { background-color: rgba(255, 255, 255, 0.7); color: #0369a1; border-color: rgba(255, 255, 255, 0.9); }
.theme-snow .lock-tip { color: #334155; text-shadow: 0 1px 2px rgba(255,255,255,0.9); }
.theme-snow .exit-btn { background: rgba(255, 255, 255, 0.6); color: #0f172a; border-color: rgba(255, 255, 255, 0.8); }

.theme-snow .input-container { background: rgba(255, 255, 255, 0.75); border-color: rgba(255, 255, 255, 0.9); }
.theme-snow .input-container:focus-within { background: rgba(255, 255, 255, 0.95); border-color: #38bdf8; box-shadow: 0 15px 40px rgba(56, 189, 248, 0.2); }
.theme-snow :deep(.glass-textarea .el-textarea__inner) { color: #0f172a; }
.theme-snow :deep(.glass-textarea .el-textarea__inner::placeholder) { color: #64748b; }
.theme-snow .send-btn { background: #38bdf8; }
.theme-snow .send-btn:hover:not(:disabled) { background: #0284c7; }

.theme-snow .message-wrapper.user .bubble { background: linear-gradient(135deg, #7dd3fc 0%, #0284c7 100%); color: #ffffff; border-color: transparent;}
.theme-snow .message-wrapper.assistant .bubble { background-color: rgba(255, 255, 255, 0.85); border-color: rgba(255, 255, 255, 0.9); box-shadow: 0 4px 20px rgba(56, 189, 248, 0.15); color: #0f172a; }

/* 🎨 主题 3：深色极透主题 (Landing 首页使用) */
.theme-landing .app-wrapper { background-color: #0f172a; }
.theme-landing .orb-1 { background: #3b82f6; }
.theme-landing .orb-2 { background: #8b5cf6; }
.theme-landing .orb-3 { background: #06b6d4; }
.theme-landing .orb-4 { background: #6366f1; }

.theme-landing .landing-content {
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
.theme-landing .landing-title,
.theme-landing .feature-card h3,
.theme-landing .scenario-title { color: #f8fafc; }
.theme-landing .landing-subtitle,
.theme-landing .feature-card p { color: #cbd5e1; }

.theme-landing .feature-card { background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.1); }
.theme-landing .feature-card:hover { background: rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.2); }
.theme-landing .scenario-tag { background: rgba(255, 255, 255, 0.1); color: #a5b4fc; border-color: rgba(255, 255, 255, 0.15); }
.theme-landing .scenario-tag:hover { background: rgba(99, 102, 241, 0.4); color: #ffffff; }

/* 🎨 主题 4：紫罗兰专属主题 (Violet) */
.theme-violet .main-layout.glass-panel {
  background: rgba(46, 22, 84, 0.4) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border-color: rgba(167, 139, 250, 0.3) !important;
  box-shadow: 0 25px 50px -12px rgba(76, 29, 149, 0.6);
}
.theme-violet .chat-header { background-color: rgba(46, 22, 84, 0.3); border-bottom-color: rgba(167, 139, 250, 0.2); }
.theme-violet .sidebar { background: rgba(23, 11, 43, 0.6); border-right-color: rgba(167, 139, 250, 0.2); }

.theme-violet .logo, .theme-violet .session-name, .theme-violet .empty-title, .theme-violet .list-title { color: #f8fafc; }
.theme-violet .empty-subtext { color: #e2e8f0; }

.theme-violet .history-item:hover { background-color: rgba(255, 255, 255, 0.1); }
.theme-violet .history-item.active { background-color: rgba(139, 92, 246, 0.35); border-color: rgba(139, 92, 246, 0.5); }
.theme-violet .uid-box { background: rgba(0,0,0,0.3); border-color: rgba(255,255,255,0.1); }
.theme-violet .uid-label { background: rgba(139, 92, 246, 0.5); color: #fff; }
.theme-violet .uid-value { color: #e2e8f0; }
.theme-violet .new-chat-btn { background: rgba(139, 92, 246, 0.2); border-color: rgba(139, 92, 246, 0.4); color: #ddd6fe; }
.theme-violet .new-chat-btn:hover { background: rgba(139, 92, 246, 0.4); }

.theme-violet .empty-icon-wrapper { background: rgba(255, 255, 255, 0.15); border-color: rgba(255, 255, 255, 0.3); }
.theme-violet .highlight-text { color: #e0e7ff; text-shadow: 0 0 10px rgba(167,139,250,0.5); }
.theme-violet .status-badge { background-color: rgba(0, 0, 0, 0.5); color: #c4b5fd; border-color: rgba(139, 92, 246, 0.3); }
.theme-violet .lock-tip { color: #cbd5e1; }
.theme-violet .exit-btn { background: rgba(0, 0, 0, 0.3); color: #cbd5e1; border-color: rgba(255, 255, 255, 0.2); }

.theme-violet .input-container { background: rgba(23, 11, 43, 0.7); border-color: rgba(139, 92, 246, 0.4); }
.theme-violet .input-container:focus-within { background: rgba(23, 11, 43, 0.9); border-color: rgba(167, 139, 250, 0.6); box-shadow: 0 15px 40px rgba(109, 40, 217, 0.25); }
.theme-violet :deep(.glass-textarea .el-textarea__inner) { color: #f8fafc; }
.theme-violet :deep(.glass-textarea .el-textarea__inner::placeholder) { color: #94a3b8; }
.theme-violet .send-btn { background: #8b5cf6; }
.theme-violet .send-btn:hover:not(:disabled) { background: #7c3aed; }

.theme-violet .message-wrapper.user .bubble { background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); border-color: transparent;}
.theme-violet .message-wrapper.assistant .bubble { background-color: rgba(255, 255, 255, 0.9); border-color: rgba(139, 92, 246, 0.4); box-shadow: 0 4px 20px rgba(109, 40, 217, 0.15); }


/* ==================== 首页 (Landing Page) ==================== */
.landing-page {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  display: flex; align-items: center; justify-content: center;
  z-index: 100; overflow: hidden;
}
.landing-scrollbar { height: 100%; width: 100%; z-index: 10; }
:deep(.landing-scrollbar .el-scrollbar__wrap) { display: flex; align-items: center; justify-content: center; }

.floating-panel { animation: float-panel 6s ease-in-out infinite; }
@keyframes float-panel { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }

.landing-content {
  text-align: center; padding: 50px 60px; border-radius: 30px;
  max-width: 800px; margin: 40px auto; transition: all 0.6s ease;
}
.landing-header { margin-bottom: 40px; }

.pulse-icon { animation: pulse-ring 2.5s infinite cubic-bezier(0.215, 0.61, 0.355, 1); }
@keyframes pulse-ring { 0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); } 70% { box-shadow: 0 0 0 20px rgba(99, 102, 241, 0); } 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); } }

.landing-icon {
  font-size: 54px; color: #6366f1; margin-bottom: 20px; background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto;
  overflow: hidden;
}
.landing-img { width: 100%; height: 100%; object-fit: contain; }

.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 40px; }
.feature-card { padding: 24px 20px; border-radius: 20px; text-align: center; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: default; }
.hover-lift:hover { transform: translateY(-8px) scale(1.02); }
.feature-icon { font-size: 28px; color: #6366f1; margin-bottom: 16px; transition: transform 0.3s; }
.hover-lift:hover .feature-icon { transform: scale(1.2); }
.feature-card h3 { font-size: 16px; font-weight: 700; margin: 0 0 8px 0; transition: color 0.6s ease; }
.feature-card p { font-size: 13px; margin: 0; line-height: 1.5; transition: color 0.6s ease; }

.scenario-section { margin-bottom: 40px; text-align: center; }
.scenario-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; letter-spacing: 1px; transition: color 0.6s ease; }
.scenario-tags { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
.scenario-tag { padding: 8px 16px; border-radius: 20px; font-size: 13px; transition: all 0.2s; box-shadow: 0 2px 6px rgba(0,0,0,0.02); cursor: default; }
.scenario-tag:hover { transform: scale(1.05); }

.shimmer-btn {
  position: relative; overflow: hidden; background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: white; border: none; padding: 16px 40px; border-radius: 50px; font-size: 16px; font-weight: 600; cursor: pointer;
  display: inline-flex; align-items: center; gap: 12px; transition: all 0.3s; box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
}
.shimmer-btn::after {
  content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
  background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0) 100%);
  transform: skewX(-20deg); animation: shimmer 3s infinite;
}
.shimmer-btn:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 15px 30px rgba(99, 102, 241, 0.4); }
.enter-icon { transition: transform 0.3s; }
.shimmer-btn:hover .enter-icon { transform: translateX(6px); }

/* ==================== 玻璃拟态基础 (Glassmorphism) ==================== */
/* 修复手机端过度消耗 GPU 的问题：限制 transition，取消 will-change 的滥用 */
.glass-panel {
  background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.6);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.glass-card { background: rgba(255, 255, 255, 0.5); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.7); }

/* 主题适配的输入框样式 */
:deep(.glass-select .el-input__wrapper),
:deep(.glass-input .el-input__wrapper),
:deep(.recover-input .el-input__wrapper) {
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.85);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05), 0 0 0 2px rgba(99, 102, 241, 0.35) inset;
  padding: 4px 12px;
}
:deep(.el-input__inner) { color: #1e293b; }
:deep(.glass-input .el-input__inner::placeholder),
:deep(.glass-textarea .el-textarea__inner::placeholder) {
  color: #64748b;
}

.theme-snow :deep(.glass-select .el-input__wrapper),
.theme-snow :deep(.glass-input .el-input__wrapper),
.theme-snow :deep(.recover-input .el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.85);
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.5) inset;
}
.theme-snow :deep(.el-input__inner) { color: #0f172a; }

.theme-violet :deep(.glass-select .el-input__wrapper),
.theme-violet :deep(.glass-input .el-input__wrapper),
.theme-violet :deep(.recover-input .el-input__wrapper),
.theme-default :deep(.glass-select .el-input__wrapper),
.theme-default :deep(.glass-input .el-input__wrapper),
.theme-default :deep(.recover-input .el-input__wrapper) {
  background-color: rgba(0, 0, 0, 0.5);
  box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.5) inset;
}
.theme-violet :deep(.el-input__inner),
.theme-default :deep(.el-input__inner) { color: #f8fafc; }


/* ==================== 聊天主框架 ==================== */
.main-layout { width: 95vw; max-width: 1400px; height: 92dvh; border-radius: 24px; overflow: hidden; z-index: 10; position: relative; }

/* ---------------- 左侧边栏 ---------------- */
.sidebar { background: rgba(248, 250, 252, 0.5); border-right: 1px solid rgba(255, 255, 255, 0.6); display: flex; flex-direction: column; padding: 24px 20px; transition: all 0.5s ease; }
.mobile-close-btn { display: none; }
.sidebar-overlay { display: none; }
.sidebar-header { margin-bottom: 28px; }
.logo-wrapper { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.logo-img { width: 15%; height: 15%; object-fit: cover; }
.logo { font-size: 20px; font-weight: 700; color: #1e293b; margin: 0; letter-spacing: 1px; }

.uid-box { background: rgba(255, 255, 255, 0.7); border-radius: 8px; display: inline-flex; align-items: center; overflow: hidden; cursor: pointer; border: 1px solid rgba(255, 255, 255, 0.9); transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
.uid-box:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.uid-label { background: #e0e7ff; color: #4f46e5; font-size: 12px; font-weight: 600; padding: 6px 10px; }
.uid-value { font-size: 13px; color: #475569; padding: 6px 12px; font-family: monospace; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.copy-icon { color: #94a3b8; transition: color 0.2s; }
.uid-box:hover .copy-icon { color: #6366f1; }

.new-chat-btn { width: 100%; border-radius: 12px; height: 46px; margin-bottom: 24px; background: #ffffff; border: 1px solid rgba(255, 255, 255, 0.9); color: #4f46e5; font-weight: 600; font-size: 15px; display: flex; align-items: center; justify-content: center; gap: 8px; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03); }
.new-chat-btn:hover { background: #eef2ff; transform: translateY(-1px); box-shadow: 0 6px 15px rgba(99, 102, 241, 0.1); }

.history-list { flex: 1; overflow: hidden; }
.list-title { font-size: 13px; font-weight: 600; color: #94a3b8; margin-bottom: 12px; letter-spacing: 1px; }
.history-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-radius: 12px; cursor: pointer; transition: all 0.2s; margin-bottom: 6px; border: 1px solid transparent; }
.history-item:hover { background-color: rgba(255, 255, 255, 0.6); }
.history-item.active { background-color: #ffffff; border-color: rgba(255,255,255,0.9); box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
.session-info { display: flex; flex-direction: column; overflow: hidden; }
.session-name { font-size: 14px; font-weight: 600; color: #334155; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.active .session-name { color: #6366f1; }
.session-time { font-size: 12px; color: #94a3b8; margin-top: 4px; }

.delete-btn-wrapper { opacity: 0; display: flex; align-items: center; justify-content: center; width: 30px; height: 30px; border-radius: 8px; transition: all 0.2s; }
.delete-btn-wrapper:hover { background-color: #fee2e2; }
.delete-icon { color: #f43f5e; font-size: 15px; }
.history-item:hover .delete-btn-wrapper { opacity: 1; }

.sidebar-footer { margin-top: 24px; }
:deep(.recover-input .el-input__wrapper) { border-radius: 10px 0 0 10px; }
:deep(.recover-input .el-input-group__append) { border-radius: 0 10px 10px 0; background-color: #ffffff; color: #64748b; box-shadow: 0 0 0 1px rgba(255,255,255,0.8) inset; border-left: none; font-weight: 600; }
.theme-snow :deep(.recover-input .el-input-group__append) { background-color: rgba(56, 189, 248, 0.6); color: #fff; }
.theme-violet :deep(.recover-input .el-input-group__append),
.theme-default :deep(.recover-input .el-input-group__append) { background-color: rgba(139, 92, 246, 0.4); color: #fff; }

/* ---------------- 右侧主区域 ---------------- */
.chat-container { display: flex; flex-direction: column; position: relative; background: transparent; }

.chat-header { height: 70px; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; background-color: rgba(255, 255, 255, 0.3); border-bottom: 1px solid rgba(255, 255, 255, 0.4); z-index: 20; transition: all 0.5s ease; }
.mobile-menu-btn { display: none; }
.role-settings { display: flex; gap: 12px; }
.custom-inputs { display: flex; gap: 12px; }
.locked-status { display: flex; align-items: center; }
.status-badge { display: flex; align-items: center; background-color: rgba(255, 255, 255, 0.8); color: #4f46e5; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; box-shadow: 0 2px 10px rgba(0,0,0,0.03); white-space: nowrap; transition: all 0.5s ease; }
.dot.connected { width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; margin-right: 10px; box-shadow: 0 0 0 2px #d1fae5; flex-shrink: 0; }
.badge-text { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px; }
.lock-tip { font-size: 13px; color: #64748b; margin-left: 20px; display: flex; align-items: center; gap: 6px; }
.exit-btn { background: rgba(255,255,255,0.6); border: 1px solid rgba(255,255,255,0.8); width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; color: #475569; cursor: pointer; transition: all 0.2s; flex-shrink: 0; }
.exit-btn:hover { background: #ffffff; color: #4f46e5; transform: scale(1.05); }

.chat-main { flex: 1; overflow-y: auto; scroll-behavior: smooth; padding: 0; }
.chat-inner { max-width: 840px; margin: 0 auto; padding: 40px 24px; }

.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 15vh; text-align: center; }
.empty-icon-wrapper { background: rgba(255, 255, 255, 0.6); width: 88px; height: 88px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 3px solid rgba(255,255,255,0.8); transition: all 0.3s ease; }
.empty-avatar { width: 72px; height: 72px; border-radius: 50%; }
.empty-title { font-size: 24px; font-weight: 600; color: #1e293b; margin: 0 0 12px 0; }
.highlight-text { color: #6366f1; }
.empty-subtext { font-size: 15px; color: #64748b; margin: 0; max-width: 400px; line-height: 1.6; }

.message-wrapper { display: flex; margin-bottom: 36px; align-items: flex-start; }
.message-wrapper.user { flex-direction: row-reverse; }

.avatar-container { border-radius: 14px; padding: 2px; background: rgba(255,255,255,0.5); flex-shrink: 0; }
.avatar { background: none; width: 42px; height: 42px; border-radius: 12px; display: block; }
.message-wrapper.user .avatar-container { margin-left: 18px; }
.message-wrapper.assistant .avatar-container { margin-right: 18px; }

.bubble { max-width: 75%; padding: 16px 22px; font-size: 15px; line-height: 1.7; word-wrap: break-word; backdrop-filter: blur(10px); transition: background-color 0.5s ease; }

/* 用户气泡（右上角直角） */
.message-wrapper.user .bubble {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: #ffffff;
  border-color: transparent;
  border-radius: 20px 4px 20px 20px;
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
}
/* AI助手气泡（左上角直角） */
.message-wrapper.assistant .bubble {
  background-color: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.6);
  color: #0f172a;
  border-radius: 4px 20px 20px 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.cursor-blink { display: inline-block; width: 8px; height: 16px; background-color: #6366f1; margin-left: 6px; vertical-align: text-bottom; animation: blink 1s step-end infinite; }

.fixed-footer { position: absolute; bottom: 32px; left: 0; right: 0; display: flex; justify-content: center; padding: 0 24px; pointer-events: none; }
.input-container { pointer-events: auto; width: 100%; max-width: 800px; display: flex; align-items: flex-end; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 24px; padding: 8px 16px 8px 20px; transition: all 0.3s; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); }
.input-container:focus-within { background: rgba(255, 255, 255, 0.95); transform: translateY(-2px); box-shadow: 0 15px 40px rgba(99, 102, 241, 0.15); }

:deep(.glass-textarea .el-textarea__inner) {
  background: transparent !important; border: none !important; box-shadow: none !important;
  resize: none; font-size: 15px;
  padding: 8px 0 !important;
  color: #1e293b;
  line-height: 24px !important;
  min-height: 40px !important;
  display: flex; align-items: center;
}
.send-btn {
  margin-left: 12px; margin-bottom: 0px;
  background: #1e293b; color: white; border: none;
  width: 40px; height: 40px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; font-size: 18px; flex-shrink: 0;
}
.send-btn:hover:not(:disabled) { background: #6366f1; transform: scale(1.05) rotate(-5deg); }
.send-btn:disabled { background: rgba(226, 232, 240, 0.8); color: #94a3b8; cursor: not-allowed; }

/* ==================== 移动端响应式 ==================== */
@media (max-width: 768px) {
  .glass-panel {
    background: rgba(255, 255, 255, 0.35);
    -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px);
    /* 保留 translateZ 以支持硬件加速毛玻璃，但移除了卡顿的 will-change */
    transform: translateZ(0); -webkit-transform: translateZ(0);
  }

  .theme-violet .main-layout.glass-panel {
    background: rgba(46, 22, 84, 0.4) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    backdrop-filter: blur(12px) !important;
    transform: translateZ(0) !important;
    -webkit-transform: translateZ(0) !important;
  }

  /* 【修复 1】：强行为移动端的誊思致雪配置清晰的 2px 毛玻璃！ */
  .theme-snow .main-layout.glass-panel {
    background: rgba(255, 255, 255, 0.15) !important;
    -webkit-backdrop-filter: blur(2px) !important;
    backdrop-filter: blur(2px) !important;
    transform: translateZ(0) !important;
    -webkit-transform: translateZ(0) !important;
  }

  .theme-default .main-layout.glass-panel {
    transform: translateZ(0) !important;
    -webkit-transform: translateZ(0) !important;
  }

  .main-layout { width: 100%; height: 100%; border-radius: 0; border: none; }
  .mobile-menu-btn { display: flex; align-items: center; justify-content: center; background: transparent; border: none; font-size: 24px; color: #475569; padding: 8px; margin-right: 12px; cursor: pointer; }

  .theme-violet .mobile-menu-btn, .theme-landing .mobile-menu-btn, .theme-default .mobile-menu-btn { color: #f8fafc; }
  .theme-snow .mobile-menu-btn { color: #0f172a; text-shadow: 0 1px 2px rgba(255,255,255,0.9); }

  .sidebar { position: fixed; left: 0; top: 0; bottom: 0; z-index: 1000; transform: translateX(-100%); background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px); border-right: none; box-shadow: 10px 0 30px rgba(0,0,0,0.1); width: 85vw !important; max-width: 320px; }
  .theme-violet .sidebar { background: rgba(15, 23, 42, 0.95); }
  .theme-snow .sidebar { background: rgba(255, 255, 255, 0.85); }
  .theme-default .sidebar { background: rgba(15, 23, 42, 0.85); border-right: none; }
  .sidebar.mobile-open { transform: translateX(0); }
  .sidebar-overlay { display: block; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); z-index: 999; backdrop-filter: blur(4px); }
  .mobile-close-btn { display: flex; position: absolute; right: 16px; top: 16px; font-size: 24px; color: #64748b; cursor: pointer; }
  .chat-header { padding: 10px 16px; height: auto; min-height: 64px; background: rgba(255, 255, 255, 0.2); }

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

  :deep(.landing-scrollbar .el-scrollbar__wrap) { align-items: flex-start; }
  .landing-content { padding: 30px 20px; margin: 30px 20px 60px 20px; width: auto; border-radius: 24px; }
  .features-grid { grid-template-columns: 1fr; gap: 16px; }
  .landing-title { font-size: 28px; }
}

/* ==================== 路由平滑过渡动画 ==================== */
.fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.fade-transform-enter-active, .fade-transform-leave-active { transition: opacity 0.5s ease, transform 0.5s ease; }
.fade-transform-enter-from { opacity: 0; transform: scale(0.98) translateY(10px); }
.fade-transform-leave-to { opacity: 0; transform: scale(1.02) translateY(-10px); }

.loader-dots { display: flex; gap: 3px; }
.loader-dots span { width: 4px; height: 4px; background-color: #94a3b8; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; }
.loader-dots span:nth-child(1) { animation-delay: -0.32s; }
.loader-dots span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
</style>
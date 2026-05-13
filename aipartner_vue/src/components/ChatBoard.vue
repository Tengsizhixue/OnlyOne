<template>
  <el-container class="chat-container">
    <el-header class="chat-header">
      <button class="mobile-menu-btn" @click="$emit('open-mobile-menu')">
        <el-icon><Menu /></el-icon>
      </button>

      <div class="locked-status">
        <div class="status-badge">
          <span class="dot connected"></span>
          正在与 <span class="badge-text">{{ roleConfig.name || '李蓝宝' }}</span> 对话
        </div>
      </div>

      <button class="exit-btn" @click="$emit('back-to-hall')" title="返回角色选择">
         <el-icon><ArrowLeft /></el-icon>
      </button>
    </el-header>

    <el-main class="chat-main" ref="chatMainRef">
      <div class="chat-inner">

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
        <button class="send-btn" :class="{ 'is-loading': isGenerating }" @click="handleSend" :disabled="isGenerating || !inputText.trim()">
          <el-icon v-if="!isGenerating"><Position /></el-icon>
          <div v-else class="loader-dots"><span></span><span></span><span></span></div>
        </button>
      </div>
    </div>
  </el-container>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { Menu, ArrowLeft, Loading, Position } from '@element-plus/icons-vue'
import { getCurrentRoleConfig } from '../config/constants.js'

const props = defineProps({
  messages: Array,
  isGenerating: Boolean,
  roleConfig: Object
})

const emit = defineEmits(['open-mobile-menu', 'back-to-hall', 'send-message'])

const inputText = ref('')
const chatMainRef = ref(null)

const formatText = (text) => text ? text.replace(/\n/g, '<br/>') : ''
const getRoleInfo = () => getCurrentRoleConfig(props.roleConfig.role_type)

const scrollToBottom = async () => {
  await nextTick()
  if (chatMainRef.value) {
    const el = chatMainRef.value.$el || chatMainRef.value
    el.scrollTop = el.scrollHeight
  }
}

// 监听消息变化自动下拉到底部
watch(() => props.messages, () => {
  scrollToBottom()
}, { deep: true })

const handleEnter = (e) => {
  if (!e.shiftKey) handleSend()
  else inputText.value += '\n'
}

const handleSend = () => {
  if (!inputText.value.trim() || props.isGenerating) return
  emit('send-message', inputText.value.trim())
  inputText.value = ''
}
</script>

<style scoped>
.chat-container { display: flex; flex-direction: column; position: relative; background: transparent; }
.chat-header { height: 70px; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; border-bottom: 1px solid transparent; z-index: 20; transition: all 0.5s ease; }
.mobile-menu-btn { display: none; }
.locked-status { display: flex; align-items: center; }
.status-badge { display: flex; align-items: center; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; white-space: nowrap; transition: all 0.5s ease; border: 1px solid transparent;}
.dot.connected { width: 8px; height: 8px; border-radius: 50%; margin-right: 10px; flex-shrink: 0; background: #34d399; box-shadow: 0 0 8px #34d399;}
.badge-text { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px; margin-left: 6px;}
.exit-btn { width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; cursor: pointer; transition: all 0.2s; flex-shrink: 0; border: 1px solid transparent;}
.exit-btn:hover { transform: scale(1.05); }

.chat-main { flex: 1; overflow-y: auto; padding: 0; }
.chat-inner { max-width: 840px; margin: 0 auto; padding: 40px 24px; position: relative; }

.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 10vh; text-align: center; animation: fade-in-up 0.8s ease-out forwards; }
@keyframes fade-in-up { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
.empty-icon-wrapper { width: 88px; height: 88px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 24px; border: 3px solid transparent; transition: all 0.3s ease; }
.empty-avatar { width: 72px; height: 72px; border-radius: 50%; }
.empty-title { font-size: 24px; font-weight: 600; margin: 0 0 12px 0; }
.empty-subtext { font-size: 15px; margin: 0; max-width: 400px; line-height: 1.6; }

/* ================= 🌟 气泡 UI 重新设计 ================= */
.message-wrapper { display: flex; margin-bottom: 36px; align-items: flex-start; }
.message-wrapper.user { flex-direction: row-reverse; }
.avatar-container { flex-shrink: 0; }
.avatar { width: 42px; height: 42px; border-radius: 12px; display: block; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
.message-wrapper.user .avatar-container { margin-left: 16px; }
.message-wrapper.assistant .avatar-container { margin-right: 16px; }

/* 基础形状与毛玻璃特效 */
.bubble {
  max-width: 75%; padding: 14px 20px; font-size: 15px; line-height: 1.8; word-wrap: break-word;
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  transition: all 0.3s ease;
}
.message-wrapper.user .bubble { border-radius: 20px 4px 20px 20px; }
.message-wrapper.assistant .bubble { border-radius: 4px 20px 20px 20px; }

/* ================= 🌈 多主题毛玻璃气泡自适应适配 ================= */

/* 默认科技蓝主题 (李蓝宝/自定义) */
:global(.theme-default) .message-wrapper.user .bubble {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(79, 70, 229, 0.05)) !important;
  border: 1px solid rgba(99, 102, 241, 0.3) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
  color: #f8fafc !important;
}
:global(.theme-default) .message-wrapper.assistant .bubble {
  background: rgba(15, 23, 42, 0.5) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
  color: #e2e8f0 !important;
}

/* ❄️ 誊思致雪主题 (修复亮色系白底白字看不清的问题) */
:global(.theme-snow) .message-wrapper.user .bubble {
  background: linear-gradient(135deg, rgba(2, 132, 199, 0.15), rgba(125, 211, 252, 0.05)) !important;
  border: 1px solid rgba(56, 189, 248, 0.4) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
  color: #0f172a !important; /* 深色字体 */
  font-weight: 500;
}
:global(.theme-snow) .message-wrapper.assistant .bubble {
  background: rgba(255, 255, 255, 0.8) !important; /* 白色半透明底 */
  border: 1px solid rgba(255, 255, 255, 0.9) !important;
  box-shadow: 0 4px 20px rgba(56, 189, 248, 0.1) !important;
  color: #0f172a !important; /* 强制深色黑体文字！ */
  font-weight: 500;
}

/* 🌸 薇尔莉特主题 (紫色系) */
:global(.theme-violet) .message-wrapper.user .bubble {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(109, 40, 217, 0.05)) !important;
  border: 1px solid rgba(139, 92, 246, 0.3) !important;
  color: #f8fafc !important;
}
:global(.theme-violet) .message-wrapper.assistant .bubble {
  background: rgba(23, 11, 43, 0.5) !important;
  border: 1px solid rgba(167, 139, 250, 0.2) !important;
  color: #e2e8f0 !important;
}

/* 🎵 音乐助手主题 (粉色系) */
:global(.theme-music) .message-wrapper.user .bubble {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.15), rgba(190, 24, 93, 0.05)) !important;
  border: 1px solid rgba(244, 114, 182, 0.3) !important;
  color: #fdf2f8 !important;
}
:global(.theme-music) .message-wrapper.assistant .bubble {
  background: rgba(33, 10, 18, 0.5) !important;
  border: 1px solid rgba(244, 114, 182, 0.2) !important;
  color: #fbcfe8 !important;
}

/* ⚔️ 游戏助手主题 (黑金系) */
:global(.theme-game) .message-wrapper.user .bubble {
  background: linear-gradient(135deg, rgba(184, 142, 81, 0.15), rgba(145, 110, 60, 0.05)) !important;
  border: 1px solid rgba(184, 142, 81, 0.3) !important;
  color: #f5eedc !important;
}
:global(.theme-game) .message-wrapper.assistant .bubble {
  background: rgba(20, 12, 8, 0.6) !important;
  border: 1px solid rgba(184, 142, 81, 0.2) !important;
  color: #e8d7ba !important;
}

/* 🧠 深度思考指示器 */
:deep(.deep-thinking-badge) {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(90deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.05));
  border: 1px solid rgba(139, 92, 246, 0.4);
  border-radius: 20px;
  color: #c4b5fd;
  font-size: 13px;
  margin-bottom: 12px;
  animation: pulse-glow 2.5s infinite alternate ease-in-out;
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.1);
}

/* 适配亮色主题下深度思考的颜色 */
:global(.theme-snow) .deep-thinking-badge {
  background: linear-gradient(90deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.02)) !important;
  border-color: rgba(139, 92, 246, 0.3) !important;
  color: #6d28d9 !important;
  font-weight: 600;
}

:deep(.think-icon) {
  animation: float-spin 3s linear infinite;
  display: inline-block;
}
:deep(.think-text) {
  letter-spacing: 0.5px;
}

@keyframes pulse-glow {
  0% { box-shadow: 0 0 5px rgba(139, 92, 246, 0.1); border-color: rgba(139, 92, 246, 0.3); }
  100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.4); border-color: rgba(139, 92, 246, 0.6); }
}
@keyframes float-spin {
  0% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-2px) rotate(180deg); }
  100% { transform: translateY(0) rotate(360deg); }
}
/* ======================================================= */

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

@media (max-width: 768px) {
  .mobile-menu-btn { display: flex; align-items: center; justify-content: center; background: transparent; border: none; font-size: 24px; padding: 8px; margin-right: 12px; cursor: pointer; }
  .chat-header { padding: 10px 16px; height: auto; min-height: 64px; }
  .chat-inner { padding: 20px 16px; }
  .bubble { max-width: 85%; padding: 12px 16px; }
  .message-wrapper.user .avatar-container { margin-left: 10px; }
  .message-wrapper.assistant .avatar-container { margin-right: 10px; }
  .fixed-footer { bottom: 16px; padding: 0 16px; }
  .input-container { border-radius: 20px; padding: 6px 12px 6px 16px; }
}
</style>
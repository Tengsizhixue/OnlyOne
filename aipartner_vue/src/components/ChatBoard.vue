<template>
  <el-container class="chat-container">
    <el-header class="chat-header">
      <button class="mobile-menu-btn" @click="$emit('open-mobile-menu')">
        <el-icon><Menu /></el-icon>
      </button>

      <div class="locked-status">
        <div class="status-badge">
          <span class="dot connected"></span>
          正在与 <span class="badge-text">{{ roleConfig.name || '伙伴' }}</span> 对话
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

.chat-main { flex: 1; overflow-y: auto; scroll-behavior: smooth; padding: 0; }
.chat-inner { max-width: 840px; margin: 0 auto; padding: 40px 24px; position: relative; }

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
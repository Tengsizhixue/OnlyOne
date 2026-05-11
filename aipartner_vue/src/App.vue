<template>
  <div class="app-wrapper" :class="themeClass">

    <DynamicBackground
      :is-landing="route.name === 'landing'"
      :has-custom-bg="hasCustomBg"
      :custom-bg-style="customBgStyle"
    />

    <router-view v-slot="{ Component }">
      <transition name="fade-transform" mode="out-in">
        <component
          :is="Component"
          @update:roleType="currentRoleType = $event"
        />
      </transition>
    </router-view>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import DynamicBackground from './components/DynamicBackground.vue'
import { getCurrentRoleConfig } from './config/constants.js' // 💡 引入配置表

const route = useRoute()
const currentRoleType = ref('李蓝宝')

const themeClass = computed(() => {
  if (route.name === 'landing') return 'theme-landing'
  if (route.name === 'secret') return 'theme-violet'
  if (currentRoleType.value === '薇尔莉特') return 'theme-violet'
  if (currentRoleType.value === '誊思致雪') return 'theme-snow'
  if (currentRoleType.value === '音乐推荐助手') return 'theme-music'
  if (currentRoleType.value === '游戏聊天助手') return 'theme-game'
  return 'theme-default'
})

const hasCustomBg = computed(() => {
  return ['薇尔莉特', '誊思致雪', '音乐推荐助手', '游戏聊天助手'].includes(currentRoleType.value)
})

// 🌟 核心清理：不再需要又臭又长的 if-else，直接调用常量
const customBgStyle = computed(() => {
  const config = getCurrentRoleConfig(currentRoleType.value)
  if (config && config.bgUrl) {
    return {
      backgroundImage: `url('${config.bgUrl}')`,
      backgroundPosition: config.bgPosition
    }
  }
  return {}
})
</script>

<style>
/* (样式与之前完全保持一致) */
html, body, #app {
  margin: 0; padding: 0;
  height: 100dvh; width: 100vw;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  color: #334155;
  background-color: #0f172a;
}

.app-wrapper {
  height: 100dvh; width: 100vw;
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
  background-color: #0f172a;
  transition: background-color 1s ease;
}

.fade-transform-enter-active, .fade-transform-leave-active { transition: opacity 0.5s ease, transform 0.5s ease; }
.fade-transform-enter-from { opacity: 0; transform: scale(0.98) translateY(10px); }
.fade-transform-leave-to { opacity: 0; transform: scale(1.02) translateY(-10px); }

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
@keyframes shimmer { 0% { left: -100%; } 100% { left: 200%; } }

.pulse-icon { animation: pulse-ring 2.5s infinite cubic-bezier(0.215, 0.61, 0.355, 1); }
@keyframes pulse-ring { 0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); } 70% { box-shadow: 0 0 0 20px rgba(99, 102, 241, 0); } 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); } }

.glass-panel {
  background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.6); transition: opacity 0.5s ease, transform 0.5s ease;
}

.glass-select .el-input__wrapper,
.glass-input .el-input__wrapper,
.recover-input .el-input__wrapper {
  border-radius: 10px; padding: 4px 12px;
  background-color: rgba(255, 255, 255, 0.85);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05), 0 0 0 2px rgba(99, 102, 241, 0.35) inset;
}
.el-input__inner { color: #1e293b; }
.glass-input .el-input__inner::placeholder,
.glass-textarea .el-textarea__inner::placeholder { color: #64748b; }

.glass-textarea .el-textarea__inner {
  background: transparent !important; border: none !important; box-shadow: none !important;
  resize: none; font-size: 15px; padding: 8px 0 !important; color: #1e293b;
  line-height: 24px !important; min-height: 40px !important; display: flex; align-items: center;
}

.theme-default .app-wrapper { background-color: #0f172a; }
.theme-default .orb-1 { background: #3b82f6; }
.theme-default .orb-2 { background: #8b5cf6; }
.theme-default .orb-3 { background: #06b6d4; }
.theme-default .orb-4 { background: #6366f1; }

.theme-default .main-layout.glass-panel { background: rgba(15, 23, 42, 0.6) !important; backdrop-filter: blur(16px) !important; -webkit-backdrop-filter: blur(16px) !important; border-color: rgba(255, 255, 255, 0.1) !important; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
.theme-default .chat-header { background-color: rgba(15, 23, 42, 0.4); border-bottom-color: rgba(255, 255, 255, 0.1); }
.theme-default .sidebar { background: rgba(15, 23, 42, 0.5); border-right-color: rgba(255, 255, 255, 0.1); }
.theme-default .logo, .theme-default .session-name, .theme-default .empty-title, .theme-default .list-title { color: #f8fafc; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
.theme-default .empty-subtext { color: #94a3b8; }
.theme-default .history-item:hover { background-color: rgba(255, 255, 255, 0.05); }
.theme-default .history-item.active { background-color: rgba(99, 102, 241, 0.2); border-color: rgba(99, 102, 241, 0.4); }
.theme-default .uid-box { background: rgba(0,0,0,0.3); border-color: rgba(255,255,255,0.1); }
.theme-default .uid-label { background: rgba(99, 102, 241, 0.6); color: #fff; }
.theme-default .uid-value { color: #e2e8f0; }
.theme-default .new-chat-btn { background: rgba(99, 102, 241, 0.15); border-color: rgba(99, 102, 241, 0.3); color: #c7d2fe; box-shadow:none;}
.theme-default .new-chat-btn:hover { background: rgba(99, 102, 241, 0.3); }
.theme-default .empty-icon-wrapper { background: rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.2); }
.theme-default .highlight-text { color: #a5b4fc; text-shadow: 0 0 10px rgba(99,102,241,0.3); }
.theme-default .status-badge { background-color: rgba(0, 0, 0, 0.4); color: #a5b4fc; border-color: rgba(99, 102, 241, 0.3); }
.theme-default .lock-tip { color: #94a3b8; }
.theme-default .exit-btn { background: rgba(0, 0, 0, 0.3); color: #cbd5e1; border-color: rgba(255, 255, 255, 0.15); }
.theme-default .input-container { background: rgba(15, 23, 42, 0.8); border-color: rgba(99, 102, 241, 0.3); }
.theme-default .input-container:focus-within { background: rgba(15, 23, 42, 0.95); border-color: rgba(99, 102, 241, 0.6); box-shadow: 0 15px 40px rgba(99, 102, 241, 0.2); }
.theme-default .glass-textarea .el-textarea__inner { color: #f8fafc; }
.theme-default .glass-textarea .el-textarea__inner::placeholder { color: #64748b; }
.theme-default .send-btn { background: #6366f1; color: white; }
.theme-default .send-btn:hover:not(:disabled) { background: #4f46e5; }
.theme-default .message-wrapper.user .bubble { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: #ffffff; border-color: transparent;}
.theme-default .message-wrapper.assistant .bubble { background-color: rgba(30, 41, 59, 0.8); border-color: rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0,0,0,0.2); color: #f8fafc; }
.theme-default .glass-select .el-input__wrapper, .theme-default .glass-input .el-input__wrapper, .theme-default .recover-input .el-input__wrapper { background-color: rgba(0, 0, 0, 0.5); box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.5) inset; }
.theme-default .el-input__inner { color: #f8fafc; }
.theme-default .recover-input .el-input-group__append { background-color: rgba(139, 92, 246, 0.4); color: #fff; border: none;}

.theme-snow .main-layout.glass-panel { background: rgba(255, 255, 255, 0.25) !important; backdrop-filter: blur(2px) !important; -webkit-backdrop-filter: blur(2px) !important; border-color: rgba(255, 255, 255, 0.6) !important; box-shadow: 0 25px 50px -12px rgba(125, 211, 252, 0.3); }
.theme-snow .chat-header { background-color: rgba(255, 255, 255, 0.2); border-bottom-color: rgba(255, 255, 255, 0.4); }
.theme-snow .sidebar { background: rgba(240, 249, 255, 0.4); border-right-color: rgba(255, 255, 255, 0.5); }
.theme-snow .logo, .theme-snow .session-name, .theme-snow .empty-title, .theme-snow .list-title { color: #0f172a; text-shadow: 0 1px 3px rgba(255,255,255,0.9); }
.theme-snow .empty-subtext { color: #334155; text-shadow: 0 1px 2px rgba(255,255,255,0.9); }
.theme-snow .history-item:hover { background-color: rgba(255, 255, 255, 0.4); }
.theme-snow .history-item.active { background-color: rgba(255, 255, 255, 0.7); border-color: rgba(255, 255, 255, 0.9); box-shadow: 0 2px 10px rgba(0,0,0,0.02);}
.theme-snow .uid-box { background: rgba(255,255,255,0.6); border-color: rgba(255,255,255,0.8); }
.theme-snow .uid-label { background: rgba(56, 189, 248, 0.7); color: #fff; }
.theme-snow .uid-value { color: #0f172a; }
.theme-snow .new-chat-btn { background: rgba(255, 255, 255, 0.7); border-color: rgba(255, 255, 255, 0.9); color: #0284c7; box-shadow: 0 4px 10px rgba(0,0,0,0.03);}
.theme-snow .new-chat-btn:hover { background: rgba(255, 255, 255, 0.9); }
.theme-snow .empty-icon-wrapper { background: rgba(255, 255, 255, 0.5); border-color: rgba(255, 255, 255, 0.8); }
.theme-snow .status-badge { background-color: rgba(255, 255, 255, 0.7); color: #0369a1; border-color: rgba(255, 255, 255, 0.9); }
.theme-snow .lock-tip { color: #334155; text-shadow: 0 1px 2px rgba(255,255,255,0.9); }
.theme-snow .exit-btn { background: rgba(255, 255, 255, 0.6); color: #0f172a; border-color: rgba(255, 255, 255, 0.8); }
.theme-snow .input-container { background: rgba(255, 255, 255, 0.75); border-color: rgba(255, 255, 255, 0.9); }
.theme-snow .input-container:focus-within { background: rgba(255, 255, 255, 0.95); border-color: #38bdf8; box-shadow: 0 15px 40px rgba(56, 189, 248, 0.2); }
.theme-snow .glass-textarea .el-textarea__inner { color: #0f172a; }
.theme-snow .glass-textarea .el-textarea__inner::placeholder { color: #64748b; }
.theme-snow .send-btn { background: #38bdf8; color: white;}
.theme-snow .send-btn:hover:not(:disabled) { background: #0284c7; }
.theme-snow .message-wrapper.user .bubble { background: linear-gradient(135deg, #7dd3fc 0%, #0284c7 100%); color: #ffffff; border-color: transparent;}
.theme-snow .message-wrapper.assistant .bubble { background-color: rgba(255, 255, 255, 0.85); border-color: rgba(255, 255, 255, 0.9); box-shadow: 0 4px 20px rgba(56, 189, 248, 0.15); color: #0f172a; }
.theme-snow .glass-select .el-input__wrapper, .theme-snow .glass-input .el-input__wrapper, .theme-snow .recover-input .el-input__wrapper { background-color: rgba(255, 255, 255, 0.85); box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.5) inset; }
.theme-snow .el-input__inner { color: #0f172a; }
.theme-snow .recover-input .el-input-group__append { background-color: rgba(56, 189, 248, 0.6); color: #fff; border:none;}

.theme-landing .landing-content { background: rgba(15, 23, 42, 0.45); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-color: rgba(255, 255, 255, 0.15); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
.theme-landing .landing-title, .theme-landing .feature-card h3, .theme-landing .scenario-title { color: #f8fafc; }
.theme-landing .landing-subtitle, .theme-landing .feature-card p { color: #cbd5e1; }
.theme-landing .feature-card { background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.1); }
.theme-landing .feature-card:hover { background: rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.2); }
.theme-landing .scenario-tag { background: rgba(255, 255, 255, 0.1); color: #a5b4fc; border-color: rgba(255, 255, 255, 0.15); }
.theme-landing .scenario-tag:hover { background: rgba(99, 102, 241, 0.4); color: #ffffff; }

.theme-violet .main-layout.glass-panel { background: rgba(46, 22, 84, 0.4) !important; backdrop-filter: blur(2px) !important; -webkit-backdrop-filter: blur(2px) !important; border-color: rgba(167, 139, 250, 0.3) !important; box-shadow: 0 25px 50px -12px rgba(76, 29, 149, 0.6); }
.theme-violet .chat-header { background-color: rgba(46, 22, 84, 0.3); border-bottom-color: rgba(167, 139, 250, 0.2); }
.theme-violet .sidebar { background: rgba(23, 11, 43, 0.6); border-right-color: rgba(167, 139, 250, 0.2); }
.theme-violet .logo, .theme-violet .session-name, .theme-violet .empty-title, .theme-violet .list-title { color: #f8fafc; }
.theme-violet .empty-subtext { color: #e2e8f0; }
.theme-violet .history-item:hover { background-color: rgba(255, 255, 255, 0.1); }
.theme-violet .history-item.active { background-color: rgba(139, 92, 246, 0.35); border-color: rgba(139, 92, 246, 0.5); }
.theme-violet .uid-box { background: rgba(0,0,0,0.3); border-color: rgba(255,255,255,0.1); }
.theme-violet .uid-label { background: rgba(139, 92, 246, 0.5); color: #fff; }
.theme-violet .uid-value { color: #e2e8f0; }
.theme-violet .new-chat-btn { background: rgba(139, 92, 246, 0.2); border-color: rgba(139, 92, 246, 0.4); color: #ddd6fe; box-shadow:none;}
.theme-violet .new-chat-btn:hover { background: rgba(139, 92, 246, 0.4); }
.theme-violet .empty-icon-wrapper { background: rgba(255, 255, 255, 0.15); border-color: rgba(255, 255, 255, 0.3); }
.theme-violet .highlight-text { color: #e0e7ff; text-shadow: 0 0 10px rgba(167,139,250,0.5); }
.theme-violet .status-badge { background-color: rgba(0, 0, 0, 0.5); color: #c4b5fd; border-color: rgba(139, 92, 246, 0.3); }
.theme-violet .lock-tip { color: #cbd5e1; }
.theme-violet .exit-btn { background: rgba(0, 0, 0, 0.3); color: #cbd5e1; border-color: rgba(255, 255, 255, 0.2); }
.theme-violet .input-container { background: rgba(23, 11, 43, 0.7); border-color: rgba(139, 92, 246, 0.4); }
.theme-violet .input-container:focus-within { background: rgba(23, 11, 43, 0.9); border-color: rgba(167, 139, 250, 0.6); box-shadow: 0 15px 40px rgba(109, 40, 217, 0.25); }
.theme-violet .glass-textarea .el-textarea__inner { color: #f8fafc; }
.theme-violet .glass-textarea .el-textarea__inner::placeholder { color: #94a3b8; }
.theme-violet .send-btn { background: #8b5cf6; color: white;}
.theme-violet .send-btn:hover:not(:disabled) { background: #7c3aed; }
.theme-violet .message-wrapper.user .bubble { background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); color:white; border-color: transparent;}
.theme-violet .message-wrapper.assistant .bubble { background-color: rgba(255, 255, 255, 0.9); border-color: rgba(139, 92, 246, 0.4); box-shadow: 0 4px 20px rgba(109, 40, 217, 0.15); color: #0f172a;}
.theme-violet .glass-select .el-input__wrapper, .theme-violet .glass-input .el-input__wrapper, .theme-violet .recover-input .el-input__wrapper { background-color: rgba(0, 0, 0, 0.5); box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.5) inset; }
.theme-violet .el-input__inner { color: #f8fafc; }
.theme-violet .recover-input .el-input-group__append { background-color: rgba(139, 92, 246, 0.4); color: #fff; border:none;}


.theme-music .main-layout.glass-panel { background: rgba(56, 20, 35, 0.45) !important; backdrop-filter: blur(4px) !important; -webkit-backdrop-filter: blur(4px) !important; border-color: rgba(244, 114, 182, 0.3) !important; box-shadow: 0 25px 50px -12px rgba(159, 18, 57, 0.6); }
.theme-music .chat-header { background-color: rgba(56, 20, 35, 0.35); border-bottom-color: rgba(244, 114, 182, 0.2); }
.theme-music .sidebar { background: rgba(33, 10, 18, 0.6); border-right-color: rgba(244, 114, 182, 0.2); }
.theme-music .logo, .theme-music .session-name, .theme-music .empty-title, .theme-music .list-title { color: #fdf2f8; }
.theme-music .empty-subtext { color: #fbcfe8; }
.theme-music .history-item:hover { background-color: rgba(255, 255, 255, 0.08); }
.theme-music .history-item.active { background-color: rgba(236, 72, 153, 0.3); border-color: rgba(236, 72, 153, 0.5); }
.theme-music .uid-box { background: rgba(0,0,0,0.3); border-color: rgba(255,255,255,0.1); }
.theme-music .uid-label { background: rgba(236, 72, 153, 0.5); color: #fff; }
.theme-music .uid-value { color: #fbcfe8; }
.theme-music .new-chat-btn { background: rgba(236, 72, 153, 0.2); border-color: rgba(236, 72, 153, 0.4); color: #fbcfe8; box-shadow:none;}
.theme-music .new-chat-btn:hover { background: rgba(236, 72, 153, 0.4); }
.theme-music .empty-icon-wrapper { background: rgba(255, 255, 255, 0.15); border-color: rgba(255, 255, 255, 0.3); }
.theme-music .highlight-text { color: #fdf2f8; text-shadow: 0 0 10px rgba(244,114,182,0.5); }
.theme-music .status-badge { background-color: rgba(0, 0, 0, 0.5); color: #f9a8d4; border-color: rgba(236, 72, 153, 0.3); }
.theme-music .lock-tip { color: #cbd5e1; }
.theme-music .exit-btn { background: rgba(0, 0, 0, 0.3); color: #fbcfe8; border-color: rgba(255, 255, 255, 0.2); }
.theme-music .input-container { background: rgba(33, 10, 18, 0.75); border-color: rgba(236, 72, 153, 0.4); }
.theme-music .input-container:focus-within { background: rgba(33, 10, 18, 0.9); border-color: rgba(244, 114, 182, 0.6); box-shadow: 0 15px 40px rgba(190, 24, 93, 0.25); }
.theme-music .glass-textarea .el-textarea__inner { color: #fdf2f8; }
.theme-music .glass-textarea .el-textarea__inner::placeholder { color: #f9a8d4; }
.theme-music .send-btn { background: #ec4899; color: white;}
.theme-music .send-btn:hover:not(:disabled) { background: #db2777; }
.theme-music .message-wrapper.user .bubble { background: linear-gradient(135deg, #ec4899 0%, #be185d 100%); color:white; border-color: transparent;}
.theme-music .message-wrapper.assistant .bubble { background-color: rgba(255, 255, 255, 0.9); border-color: rgba(236, 72, 153, 0.4); box-shadow: 0 4px 20px rgba(190, 24, 93, 0.15); color: #0f172a;}
.theme-music .glass-select .el-input__wrapper, .theme-music .glass-input .el-input__wrapper, .theme-music .recover-input .el-input__wrapper { background-color: rgba(0, 0, 0, 0.5); box-shadow: 0 0 0 2px rgba(244, 114, 182, 0.5) inset; }
.theme-music .el-input__inner { color: #fdf2f8; }
.theme-music .recover-input .el-input-group__append { background-color: rgba(236, 72, 153, 0.4); color: #fff; border:none;}

.theme-game .main-layout.glass-panel { background: rgba(20, 12, 8, 0.6) !important; backdrop-filter: blur(4px) !important; -webkit-backdrop-filter: blur(4px) !important; border-color: rgba(184, 142, 81, 0.35) !important; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8); }
.theme-game .chat-header { background-color: rgba(20, 12, 8, 0.45); border-bottom-color: rgba(184, 142, 81, 0.25); }
.theme-game .sidebar { background: rgba(12, 8, 5, 0.75); border-right-color: rgba(184, 142, 81, 0.25); }
.theme-game .logo, .theme-game .session-name, .theme-game .empty-title, .theme-game .list-title { color: #f5eedc; }
.theme-game .empty-subtext { color: #c4b59d; }
.theme-game .history-item:hover { background-color: rgba(255, 255, 255, 0.05); }
.theme-game .history-item.active { background-color: rgba(184, 142, 81, 0.2); border-color: rgba(184, 142, 81, 0.4); }
.theme-game .uid-box { background: rgba(0,0,0,0.5); border-color: rgba(255,255,255,0.08); }
.theme-game .uid-label { background: rgba(145, 110, 60, 0.6); color: #fff; }
.theme-game .uid-value { color: #c4b59d; }
.theme-game .new-chat-btn { background: rgba(184, 142, 81, 0.15); border-color: rgba(184, 142, 81, 0.3); color: #e8d7ba; box-shadow:none;}
.theme-game .new-chat-btn:hover { background: rgba(184, 142, 81, 0.3); }
.theme-game .empty-icon-wrapper { background: rgba(0, 0, 0, 0.3); border-color: rgba(184, 142, 81, 0.4); }
.theme-game .highlight-text { color: #f5eedc; text-shadow: 0 0 10px rgba(184,142,81,0.4); }
.theme-game .status-badge { background-color: rgba(0, 0, 0, 0.5); color: #d4a359; border-color: rgba(184, 142, 81, 0.3); }
.theme-game .lock-tip { color: #9c8b74; }
.theme-game .exit-btn { background: rgba(0, 0, 0, 0.4); color: #c4b59d; border-color: rgba(255, 255, 255, 0.1); }
.theme-game .input-container { background: rgba(12, 8, 5, 0.8); border-color: rgba(184, 142, 81, 0.3); }
.theme-game .input-container:focus-within { background: rgba(20, 12, 8, 0.95); border-color: rgba(212, 168, 105, 0.5); box-shadow: 0 15px 40px rgba(145, 110, 60, 0.3); }
.theme-game .glass-textarea .el-textarea__inner { color: #f5eedc; }
.theme-game .glass-textarea .el-textarea__inner::placeholder { color: #8a7a63; }
.theme-game .send-btn { background: #96703b; color: white;}
.theme-game .send-btn:hover:not(:disabled) { background: #7a5a2e; }
.theme-game .message-wrapper.user .bubble { background: linear-gradient(135deg, #96703b 0%, #5c411e 100%); color:white; border-color: transparent;}
.theme-game .message-wrapper.assistant .bubble { background-color: rgba(25, 18, 14, 0.9); border-color: rgba(184, 142, 81, 0.3); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4); color: #e8d7ba;}
.theme-game .glass-select .el-input__wrapper, .theme-game .glass-input .el-input__wrapper, .theme-game .recover-input .el-input__wrapper { background-color: rgba(0, 0, 0, 0.5); box-shadow: 0 0 0 2px rgba(184, 142, 81, 0.4) inset; }
.theme-game .el-input__inner { color: #f5eedc; }
.theme-game .recover-input .el-input-group__append { background-color: rgba(145, 110, 60, 0.4); color: #fff; border:none;}


@media (max-width: 768px) {
  .glass-panel {
    background: rgba(255, 255, 255, 0.35);
    -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px);
    transform: translateZ(0); -webkit-transform: translateZ(0);
  }

  .theme-violet .main-layout.glass-panel {
    background: rgba(46, 22, 84, 0.4) !important;
    -webkit-backdrop-filter: blur(2px) !important;
    backdrop-filter: blur(2px) !important;
    transform: translateZ(0) !important; -webkit-transform: translateZ(0) !important;
  }

  .theme-snow .main-layout.glass-panel {
    background: rgba(255, 255, 255, 0.15) !important;
    -webkit-backdrop-filter: blur(2px) !important;
    backdrop-filter: blur(2px) !important;
    transform: translateZ(0) !important; -webkit-transform: translateZ(0) !important;
  }

  .theme-music .main-layout.glass-panel {
    background: rgba(56, 20, 35, 0.45) !important;
    -webkit-backdrop-filter: blur(3px) !important;
    backdrop-filter: blur(3px) !important;
    transform: translateZ(0) !important; -webkit-transform: translateZ(0) !important;
  }

  .theme-game .main-layout.glass-panel {
    background: rgba(20, 12, 8, 0.55) !important;
    -webkit-backdrop-filter: blur(3px) !important;
    backdrop-filter: blur(3px) !important;
    transform: translateZ(0) !important; -webkit-transform: translateZ(0) !important;
  }

  .theme-default .main-layout.glass-panel, .theme-landing .landing-content { transform: translateZ(0) !important; -webkit-transform: translateZ(0) !important; }

  .theme-violet .mobile-menu-btn, .theme-music .mobile-menu-btn, .theme-game .mobile-menu-btn, .theme-landing .mobile-menu-btn, .theme-default .mobile-menu-btn { color: #f8fafc !important; }
  .theme-snow .mobile-menu-btn { color: #0f172a !important; text-shadow: 0 1px 2px rgba(255,255,255,0.9); }
  .theme-game .mobile-menu-btn { color: #f5eedc !important; }

  .theme-violet .sidebar { background: rgba(15, 23, 42, 0.95) !important; }
  .theme-snow .sidebar { background: rgba(255, 255, 255, 0.85) !important; }
  .theme-music .sidebar { background: rgba(33, 10, 18, 0.95) !important; }
  .theme-game .sidebar { background: rgba(12, 8, 5, 0.95) !important; }
  .theme-default .sidebar { background: rgba(15, 23, 42, 0.85) !important; }

  .sidebar-overlay { background: rgba(0,0,0,0.4); backdrop-filter: blur(4px); }
}
</style>
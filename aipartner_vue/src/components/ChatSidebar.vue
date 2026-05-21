<template>
  <div class="sidebar-overlay" v-show="isMobileMenuOpen" @click="$emit('close-mobile-menu')"></div>

  <el-aside width="280px" class="sidebar" :class="{ 'mobile-open': isMobileMenuOpen }">
    <div class="mobile-close-btn" @click="$emit('close-mobile-menu')">
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

    <button class="new-chat-btn" @click="$emit('create-session')">
      <el-icon class="btn-icon"><Plus /></el-icon>
      <span>新建对话</span>
    </button>

    <div class="quest-section">
      <div class="list-title">神秘指引</div>
      <div class="quest-card glass-panel" @click="copyQuest" title="点击复制谜题内容">
        <p v-if="currentQuest" class="quest-text">{{ currentQuest.question }}</p>
        <p v-else class="quest-text success">恭喜你所有常规记忆已解开！你居然看完了这么多内容😄。代码列表：160615、180818、191001、240802、251027、260315、260410</p>
        <el-icon v-if="currentQuest" class="quest-copy-icon"><DocumentCopy /></el-icon>
      </div>
    </div>

    <div class="history-list">
      <div class="list-title">记忆宝匣</div>
      <el-scrollbar height="calc(100vh - 320px)" class="custom-scrollbar">
        <div
          v-for="session in sessions"
          :key="session.session_id"
          :class="['history-item', { active: currentSessionId === session.session_id }]"
          @click="$emit('load-session', session.session_id)"
        >
          <div class="session-info">
            <span class="session-name">{{ session.name }}</span>
            <span class="session-time">{{ session.display_time }}</span>
          </div>
          <div class="delete-btn-wrapper">
            <el-icon class="delete-icon" @click.stop="$emit('delete-session', session.session_id)"><Delete /></el-icon>
          </div>
        </div>
      </el-scrollbar>
    </div>

    <div class="sidebar-footer">
      <el-input v-model="recoverUidLocal" placeholder="输入8位恢复码..." class="recover-input">
        <template #append>
          <el-button class="recover-btn" @click="$emit('sync-history', recoverUidLocal)">同步</el-button>
        </template>
      </el-input>
    </div>
  </el-aside>
</template>

<script setup>
import { ref } from 'vue'
import { Close, DocumentCopy, Plus, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { currentQuest } from '../store/questState.js'

const props = defineProps({
  isMobileMenuOpen: Boolean,
  uid: String,
  sessions: Array,
  currentSessionId: String
})

const emit = defineEmits(['close-mobile-menu', 'create-session', 'load-session', 'delete-session', 'sync-history'])

const recoverUidLocal = ref('')

const copyUid = async () => {
  try {
    await navigator.clipboard.writeText(props.uid)
    ElMessage.success('身份码已复制至剪贴板')
  } catch (err) {
    const input = document.createElement('input')
    input.value = props.uid
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
    ElMessage.success('身份码已灵动复制至剪贴板')
  }
}

const copyQuest = async () => {
  if (!currentQuest.value) return
  try {
    await navigator.clipboard.writeText(currentQuest.value.question)
    ElMessage.success('内容已复制 ')
  } catch (err) {
    const input = document.createElement('input')
    input.value = currentQuest.value.question
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
    ElMessage.success('内容已复制')
  }
}
</script>

<style scoped>
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

@media (max-width: 768px) {
  .sidebar { position: fixed; left: 0; top: 0; bottom: 0; z-index: 1000; transform: translateX(-100%); width: 85vw !important; max-width: 320px; border-right: none;}
  .sidebar.mobile-open { transform: translateX(0); }
  .sidebar-overlay { display: block; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 999; }
  .mobile-close-btn { display: flex; position: absolute; right: 16px; top: 16px; font-size: 24px; cursor: pointer; }
}
</style>
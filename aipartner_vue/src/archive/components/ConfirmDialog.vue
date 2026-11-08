<template>
  <!-- 挂到 body：栏上有 content-visibility:auto，留在原地的话 position:fixed
       会相对那一栏定位，弹窗就会跟着页面滑动（微信里尤其明显） -->
  <Teleport to="body">
    <div v-if="state.open" class="confirm-mask" @click.self="settleConfirm(false)">
      <div class="confirm-box" role="dialog" aria-modal="true" :aria-label="state.message">
        <p class="confirm-msg">{{ state.message }}</p>
        <div class="confirm-acts">
          <button class="confirm-yes" type="button" @click="settleConfirm(true)">
            {{ state.okText }}
          </button>
          <button class="confirm-no" type="button" @click="settleConfirm(false)">取消</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { onBeforeUnmount, onMounted } from 'vue'
import { confirmState as state, settleConfirm } from '../confirm.js'

function onKey(ev) {
  if (!state.open) return
  if (ev.key === 'Escape' || ev.key === 'Esc') settleConfirm(false)
}

onMounted(() => document.addEventListener('keydown', onKey))

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKey)
  // 页面切走时还挂着的话，让 await 立即结束
  if (state.open) settleConfirm(false)
})
</script>

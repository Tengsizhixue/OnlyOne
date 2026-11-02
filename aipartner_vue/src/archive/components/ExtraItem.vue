<template>
  <div ref="root" class="extra-item">
    <p class="extra-hint">{{ item.hint }}</p>

    <form autocomplete="off" class="extra-form" @submit.prevent="submit">
      <input
        v-model="answer"
        aria-label="输入人物姓名"
        autocomplete="off"
        class="extra-input"
        :disabled="unlocked"
        placeholder="输入人物姓名"
        type="text"
      />
      <button class="extra-check" type="submit" :disabled="unlocked || busy">
        {{ unlocked ? '已解锁' : '确认' }}
      </button>
    </form>

    <p aria-live="polite" class="extra-feedback" :class="{ ok: unlocked }">{{ feedback }}</p>

    <template v-if="unlocked && descHtml">
      <div class="extra-description" :class="{ 'is-expanded': expanded }" v-html="descHtml"></div>
      <button class="extra-toggle" type="button" :aria-expanded="expanded" @click="toggle">
        {{ expanded ? '收起全文' : '展开全文' }}
      </button>
    </template>
  </div>
</template>

<script setup>
import { computed, nextTick, ref } from 'vue'
import { renderTokens } from '../render.js'

const props = defineProps({
  item: { type: Object, required: true },
  state: { type: Object, default: () => ({}) },
  names: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['submit'])

const answer = ref('')
const expanded = ref(false)
const root = ref(null)

const unlocked = computed(() => !!props.state.unlocked)
const busy = computed(() => !!props.state.busy)
const descHtml = computed(() =>
  unlocked.value ? renderTokens(props.state.description || '', props.names) : ''
)
const feedback = computed(() => {
  if (props.state.feedback) return props.state.feedback
  return unlocked.value ? '回答正确，已解锁。' : '答对后即可查看具体描述。'
})

function submit() {
  if (unlocked.value || busy.value) return
  emit('submit', { id: props.item.id, answer: answer.value })
}

function toggle() {
  expanded.value = !expanded.value
  if (!expanded.value) {
    nextTick(() => {
      if (root.value) root.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  }
}
</script>

<template>
  <div class="extra-item">
    <p class="extra-hint">{{ item.hint }}</p>

    <form v-if="!answered" autocomplete="off" class="extra-form" @submit.prevent="submit">
      <input
        v-model="answer"
        aria-label="输入人物姓名"
        autocomplete="off"
        class="extra-input"
        :disabled="busy"
        placeholder="输入人物姓名"
        type="text"
      />
      <button class="extra-check" type="submit" :disabled="busy">确认</button>
    </form>
    <p v-else class="extra-done">已答对</p>

    <p v-if="feedback" aria-live="polite" class="extra-feedback" :class="{ ok: answered }">{{ feedback }}</p>

    <template v-if="unlocked && text">
      <div class="extra-tabs">
        <button
          class="extra-tab"
          :class="{ on: tab === 'ai' }"
          type="button"
          @click="toggle('ai')"
        >
          AI 总结
        </button>
        <button
          class="extra-tab"
          :class="{ on: tab === 'raw' }"
          type="button"
          @click="toggle('raw')"
        >
          原文
        </button>
      </div>

      <div v-if="tab === 'ai'" class="extra-panel" v-html="text.ai"></div>

      <div v-else-if="tab === 'raw'" class="extra-panel">
        <div v-if="text.raw" v-html="text.raw"></div>

        <div v-if="choice" class="extra-choice">
          <p class="extra-choice-q">{{ choice.question }}</p>
          <div class="extra-choice-opts">
            <button
              v-for="opt in choice.options"
              :key="opt.key"
              class="extra-opt"
              :class="{ sel: picked === opt.key }"
              type="button"
              @click="picked = opt.key"
            >
              <span class="extra-opt-k">{{ opt.key }}</span>
              <span class="extra-opt-t">{{ opt.text }}</span>
            </button>
          </div>

          <template v-if="picked">
            <p class="extra-choice-reply">{{ pickedReply }}</p>
            <p class="extra-choice-right">正确答案：{{ choice.correct }} · {{ correctText }}</p>
            <div class="extra-choice-exp" v-html="choice.explanation"></div>
          </template>
        </div>
      </div>

      <!-- 内容很长，底部再给一次收起，省得滚回顶部 -->
      <button v-if="tab" class="extra-collapse" type="button" @click="tab = ''">
        <span class="extra-collapse-ar" aria-hidden="true">↑</span>
        收起
      </button>
    </template>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  item: { type: Object, required: true },
  state: { type: Object, default: () => ({}) },
  text: { type: Object, default: null },
  unlocked: { type: Boolean, default: false },
})

const emit = defineEmits(['submit'])

const answer = ref('')
const picked = ref('')
const tab = ref('')

const answered = computed(() => !!props.state.answered)
const busy = computed(() => !!props.state.busy)
const choice = computed(() => (props.text && props.text.choice) || null)

const pickedReply = computed(() => {
  if (!choice.value || !picked.value) return ''
  const opt = choice.value.options.find((item) => item.key === picked.value)
  return opt ? opt.reply : ''
})

const correctText = computed(() => {
  if (!choice.value) return ''
  const opt = choice.value.options.find((item) => item.key === choice.value.correct)
  return opt ? opt.text : ''
})

const feedback = computed(() => {
  if (props.state.feedback) return props.state.feedback
  // 答对之后上面已经有「已答对」，这里不再重复
  return answered.value ? '' : '答对三个问题后可查看内容。'
})

function submit() {
  if (answered.value || busy.value) return
  emit('submit', { id: props.item.id, answer: answer.value })
}

// 两个内容一次只展开一个，避免整页拉得很长；再点一次收起
function toggle(name) {
  tab.value = tab.value === name ? '' : name
}
</script>

<template>
  <details class="extra-fold">
    <summary class="extra-fold-summary">
      <span aria-hidden="true" class="extra-fold-dot"></span>
      <span>附加内容</span>
      <span aria-hidden="true" class="extra-fold-state"></span>
    </summary>

    <div class="extra-body">
      <p v-if="section.intro" class="extra-intro">{{ section.intro }}</p>

      <!-- 答完三题：先给一句说明，再展开那几个人 -->
      <template v-if="unlocked">
        <p v-if="note" class="extra-note">{{ note }}</p>
        <ExtraItem v-for="item in section.items" :key="item.id" :item="item" />
      </template>

      <!-- 没答：三个问题 + 三个输入框 -->
      <form v-else class="extra-gate" @submit.prevent="submit">
        <label v-for="(q, i) in questions" :key="i" class="extra-q">
          <span class="extra-q-text">{{ q }}</span>
          <input
            v-model="answers[i]"
            class="extra-input"
            type="text"
            autocomplete="off"
            autocapitalize="off"
            spellcheck="false"
            :disabled="busy"
          />
        </label>
        <div class="extra-gate-row">
          <button class="extra-submit" type="submit" :disabled="busy">
            {{ busy ? '核对中…' : '提交' }}
          </button>
        </div>
        <p v-if="error" class="extra-error">{{ error }}</p>
      </form>
    </div>
  </details>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import ExtraItem from './ExtraItem.vue'
import { unlockExtra } from '../api.js'

const props = defineProps({
  section: { type: Object, required: true },
  stageId: { type: String, required: true },
  unlocked: { type: Boolean, default: false },
})

const emit = defineEmits(['unlocked'])

const questions = computed(() => (props.section.gate && props.section.gate.questions) || [])
const note = computed(() => (props.section.gate && props.section.gate.note) || '')

const answers = ref(questions.value.map(() => ''))
const busy = ref(false)
const error = ref('')

watch(questions, (list) => {
  answers.value = list.map(() => '')
})

async function submit() {
  if (busy.value) return
  const values = answers.value.map((v) => (v || '').trim())
  // 前端先挡一次，免得空白提交还跑一趟网络
  if (values.length !== questions.value.length || values.some((v) => !v)) {
    error.value = '三个问题都要填。'
    return
  }
  busy.value = true
  error.value = ''
  try {
    await unlockExtra(props.stageId, values)
    emit('unlocked')
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

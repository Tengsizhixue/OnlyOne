<template>
  <details class="extra-fold">
    <summary class="extra-fold-summary">
      <span aria-hidden="true" class="extra-fold-dot"></span>
      <span>附加内容</span>
      <span aria-hidden="true" class="extra-fold-state"></span>
    </summary>

    <section class="col extra-col">
      <p v-if="intro" class="extra-intro">{{ intro }}</p>
      <p v-if="progressText" class="extra-progress">{{ progressText }}</p>

      <div v-for="item in visibleItems" :key="item.id" class="extra-step">
        <ExtraItem
          :item="item"
          :state="states[item.id] || {}"
          :text="texts[item.id] || null"
          :unlocked="all"
          @submit="onSubmit"
        />
      </div>

      <p v-if="ranked" class="extra-rank">你是第 {{ ranking.rank }} 个全部答对的人</p>
    </section>
  </details>
</template>

<script setup>
import { computed } from 'vue'
import ExtraItem from './ExtraItem.vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  intro: { type: String, default: '' },
  names: { type: Object, default: () => ({}) },
  states: { type: Object, default: () => ({}) },
  texts: { type: Object, default: () => ({}) },
  all: { type: Boolean, default: false },
  ranking: { type: Object, default: null },
})

const emit = defineEmits(['unlock'])

function isDone(id) {
  const state = props.states[id]
  return !!(state && state.answered)
}

// 题目一道一道出现：答对第 1 个才露出第 2 个，答对第 2 个才露出第 3 个。
// 已经答过的仍然留在上面（标着「已答对」），回访时也能看到自己答到哪了。
const visibleItems = computed(() => {
  const shown = []
  for (const item of props.items) {
    shown.push(item)
    if (!isDone(item.id)) break
  }
  return shown
})

// 三题全对才解锁，所以要把进度告诉人，否则答对一题会以为没生效
const progressText = computed(() => {
  if (props.all || !props.items.length) return ''
  const total = props.items.length
  const done = props.items.filter((item) => isDone(item.id)).length
  if (!done) return ''
  return `已答对 ${done}/${total} 人，下面等着第 ${done + 1} 个。`
})

const ranked = computed(() => {
  const data = props.ranking
  return !!(data && data.total && data.rank)
})

function onSubmit(payload) {
  emit('unlock', payload.id, payload.answer)
}
</script>

<template>
  <details class="extra-fold">
    <summary class="extra-fold-summary">
      <span aria-hidden="true" class="extra-fold-dot"></span>
      <span>附加内容</span>
      <span aria-hidden="true" class="extra-fold-state"></span>
    </summary>

    <section class="col extra-col">
      <p v-if="intro" class="extra-intro">{{ intro }}</p>
      <ExtraItem
        v-for="item in items"
        :key="item.id"
        :item="item"
        :state="states[item.id] || {}"
        :names="names"
        @submit="onSubmit"
      />
    </section>
  </details>
</template>

<script setup>
import ExtraItem from './ExtraItem.vue'

defineProps({
  items: { type: Array, default: () => [] },
  intro: { type: String, default: '' },
  names: { type: Object, default: () => ({}) },
  states: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['unlock'])

function onSubmit(payload) {
  emit('unlock', payload.id, payload.answer)
}
</script>

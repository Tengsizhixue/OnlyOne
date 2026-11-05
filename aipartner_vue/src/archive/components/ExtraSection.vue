<template>
  <details class="extra-fold">
    <summary class="extra-fold-summary">
      <span aria-hidden="true" class="extra-fold-dot"></span>
      <span>附加内容</span>
      <span aria-hidden="true" class="extra-fold-state"></span>
    </summary>

    <div class="extra-body">
      <p v-if="section.intro" class="extra-intro">{{ section.intro }}</p>

      <ExtraItem v-for="item in section.items" :key="item.id" :item="item" />
    </div>
  </details>
</template>

<script setup>
import ExtraItem from './ExtraItem.vue'

defineProps({
  section: { type: Object, required: true },
})
</script>

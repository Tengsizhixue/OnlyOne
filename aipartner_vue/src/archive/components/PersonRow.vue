<template>
  <div
    class="p"
    :class="{ 'is-del': person.deleted, 'is-open': open, 'is-reveal': revealing }"
    :id="'person-' + person.id"
    :style="{ '--i': revealIndex }"
  >
    <button class="p-btn" type="button" :aria-expanded="open" @click="$emit('toggle', person)">
      <span aria-hidden="true" class="p-dot"></span>
      <span class="p-tx">{{ displayName }}</span>
    </button>
  </div>
  <!-- 描述单独成块：手机两列时它跨满整行，人名仍留在原来那一列里，点开不会跳到左边 -->
  <div v-if="open && descHtml" class="p-body">
    <p class="quote" :class="{ 'quote-del': person.deleted }" v-html="descHtml"></p>
  </div>
</template>

<script setup>
defineProps({
  person: { type: Object, required: true },
  displayName: { type: String, default: '***' },
  open: { type: Boolean, default: false },
  descHtml: { type: String, default: '' },
  revealing: { type: Boolean, default: false },
  revealIndex: { type: Number, default: 0 },
})

defineEmits(['toggle'])
</script>

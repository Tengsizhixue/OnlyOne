<template>
  <li class="p" :class="{ 'is-del': person.deleted, 'is-open': open }" :id="'person-' + person.id">
    <button class="p-btn" type="button" :aria-expanded="open" @click="$emit('toggle', person)">
      <span aria-hidden="true" class="p-dot"></span>
      <span class="p-tx">{{ displayName }}</span>
    </button>
    <p
      v-if="open && descHtml"
      class="quote"
      :class="{ 'quote-del': person.deleted }"
      v-html="descHtml"
    ></p>
  </li>
</template>

<script setup>
defineProps({
  person: { type: Object, required: true },
  displayName: { type: String, default: '***' },
  open: { type: Boolean, default: false },
  descHtml: { type: String, default: '' },
})

defineEmits(['toggle'])
</script>

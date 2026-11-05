<template>
  <section class="photo-album">
    <header class="photo-head">
      <h3 class="photo-title">{{ album.title }}</h3>
    </header>

    <!-- 没解锁：只有一道题，答对后端才把图片地址发下来 -->
    <form v-if="!images.length" class="photo-form" @submit.prevent="submit">
      <label class="photo-q" :for="inputId">{{ album.question }}</label>
      <div class="photo-row">
        <input
          :id="inputId"
          v-model="answer"
          class="photo-input"
          type="text"
          autocomplete="off"
          autocapitalize="off"
          spellcheck="false"
          placeholder="输入名字"
          :disabled="busy"
        />
        <button class="photo-submit" type="submit" :disabled="busy">
          {{ busy ? '核对中…' : '查看' }}
        </button>
      </div>
      <p v-if="error" class="photo-error">{{ error }}</p>
    </form>

    <template v-else>
      <!-- 说明文字只在解锁之后出现，答题前不透露内容 -->
      <p v-if="album.note" class="photo-note">{{ album.note }}</p>

      <div class="photo-grid">
        <button
          v-for="(item, i) in images"
          :key="urlOf(item)"
          class="photo-cell"
          type="button"
          @click="$emit('open', images, i)"
        >
          <img :src="thumbOf(item)" alt="" loading="lazy" decoding="async" />
        </button>
      </div>

      <p class="photo-hint">点开看大图，可以单张下载。</p>
    </template>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { unlockPhoto } from '../api.js'

const props = defineProps({
  album: { type: Object, required: true },
  images: { type: Array, default: () => [] },
})

const emit = defineEmits(['open', 'unlocked'])

const answer = ref('')
const error = ref('')
const busy = ref(false)

const inputId = computed(() => `photo-q-${props.album.id}`)

// 后端给的是 {url, thumb}；兼容早期纯字符串的形式
function urlOf(item) {
  return typeof item === 'string' ? item : item.url
}
function thumbOf(item) {
  return typeof item === 'string' ? item : item.thumb || item.url
}

async function submit() {
  const value = answer.value.trim()
  if (!value || busy.value) return
  busy.value = true
  error.value = ''
  try {
    const res = await unlockPhoto(props.album.id, value)
    emit('unlocked', props.album.id, res.images || [])
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

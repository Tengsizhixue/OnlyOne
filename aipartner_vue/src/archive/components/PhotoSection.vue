<template>
  <details class="extra-fold photo-fold">
    <summary class="extra-fold-summary">
      <span aria-hidden="true" class="extra-fold-dot"></span>
      <span>拓展</span>
      <span aria-hidden="true" class="extra-fold-state"></span>
    </summary>

    <div class="extra-body">
      <PhotoAlbum
        v-for="album in albums"
        :key="album.id"
        :album="album"
        :images="owned[album.id] || []"
        @open="openViewer"
        @unlocked="onUnlocked"
      />
    </div>
  </details>

  <Teleport to="body">
    <div v-if="viewer" class="photo-viewer" @click.self="close">
      <button class="pv-btn pv-close" type="button" aria-label="关闭" @click="close">×</button>
      <button
        v-if="viewer.images.length > 1"
        class="pv-btn pv-prev"
        type="button"
        aria-label="上一张"
        @click="step(-1)"
      >
        ‹
      </button>

      <img class="pv-img" :src="shown" :data-full="currentUrl" alt="" />

      <button
        v-if="viewer.images.length > 1"
        class="pv-btn pv-next"
        type="button"
        aria-label="下一张"
        @click="step(1)"
      >
        ›
      </button>

      <div class="pv-bar">
        <span class="pv-idx">{{ viewer.index + 1 }} / {{ viewer.images.length }}</span>
        <a class="pv-dl" :href="currentUrl" download>下载这张</a>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import PhotoAlbum from './PhotoAlbum.vue'

const props = defineProps({
  albums: { type: Array, default: () => [] },
  unlocked: { type: Object, default: () => ({}) },
})

// 已解锁的相册 → 图片列表。解锁接口返回后直接塞进来，不用刷新
const owned = reactive({})
watch(
  () => props.unlocked,
  (value) => Object.assign(owned, value || {}),
  { immediate: true, deep: true },
)

const viewer = ref(null)
const shown = ref('') // 浮层当前显示的地址：先缩略图，原图就绪后替换
let prevOverflow = ''
let want = 0 // 防止快速翻页时上一张的原图加载完把这一张盖掉

// 后端给 {url, thumb}；兼容早期纯字符串的形式
function fields(item) {
  return typeof item === 'string'
    ? { url: item, thumb: '' }
    : { url: item.url, thumb: item.thumb || '' }
}

const currentUrl = computed(() => {
  const v = viewer.value
  return v ? fields(v.images[v.index]).url : ''
})

// 缩略图 12KB 左右几乎瞬时，先铺上；原图（最大 6MB）在后台加载完再无缝替换
function paint() {
  const v = viewer.value
  if (!v) return
  const { url, thumb } = fields(v.images[v.index])
  const my = ++want
  shown.value = thumb || url
  if (thumb && thumb !== url) {
    const img = new Image()
    img.onload = () => {
      if (my === want) shown.value = url
    }
    img.src = url
  }
}

function onUnlocked(id, images) {
  owned[id] = images
}

function openViewer(images, index) {
  viewer.value = { images, index }
  paint()
  prevOverflow = document.body.style.overflow
  document.body.style.overflow = 'hidden'
}

function close() {
  viewer.value = null
  want += 1
  document.body.style.overflow = prevOverflow
}

function step(delta) {
  const v = viewer.value
  if (!v) return
  v.index = (v.index + delta + v.images.length) % v.images.length
  paint()
}

function onKey(e) {
  if (!viewer.value) return
  if (e.key === 'Escape') close()
  else if (e.key === 'ArrowLeft') step(-1)
  else if (e.key === 'ArrowRight') step(1)
}

onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKey)
  if (viewer.value) document.body.style.overflow = prevOverflow
})
</script>

<template>
  <div class="extra-item">
    <p class="extra-hint">{{ item.hint }}</p>

    <div class="extra-tabs">
      <!-- 作者现在自己写的看法排第一；没有的条目不显示这个标签 -->
      <button
        v-if="item.now"
        class="extra-tab"
        :class="{ on: tab === 'now' }"
        type="button"
        @click="toggle('now')"
      >
        现在的看法
      </button>
      <!-- 没有原文的条目（如某同学）不显示「原文」 -->
      <button
        v-if="item.raw"
        class="extra-tab"
        :class="{ on: tab === 'raw' }"
        type="button"
        @click="toggle('raw')"
      >
        原文
      </button>
      <button
        class="extra-tab"
        :class="{ on: tab === 'ai' }"
        type="button"
        @click="toggle('ai')"
      >
        AI 总结
      </button>
    </div>

    <!-- 正文里的人名引用跟着已揭示的人名走：揭示过就显示真名，否则仍是 *** -->
    <div v-if="tab" class="extra-panel" v-html="panelHtml"></div>

    <!-- 内容很长，底部再给一次收起，省得滚回顶部 -->
    <button v-if="tab" class="extra-collapse" type="button" @click="tab = ''">
      <span class="extra-collapse-ar" aria-hidden="true">↑</span>
      收起
    </button>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { renderTokens } from '../render.js'

const props = defineProps({
  item: { type: Object, required: true },
  // 已揭示的人名：{ p047: '真名', ... }，只由 /state 与解锁接口下发
  names: { type: Object, default: () => ({}) },
})

const tab = ref('')

// 用 computed 而不是挂载后改 DOM：解锁人名导致 names 变化时，正文会跟着重渲染
const panelHtml = computed(() =>
  tab.value ? renderTokens(props.item[tab.value] || '', props.names) : ''
)

// 三个面板一次只展开一个，避免整页拉得很长；再点一次收起
function toggle(name) {
  tab.value = tab.value === name ? '' : name
}
</script>

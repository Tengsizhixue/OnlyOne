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

    <div v-if="tab === 'now'" class="extra-panel" v-html="item.now"></div>
    <div v-else-if="tab === 'raw'" class="extra-panel" v-html="item.raw"></div>
    <div v-else-if="tab === 'ai'" class="extra-panel" v-html="item.ai"></div>

    <!-- 内容很长，底部再给一次收起，省得滚回顶部 -->
    <button v-if="tab" class="extra-collapse" type="button" @click="tab = ''">
      <span class="extra-collapse-ar" aria-hidden="true">↑</span>
      收起
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  item: { type: Object, required: true },
})

const tab = ref('')

// 三个面板一次只展开一个，避免整页拉得很长；再点一次收起
function toggle(name) {
  tab.value = tab.value === name ? '' : name
}
</script>

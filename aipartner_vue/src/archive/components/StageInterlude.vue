<template>
  <!-- 原生 details：点标题行即可展开 / 收起，键盘也原生可用。
       默认收起：只留一行标题，点开才看得到这段介绍。 -->
  <details class="col interlude-col" :data-stage="stage.id">
    <summary class="interlude-summary">
      <span aria-hidden="true" class="cdot"></span>
      <h2 class="col-title">{{ stage.title }}</h2>
      <span aria-hidden="true" class="interlude-state"></span>
    </summary>

    <div class="interlude-body">
      <p class="interlude-intro">{{ stage.intro }}</p>

      <ul class="interlude-lines">
        <li v-for="(line, index) in stage.lines" :key="index">{{ line }}</li>
      </ul>
    </div>
  </details>
</template>

<script setup>
// 时间线上一段纯文字的介绍：没有人名、没有答题框、没有分组。
// 内容全部来自 content.json 的 stage.intro / stage.lines，这里不写死任何字。
defineProps({
  stage: { type: Object, required: true },
})
</script>

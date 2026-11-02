<template>
  <section class="col" :data-stage="stage.id">
    <div class="col-head">
      <span aria-hidden="true" class="cdot"></span>
      <h2 class="col-title">{{ stage.title }}</h2>
    </div>

    <form autocomplete="off" class="phase-unlock-form" @submit.prevent="submit">
      <input
        v-model="input"
        :aria-label="'输入' + stage.title + '任意人物姓名'"
        autocomplete="off"
        class="phase-unlock-input"
        :disabled="unlocked"
        placeholder="输入本阶段任意人名"
        type="text"
      />
      <button class="phase-unlock-btn" type="submit" :disabled="unlocked || busy">
        {{ unlocked ? '已解锁' : '解锁本阶段' }}
      </button>
    </form>
    <p class="phase-unlock-feedback" :class="{ ok: feedbackOk }">{{ feedbackText }}</p>

    <div v-for="group in stage.groups" :key="group.id" class="group">
      <button
        :aria-expanded="!!openGroups[group.id]"
        class="cnt"
        type="button"
        @click="toggleGroup(group.id)"
      >
        <span class="cnt-t"><span aria-hidden="true" class="tick"></span>{{ group.title }}</span>
        <span class="cnt-n">{{ countOf(group) }}</span>
      </button>

      <ul v-show="openGroups[group.id]" class="roster">
        <PersonRow
          v-for="person in group.people"
          :key="person.id"
          :person="person"
          :display-name="displayName(person)"
          :open="!!openPeople[person.id]"
          :desc-html="descFor(person)"
          @toggle="togglePerson"
        />
      </ul>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, reactive, ref } from 'vue'
import PersonRow from './PersonRow.vue'
import { renderTokens } from '../render.js'

const props = defineProps({
  stage: { type: Object, required: true },
  names: { type: Object, default: () => ({}) },
  unlocked: { type: Boolean, default: false },
  feedback: { type: Object, default: null },
})

const emit = defineEmits(['unlock'])

const input = ref('')
const openGroups = reactive({})
const openPeople = reactive({})

const allPeople = computed(() =>
  props.stage.groups.flatMap((group) =>
    group.people.map((person) => ({ ...person, groupId: group.id }))
  )
)

const busy = computed(() => !!(props.feedback && props.feedback.busy))
const feedbackOk = computed(() => props.unlocked || !!(props.feedback && props.feedback.ok))
const feedbackText = computed(() => {
  if (props.feedback && props.feedback.text) return props.feedback.text
  return props.unlocked
    ? '本阶段已解锁。'
    : '本阶段人物及描述中的姓名均为匿名状态。'
})

function displayName(person) {
  return props.names[person.id] || '***'
}

function descFor(person) {
  return openPeople[person.id] ? renderTokens(person.desc, props.names) : ''
}

function countOf(group) {
  return group.people.filter((person) => !person.deleted).length
}

function submit() {
  if (props.unlocked || busy.value) return
  emit('unlock', props.stage.id, input.value)
}

function toggleGroup(id) {
  openGroups[id] = !openGroups[id]
}

function togglePerson(person) {
  // 划去的人：如果同阶段存在同名且未划去的条目，跳过去
  if (person.deleted && props.names[person.id]) {
    const target = allPeople.value.find(
      (item) =>
        !item.deleted &&
        item.id !== person.id &&
        props.names[item.id] === props.names[person.id]
    )
    if (target) {
      openGroups[target.groupId] = true
      openPeople[target.id] = true
      nextTick(() => {
        const el = document.getElementById('person-' + target.id)
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      })
      return
    }
  }
  openPeople[person.id] = !openPeople[person.id]
}
</script>

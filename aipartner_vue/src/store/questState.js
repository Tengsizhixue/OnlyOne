import { ref, computed } from 'vue'

// 1. 🧩 所有的谜题配置都在这里！
export const SECRET_QUESTS = [
  { id: 1, question: "尝试在聊天框发送160615", code: "160615" },
  { id: 2, question: "世界上只有两个人的苹果手机收不到消息，其中的一个是谁？", code: "260315" },
  { id: 3, question: "去年印象深刻的作品？", code: "251027" },
  { id: 4, question: "今年印象深刻的作品？", code: "260410" },
  { id: 5, question: "对待网游与ea的态度？", code: "180818" },
  { id: 6, question: "经常用什么头像？", code: "191001" },
  { id: 7, question: "听歌的习惯是什么？", code: "240802" }
]

// 2. 从本地缓存读取已解锁的密码记录（防止刷新后进度丢失）
const saved = localStorage.getItem('unlocked_secrets')
export const unlockedCodes = ref(saved ? JSON.parse(saved) : [])

// 3. 解锁新进度的函数 (当用户进入特定的彩蛋页时调用)
export const unlockCode = (code) => {
  if (!unlockedCodes.value.includes(code)) {
    unlockedCodes.value.push(code)
    localStorage.setItem('unlocked_secrets', JSON.stringify(unlockedCodes.value))
  }
}

// 4. 计算当前需要展示的下一个问题
export const currentQuest = computed(() => {
  // 查找第一个还没被解锁的谜题
  return SECRET_QUESTS.find(q => !unlockedCodes.value.includes(q.code))
})

// 5. 判断是否全部通关 (原逻辑不再作为限制条件，但仍可留作记录判定)
export const isAllUnlocked = computed(() => {
  return SECRET_QUESTS.every(q => unlockedCodes.value.includes(q.code))
})

// 6. 🌟 特殊条目的解锁状态（附加内容和结局）
export const visitedExtras = ref({
  final: false, // 结局
  extra200326: false,
  extra210318: false,
  extra230602: false
})

// 从本地缓存读取特殊条目的访问记录
const savedExtras = localStorage.getItem('visited_extras')
if (savedExtras) {
  Object.assign(visitedExtras.value, JSON.parse(savedExtras))
}

// 标记特殊条目为已访问
export const markExtraAsVisited = (key) => {
  if (!visitedExtras.value[key]) {
    visitedExtras.value[key] = true
    localStorage.setItem('visited_extras', JSON.stringify(visitedExtras.value))
  }
}
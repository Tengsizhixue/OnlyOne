import { ref, computed } from 'vue'

// 1. 🧩 所有的谜题配置都在这里！
// 后续你要修改顺序、或者追加新问题，只需要在这里修改或添加对应的对象即可，不需要改动任何页面代码。
export const SECRET_QUESTS = [
  { id: 1, question: "你可以尝试在聊天框发送111111", code: "111111" },
  { id: 2, question: "世界上只有两个人的苹果手机收不到消息，其中的一个是谁？", code: "260315" },
  { id: 3, question: "去年印象深刻的作品？", code: "251027" },
  { id: 4, question: "今年印象深刻的作品？", code: "260410" },
  { id: 5, question: "为什么不喜欢网游？", code: "180818" },
  { id: 6, question: "经常用什么头像？", code: "19xxxx" },
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

// 5. 判断是否全部通关
export const isAllUnlocked = computed(() => {
  return SECRET_QUESTS.every(q => unlockedCodes.value.includes(q.code))
})
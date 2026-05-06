<template>
  <div class="secret-page glass-panel shadow-2xl">

    <div v-if="secretCode === '260315'" class="secret-content">
      <h1 class="highlight-text" style="color: #60a5fa;">📱 李红宝的失联空间</h1>
      <p class="subtitle">特殊代码认证：260315</p>
      <div class="content-box">
        <p>这里是李红宝的专属页面骨架。</p>
        <p>（后续内容待设计：可以在这里放他的自述、收不到消息的搞笑图片等...）</p>
      </div>
      <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
    </div>

    <div v-else-if="secretCode === '251027'" class="secret-content">
      <h1 class="highlight-text" style="color: #34d399;">⏳ 时空与灵魂的交界处</h1>
      <p class="subtitle">特殊代码认证：251027</p>
      <div class="content-box">
        <p>这里是《我在七年后等着你》与《灵魂摆渡者》的专属回忆页面。</p>
        <p>（后续内容待设计：可以放游戏截图、音频、或者你对这两款游戏的感悟...）</p>
      </div>
      <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
    </div>

    <div v-else-if="secretCode === '260410'" class="secret-content">
      <h1 class="highlight-text" style="color: #fbbf24;">⚖️ 神之天平的隐秘画卷</h1>
      <p class="subtitle">特殊代码认证：260410</p>
      <div class="content-box">
        <p>这里是《神之天平》的专属展示页面。</p>
        <p>（后续内容待设计：留给这款让你印象深刻的游戏...）</p>
      </div>
      <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
    </div>

    <!-- ★★★ 新增：薇尔莉特专属暗号 -->
    <div v-else-if="secretCode === '19xxxx'" class="secret-content">
      <h1 class="highlight-text" style="color: #c084fc;">✉️ 无名信件的归宿</h1>
      <p class="subtitle">特殊代码认证：19xxxx</p>
      <div class="content-box">
        <p>这里是薇尔莉特为你寄来的专属信件空间。</p>
        <p>（后续内容待设计：可以放入你想展示的动漫截图、感人信件文本等...）</p>
      </div>
      <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
    </div>

    <!-- ★★★ 新增：音乐聊天助手专属暗号 -->
    <div v-else-if="secretCode === '240802'" class="secret-content">
      <h1 class="highlight-text" style="color: #f472b6;">🎧 灵魂的音乐电台</h1>
      <p class="subtitle">特殊代码认证：240802</p>
      <div class="content-box">
        <p>这里是音乐推荐助手的专属收藏夹。</p>
        <p>（后续内容待设计：可以在这里嵌入你喜欢的歌曲列表，比如“会呼吸的痛”、“虚拟”等...）</p>
      </div>
      <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
    </div>

    <!-- ★★★ 新增：游戏聊天助手专属暗号 -->
    <div v-else-if="secretCode === '180818'" class="secret-content">
      <h1 class="highlight-text" style="color: #34d399;">🕹️ 隐藏的数字绿洲</h1>
      <p class="subtitle">特殊代码认证：180818</p>
      <div class="content-box">
        <p>这里是游戏聊天助手的专属基地。</p>
        <p>（后续内容待设计：可以放入你的游戏截图库、通关纪念截图、或者是成就墙...）</p>
      </div>
      <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
    </div>

    <div v-else class="secret-content">
      <h1 class="highlight-text">🎉 恭喜你找到了第一个特殊页面！</h1>
      <p>但是这里什么都没有，如果你后面发现了其他特殊的数字，可以试一试在对话框里输入</p>
      <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
    </div>

  </div>
</template>

<script setup>
defineProps({
  secretCode: {
    type: String,
    default: ''
  }
})

defineEmits(['back'])
</script>

<style scoped>
.secret-page {
  width: 90vw;
  max-width: 800px;
  padding: 60px;
  text-align: center;
  border-radius: 24px;
  z-index: 100;
  color: white;
}
.secret-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.highlight-text {
  margin-bottom: 10px;
  font-size: 28px;
}
.subtitle {
  color: #94a3b8;
  font-family: monospace;
  margin-bottom: 30px;
  letter-spacing: 2px;
}
.content-box {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 40px;
  border-radius: 16px;
  margin-bottom: 40px;
  width: 100%;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
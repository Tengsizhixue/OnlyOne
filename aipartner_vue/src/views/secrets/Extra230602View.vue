<template>
  <SecretLayout
    bg-image=""
    title="？？？？"
    title-color="#cbd5e1"
    code="？？？？"
    hide-quest-widget
    @back="$emit('back')"
    v-slot="{ back }"
  >
    <div class="monologue-room">
      <div class="prose-content">
        <p class="fade-in-text" style="animation-delay: 0.1s;">
          后面两年基本没什么事，或者是我真的想不起来我做过了什么，没去争论初中的事情倒不倒霉，也不想讨论那次住院对我有什么影响，也懒得再去做一些其他的事，因为在我印象中，为了防止再出现类似的事，我对一件事情有想法的话都不会立刻去做，而是等个1,2天再去做，这样能防止我大脑应激。
        </p>
        <p class="fade-in-text" style="animation-delay: 0.3s;">
          其实18年到23年的事都是连在一块的，连锁反应，在前几年我还是蛮开心的，但后面那四年我认为最贴合我的一个词是“压抑”，现在你应该知道了我为什么要说“真正的生活不该只有单程票，它既需要重逢的信念，也需要放手的勇气，更需要与自己和解的气概”因为在那四年里面，我一个都没做到，
        </p>
        <p class="fade-in-text" style="animation-delay: 0.5s;">
          如果从一开始，我就不去纠结住院与倒霉这些事，那初中对我来说，本就是一个圆满的结局——用几年的努力，换来一张通往理想高中的票。至少像《去月球》里的老约翰那样，在记忆的尽头，与不完美的人生达成和解。
        </p>
        <p class="fade-in-text" style="animation-delay: 0.7s;">
          如果我能意识到，有些事值得坚持到底，那么即便结局不尽如人意，我也能换来一张写满"我经历过"的票。就像《我在7年后等着你》里那样——只要努力过，便不算辜负。
        </p>
        <p class="fade-in-text" style="animation-delay: 0.9s;">
          如果我能懂得，有些事应该放手，那我早已卸下重担，轻松换取一张通往解脱与自由的票。如同《灵魂摆渡者》教会我的：告别不是终点，而是旅途中的另一段风景。
        </p>

      </div>

      <div class="bottom-action fade-in-text" style="animation-delay: 1.2s;">
        <button class="shimmer-btn quiet-btn" @click="back">返回聊天</button>
      </div>
    </div>
  </SecretLayout>
</template>

<script setup>
import SecretLayout from '../../components/SecretLayout.vue'
defineEmits(['back'])
</script>

<style scoped>
.monologue-room {
  width: 100%; flex: 1; display: flex; flex-direction: column; align-items: center;
  overflow-y: auto; overflow-x: hidden; padding-right: 4px; box-sizing: border-box;
}
.monologue-room::-webkit-scrollbar { width: 6px; }
.monologue-room::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.3); border-radius: 4px; }

.prose-content {
  width: 100%; max-width: 680px; padding: 20px 0 40px 0; text-align: left;
}
.prose-content p {
  font-family: 'Noto Serif SC', 'ZCOOL XiaoWei', "STKaiti", "KaiTi", serif;
  font-size: 16px; line-height: 2.2; color: #cbd5e1; margin-bottom: 24px; text-indent: 2em;
  text-shadow: 0 1px 2px rgba(0,0,0,0.5); letter-spacing: 0.5px;
}

.fade-in-text {
  opacity: 0; transform: translateY(10px) scale(0.98); filter: blur(2px);
  animation: gentle-fade 1.2s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
}

@keyframes gentle-fade {
  to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}

.quiet-btn {
  background: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: #cbd5e1 !important; box-shadow: none !important; letter-spacing: 2px; transition: all 0.4s ease;
}
.quiet-btn:hover {
  background: rgba(255, 255, 255, 0.15) !important; color: #fff !important;
  border-color: rgba(255, 255, 255, 0.3) !important; transform: translateY(-2px);
}
.bottom-action { margin-top: 20px; display: flex; justify-content: center; }

@media (max-width: 768px) {
  .prose-content { padding: 10px 10px 30px 10px; }
  .prose-content p { font-size: 15px; line-height: 2; margin-bottom: 20px; }
}
</style>
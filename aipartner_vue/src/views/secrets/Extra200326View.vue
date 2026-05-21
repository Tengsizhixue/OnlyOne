<template>
  <SecretLayout
    bg-image=""
    title="？？？？"
    title-color="#cbd5e1"
    code="200326"
    hide-quest-widget
    @back="$emit('back')"
    v-slot="{ back }"
  >
    <div class="monologue-room">
      <div class="prose-content">
        <p class="fade-in-text" style="animation-delay: 0.1s;">
          前面的那些页面都是以年月日来命名的，中间我空了4年没有讨论，其实原本就是不打算写的，这个网站也是到此结束的。我不推荐你看1是因为这段时间对于我来说过于复杂了，具体事情你不了解，说了也没有意义，你还可能根本就看不懂。
          2是因为这些内容可能并不算是正能量，我不想被挂上卖惨的标签，但是已经写了这么多了，你也愿意看，那我再多写一点也无所谓。相信你也看完了一开始那三款游戏（七年后、灵魂摆渡、去月球）的页面，这个页面更像是写给2020年的我的一份寄语。如果2020年的3月我懂得那些大道理的话，那后面四年应该变成我青春最美好的时候。
        </p>
        <p class="fade-in-text" style="animation-delay: 0.3s;">
          但很可惜，那时候我不懂得如何与自己和解，也不知道哪些事情需要坚持哪些事情需要放弃，具体的事我就不聊了，简单来说就是18年-20年只是有点倒霉，但是那时候我比较单纯，比较完美主义，认为付出就一定有回报，以现在的目光看，确实是有回报的，但当时我并没有发现，我把所有的注意力都放在了20年3月的那次住院。客观来说原本并不算什么大事，但那件事对我心理上面的影响其实很大，直到21年的5月我才彻底不想谈论这件事，尤其是和家人，我都极其避免谈论高中以前的任何事情，之后的很长时间可以说我都活在那次住院的阴影之下。
        </p>
        <p class="fade-in-text" style="animation-delay: 0.5s;">
          其实那年按结果来说并不算差，因为有一个能去县里面最好的高中名额，但我当时真的完全不在意，经过那次住院后我就不想给自己压力，上个普通高中就行了，好的高中竞争太大离家也远，而且认为什么事情都不做就不会遇到任何烦恼，当时我就一直认为自己很倒霉，为什么很多倒霉的事情都会给我遇见，自己已经很努力了还是避免不了。
        </p>
        <p class="fade-in-text" style="animation-delay: 0.7s;">
          在小时候别人认为我内向，不怎么说话，我其实尝试过去做一些更加外向的事，18、19年是我最外向的时候了，很多活动我都愿意主动去参与，和外面的陌生人也愿意聊，但自从那次住院后，我就开始变得敏感，甚至后来直接封闭自我，对很多事变得极其保守，而且我认为对待别人冷漠可以省很多事，我的行为逻辑可以用一句话来概括“身边环境的稳定大于一切”。
        </p>
      </div>

      <div class="bottom-action fade-in-text" style="animation-delay: 1.0s;">
        <button class="shimmer-btn quiet-btn" @click="back">返回前言</button>
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
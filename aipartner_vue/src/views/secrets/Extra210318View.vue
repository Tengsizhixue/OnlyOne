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
          可能会有人认为我高中很倒霉，我其实不太认同。我不喜欢高中并不是因为我遇到了什么人，遇到了什么事，而是这一切都是因为那次住院而起，一并给我留下了很多不好的回忆。在高一我的主要矛盾是和家人争论去县里面最好的高中上学是不是对的，这件事我真的和家人吵了一年多，我只想在一所普通的高中里面摆烂。你们可能不理解，但其实那时候我的精神状态很不好，大脑不想动，那几年我的思想都很奇葩，遇到事情不是去解决而是丢弃大脑放弃思考，这就是别人最不能理解我的地方，我遇见一件麻烦事不是努力解决而是想着怎么快速让这件事情结束。
        </p>
        <p class="fade-in-text" style="animation-delay: 0.3s;">
          我举个很简单的例子，在那时候我喜欢别人，但被对方知道了，我第一反应不是追，我想的是直接跟对方爆了，然后对方肯定不喜欢我，这件事情就结束了。我现在肯定是知道这么干就是脑子有病，但当时我就是这么想的，根本就没有考虑过后果，后面的事情很多人都知道了，我就不再多说了，单论这件事，并不是我倒霉，而是对方倒霉才对，对方正常上个学遇到个脑残。
        </p>
        <p class="fade-in-text" style="animation-delay: 0.5s;">
          再说另一件事，高中同学经常聊你东哥，很多人认为我当时和你东哥坐在一起完全就是倒霉，但我当时完全可以不搭理他，就像高三那样，座位分在一块直接搬走就行了，但是我却选择了什么事情都和他说，什么事都相信他，我当时真的看不出来他是什么性格的人吗？只不过是因为前几年在初中不怎么想和那几个同学聊天，高中想多聊聊而已，只不过没猜到后面会发生什么样的事。
        </p>
        <p class="fade-in-text" style="animation-delay: 0.7s;">
          不过有件事我倒是可以确定，他的确是我见过最神的人，这么多年过去了，我依旧没有找到有一个和他相似的人，不过我也真的不想遇到就是了。
        </p>
      </div>

      <div class="bottom-action fade-in-text" style="animation-delay: 1.0s;">
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
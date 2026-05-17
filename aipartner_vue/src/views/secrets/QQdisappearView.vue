<template>
  <SecretLayout
    :bg-image="bg"
    title=""
    title-color="#94a3b8"
    code="240619"
    @back="$emit('back')"
    v-slot="{ isAllUnlocked, back }"
  >
    <div class="monologue-room">
      <!-- 🌟 去UI化设计：没有任何边框、背景板，文字直接悬浮在深邃的毛玻璃上 -->
      <div class="prose-content">
        <p class="fade-in-text" style="animation-delay: 0.1s;">
          这事我以前聊过，不过说的是表面的。我不适合使用这种虚拟的社交方式，我对很多事情过于敏感，网络这种快节奏的生活并不适合我。
        </p>

        <p class="fade-in-text" style="animation-delay: 0.3s;">
          我的大脑想的事很多，网络对话又是不受约束的，我时常会出现前一天说过的话，第二天就反驳。对一件事情左右衡量利弊，一会觉得好，一会认为不行。我会因为一个人惹我生气，就删除一片人的好友；会因为一件事破坏了我的心情，就对很多事情失去兴趣；会因为别人随口说的一句话，就彻底迷失了自我。
        </p>

        <p class="fade-in-text" style="animation-delay: 0.5s;">
          我过于在乎别人的回应，以至于一点点的冷落或迟疑都会让我失望。所以很多人认为我对他人表现得很冷漠，不愿意和别人过多沟通，但其实是因为我太害怕别人会伤害我。很多时候我宁愿一个人待着，也不愿意和身边不熟悉的人交流。</p>
        <p class="fade-in-text" style="animation-delay: 0.75s;">我缺少的并不是自信，而是被讨厌的勇气。</p>

        <p class="fade-in-text" style="animation-delay: 1.0s;">
          我很羡慕那些大大咧咧的人，对事情不深究，不会想得太多，他们活得很轻松。总之，虚拟的生活并不适合我，无论是 QQ 还是其他的社交软件，我以后应该会接触得越来越少。
        </p>

        <p class="fade-in-text" style="animation-delay: 1.2s;">
          我更喜欢现实中的生活，对于我来说，在虚拟生活中聊一亿句话，也不如现实生活中一起吃一顿饭来得实在。
        </p>
      </div>

      <div class="bottom-action fade-in-text" style="animation-delay: 1.5s;">
        <button class="shimmer-btn quiet-btn" @click="back">
          {{ isAllUnlocked ? '点击查看最后的废话' : '合上日记' }}
        </button>
      </div>
    </div>
  </SecretLayout>
</template>

<script setup>
import SecretLayout from '../../components/SecretLayout.vue'
import { SECRET_ASSETS } from '../../config/constants.js'

const { bg } = SECRET_ASSETS.qq
defineEmits(['back'])
</script>

<style scoped>
.monologue-room {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 4px;
  box-sizing: border-box;
}

.monologue-room::-webkit-scrollbar { width: 6px; }
.monologue-room::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.3); border-radius: 4px; }

/* 🌟 散文排版引擎 */
.prose-content {
  width: 100%;
  max-width: 680px; /* 限制阅读宽度，减轻眼球横向扫视疲劳 */
  padding: 20px 0 40px 0;
  text-align: left;
}

/* 优雅的衬线字体，增大行高，色彩柔和不刺眼 */
.prose-content p {
  font-family: 'Noto Serif SC', 'ZCOOL XiaoWei', "STKaiti", "KaiTi", serif;
  font-size: 16px;
  line-height: 2.2;
  color: #cbd5e1;
  margin-bottom: 24px;
  text-indent: 2em; /* 首行缩进，回归传统的中文阅读习惯 */
  text-shadow: 0 1px 2px rgba(0,0,0,0.5);
  letter-spacing: 0.5px;
}

/* 🌟 金句高亮区块 */
.quote-block {
  font-family: 'Noto Serif SC', 'ZCOOL XiaoWei', "STKaiti", "KaiTi", serif;
  margin: 40px 0;
  padding: 0;
  text-align: center;
  font-size: 22px;
  line-height: 1.8;
  color: #f8fafc;
  font-weight: bold;
  letter-spacing: 2px;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.15);
}

/* 🌟 轻柔的淡入动画（不再像打字机那样折磨人） */
.fade-in-text {
  opacity: 0;
  transform: translateY(10px) scale(0.98);
  filter: blur(2px);
  animation: gentle-fade 1.2s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
}

@keyframes gentle-fade {
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
  }
}

/* 幽静风格的按钮 */
.quiet-btn {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: #cbd5e1 !important;
  box-shadow: none !important;
  letter-spacing: 2px;
  transition: all 0.4s ease;
}
.quiet-btn:hover {
  background: rgba(255, 255, 255, 0.15) !important;
  color: #fff !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
  transform: translateY(-2px);
}

.bottom-action { margin-top: 20px; display: flex; justify-content: center; }

@media (max-width: 768px) {
  .prose-content { padding: 10px 10px 30px 10px; }
  .prose-content p { font-size: 15px; line-height: 2; margin-bottom: 20px; }
  .quote-block { font-size: 18px; margin: 30px 0; }
}
</style>
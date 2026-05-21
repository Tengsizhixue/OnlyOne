<template>
  <SecretLayout
    :bg-image="bg"
    title="📱 你发现了李红宝的失联空间"
    title-color="#60a5fa"
    code="260315"
    @back="$emit('back')"
    v-slot="{ openImage, back }"
  >
    <div class="story-box">
      <p>有次给他发消息，半天不回，然后说是苹果手机问题没信息提醒，说下次要@他。结果后面@他了，到第二天才回，还说是苹果手机问题，收不到消息，真的不是他的问题，实则只是开了免打扰。</p>
      <img :src="img1" alt="李红宝插图" class="content-img" />
      <p>(上面的内容只是开个玩笑）</p>
      <p>我基本都是在群聊里面说话，很少和别人私聊。就算在现实里面关系很好的朋友，我也几乎不在网上聊天</p>

      <div class="redacted-block">
        <p>因为我有点轻度焦虑，只要别人不回我消息，我就会越来越急，在群里面发消息，就算一个人有事，其他人也会回我。</p>
        <p>你可能会跟我说，别人不发消息可能是因为有事在忙。我当然知道，不然我怎么和朋友都不在网上单独聊，我单纯就是急，和别人是怎么想的完全没关系。对我来说，这就是一种本能反应，另外就是我很懒，一件事要么行，要么不行，我懒得等。不过在现实生活里我对这方面倒是无所谓的态度，除非有人过于磨叽了，讲个话左脑攻击右脑</p>
      </div>
      <p>我不怎么在网上聊天还有一个原因就是我不玩网游，这方面的我应该后面还会再提。</p>

      <div class="bottom-action">
        <button class="shimmer-btn" @click="back">返回前言</button>
      </div>
    </div>
  </SecretLayout>
</template>

<script setup>
import { Picture } from '@element-plus/icons-vue'
import SecretLayout from '../../components/SecretLayout.vue'
import { SECRET_ASSETS } from '../../config/constants.js'
const { bg, img1 } = SECRET_ASSETS.lihongbao
defineEmits(['back'])
</script>

<style scoped>
.story-box { background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(96, 165, 250, 0.2); padding: 30px; border-radius: 16px; margin-bottom: 30px; width: 100%; text-align: left; box-shadow: 0 10px 30px rgba(0,0,0,0.1); flex: 1; overflow-y: auto; }
.story-box::-webkit-scrollbar { width: 8px; }
.story-box::-webkit-scrollbar-track { background: transparent; }
.story-box::-webkit-scrollbar-thumb { background: rgba(96, 165, 250, 0.3); border-radius: 4px; }
.story-box::-webkit-scrollbar-thumb:hover { background: rgba(96, 165, 250, 0.6); }
.story-box p { font-size: 16px; line-height: 2; margin-bottom: 16px; color: #f8fafc; text-indent: 2em; }
.story-box p:last-child { margin-bottom: 0; }
.redacted-block { position: relative; margin-bottom: 16px; }
.redacted-block::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(135deg, rgba(20, 20, 25, 0.95) 0%, rgba(10, 10, 15, 0.98) 50%, rgba(5, 5, 10, 1) 100%); border-radius: 8px; z-index: 10; backdrop-filter: blur(8px); }
.redacted-block::after { content: '[去除了废话，这里BB太多了，我自己都看不下去]'; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: rgba(255, 255, 255, 0.6); font-size: 14px; font-weight: 600; z-index: 11; letter-spacing: 2px; }
.content-img { width: 100%; max-width: 600px; border-radius: 12px; margin: 16px auto; display: block; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4); }
.extra-links { margin-top: 24px; padding-top: 16px; border-top: 1px dashed rgba(96, 165, 250, 0.3); display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.links-label { font-size: 14px; color: #bfdbfe; font-weight: 600; }
.img-link { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(96, 165, 250, 0.1); border: 1px solid rgba(96, 165, 250, 0.3); color: #eff6ff; text-decoration: none; border-radius: 20px; font-size: 13px; transition: all 0.3s ease; cursor: pointer; }
.img-link:hover { background: rgba(96, 165, 250, 0.25); border-color: rgba(96, 165, 250, 0.6); color: #fff; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(96, 165, 250, 0.2); }
.bottom-action { margin-top: 40px; display: flex; justify-content: center; }
@media (max-width: 768px) {
  .story-box { padding: 18px; font-size: 14px; margin-bottom: 20px; border-radius: 12px; line-height: 1.8; }
  .extra-links { margin-top: 16px; padding-top: 12px; }
  .img-link { padding: 5px 12px; font-size: 12px; }
}
</style>
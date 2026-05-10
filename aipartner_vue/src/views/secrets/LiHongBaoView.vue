<template>
  <SecretLayout
    bg-image="https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E6%9D%8E%E7%BA%A2%E5%AE%9D%E8%83%8C%E6%99%AF%E5%9B%BE.png"
    title="📱 你发现了李红宝的失联空间"
    title-color="#60a5fa"
    code="260315"
    @back="$emit('back')"
    v-slot="{ openImage }"
  >
    <div class="story-box">
      <p>有次给他发消息，半天不回，然后说是苹果手机问题没信息提醒，说下次要@他。结果后面@他了，到第二天才回，还说是苹果手机问题，收不到消息，真的不是他的问题。</p>
      <img src="https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E6%9D%8E%E7%BA%A2%E5%AE%9D%E6%8F%92%E5%9B%BE1.png" alt="李红宝插图" class="content-img" />
      <p>(上面的内容只是开个玩笑）</p>
      <p>我基本都是在群聊里面说话，很少和别人私聊。就算在现实里面关系很好的朋友，我也几乎不在网上聊天，
        因为我有点轻度焦虑，只要别人不回我消息，我就会越来越急，在群里面发消息，就算一个人有事，其他人也会回我。</p>
      <p>你可能会跟我说，别人不发消息可能是因为有事在忙。我当然知道，
        不然我怎么和朋友都不在网上单独聊，我单纯就是急，和别人是怎么想的完全没关系。
        对我来说，这就是一种本能反应，另外就是我很懒，一件事要么行，要么不行，我懒得等。
        不过在现实生活里我对这方面倒是无所谓的态度，除非有人过于磨叽了，讲个话左脑攻击右脑</p>
      <p>我不怎么在网上聊天还有一个原因就是我不玩网游，这方面的我应该后面还会再提。</p>
    </div>
  </SecretLayout>
</template>

<script setup>
import { Picture } from '@element-plus/icons-vue'
import SecretLayout from '../../components/SecretLayout.vue'

defineEmits(['back'])
</script>

<style scoped>
.story-box {
  background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(96, 165, 250, 0.2);
  padding: 30px; border-radius: 16px; margin-bottom: 30px; width: 100%; text-align: left;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  flex: 1; overflow-y: auto;
}
.story-box::-webkit-scrollbar { width: 8px; }
.story-box::-webkit-scrollbar-track { background: transparent; }
.story-box::-webkit-scrollbar-thumb { background: rgba(96, 165, 250, 0.3); border-radius: 4px; }
.story-box::-webkit-scrollbar-thumb:hover { background: rgba(96, 165, 250, 0.6); }

.story-box p { font-size: 16px; line-height: 2; margin-bottom: 16px; color: #f8fafc; text-indent: 2em; }
.story-box p:last-child { margin-bottom: 0; }

.content-img {
  width: 100%; max-width: 600px; border-radius: 12px;
  margin: 16px auto; display: block; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.extra-links {
  margin-top: 24px; padding-top: 16px; border-top: 1px dashed rgba(96, 165, 250, 0.3);
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
}
.links-label { font-size: 14px; color: #bfdbfe; font-weight: 600; }
.img-link {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px;
  background: rgba(96, 165, 250, 0.1); border: 1px solid rgba(96, 165, 250, 0.3);
  color: #eff6ff; text-decoration: none; border-radius: 20px; font-size: 13px;
  transition: all 0.3s ease; cursor: pointer;
}
.img-link:hover {
  background: rgba(96, 165, 250, 0.25); border-color: rgba(96, 165, 250, 0.6);
  color: #fff; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(96, 165, 250, 0.2);
}

@media (max-width: 768px) {
  .story-box { padding: 18px; font-size: 14px; margin-bottom: 20px; border-radius: 12px; line-height: 1.8; }
  .extra-links { margin-top: 16px; padding-top: 12px; }
  .img-link { padding: 5px 12px; font-size: 12px; }
}
</style>
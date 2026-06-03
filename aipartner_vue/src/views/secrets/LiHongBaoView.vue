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
        <p>在说明原因之前我先说个小故事，有的人应该知道。初中那时候，玩的一款名字叫幻想三国的游戏，
          闲着无聊，在游戏里面创了个女角色，因为这个游戏是偏社交的，什么交易，单挑，拜师什么的，
          就是我装成女的和别人去聊天，具体怎么装的我都忘了，反正不知道怎么和一个人聊起来了，后面说要加QQ
          我就装我没QQ，让他教我创QQ，后面他还真帮我创了一个。那人还挺好，在游戏里面给我了很多东西。
          这游戏里面是有骗子的，那时候我就被一个人骗了，装备什么的全被骗走，那个男的知道后，我不记得是他
          找对面买回来的，还是他自己打的一套装备，反正至少值个几十块吧，就送给我了，当时我是没在意的，因为我就是
          装异性骗人玩玩。就是差不多过来半个月吧，他问我是不是骗他，我一开始以为是被发现了，结果他问我是不是学生
          ，因为我上学都是中午和晚上玩，后来我具体怎么聊的已经不记得了，反正对面好像也没管。有天跟他聊天，
          聊老家是哪的，聊到最后最离谱的来了，发现是一个镇上的。是真的一个镇上的，我这时候发现情况不对，想着跑路了
          。我虽然不记得后面具体聊了些什么，反正我就是跑路了，游戏没登，那个QQ号也甩了，我记得他还发给我钱，
          不记得为什么发我钱 （没记错是50块钱，因为我对50块钱印象还是蛮深的，小时候买充值卡被骗了50，
          我同学当场给我50安慰我 还有就是后面关于高中50块钱话费的事，这个就不聊了，聊着尴尬）虽然我是无聊装异性逗人玩，
          但我还是有良心的，没收他钱，就这样我以为一场恶作剧就结束了。
        </p>
        <p>过了好几年，我已经上高中了，想起来这款以前玩的游戏，就想着登上去看看，这游戏不是能结婚嘛，
        然后我看配偶那一栏还是他，不过他也没玩了，离线了很久，但是他那个游戏签名叫“我一直等你回来”。
        虽然对我来说真的很难绷啊，我就是装异性逗他玩的，他到最后都没发现我是个男的，不过不知道是最好的结局，哈哈。</p>
        <p>小故事说完了，现在聊聊为什么我最近都不在网上聊天的原因。</p>
        <p>1是因为自从一些事情之后我变得有些焦虑，网络这种只能通过文字进行沟通，看不出对方表情，
        看不出来对方真实情感的社交方式会让我非常着急，对方可能因为有一些事情，暂时没有回消息，我却非常着急，
        就算是关系好的朋友，我也会很急。除非是真有事，一般有群聊我都是在群里面说话，因为一个人有时，其他人也会回我。</p>
        <p>2是因为我害怕自己的意思会被误解，有时候我聊天会说一大堆，但是对方有时根本就没看懂我什么意思，
        然后我又会特别急，想着去解释，最后越聊越乱。</p>
        <p>3是因为对现在的我来说网络社交没有意义，现实里面关系好的，就算不在网上聊天也差不到哪去，
        关系不好的，就算网上聊的再多，不在现实里面聊天也没用。我从来没有因为网上聊得好，而在现实里面交朋友的情况
        在高中以前我确实有关系很好的网友，但我的QQ和微信都注销重新换过，所以那些网友也早就不存在了。</p>
        <p>4是因为网上的有些事情给我留下了非常不好的印象</p>
      </div>
      <p>我不怎么在网上聊天还有一个原因就是我不玩网游，这方面的我应该后面还会再提。</p>

      <div class="bottom-action">
        <button class="shimmer-btn" @click="back">返回前言</button>
      </div>
    </div>
  </SecretLayout>
</template>

<script setup>
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
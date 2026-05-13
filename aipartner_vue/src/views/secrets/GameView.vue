<template>
  <SecretLayout
    :bg-image="''"
    title="游戏的极端"
    title-color="#f87171"
    code="180818"
    @back="$emit('back')"
    v-slot="{ openImage, isAllUnlocked, back }"
  >
    <div class="gamer-room">
      <div class="story-box cyberpunk-theme">

        <div class="manifesto">
          <div class="manifesto-title">我这辈子都不会干这么几件事：</div>
          <span class="highlight-item">1. 玩 EA 的任何游戏</span><br>
          <span class="highlight-item">2. 玩 PVP 网游（线下找我玩除外）</span>
        </div>

        <p>
          EA 是我见过最恶心的游戏厂家了，我和 EA 客服的关系就像是18世纪黑人和白人的关系。EA 的脑残客服我到现在都记得，太恶心了，
          就故意戏弄你。之前把 QQ 注销了，但是我很多游戏绑定的都是 QQ 邮箱，基本没换绑。 有且仅有EA 这个厂商，问你一堆莫名其妙的问题：
          什么你几岁了？哪年出生的？然后最后来一句“你的回答已经很接近正确答案了”🙄。
          而且ea的手机端网页有bug，根本就不能通过手机网页来找客服，ea只有国外的客服，那时候我电脑还没折腾魔法，找半天找个免费软件，每天还只能免费用15分钟。
          而且花了这仅有的15分钟品尝了一顿完美的💩，哦不对，不止一遍，我在两年时间里找了5次ea的客服，只有一个客服态度还不错，但也没用。
        </p>

        <p>
          每次对话都搞几十分钟，然后故意恶心你一句，我花钱买的游戏还要证明我为什么是我，其他的厂商完全就没有这个问题，把购买账单发过去就帮你换绑了。
        </p>

        <div class="glitch-divider">
          <span class="glitch-line long"></span>
          <span class="glitch-line short"></span>
          <span class="glitch-line long"></span>
        </div>

        <p>
          其实在初中我还是很喜欢玩 PVP 游戏的，那时候右手摔骨折了都要打王者，我朋友还开玩笑说绑着石膏还拿了个五杀。在 20 年后我基本就慢慢开始远离网游了，玩也只玩辅助类的角色，主要是没有像和初中同学的那种感觉了。
        </p>

        <p>
          我彻底不玩是在去年差不多这时候，有天我打开《三角洲》，匹配了一把，匹到两个队友，因为抢一个东西，从头吵到尾。听着我非常烦，因为我原本那天上了一天课，晚上只想娱乐娱乐，越玩越烦人。
        </p>

        <p>
          对我来说网游唯一的价值就是能和朋友一起玩，打得好别人说你开挂，打的差有人骂你菜。
          我原本就是娱乐的，不如玩玩单机或者 PVE 游戏。打的不高兴就直接载入存档重新打，还打不过直接删游戏换一个游戏，我只想让自己高兴。
          所以除非是线下大家聚在一起，不然我真的不想打开pvp网游。
        </p>

        <p>
          这也是我最近不怎么在网上聊天的一个原因，因为我朋友很多都是玩 PVP 的，毕竟玩游戏有时候就是聊聊天，但我真的是玩不下去了。
        </p>

        <div class="glitch-divider">
          <span class="glitch-line short"></span>
          <span class="glitch-line long"></span>
          <span class="glitch-line short"></span>
        </div>

        <img :src="img1" alt="骑马与砍杀" class="content-img"/>

        <p>
          现在应该说说我最喜欢的了，《骑马与砍杀》。
        </p>

        <p>
          这游戏陪了我很久很久，我小时候很少能接触到电脑，在小学 4、5 年级的时候看到我哥电脑上有这款游戏，可以说是一见钟情。我童年最大的愿望就是能有一台电脑去玩骑马与砍杀，那几年基本上能碰到电脑，我都要试一试这个电脑能不能玩。
        </p>

        <p>
          这个愿望直到我高考后才实现，我早就买了正版的游戏，但直到很多年才在属于自己的电脑上打开。
        </p>

        <p>
          这个游戏本体内容倒是没多少，主要是无私的 mod 作者，制作了很多好玩的 mod。
          虽然以现在的目光来看游戏画质很差，操作很僵硬，但我有空余时间依然愿意打开它，它也给我带来了很多美好的记忆，
          如果给我玩过的游戏排名的话，这游戏永远都是我心目中的第一名。
        </p>

        <div class="extra-links">
          <span class="links-label">🔗 附加内容：</span>
          <span @click="openImage(attach1)" class="img-link">
            <el-icon><Picture /></el-icon> 游戏时长
          </span>
          <span @click="openImage(attach2)" class="img-link">
            <el-icon><Picture /></el-icon> 以前相关评论
          </span>
        </div>

        <div class="bottom-action">
          <button class="shimmer-btn" @click="back">
            {{ isAllUnlocked ? '点击查看最后的废话' : '返回聊天' }}
          </button>
        </div>

      </div>
    </div>
  </SecretLayout>
</template>

<script setup>
import { Picture } from '@element-plus/icons-vue'
import SecretLayout from '../../components/SecretLayout.vue'
import { SECRET_ASSETS } from '../../config/constants.js'

const { img1, attach1, attach2 } = SECRET_ASSETS.game
defineEmits(['back'])
</script>

<style scoped>
/* 样式保持不变 */
.gamer-room { width: 100%; flex: 1; display: flex; flex-direction: column; overflow-y: auto; overflow-x: hidden; padding-right: 4px; box-sizing: border-box; }
.gamer-room::-webkit-scrollbar { width: 6px; }
.gamer-room::-webkit-scrollbar-track { background: transparent; }
.gamer-room::-webkit-scrollbar-thumb { background: rgba(239, 68, 68, 0.4); border-radius: 4px; }
.gamer-room::-webkit-scrollbar-thumb:hover { background: rgba(239, 68, 68, 0.8); }
.cyberpunk-theme { background: rgba(9, 9, 11, 0.85); border: 1px solid rgba(239, 68, 68, 0.3); border-left: 4px solid #ef4444; box-shadow: 0 10px 40px rgba(0,0,0,0.8), inset 0 0 20px rgba(239, 68, 68, 0.08); padding: 40px; border-radius: 8px; margin-bottom: 24px; width: 100%; text-align: left; flex: none; overflow: visible; box-sizing: border-box; word-wrap: break-word; }
.manifesto { background: linear-gradient(90deg, rgba(239, 68, 68, 0.15), transparent); border-left: 3px solid #f87171; padding: 16px 20px; border-radius: 0 8px 8px 0; margin-bottom: 30px; }
.manifesto-title { font-size: 16px; font-weight: bold; color: #fca5a5; margin-bottom: 8px; }
.highlight-item { display: inline-block; margin-top: 6px; font-weight: 600; color: #fee2e2; letter-spacing: 0.5px; }
.cyberpunk-theme p { font-size: 15px; line-height: 2.1; margin-bottom: 20px; color: #e2e8f0; text-indent: 2em; text-shadow: 0 1px 2px rgba(0,0,0,0.9); letter-spacing: 0.5px; }
.cyberpunk-theme strong { color: #f87171; padding: 0 2px; }
.glitch-divider { display: flex; align-items: center; justify-content: center; gap: 6px; margin: 36px 0; opacity: 0.7; }
.glitch-line { height: 2px; background: #ef4444; box-shadow: 0 0 8px #ef4444; }
.glitch-line.long { width: 60px; }
.glitch-line.short { width: 12px; }
.content-img { width: 100%; max-width: 600px; border-radius: 8px; border: 1px solid rgba(239, 68, 68, 0.4); margin: 10px auto 24px auto; display: block; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), 0 0 15px rgba(239, 68, 68, 0.1); cursor: pointer; transition: transform 0.3s ease; }
.content-img:hover { transform: scale(1.02); border-color: rgba(239, 68, 68, 0.8); }
.extra-links { margin-top: 32px; padding-top: 20px; border-top: 1px dashed rgba(239, 68, 68, 0.4); display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.links-label { font-size: 14px; color: #fca5a5; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
.img-link { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #fee2e2; text-decoration: none; border-radius: 20px; font-size: 13px; transition: all 0.3s ease; cursor: pointer; backdrop-filter: blur(4px); }
.img-link:hover { background: rgba(239, 68, 68, 0.3); border-color: #ef4444; color: #fff; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3); }

.bottom-action { margin-top: 40px; display: flex; justify-content: center; }

@media (max-width: 768px) {
  .cyberpunk-theme { padding: 20px 16px; margin-bottom: 20px; }
  .cyberpunk-theme p { font-size: 14px; line-height: 1.9; margin-bottom: 16px; }
  .manifesto { padding: 12px 16px; margin-bottom: 24px; }
  .manifesto-title { font-size: 15px; }
  .glitch-divider { margin: 24px 0; }
  .glitch-line.long { width: 40px; }
  .content-img { margin: 10px auto 20px auto; }
  .extra-links { margin-top: 20px; padding-top: 16px; }
  .img-link { padding: 5px 12px; font-size: 12px; }
}
</style>
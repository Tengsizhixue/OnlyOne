<template>
  <!-- 💡 核心修复：添加 v-slot="{ openImage }" -->
  <SecretLayout
    bg-image="https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?auto=format&fit=crop&w=2000&q=80"
    title="⚖️ 神之天平的隐秘画卷"
    title-color="#fbbf24"
    code="260410"
    @back="$emit('back')"
    v-slot="{ openImage }"
  >
    <div class="story-box">
      <img src="https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E5%A4%A9%E5%B9%B3%E5%B0%81%E9%9D%A2.png" alt="天平封面" class="content-img" />

      <p>《神之天平》的开篇并不复杂，甚至可以说是一种刻意的朴素：主角与青梅竹马阿努莉丝在突如其来的魔物袭击中失散，当他从昏迷中醒来时，身边只剩一只不知为何会说话的乌鸦。旅途中，他意外获得了一件能够穿越时空的神器。仅看这段开场，故事的前半段似乎只是一套我们再熟悉不过的模板——打倒魔王、拯救爱人、然后迎来大团圆。一切都像是某种令人安心的、被无数作品验证过的古典英雄叙事。</p>
      <p>然而这种安心的错觉，恰恰是游戏最先开始瓦解的东西。</p>
      <p>和《我在7年后等着你》一样，本作的核心也是“穿越”时空。但两者的“穿越”在底色上存在着本质的不同。这里的每一次回溯都不是轻巧的跳跃，你无法毫无负担地回到过去某个节点去修修补补。这里的法则是无情的等价交换：你想要得到什么，就必须献上同等重量的事物来交换。那不是写在契约上的漂亮话，而是每一次发动能力时，天平都实实在在地称量着你的决意。</p>
      <p>你不是一个置身事外的观众，你亲手做出抉择，又被迫目睹每一个选择引发的连锁反应——有时候，出于绝对的善意伸出援手，却结出意想不到的恶果；有时候，试图拯救某样重要之物，却注定伴随着另一种难以承受的失去。哪怕早就知道必须支付代价，主角依然一次次选择前进，没有停步。驱动他的，是一种极其纯粹且固执的信念：只要足够努力，就一定能迎来那个万事周全的“完美结局”。可换一个角度看，你也可以说他自私——他只是没办法接受失去阿努莉丝，也没办法眼睁睁放弃任何一个并肩走来的伙伴。</p>

      <img src="https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E5%A4%A9%E5%B9%B3%E5%91%BD%E8%BF%90.png" alt="天平命运" class="content-img" />

      <p>于是你真的走到了最后。你拯救了世界。可天平的另一端，早已在你一次次“想要全部抓住”的拉扯中，静静放上了同样沉重的砝码。</p>
      <p>而当结局动画缓缓播完，你以为故事就此落幕时，天平突然自行启动——那一瞬间，所有的获得、失去、告别与眼泪仿佛被猛地抽回起点。你以为你已通关，但一切不过是刚刚回到最初的样式。真正的故事，在此刻才拉开序幕，而所有被小心翼翼折叠隐藏起来的真相，也开始将锋利的棱角逐寸浮出水面。</p>

      <div class="extra-links">
        <span class="links-label">🔗 附加内容：</span>
        <span @click="openImage('https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E7%BC%BA%E7%82%B91.png')" class="img-link">
          <el-icon><Picture /></el-icon> 缺点1
        </span>
        <span @click="openImage('https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E7%BC%BA%E7%82%B92.png')" class="img-link">
          <el-icon><Picture /></el-icon> 缺点2
        </span>
      </div>
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
  background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(251, 191, 36, 0.2);
  padding: 30px; border-radius: 16px; margin-bottom: 30px; width: 100%; text-align: left;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  flex: 1; overflow-y: auto;
}
.story-box::-webkit-scrollbar { width: 8px; }
.story-box::-webkit-scrollbar-track { background: transparent; }
.story-box::-webkit-scrollbar-thumb { background: rgba(251, 191, 36, 0.3); border-radius: 4px; }
.story-box::-webkit-scrollbar-thumb:hover { background: rgba(251, 191, 36, 0.6); }

.story-box p { font-size: 16px; line-height: 2; margin-bottom: 16px; color: #f8fafc; text-indent: 2em; }
.story-box p:last-child { margin-bottom: 0; }

.content-img {
  width: 100%; max-width: 600px; border-radius: 12px;
  margin: 16px auto; display: block; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.extra-links {
  margin-top: 32px; padding-top: 16px; border-top: 1px dashed rgba(251, 191, 36, 0.3);
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
}
.links-label { font-size: 14px; color: #fde68a; font-weight: 600; }
.img-link {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px;
  background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.3);
  color: #fef3c7; text-decoration: none; border-radius: 20px; font-size: 13px;
  transition: all 0.3s ease; cursor: pointer;
}
.img-link:hover {
  background: rgba(251, 191, 36, 0.25); border-color: rgba(251, 191, 36, 0.6);
  color: #fff; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
}

@media (max-width: 768px) {
  .story-box { padding: 18px; font-size: 14px; margin-bottom: 20px; border-radius: 12px; line-height: 1.8; }
  .extra-links { margin-top: 16px; padding-top: 12px; }
  .img-link { padding: 5px 12px; font-size: 12px; }
}
</style>
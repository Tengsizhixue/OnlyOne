<template>
  <SecretLayout
    :bg-image="bg"
    title="⚖️ 你找到了神之天平的隐秘画卷"
    title-color="#fbbf24"
    code="260410"
    @back="handleBack"
    v-slot="{ openImage, isAllUnlocked, back }"
  >
    <audio ref="audio1" :src="audioStart" preload="metadata" @ended="onEnded(1)"></audio>
    <audio ref="audio2" :src="audioEnd" preload="metadata" @ended="onEnded(2)"></audio>

    <div class="epic-room">
      <div class="story-box golden-theme">
        <p class="author-note">(以下内容主体由 AI 编写)</p>

        <div
          class="custom-audio-player"
          :class="{ 'is-playing': currentAudio === 1 && isPlaying }"
          @click="toggleAudio(1)"
        >
          <div class="player-left">
            <el-icon class="play-icon">
              <VideoPause v-if="currentAudio === 1 && isPlaying" />
              <VideoPlay v-else />
            </el-icon>
            <span class="track-name">活过的证明.mp3</span>
          </div>
          <div v-if="currentAudio === 1 && isPlaying" class="playing-bars">
            <span></span><span></span><span></span>
          </div>
        </div>

        <img :src="cover" alt="天平封面" class="content-img" />

        <p>《神之天平》的开篇并不复杂，甚至可以说是一种刻意的朴素：主角与青梅竹马阿努莉丝在突如其来的魔物袭击中失散，当他从昏迷中醒来时，身边只剩一只不知为何会说话的乌鸦。旅途中，他意外获得了一件能够穿越时空的神器。仅看这段开场，故事的前半段似乎只是一套我们再熟悉不过的模板——打倒魔王、拯救爱人、然后迎来大团圆。一切都像是某种令人安心的、被无数作品验证过的古典英雄叙事。</p>
        <p>然而这种安心的错觉，恰恰是游戏最先开始瓦解的东西。</p>
        <p>和《我在7年后等着你》一样，本作的核心也是“穿越”时空。但两者的“穿越”在底色上存在着本质的不同。这里的每一次回溯都不是轻巧的跳跃，你无法毫无负担地回到过去某个节点去修修补补。这里的法则是无情的等价交换：你想要得到什么，就必须献上同等重量的事物来交换。那不是写在契约上的漂亮话，而是每一次发动能力时，天平都实实在在地称量着你的决意。</p>
        <p>你不是一个置身事外的观众，你亲手做出抉择，又被迫目睹每一个选择引发的连锁反应——有时候，出于绝对的善意伸出援手，却结出意想不到的恶果；有时候，试图拯救某样重要之物，却注定伴随着另一种难以承受的失去。哪怕早就知道必须支付代价，主角依然一次次选择前进，没有停步。驱动他的，是一种极其纯粹且固执的信念：只要足够努力，就一定能迎来那个万事周全的“完美结局”。可换一个角度看，你也可以说他自私——他只是没办法接受失去阿努莉丝，也没办法眼睁睁放弃任何一个并肩走来的伙伴。</p>

        <img :src="destiny" alt="天平命运" class="content-img" />

        <p>于是你真的走到了最后。你拯救了世界。可天平的另一端，早已在你一次次“想要全部抓住”的拉扯中，静静放上了同样沉重的砝码。</p>
        <p>而当结局动画缓缓播完，你以为故事就此落幕时，天平突然自行启动——那一瞬间，所有的获得、失去、告别与眼泪仿佛被猛地抽回起点。你以为你已通关，但一切不过是刚刚回到最初的样式。真正的故事，在此刻才拉开序幕，而所有被小心翼翼折叠隐藏起来的真相，也开始将锋利的棱角逐寸浮出水面。</p>

        <div
          class="custom-audio-player bottom-player"
          :class="{ 'is-playing': currentAudio === 2 && isPlaying }"
          @click="toggleAudio(2)"
        >
          <div class="player-left">
            <el-icon class="play-icon">
              <VideoPause v-if="currentAudio === 2 && isPlaying" />
              <VideoPlay v-else />
            </el-icon>
            <span class="track-name">结局.mp3</span>
          </div>
          <div v-if="currentAudio === 2 && isPlaying" class="playing-bars">
            <span></span><span></span><span></span>
          </div>
        </div>

        <div class="extra-links">
          <span class="links-label">🔗附加内容：</span>
          <span @click="openImage(imgDefect1)" class="img-link">
            <el-icon><Picture /></el-icon> 缺点一
          </span>
          <span @click="openImage(imgDefect2)" class="img-link">
            <el-icon><Picture /></el-icon> 缺点二
          </span>
           <span @click="openImage(bg)" class="img-link">
            <el-icon><Picture /></el-icon> 此网页背景图片
          </span>
        </div>

        <div class="bottom-action">
          <button class="shimmer-btn" @click="back">
            {{ isAllUnlocked ? '开启终局之门 ✨' : '返回聊天' }}
          </button>
        </div>
      </div>
    </div>
  </SecretLayout>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { Picture, VideoPlay, VideoPause } from '@element-plus/icons-vue'
import SecretLayout from '../../components/SecretLayout.vue'
import { SECRET_ASSETS } from '../../config/constants.js'

const { bg, cover, destiny, audioStart, audioEnd, imgDefect1, imgDefect2 } = SECRET_ASSETS.astlibra

const emit = defineEmits(['back'])

const audio1 = ref(null)
const audio2 = ref(null)
const currentAudio = ref(null)
const isPlaying = ref(false)

const toggleAudio = (num) => {
  const targetAudio = num === 1 ? audio1.value : audio2.value
  const otherAudio = num === 1 ? audio2.value : audio1.value

  if (currentAudio.value === num) {
    if (isPlaying.value) {
      targetAudio?.pause()
      isPlaying.value = false
    } else {
      // 🌟 优化：加上 catch 捕获浏览器拦截错误
      targetAudio?.play().catch(e => console.warn('音频播放被拦截:', e))
      isPlaying.value = true
    }
  }
  else {
    if (otherAudio) {
      otherAudio.pause()
    }
    if (targetAudio) {
      targetAudio.currentTime = 0
      // 🌟 优化：加上 catch 捕获浏览器拦截错误
      targetAudio.play().catch(e => console.warn('音频播放被拦截:', e))
    }
    currentAudio.value = num
    isPlaying.value = true
  }
}

const onEnded = (num) => {
  if (currentAudio.value === num) {
    isPlaying.value = false
  }
}

const handleBack = () => {
  if (audio1.value) { audio1.value.pause(); audio1.value.currentTime = 0; }
  if (audio2.value) { audio2.value.pause(); audio2.value.currentTime = 0; }
  isPlaying.value = false
  emit('back')
}

onUnmounted(() => {
  if (audio1.value) { audio1.value.pause(); audio1.value.currentTime = 0; }
  if (audio2.value) { audio2.value.pause(); audio2.value.currentTime = 0; }
})
</script>

<style scoped>
/* 样式保持不变 */
.epic-room { width: 100%; flex: 1; display: flex; flex-direction: column; overflow-y: auto; overflow-x: hidden; padding-right: 4px; box-sizing: border-box; }
.epic-room::-webkit-scrollbar { width: 6px; }
.epic-room::-webkit-scrollbar-track { background: transparent; }
.epic-room::-webkit-scrollbar-thumb { background: rgba(251, 191, 36, 0.4); border-radius: 4px; }
.epic-room::-webkit-scrollbar-thumb:hover { background: rgba(251, 191, 36, 0.8); }
.story-box { background: rgba(25, 20, 15, 0.75); border: 1px solid rgba(251, 191, 36, 0.35); box-shadow: 0 10px 40px rgba(0,0,0,0.6), inset 0 0 20px rgba(251, 191, 36, 0.05); padding: 30px; border-radius: 16px; margin-bottom: 24px; width: 100%; text-align: left; flex: none; overflow: visible; box-sizing: border-box; word-wrap: break-word; }
.story-box p { font-size: 16px; line-height: 2; margin-bottom: 16px; color: #fef3c7; text-indent: 2em; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
.story-box p:last-child { margin-bottom: 0; }
.author-note { text-align: center; text-indent: 0 !important; font-size: 13px !important; color: rgba(251, 191, 36, 0.6) !important; font-style: italic; margin-bottom: 24px !important; }
.content-img { width: 100%; max-width: 600px; border-radius: 8px; border: 2px solid rgba(251, 191, 36, 0.4); margin: 20px auto; display: block; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7); }
.custom-audio-player { display: flex; justify-content: space-between; align-items: center; background: linear-gradient(90deg, rgba(251, 191, 36, 0.15), rgba(251, 191, 36, 0.05)); border: 1px solid rgba(251, 191, 36, 0.3); padding: 14px 24px; border-radius: 12px; cursor: pointer; transition: all 0.3s ease; margin: 10px 0 24px 0; }
.custom-audio-player.bottom-player { margin: 30px 0 10px 0; }
.custom-audio-player:hover { background: linear-gradient(90deg, rgba(251, 191, 36, 0.25), rgba(251, 191, 36, 0.1)); border-color: rgba(251, 191, 36, 0.6); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(251, 191, 36, 0.15); }
.custom-audio-player.is-playing { background: linear-gradient(90deg, rgba(251, 191, 36, 0.35), rgba(251, 191, 36, 0.15)); border-color: rgba(251, 191, 36, 0.8); box-shadow: 0 0 20px rgba(251, 191, 36, 0.2); }
.player-left { display: flex; align-items: center; gap: 14px; }
.play-icon { font-size: 26px; color: #fbbf24; filter: drop-shadow(0 0 5px rgba(251,191,36,0.5)); }
.track-name { font-size: 16px; font-weight: bold; color: #fef3c7; letter-spacing: 1px;}
.playing-bars { display: flex; gap: 3px; height: 16px; align-items: flex-end; }
.playing-bars span { display: inline-block; width: 4px; background-color: #fbbf24; border-radius: 2px; animation: bounce 1s ease infinite alternate; box-shadow: 0 0 5px #fbbf24; }
.playing-bars span:nth-child(2) { animation-delay: 0.3s; }
.playing-bars span:nth-child(3) { animation-delay: 0.6s; }
@keyframes bounce { 0% { height: 4px; } 100% { height: 18px; } }
.extra-links { margin-top: 32px; padding-top: 20px; border-top: 1px dashed rgba(251, 191, 36, 0.4); display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.links-label { font-size: 14px; color: #fde68a; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
.img-link { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(251, 191, 36, 0.15); border: 1px solid rgba(251, 191, 36, 0.4); color: #fef3c7; text-decoration: none; border-radius: 20px; font-size: 13px; transition: all 0.3s ease; cursor: pointer; backdrop-filter: blur(4px); }
.img-link:hover { background: rgba(251, 191, 36, 0.3); border-color: #fbbf24; color: #fff; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3); }

.bottom-action { margin-top: 40px; display: flex; justify-content: center; }

@media (max-width: 768px) {
  .story-box { padding: 18px; font-size: 15px; margin-bottom: 20px; border-radius: 12px; }
  .story-box p { line-height: 1.8; margin-bottom: 14px; }
  .custom-audio-player { padding: 12px 18px; }
  .play-icon { font-size: 22px; }
  .track-name { font-size: 14px; }
  .extra-links { margin-top: 20px; padding-top: 16px; }
  .img-link { padding: 5px 12px; font-size: 12px; }
}
</style>
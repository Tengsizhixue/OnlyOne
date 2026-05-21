<template>
  <SecretLayout
    title="时空“穿越”"
    title-color="#7dd3fc"
    code="251027"
    @back="handleBack"
    v-slot="{ openImage, back }"
  >
    <audio ref="globalAudio" :src="currentAudioSrc" preload="metadata" @ended="onEnded"></audio>

    <div class="ethereal-room">
      <div class="memory-box moonlight-theme">
        <p class="prologue">
          在现实生活中，我们既渴望永恒的羁绊，又恐惧失去带来的虚无；既需要社交的温度，又厌倦失控的冲突；有时我们试图在那道无法跨越的鸿沟里，为一生的遗憾寻找一个出口。
          《我在7年后等着你》中那份跨越时间也要守护的约定，《灵魂摆渡者》中那些明知终将告别却依然倾注的关怀，以及《去月球》中那场在记忆尽头重塑的人生，恰是这种矛盾在游戏世界里的三种映照。
        </p>

        <div class="divider">
          <span class="diamond"></span><span class="line"></span><span class="diamond"></span>
        </div>

        <img :src="img7Years" alt="我在七年后等着你" class="content-img" />

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
            <span class="track-name">战火.mp3</span>
          </div>
          <div v-if="currentAudio === 1 && isPlaying" class="playing-bars">
            <span></span><span></span><span></span>
          </div>
        </div>

        <p>《我在7年后等着你》呈现的是一种“向外的重逢”。它用纯粹的执着，把“告别”变成“重逢”的伏笔。
          明线是主角寻找记忆、完成约定的旅程；暗线则指向一桩牵涉人体器官交易的医院阴谋。当你玩到最后便会发现游戏里的角色都是被困在爱与执念中的普通人，他们所做的一切都是为了一个美好的结局。
          这种从告别到团圆的叙事弧光，恰好满足了我们对“努力必有回报”的渴望。</p>

        <div
          class="custom-audio-player"
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

        <img :src="imgHappiness" alt="请你获得幸福" class="content-img filter-soft" />

        <div class="divider">
          <span class="diamond"></span><span class="line"></span><span class="diamond"></span>
        </div>

        <img :src="imgSpiritfarer" alt="灵魂摆渡者" class="content-img" />

        <p>而《灵魂摆渡者》则给出了另一种“向内的告别”。你陪伴一个个灵魂走完最后的旅程，送他们前往永恒之门。
          船越建越大，人却越来越少——当不得不送走那些倾注了情感的角色时，原本温暖的任务逐渐变成情感的负重，让人难以前行。
          然而，当你最终完成所有使命，驾驶着空船，准备送走最后一位乘客——主角自己时，才会真正明白：我们终其一生，都是在摆渡他人，最终摆渡自己。
          告别并不是终点，只是人生中的旅途。</p>

        <img :src="imgHeart" alt="爱心" class="content-img filter-soft" />

        <div class="divider">
          <span class="diamond"></span><span class="line"></span><span class="diamond"></span>
        </div>

        <img :src="imgMoon" alt="去月球" class="content-img" />

        <div
          class="custom-audio-player"
          :class="{ 'is-playing': currentAudio === 3 && isPlaying }"
          @click="toggleAudio(3)"
        >
          <div class="player-left">
            <el-icon class="play-icon">
              <VideoPause v-if="currentAudio === 3 && isPlaying" />
              <VideoPlay v-else />
            </el-icon>
            <span class="track-name">去月球音乐.aac</span>
          </div>
          <div v-if="currentAudio === 3 && isPlaying" class="playing-bars">
            <span></span><span></span><span></span>
          </div>
        </div>

        <p>《去月球》构建了一场“向后的和解”。它站在生命的终点回望，试图在支离破碎的记忆中，为一段充满错位与孤独的人生补齐最后一块拼图。
          你穿梭于老约翰的过往，看他在现实的平庸与命运的残酷中，逐渐遗失了那个关于“月球”的初衷。
          虽然那些被修改的记忆并未改变现实中破碎的真相，但当那枚火箭在夕阳中升空、两只苍老的手在虚幻中相握时，已经证明了过程永远比结果更为重要。</p>

        <p class="epilogue">三款游戏，三种关于“告别”的叙事：一个告诉我们如何重逢，一个教会我们如何放手，而最后一个则展示了如何与遗憾共存。
          它们共同指向一个命题——真正的生活不该只有单程票，它既需要重逢的信念，也需要放手的勇气，更需要与自己和解的气概</p>

        <div class="extra-links">
          <span class="links-label">附件：</span>
          <span @click="openImage(attach1)" class="img-link">
            <el-icon><Picture /></el-icon> 去年写的原文
          </span>
          <span @click="openImage(attach2)" class="img-link">
            <el-icon><Picture /></el-icon> 原文AI化
          </span>
          <span @click="openImage(attach3)" class="img-link">
            <el-icon><Picture /></el-icon> 原文AI化再缩写
          </span>
          <span @click="openImage(attach4)" class="img-link">
            <el-icon><Picture /></el-icon> 19年的游戏购买记录
          </span>
        </div>

        <div class="bottom-action">
          <button class="shimmer-btn" @click="back">返回前言</button>
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

const {
  img7Years, audioZhanHuo, audioJieJu, imgHappiness,
  imgSpiritfarer, imgHeart, imgMoon, audioMoon,
  attach1, attach2, attach3, attach4
} = SECRET_ASSETS.memory

const emit = defineEmits(['back'])

const globalAudio = ref(null)
const currentAudioSrc = ref('')
const currentAudio = ref(null)
const isPlaying = ref(false)

const audioSources = { 1: audioZhanHuo, 2: audioJieJu, 3: audioMoon }

const toggleAudio = (num) => {
  if (!globalAudio.value) return
  const audio = globalAudio.value

  if (currentAudio.value === num) {
    if (isPlaying.value) {
      audio.pause()
      isPlaying.value = false
    } else {
      audio.play().catch(e => console.warn('音频播放被拦截:', e))
      isPlaying.value = true
    }
  } else {
    currentAudio.value = num
    currentAudioSrc.value = audioSources[num]
    isPlaying.value = true
    setTimeout(() => {
      if (globalAudio.value) {
        globalAudio.value.currentTime = 0
        globalAudio.value.play().catch(e => console.warn('音频播放被拦截:', e))
      }
    }, 50)
  }
}

const onEnded = () => { isPlaying.value = false }

const handleBack = () => {
  if (globalAudio.value) { globalAudio.value.pause(); globalAudio.value.currentTime = 0; }
  isPlaying.value = false
  emit('back')
}

onUnmounted(() => handleBack())
</script>

<style scoped>
.ethereal-room { width: 100%; flex: 1; display: flex; flex-direction: column; overflow-y: auto; overflow-x: hidden; padding-right: 4px; box-sizing: border-box; }
.ethereal-room::-webkit-scrollbar { width: 6px; }
.ethereal-room::-webkit-scrollbar-track { background: transparent; }
.ethereal-room::-webkit-scrollbar-thumb { background: rgba(125, 211, 252, 0.4); border-radius: 4px; }
.ethereal-room::-webkit-scrollbar-thumb:hover { background: rgba(125, 211, 252, 0.8); }
.memory-box { background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(186, 230, 253, 0.3); box-shadow: 0 10px 40px rgba(0,0,0,0.7), inset 0 0 30px rgba(186, 230, 253, 0.05); padding: 40px; border-radius: 16px; margin-bottom: 24px; width: 100%; text-align: left; flex: none; overflow: visible; box-sizing: border-box; word-wrap: break-word; }
.memory-box p { font-size: 16px; line-height: 2.2; margin-bottom: 20px; color: #e0f2fe; text-indent: 2em; text-shadow: 0 1px 3px rgba(0,0,0,0.9); }
.prologue { font-size: 17px !important; color: #bae6fd !important; font-style: italic; letter-spacing: 1px; }
.epilogue { margin-top: 30px; border-top: 1px solid rgba(186, 230, 253, 0.2); padding-top: 20px; font-weight: 500; }
.divider { display: flex; align-items: center; justify-content: center; gap: 10px; margin: 30px 0; opacity: 0.6; }
.diamond { width: 6px; height: 6px; background: #38bdf8; transform: rotate(45deg); box-shadow: 0 0 8px #38bdf8;}
.line { width: 120px; height: 1px; background: linear-gradient(90deg, transparent, #7dd3fc, transparent); }
.content-img { width: 100%; max-width: 650px; border-radius: 8px; border: 1px solid rgba(186, 230, 253, 0.4); margin: 24px auto; display: block; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7), 0 0 15px rgba(125, 211, 252, 0.1); }
.filter-soft { filter: brightness(0.9) contrast(1.05); }
.custom-audio-player { display: flex; justify-content: space-between; align-items: center; background: linear-gradient(90deg, rgba(56, 189, 248, 0.15), rgba(56, 189, 248, 0.05)); border: 1px solid rgba(125, 211, 252, 0.3); padding: 14px 24px; border-radius: 12px; cursor: pointer; transition: all 0.3s ease; margin: 10px 0 24px 0; }
.custom-audio-player:hover { background: linear-gradient(90deg, rgba(56, 189, 248, 0.25), rgba(56, 189, 248, 0.1)); border-color: rgba(125, 211, 252, 0.6); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(56, 189, 248, 0.15); }
.custom-audio-player.is-playing { background: linear-gradient(90deg, rgba(56, 189, 248, 0.35), rgba(56, 189, 248, 0.15)); border-color: rgba(125, 211, 252, 0.8); box-shadow: 0 0 20px rgba(56, 189, 248, 0.25); }
.player-left { display: flex; align-items: center; gap: 14px; }
.play-icon { font-size: 26px; color: #7dd3fc; filter: drop-shadow(0 0 5px rgba(125,211,252,0.5)); }
.track-name { font-size: 15px; font-weight: bold; color: #f0f9ff; letter-spacing: 1px;}
.playing-bars { display: flex; gap: 3px; height: 16px; align-items: flex-end; }
.playing-bars span { display: inline-block; width: 4px; background-color: #7dd3fc; border-radius: 2px; animation: bounce 1s ease infinite alternate; box-shadow: 0 0 5px #7dd3fc; }
.playing-bars span:nth-child(2) { animation-delay: 0.3s; }
.playing-bars span:nth-child(3) { animation-delay: 0.6s; }
@keyframes bounce { 0% { height: 4px; } 100% { height: 18px; } }
.extra-links { margin-top: 32px; padding-top: 20px; border-top: 1px dashed rgba(125, 211, 252, 0.3); display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.links-label { font-size: 14px; color: #bae6fd; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
.img-link { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); color: #f0f9ff; text-decoration: none; border-radius: 20px; font-size: 13px; transition: all 0.3s ease; cursor: pointer; backdrop-filter: blur(4px); }
.img-link:hover { background: rgba(56, 189, 248, 0.3); border-color: #7dd3fc; color: #fff; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3); }
.bottom-action { margin-top: 40px; display: flex; justify-content: center; }

@media (max-width: 768px) {
  .memory-box { padding: 20px 16px; margin-bottom: 20px; border-radius: 12px; }
  .memory-box p { font-size: 15px; line-height: 1.9; margin-bottom: 14px; }
  .prologue { font-size: 15px !important; }
  .custom-audio-player { padding: 12px 16px; margin: 10px 0 20px 0;}
  .play-icon { font-size: 22px; }
  .track-name { font-size: 14px; }
  .extra-links { margin-top: 20px; padding-top: 16px; }
  .img-link { padding: 5px 12px; font-size: 12px; }
  .divider { margin: 20px 0; }
}
</style>
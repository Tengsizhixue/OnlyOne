<template>
  <SecretLayout
    :bg-image="bg"
    title="🎶 你找到了音乐的力量"
    title-color="#f472b6"
    code="240802"
    @back="handleBack"
    v-slot="{ openImage, back }"
  >
    <audio ref="globalAudio" :src="currentAudioSrc" preload="metadata" @ended="onAudioEnded"></audio>

    <div class="music-room">
      <div class="story-box">
        <p>我听歌有个习惯，一个时间段里面肯定有一首歌我会逮着死听，18年以前没这个习惯，就什么歌火就听什么。</p>
        <p>19年我非常歧视中文歌，因为那个时间段很多热歌都是抄袭的，一打开评论区全是吵架撕逼，而我听歌都是喜欢看评论区的，所以当年基本都是用网易云，只听纯音乐和日式的ACG，听的最多的是《四月是你的谎言》中的一个插曲，叫again，我当时非常喜欢一个作者的纯音乐，我记得名字叫羽肿，我现在倒是不怎么听，纯音乐最大的缺点就是记不住名字。</p>
        <p>后面反着来了，基本全是中文歌，早就把网易云注销换QQ音乐，网易云版权太少，中间几年听的最多的是虚拟，这歌是我听过次数最多的，这歌无论是旋律还是歌词，我当时都很喜欢，现在我在抖音里面刷到还是愿意听一听的。</p>
        <p>最近几年听的最多的是梁静茹的会呼吸的痛，这歌是作者写给母亲的，感染力还是很强的，现在我已经听了快900遍，再听个两年应该就超过虚拟了。</p>

        <div class="extra-links">
          <span class="links-label">附加内容：</span>
          <span @click="openImage(attach1)" class="img-link">
            <el-icon><Picture /></el-icon> 去年听的歌单
          </span>
           <span @click="openImage(attach2)" class="img-link">
            <el-icon><Picture /></el-icon> 前年听的歌单
          </span>
        </div>
      </div>

      <div class="music-player">
        <div
          v-for="song in playlist"
          :key="song.id"
          class="music-item"
          :class="{ 'is-playing': currentSong?.id === song.id && isPlaying }"
          @click="togglePlay(song)"
        >
          <div class="song-cover" :class="{ 'rotating': currentSong?.id === song.id && isPlaying }">
            <el-icon v-if="!song.cover"><Picture /></el-icon>
            <img v-else :src="song.cover" class="cover-img" />
            <div v-if="currentSong?.id === song.id && isPlaying" class="playing-bars">
              <span></span><span></span><span></span>
            </div>
          </div>
          <div class="song-info">
            <div class="song-title">{{ song.title }}</div>
            <div class="song-artist">{{ song.artist }}</div>
          </div>
          <div class="song-action">
            <el-icon size="28" :color="currentSong?.id === song.id && isPlaying ? '#f472b6' : '#cbd5e1'">
              <VideoPause v-if="currentSong?.id === song.id && isPlaying" />
              <VideoPlay v-else />
            </el-icon>
          </div>
        </div>
      </div>

      <div class="bottom-action">
        <button class="shimmer-btn" @click="back">返回前言</button>
      </div>
    </div>
  </SecretLayout>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { Picture, VideoPlay, VideoPause } from '@element-plus/icons-vue'
import SecretLayout from '../../components/SecretLayout.vue'
import { SECRET_ASSETS } from '../../config/constants.js'

const { bg, againAudio, xuniAudio, huxiAudio, cover1, cover2, cover3, attach1, attach2 } = SECRET_ASSETS.music
const emit = defineEmits(['back'])

const globalAudio = ref(null)
const currentAudioSrc = ref('')
const currentSong = ref(null)
const isPlaying = ref(false)

const playlist = ref([
  { id: 1, title: 'again', artist: '《四月是你的谎言》插曲', src: againAudio, cover: cover1 },
  { id: 2, title: '虚拟', artist: '陈粒', src: xuniAudio, cover: cover2 },
  { id: 3, title: '会呼吸的痛', artist: '梁静茹', src: huxiAudio, cover: cover3 }
])

const togglePlay = (song) => {
  if (!globalAudio.value) return
  const audio = globalAudio.value

  if (currentSong.value?.id === song.id) {
    if (isPlaying.value) { audio.pause(); isPlaying.value = false }
    else { audio.play().catch(err => { if (err.name !== 'AbortError') console.error('播放失败:', err) }); isPlaying.value = true }
    return
  }

  currentSong.value = song; currentAudioSrc.value = song.src; isPlaying.value = true
  setTimeout(() => {
    if (globalAudio.value) { globalAudio.value.currentTime = 0; globalAudio.value.play().catch(err => { if (err.name !== 'AbortError') console.error('播放失败:', err) }) }
  }, 50)
}

const onAudioEnded = () => { isPlaying.value = false }

const handleBack = () => {
  if (globalAudio.value) { globalAudio.value.pause(); globalAudio.value.currentTime = 0; isPlaying.value = false }
  emit('back')
}

onUnmounted(() => {
  if (globalAudio.value) { globalAudio.value.pause(); globalAudio.value.currentTime = 0 }
})
</script>

<style scoped>
.music-room { width: 100%; flex: 1; display: flex; flex-direction: column; overflow-y: auto; overflow-x: hidden; padding-right: 4px; box-sizing: border-box; }
.music-room::-webkit-scrollbar { width: 6px; }
.music-room::-webkit-scrollbar-track { background: transparent; }
.music-room::-webkit-scrollbar-thumb { background: rgba(244, 114, 182, 0.3); border-radius: 4px; }
.music-room::-webkit-scrollbar-thumb:hover { background: rgba(244, 114, 182, 0.6); }
.story-box { background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(244, 114, 182, 0.2); padding: 30px; border-radius: 16px; margin-bottom: 24px; width: 100%; text-align: left; box-shadow: 0 10px 30px rgba(0,0,0,0.1); flex: none; overflow: visible; box-sizing: border-box; word-wrap: break-word; }
.story-box p { font-size: 16px; line-height: 2; margin-bottom: 16px; color: #fdf2f8; text-indent: 2em; }
.story-box p:last-child { margin-bottom: 0; }
.extra-links { margin-top: 24px; padding-top: 16px; border-top: 1px dashed rgba(244, 114, 182, 0.3); display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.links-label { font-size: 14px; color: #fbcfe8; font-weight: 600; }
.img-link { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(244, 114, 182, 0.1); border: 1px solid rgba(244, 114, 182, 0.3); color: #fdf2f8; text-decoration: none; border-radius: 20px; font-size: 13px; transition: all 0.3s ease; cursor: pointer; }
.img-link:hover { background: rgba(244, 114, 182, 0.25); border-color: rgba(244, 114, 182, 0.6); color: #fff; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(244, 114, 182, 0.2); }
.music-player { width: 100%; display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px; flex-shrink: 0; }
.music-item { display: flex; align-items: center; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 14px 20px; border-radius: 16px; cursor: pointer; transition: all 0.3s ease; }
.music-item:hover { background: rgba(255, 255, 255, 0.15); transform: translateY(-2px); border-color: rgba(244, 114, 182, 0.3); }
.music-item.is-playing { background: rgba(244, 114, 182, 0.15); border-color: rgba(244, 114, 182, 0.5); box-shadow: 0 4px 15px rgba(244, 114, 182, 0.1); }
.song-cover { width: 45px; height: 45px; border-radius: 50%; background: rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: center; margin-right: 16px; font-size: 24px; color: #94a3b8; position: relative; overflow: hidden; flex-shrink: 0; transition: transform 0.3s ease; }
.song-cover.rotating { animation: rotate-disc 3s linear infinite; }
@keyframes rotate-disc { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.cover-img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }
.song-info { flex: 1; text-align: left; display: flex; flex-direction: column; gap: 4px; }
.song-title { font-size: 16px; font-weight: 600; color: #f8fafc; transition: color 0.3s; }
.is-playing .song-title { color: #f472b6; }
.song-artist { font-size: 13px; color: #94a3b8; }
.song-action { display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; transition: all 0.3s; }
.music-item:hover .song-action { background: rgba(255, 255, 255, 0.1); }
.playing-bars { position: absolute; bottom: 8px; display: flex; gap: 2px; height: 12px; align-items: flex-end; }
.playing-bars span { display: inline-block; width: 3px; background-color: #f472b6; border-radius: 2px; animation: bounce 1s ease infinite alternate; }
.playing-bars span:nth-child(2) { animation-delay: 0.3s; }
.playing-bars span:nth-child(3) { animation-delay: 0.6s; }
@keyframes bounce { 0% { height: 3px; } 100% { height: 12px; } }
.bottom-action { margin-top: 20px; display: flex; justify-content: center; margin-bottom: 40px; }

@media (max-width: 768px) {
  .story-box { padding: 16px 20px; font-size: 15px; margin-bottom: 20px; border-radius: 12px; }
  .story-box p { line-height: 1.7; margin-bottom: 12px; }
  .extra-links { margin-top: 16px; padding-top: 12px; }
  .img-link { padding: 5px 12px; font-size: 12px; }
  .music-player { gap: 8px; margin-bottom: 16px; }
  .music-item { padding: 12px 16px; border-radius: 12px; }
  .song-cover { width: 40px; height: 40px; margin-right: 12px; }
}
</style>
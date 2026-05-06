<template>
  <div class="secret-page shadow-2xl">
    <!-- 独特的背景层，fixed 铺满全屏，放在最底层 -->
    <div class="secret-bg"></div>

    <audio ref="audioRef" :src="currentAudioSrc" @ended="onAudioEnded"></audio>

    <div class="secret-content music-room">
      <h1 class="highlight-text" style="color: #f472b6;">🎧 灵魂的音乐电台</h1>
      <p class="subtitle">特殊代码认证：240802</p>

      <div class="story-box">
        <p>
          我听歌有个习惯，一个时间段里面肯定有一首歌我会逮着死听，18年以前没这个习惯，就什么歌火就听什么。
        </p>
        <p>
          19年我非常歧视中文歌，因为那个时间段很多热歌都是抄袭的，一打开评论区全是吵架撕逼，而我听歌都是喜欢看评论区的，所以当年基本都是用网易云，只听纯音乐和日式的ACG，听的最多的是《四月是你的谎言》中的一个插曲，叫 <strong>again</strong>，我当时非常喜欢一个作者的纯音乐，我记得名字叫羽肿，我现在倒是不怎么听，纯音乐最大的缺点就是记不住名字。
        </p>
        <p>
          后面反着来了，基本全是中文歌，早就把网易云注销换QQ音乐，网易云版权太少，中间几年听的最多的是 <strong>虚拟</strong>，这歌是我听过次数最多的，这歌无论是旋律还是歌词，我当时都很喜欢，现在我在抖音里面刷到还是愿意听一听的。
        </p>
        <p>
          最近几年听的最多的是梁静茹的 <strong>会呼吸的痛</strong>，这歌是作者写给母亲的，感染力还是很强的，现在我已经听了快900遍，再听个两年应该就超过虚拟了。
        </p>
      </div>

      <div class="music-player">
        <div
          v-for="song in playlist"
          :key="song.id"
          class="music-item"
          :class="{ 'is-playing': currentSong?.id === song.id && isPlaying }"
          @click="togglePlay(song)"
        >
          <div class="song-cover">
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

      <button class="enter-btn shimmer-btn" @click="handleBack">返回聊天</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { Picture, VideoPlay, VideoPause } from '@element-plus/icons-vue'

// 💡 替换为你的阿里云 OSS 音频文件链接
const againAudio = 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/again.aac'
const xuniAudio = 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/%E8%99%9A%E6%8B%9F.aac'
const huxiAudio = 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/%E4%BC%9A%E5%91%BC%E5%90%B8%E7%9A%84%E7%97%9B.mp3'

const emit = defineEmits(['back'])

const audioRef = ref(null)
const currentAudioSrc = ref('')
const currentSong = ref(null)
const isPlaying = ref(false)

const playlist = ref([
  { id: 1, title: 'again', artist: '《四月是你的谎言》插曲', src: againAudio, cover: '' },
  { id: 2, title: '虚拟', artist: '陈粒', src: xuniAudio, cover: '' },
  { id: 3, title: '会呼吸的痛', artist: '梁静茹', src: huxiAudio, cover: '' }
])

const togglePlay = (song) => {
  if (!audioRef.value) return
  if (currentSong.value?.id === song.id) {
    if (isPlaying.value) {
      audioRef.value.pause()
      isPlaying.value = false
    } else {
      audioRef.value.play()
      isPlaying.value = true
    }
    return
  }
  currentSong.value = song
  currentAudioSrc.value = song.src
  isPlaying.value = true
  setTimeout(() => {
    if (audioRef.value) audioRef.value.play()
  }, 50)
}

const onAudioEnded = () => { isPlaying.value = false }

const handleBack = () => {
  try {
    if (audioRef.value) {
      audioRef.value.pause()
      isPlaying.value = false
    }
  } catch (e) {
    console.error('音频暂停异常:', e)
  } finally {
    emit('back')
  }
}

onUnmounted(() => {
  if (audioRef.value) audioRef.value.pause()
})
</script>

<style scoped>
/* ====== 新增：全屏独立背景层 ====== */
.secret-bg {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  /* 音乐主题临时占位图：音响/电台风格 */
  background-image: url('https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=2000&q=80');
  background-size: cover; background-position: center;
  filter: brightness(0.35); /* 大幅压暗背景，保证文字对比度 */
  z-index: -1; pointer-events: none;
}

/* ====== 修改：独立的深色毛玻璃卡片 ====== */
.secret-page {
  width: 90vw; max-width: 800px; padding: 40px 60px; text-align: center; border-radius: 24px;
  z-index: 100; color: #f8fafc; max-height: 90dvh; overflow-y: auto;
  background: rgba(15, 23, 42, 0.7); /* 深色半透明层 */
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
.secret-page::-webkit-scrollbar { width: 6px; }
.secret-page::-webkit-scrollbar-track { background: transparent; }
.secret-page::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 4px; }
.secret-content { display: flex; flex-direction: column; align-items: center; justify-content: center; }
.highlight-text { margin-bottom: 10px; font-size: 28px; }
.subtitle { color: #94a3b8; font-family: monospace; margin-bottom: 30px; letter-spacing: 2px; }

/* 专属样式 */
.music-room .story-box { background: rgba(0, 0, 0, 0.35); border: 1px solid rgba(244, 114, 182, 0.2); padding: 30px; border-radius: 16px; margin-bottom: 30px; width: 100%; text-align: left; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
.music-room .story-box p { font-size: 15px; line-height: 1.8; margin-bottom: 16px; color: #fdf2f8; text-indent: 2em; }
.music-room .story-box p:last-child { margin-bottom: 0; }
.music-room .story-box strong { color: #f472b6; font-weight: 600; padding: 0 4px; }
.music-player { width: 100%; display: flex; flex-direction: column; gap: 16px; margin-bottom: 40px; }
.music-item { display: flex; align-items: center; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 16px 20px; border-radius: 16px; cursor: pointer; transition: all 0.3s ease; }
.music-item:hover { background: rgba(255, 255, 255, 0.15); transform: translateY(-2px); border-color: rgba(244, 114, 182, 0.3); }
.music-item.is-playing { background: rgba(244, 114, 182, 0.15); border-color: rgba(244, 114, 182, 0.5); box-shadow: 0 4px 15px rgba(244, 114, 182, 0.1); }
.song-cover { width: 50px; height: 50px; border-radius: 10px; background: rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: center; margin-right: 16px; font-size: 24px; color: #94a3b8; position: relative; overflow: hidden; flex-shrink: 0; }
.cover-img { width: 100%; height: 100%; object-fit: cover; }
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
@media (max-width: 768px) { .secret-page { padding: 30px 20px; } .music-room .story-box { padding: 20px; } }
</style>




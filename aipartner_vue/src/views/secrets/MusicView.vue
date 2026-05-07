<template>
  <div class="secret-view-container">
    <!-- 独立的背景层，提出到容器外部解决穿透问题 -->
    <div class="secret-bg"></div>

    <audio ref="audioRef" :src="currentAudioSrc" @ended="onAudioEnded"></audio>

    <div class="secret-page shadow-2xl">
      <div class="secret-content music-room">
        <h1 class="highlight-text" style="color: #f472b6;">音乐，陪伴我很多年</h1>
        <p class="subtitle">恭喜你找到：240802</p>

        <!-- 文字区：使用了 flex: 1 撑满剩余高度 -->
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

          <!-- 新增：附加图片链接区 -->
          <div class="extra-links">
            <span class="links-label">附加内容（图片加载慢，因为我懒得找图床）：</span>
            <span @click="openImage('https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E5%8E%BB%E5%B9%B4%E5%90%AC%E7%9A%84%E6%AD%8C%E5%8D%95.png')" class="img-link">
              <el-icon><Picture /></el-icon> 去年听的歌单
            </span>
             <span @click="openImage('https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E5%89%8D%E5%B9%B4%E5%90%AC%E7%9A%84%E6%AD%8C%E5%8D%95.png')" class="img-link">
              <el-icon><Picture /></el-icon> 前年听的歌单
            </span>
          </div>
        </div>

        <!-- 播放器区域：放置在底部 -->
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

        <button class="enter-btn shimmer-btn" @click="handleBack">返回聊天</button>
      </div>
    </div>

    <!-- 💡 新增：图片全屏预览遮罩 -->
    <transition name="fade">
      <div v-if="showPreview" class="image-preview-overlay" @click="closeImage">
        <el-icon class="close-preview-btn"><Close /></el-icon>
        <img :src="previewImage" class="preview-img" />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { Picture, VideoPlay, VideoPause, Close } from '@element-plus/icons-vue'

const againAudio = 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/again.aac'
const xuniAudio = 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/%E8%99%9A%E6%8B%9F.aac'
const huxiAudio = 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/%E4%BC%9A%E5%91%BC%E5%90%B8%E7%9A%84%E7%97%9B.mp3'

const emit = defineEmits(['back'])

const audioRef = ref(null)
const currentAudioSrc = ref('')
const currentSong = ref(null)
const isPlaying = ref(false)

const playlist = ref([
  { id: 1, title: 'again', artist: '《四月是你的谎言》插曲', src: againAudio, cover: 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/againAvatar.png' },
  { id: 2, title: '虚拟', artist: '陈粒', src: xuniAudio, cover: 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/xuniAvatar.png' },
  { id: 3, title: '会呼吸的痛', artist: '梁静茹', src: huxiAudio, cover: 'https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/hhxdtAvatar.png' }
])

// 💡 新增：图片预览状态控制
const showPreview = ref(false)
const previewImage = ref('')

const openImage = (url) => {
  previewImage.value = url
  showPreview.value = true
}

const closeImage = () => {
  showPreview.value = false
  previewImage.value = ''
}

const togglePlay = (song) => {
  if (!audioRef.value) return

  const audio = audioRef.value

  if (currentSong.value?.id === song.id) {
    if (isPlaying.value) {
      audio.pause()
      isPlaying.value = false
    } else {
      audio.play().catch(err => {
        if (err.name !== 'AbortError') {
          console.error('播放失败:', err)
        }
      })
      isPlaying.value = true
    }
    return
  }

  currentSong.value = song
  currentAudioSrc.value = song.src
  isPlaying.value = true

  setTimeout(() => {
    if (audioRef.value) {
      audioRef.value.play().catch(err => {
        if (err.name !== 'AbortError') {
          console.error('播放失败:', err)
        }
      })
    }
  }, 50)
}

const onAudioEnded = () => { isPlaying.value = false }

const handleBack = () => {
  try {
    if (audioRef.value) {
      audioRef.value.pause()
      audioRef.value.currentTime = 0
      isPlaying.value = false
    }
  } catch (e) {
    console.error('音频暂停异常:', e)
  } finally {
    emit('back')
  }
}

onUnmounted(() => {
  if (audioRef.value) {
    audioRef.value.pause()
    audioRef.value.currentTime = 0
  }
})
</script>

<style scoped>
.secret-view-container {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; justify-content: center; align-items: center;
}
.secret-bg {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background-color: #050505;
  background-image: url('https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=2000&q=80');
  background-size: cover; background-position: center;
  filter: brightness(0.65); z-index: -1; pointer-events: none;
}
.secret-page {
  width: 95vw; max-width: 1200px; height: 90vh;
  padding: 40px 60px; text-align: center; border-radius: 24px;
  z-index: 100; color: #f8fafc;
  background: rgba(20, 10, 25, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.3);
  display: flex; flex-direction: column;
}
.secret-content { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; }
.highlight-text { margin-bottom: 10px; font-size: 32px; font-weight: bold; flex-shrink: 0; }
.subtitle { color: #94a3b8; font-family: monospace; margin-bottom: 20px; letter-spacing: 2px; flex-shrink: 0; }

/* ======== 区域划分处理 ======== */
.music-room .story-box {
  background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(244, 114, 182, 0.2);
  padding: 30px; border-radius: 16px; margin-bottom: 24px; width: 100%; text-align: left;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  flex: 1;
  overflow-y: auto;
}
.music-room .story-box::-webkit-scrollbar { width: 8px; }
.music-room .story-box::-webkit-scrollbar-track { background: transparent; }
.music-room .story-box::-webkit-scrollbar-thumb { background: rgba(244, 114, 182, 0.3); border-radius: 4px; }
.music-room .story-box::-webkit-scrollbar-thumb:hover { background: rgba(244, 114, 182, 0.6); }

.music-room .story-box p { font-size: 16px; line-height: 2; margin-bottom: 16px; color: #fdf2f8; text-indent: 2em; }
.music-room .story-box p:last-child { margin-bottom: 0; }
.music-room .story-box strong { color: #f472b6; font-weight: 600; padding: 0 4px; }

/* ======== 附加图片链接样式 ======== */
.extra-links {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px dashed rgba(244, 114, 182, 0.3);
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.links-label {
  font-size: 14px;
  color: #fbcfe8;
  font-weight: 600;
}
.img-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(244, 114, 182, 0.1);
  border: 1px solid rgba(244, 114, 182, 0.3);
  color: #fdf2f8;
  text-decoration: none;
  border-radius: 20px;
  font-size: 13px;
  transition: all 0.3s ease;
  cursor: pointer;
}
.img-link:hover {
  background: rgba(244, 114, 182, 0.25);
  border-color: rgba(244, 114, 182, 0.6);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 114, 182, 0.2);
}

/* ======== 播放器样式 ======== */
.music-player { width: 100%; display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px; flex-shrink: 0; }
.music-item { display: flex; align-items: center; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 14px 20px; border-radius: 16px; cursor: pointer; transition: all 0.3s ease; }
.music-item:hover { background: rgba(255, 255, 255, 0.15); transform: translateY(-2px); border-color: rgba(244, 114, 182, 0.3); }
.music-item.is-playing { background: rgba(244, 114, 182, 0.15); border-color: rgba(244, 114, 182, 0.5); box-shadow: 0 4px 15px rgba(244, 114, 182, 0.1); }

.song-cover {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 24px;
  color: #94a3b8;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.song-cover.rotating {
  animation: rotate-disc 3s linear infinite;
}

@keyframes rotate-disc {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

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

.enter-btn { flex-shrink: 0; }
@keyframes bounce { 0% { height: 3px; } 100% { height: 12px; } }

/* 💡 新增：图片预览遮罩与动画样式 */
.image-preview-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px);
  z-index: 9999; display: flex; justify-content: center; align-items: center;
  cursor: zoom-out;
}
.preview-img {
  max-width: 90%; max-height: 90%; border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.close-preview-btn {
  position: absolute; top: 30px; right: 30px; font-size: 36px;
  color: rgba(255, 255, 255, 0.7); cursor: pointer; transition: all 0.3s;
}
.close-preview-btn:hover { transform: scale(1.1); color: #f472b6; }

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 💡 移动端减负排版 */
@media (max-width: 768px) {
  .secret-page {
    width: 100vw;
    height: 100dvh;
    border-radius: 0;
    padding: 80px 20px 100px;
    border: none;
    background: rgba(20, 10, 25, 0.3);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }
  .music-room .story-box {
    padding: 1px;
    font-size: 14px;
    margin-bottom: 20px;
    border-radius: 12px;
    line-height: 1.1;
  }
  .extra-links {
    margin-top: 16px;
    padding-top: 12px;
  }
  .img-link {
    padding: 5px 12px;
    font-size: 12px;
  }
  .highlight-text { font-size: 24px; margin-bottom: 6px; }
  .subtitle { font-size: 12px; margin-bottom: 16px; }
  .music-item { padding: 12px 20px; border-radius: 12px; }
  .song-cover {
    width: 40px;
    height: 40px;
    margin-right: 12px;
    border-radius: 50%;
  }
  .cover-img {
    border-radius: 50%;
  }
}
</style>
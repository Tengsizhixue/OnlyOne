<template>
  <div class="secret-view-container">
    <div class="secret-bg"></div>

    <div class="secret-page shadow-2xl">
      <div class="secret-content">
        <h1 class="highlight-text" style="color: #60a5fa;">你发现了李红宝的失联空间</h1>
        <p class="subtitle">恭喜你找到：260315</p>

        <!-- 替换为带有段落格式和链接区域的 story-box -->
        <div class="story-box">
          <p>这件事让我印象比较深，因为有次给他发消息，半天不回，然后说是苹果手机问题没信息提醒，说下次要@他。结果后面@他了，到第二天才回，还说是苹果手机问题，收不到消息，真的不是他的问题。</p>
          <p>我现在基本都是在群聊里面说话，很少和别人私聊。就算在现实里面关系很好的朋友，我也几乎不在网上聊天，因为我有点轻度焦虑，只要别人不回我消息，我就会越来越急，在群里面发消息，就算一个人有事，其他人也会回我。</p>
          <p>你可能会跟我说，别人不发消息可能是因为有事在忙。我当然知道，道理我都懂，不然我怎么和朋友都不在网上单独聊，我单纯就是急，和别人是怎么想的完全没关系。</p>
          <p>对我来说，这就是一种本能反应，就和我之前的失眠一样，应该很多人都不知道，我差不多4，5年睡眠都很不稳定，就不知道什么原因，在那几年有时候就是一整夜都睡不着，但根本就不知道为什么，感觉一到晚上就对附近的事物非常敏感，后面实在受不了，去医院开药，吃了半年的药才彻底好。</p>
          <p>我不怎么在网上聊天还有一个原因就是我不玩网游，这方面的我应该后面还会再提。</p>

          <!-- 附加图片链接区（失联主题蓝色系） -->
          <div class="extra-links">
            <span class="links-label">🔗 附加内容：</span>
            <span @click="openImage('https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E6%A1%88%E5%8F%91%E7%8E%B0%E5%9C%BA1.png')" class="img-link">
              <el-icon><Picture /></el-icon> 案发现场1
            </span>
            <span @click="openImage('https://tengsizhixue.oss-cn-hangzhou.aliyuncs.com/onlyone/%E6%A1%88%E5%8F%91%E7%8E%B0%E5%9C%BA2.png')" class="img-link">
              <el-icon><Picture /></el-icon> 案发现场2
            </span>
          </div>
        </div>

        <button class="enter-btn shimmer-btn" @click="$emit('back')">返回聊天</button>
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
import { ref } from 'vue'
import { Picture, Close } from '@element-plus/icons-vue'

defineEmits(['back'])

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
</script>

<style scoped>
.secret-view-container {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; justify-content: center; align-items: center;
}
.secret-bg {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background-color: #050505;
  background-image: url('https://images.unsplash.com/photo-1510936111840-65e151ad71bb?auto=format&fit=crop&w=2000&q=80');
  background-size: cover; background-position: center;
  filter: brightness(0.65); z-index: -1; pointer-events: none;
}
.secret-page {
  width: 95vw; max-width: 1200px; height: 90vh;
  padding: 40px 60px; text-align: center; border-radius: 24px; z-index: 1; color: #f8fafc;
  background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.3);
  display: flex; flex-direction: column;
}
.secret-content { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; }
.highlight-text { margin-bottom: 10px; font-size: 32px; font-weight: bold; flex-shrink: 0; }
.subtitle { color: #94a3b8; font-family: monospace; margin-bottom: 20px; letter-spacing: 2px; flex-shrink: 0; }

/* ======== 区域划分处理（匹配主题蓝色） ======== */
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

/* ======== 附加图片链接样式（科技蓝色调） ======== */
.extra-links {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px dashed rgba(96, 165, 250, 0.3);
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.links-label {
  font-size: 14px;
  color: #bfdbfe;
  font-weight: 600;
}
.img-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(96, 165, 250, 0.1);
  border: 1px solid rgba(96, 165, 250, 0.3);
  color: #eff6ff;
  text-decoration: none;
  border-radius: 20px;
  font-size: 13px;
  transition: all 0.3s ease;
  cursor: pointer;
}
.img-link:hover {
  background: rgba(96, 165, 250, 0.25);
  border-color: rgba(96, 165, 250, 0.6);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(96, 165, 250, 0.2);
}

.enter-btn { flex-shrink: 0; }

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
.close-preview-btn:hover { transform: scale(1.1); color: #60a5fa; }

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .secret-page {
    width: 100vw;
    height: 100dvh;
    border-radius: 0;
    padding: 50px 20px 80px;
    border: none;
    background: rgba(15, 23, 42, 0.3);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }
  .story-box {
    padding: 18px;
    font-size: 14px;
    margin-bottom: 20px;
    border-radius: 12px;
    line-height: 1.8;
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
}
</style>
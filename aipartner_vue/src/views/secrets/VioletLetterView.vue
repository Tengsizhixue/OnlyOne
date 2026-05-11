<template>
  <SecretLayout
    :bg-image="bg"
    title="✉️ 无名信件总有寄件人"
    title-color="#d8b4fe"
    code="191001"
    @back="$emit('back')"
    v-slot="{ openImage, isAllUnlocked, back }"
  >
    <div class="violet-room">
      <div class="letter-box violet-theme">

        <div class="image-wrapper">
          <img
            :src="topImg"
            alt="薇尔莉特"
            class="content-img"
            @click="openImage(topImg)"
          />
        </div>

        <p>
          这动漫我是19年看的，和我那个名字“誊思致雪”是一样的，一开始还是有特殊含义了，后面完全就是路径依赖，懒得换。
          具体是什么时候看的紫罗兰我都忘了，在那个时候我就喜欢用的薇尔莉特的头像。怎么说呢，感觉自那之后我的很多习惯就没怎么变过。
          在那两年我还是看过不少动漫的，后面就看的很少了。包括什么妖狐小红娘、四月是你的谎言、你的名字、一人之下、未闻花名、柯南。
          当时最喜欢的并不是紫罗兰而是四月是你的谎言，其中的一首插曲我还听了很长时间。
        </p>

        <div class="letter-divider">
          <span class="letter-line"></span>
          <span class="wax-seal"></span>
          <span class="letter-line"></span>
        </div>

        <p>
          紫罗兰给我留下很深的印象，一开始完全是因为这动漫我感觉画质非常好，里面的风景都很好看，后面完全就是人物魅力了。
          如果你看过了我之前写的关于《我在七年后等着你》写的原文，你应该也能知道是为什么。
          我当时非常喜欢单纯的东西，那游戏和这个动漫的内核基本上都一样，纯真地追求美好的执念，无论是对待友情和爱情，主角都太“纯”了，所以风评也是两极分化。
        </p>

        <p>
          说到这个我突然想起来，我干过一件非常无聊的事。
          在那年《我在七年后等着你》这个游戏的评价是很高的，差评很少，我闲着没事干看到差评就骂，我记得那几天晚上都是直接通宵和别人对骂。
          不过早就是往事了，现在别说骂了，我都懒得在网上评论任何事。
        </p>

        <div class="letter-divider">
          <span class="letter-line"></span>
          <span class="wax-seal"></span>
          <span class="letter-line"></span>
        </div>

        <p>
          说回紫罗兰，除了微信亲戚比较多，我一般都找个薇尔莉特的头像贴上去，倒不是说我现在有多么喜欢，就是懒得找其他的，
          有的时候连薇尔莉特的头像都懒得找，随便找个非常土的头像往上一贴，贼省事。
        </p>

        <p>
          由于和紫罗兰永恒花园有关的评论已经找不到了，有关的账号我也早就注销了，所以附加内容并没有什么内容。
        </p>


        <div class="extra-links">
          <span class="links-label">🔗 附加内容：</span>
          <span @click="openImage(attach1)" class="img-link">
            <el-icon><Picture /></el-icon> 以前的吵架图
          </span>
        </div>

        <!-- 🌟 将退出和通关按钮置于文章末尾 -->
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
import { Picture } from '@element-plus/icons-vue'
import SecretLayout from '../../components/SecretLayout.vue'
import { SECRET_ASSETS } from '../../config/constants.js'

// 💡 从配置表解构资源
const { bg, topImg, attach1 } = SECRET_ASSETS.violet

defineEmits(['back'])
</script>

<style scoped>
/* 样式保持不变 */
.violet-room { width: 100%; flex: 1; display: flex; flex-direction: column; overflow-y: auto; overflow-x: hidden; padding-right: 4px; box-sizing: border-box; }
.violet-room::-webkit-scrollbar { width: 6px; }
.violet-room::-webkit-scrollbar-track { background: transparent; }
.violet-room::-webkit-scrollbar-thumb { background: rgba(192, 132, 252, 0.4); border-radius: 4px; }
.violet-room::-webkit-scrollbar-thumb:hover { background: rgba(192, 132, 252, 0.8); }
.violet-theme { background: rgba(30, 20, 45, 0.85); border: 1px solid rgba(192, 132, 252, 0.3); box-shadow: 0 10px 40px rgba(0,0,0,0.7), inset 0 0 30px rgba(192, 132, 252, 0.05); padding: 40px; border-radius: 12px; margin-bottom: 24px; width: 100%; text-align: left; flex: none; overflow: visible; box-sizing: border-box; word-wrap: break-word; }
.violet-theme p { font-size: 15px; line-height: 2.2; margin-bottom: 20px; color: #f3e8ff; text-indent: 2em; text-shadow: 0 1px 3px rgba(0,0,0,0.9); letter-spacing: 0.5px; }
.image-wrapper { display: flex; justify-content: center; margin-bottom: 30px; }
.content-img { width: 100%; max-width: 650px; border-radius: 8px; border: 1px solid rgba(192, 132, 252, 0.4); box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(192, 132, 252, 0.15); cursor: pointer; transition: transform 0.4s ease, border-color 0.4s ease; }
.content-img:hover { transform: scale(1.02); border-color: rgba(216, 180, 254, 0.8); }
.letter-divider { display: flex; align-items: center; justify-content: center; gap: 12px; margin: 36px 0; opacity: 0.7; }
.wax-seal { width: 10px; height: 10px; background: #c084fc; border-radius: 50%; box-shadow: 0 0 10px #c084fc, inset 0 0 4px rgba(0,0,0,0.5); }
.letter-line { height: 1px; width: 120px; background: linear-gradient(90deg, transparent, #c084fc, transparent); }
.extra-links { margin-top: 40px; padding-top: 20px; border-top: 1px dashed rgba(192, 132, 252, 0.3); display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.links-label { font-size: 14px; color: #d8b4fe; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
.img-link { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(192, 132, 252, 0.15); border: 1px solid rgba(192, 132, 252, 0.3); color: #f3e8ff; text-decoration: none; border-radius: 20px; font-size: 13px; transition: all 0.3s ease; cursor: pointer; backdrop-filter: blur(4px); }
.img-link:hover { background: rgba(192, 132, 252, 0.3); border-color: #d8b4fe; color: #fff; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(192, 132, 252, 0.3); }

.bottom-action { margin-top: 40px; display: flex; justify-content: center; }

@media (max-width: 768px) {
  .violet-theme { padding: 24px 16px; margin-bottom: 20px; }
  .violet-theme p { font-size: 14px; line-height: 2; margin-bottom: 16px; }
  .letter-divider { margin: 24px 0; }
  .letter-line { width: 80px; }
  .image-wrapper { margin-bottom: 20px; }
  .extra-links { margin-top: 24px; padding-top: 16px; }
  .img-link { padding: 5px 12px; font-size: 12px; }
}
</style>
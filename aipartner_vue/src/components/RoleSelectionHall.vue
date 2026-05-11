<template>
  <div class="selection-hall" @touchstart.passive="handleTouchStart" @touchend.passive="handleTouchEnd" @wheel="handleWheel">

    <!-- 🌟 修改1 & 2：独立大背景层，强制中心对齐，保证图像原汁原味地居中 -->
    <div class="hall-bg-layer">
      <div
        v-for="(role, index) in availableRoles"
        :key="'bg-'+role.role_type"
        class="hall-bg-image"
        :style="{ backgroundImage: `url(${getCurrentRoleConfig(role.role_type).hallBgUrl || getCurrentRoleConfig(role.role_type).bgUrl})` }"
        :class="{ 'show-bg': index === activeCarouselIndex }"
      ></div>
    </div>

    <!-- 🌟 修改1：移除四周发黑发虚的径向渐变，改为极其微弱的纯色遮罩，彻底还给大背景清晰度 -->
    <div class="hall-overlay"></div>

    <!-- 当触发进出场动画时，隐藏外围 UI -->
    <button class="top-exit-btn" :class="{ 'ui-fade-out': isEnteringChat }" @click="router.push('/')" title="返回首页">
      <el-icon><House /></el-icon>
    </button>

    <div class="carousel-3d">
      <div
        v-for="(role, index) in availableRoles"
        :key="role.role_type"
        class="carousel-card"
        :class="{ active: index === activeCarouselIndex }"
        :style="getCardStyle(index)"
        @click="handleCardClick(index)"
      >
        <div class="card-inner-bg" :style="{
          backgroundImage: `url(${getCurrentRoleConfig(role.role_type).bgUrl})`,
          backgroundPosition: getCurrentRoleConfig(role.role_type).bgPosition
        }"></div>

        <div class="card-mask"></div>

        <div class="card-glow-border" :style="{
          borderColor: index === activeCarouselIndex ? 'rgba(255,255,255,0.9)' : 'rgba(255, 255, 255, 0.15)',
          boxShadow: index === activeCarouselIndex
            ? `0 0 25px 2px ${getCurrentRoleConfig(role.role_type).glowColor}, 0 0 40px 8px rgba(255,255,255,0.1), inset 0 0 20px ${getCurrentRoleConfig(role.role_type).glowColor}`
            : 'none'
        }"></div>

        <!-- 卡片内容层 -->
        <div class="card-content">
          <img
            :src="getCurrentRoleConfig(role.role_type).avatar"
            class="card-avatar"
            :style="{
              borderColor: index === activeCarouselIndex ? getCurrentRoleConfig(role.role_type).themeColor : 'rgba(255,255,255,0.6)'
            }"
          />

          <h3 class="card-name" :style="{
            color: index === activeCarouselIndex ? getCurrentRoleConfig(role.role_type).themeColor : '#f1f5f9'
          }">{{ role.name }}</h3>

          <p class="card-desc">{{ getCurrentRoleConfig(role.role_type).welcomeText }}</p>

          <div class="click-hint" :class="{ visible: index === activeCarouselIndex && !isEnteringChat }">
            <span class="shimmer-text">点击进入对话</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 控制按钮 -->
    <div class="carousel-controls" :class="{ 'ui-fade-out': isEnteringChat }">
      <button class="nav-arrow" @click.stop="prevRole" :disabled="activeCarouselIndex === 0">
        <el-icon><ArrowLeftBold/></el-icon>
      </button>
      <button class="nav-arrow" @click.stop="nextRole" :disabled="activeCarouselIndex === availableRoles.length - 1">
        <el-icon><ArrowRightBold/></el-icon>
      </button>
    </div>

    <transition name="fade-hall">
      <div class="custom-inputs-center" v-if="roleConfig.role_type === '自定义' && !isEnteringChat">
        <el-input v-model="roleConfig.name" placeholder="设定伙伴的称呼" class="glass-input custom-name-input" />
        <el-input v-model="roleConfig.nature" type="textarea" placeholder="设定TA的性格与世界观..." class="glass-textarea" />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { House, ArrowLeftBold, ArrowRightBold } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getCurrentRoleConfig } from '../config/constants.js'

const props = defineProps({
  availableRoles: { type: Array, required: true },
  roleConfig: { type: Object, required: true }
})

const emit = defineEmits(['update-role', 'enter-chat'])
const router = useRouter()

const activeCarouselIndex = ref(0)
const isMobile = ref(false)

// 沉浸式动画状态变量
const isEnteringChat = ref(false)

let touchStartX = 0
let lastWheelTime = 0

const nextRole = () => {
  if (isEnteringChat.value) return
  if (activeCarouselIndex.value < props.availableRoles.length - 1) {
    activeCarouselIndex.value++
  }
}

const prevRole = () => {
  if (isEnteringChat.value) return
  if (activeCarouselIndex.value > 0) {
    activeCarouselIndex.value--
  }
}

const handleCardClick = (index) => {
  if (activeCarouselIndex.value === index) {
    if (props.roleConfig.role_type === '自定义' && (!props.roleConfig.name || !props.roleConfig.name.trim())) {
      ElMessage.warning('请先为自定义伙伴设定称呼！')
      return
    }

    // 触发冲向屏幕的景深动画
    isEnteringChat.value = true

    setTimeout(() => {
      emit('enter-chat')
      setTimeout(() => { isEnteringChat.value = false }, 100)
    }, 200)

  } else {
    activeCarouselIndex.value = index
  }
}

const handleWheel = (e) => {
  if (isEnteringChat.value) return
  const now = Date.now()
  if (now - lastWheelTime < 250) return

  if (e.deltaY > 30) {
    nextRole()
    lastWheelTime = now
  } else if (e.deltaY < -30) {
    prevRole()
    lastWheelTime = now
  }
}

const handleTouchStart = (e) => {
  if (isEnteringChat.value) return
  touchStartX = e.touches[0].clientX
}

const handleTouchEnd = (e) => {
  if (isEnteringChat.value) return
  const touchEndX = e.changedTouches[0].clientX
  const delta = touchStartX - touchEndX
  if (Math.abs(delta) > 30) {
    if (delta > 0) nextRole()
    else prevRole()
  }
}

// 🌟 修改3：3D矩阵算法重构（将 Convex 凸形算法改为 Concave 凹形算法）
const getCardStyle = (index) => {
  const offset = index - activeCarouselIndex.value
  const absOffset = Math.abs(offset)
  const sign = Math.sign(offset)

  // 设置推开的间距和旋转幅度
  const xTranslate = isMobile.value ? 140 : 320
  const zTranslate = isMobile.value ? 160 : 250
  const rotate = isMobile.value ? 45 : 55
  const scale = 1 - absOffset * 0.2

  let transform = ''
  let opacity = 1
  let zIndex = 100 - absOffset

  if (isEnteringChat.value) {
    // 电影级过场状态
    if (offset === 0) {
      transform = `translate3d(0px, 0px, 400px) scale(1.15)`
      opacity = 0
    } else {
      transform = `translate3d(${sign * (xTranslate * absOffset + 150)}px, 0, ${-zTranslate * absOffset - 100}px) rotateY(${sign * (rotate + 20)}deg) scale(${scale - 0.2})`
      opacity = 0
    }
  } else {
    // 常规轮播状态
    if (offset === 0) {
      transform = `translate3d(0px, 0px, 50px) rotateY(0deg) scale(1)`
      opacity = 1
    } else {
      // 💡 核心改动：把原本的 rotateY(${-sign * rotate}deg) 改成正号 rotateY(${sign * rotate}deg)
      // 这会让两侧卡片的“内边缘”向用户靠拢，形成类似环幕电影的“凹形”包围感
      transform = `translate3d(${sign * xTranslate * absOffset}px, 0, ${-zTranslate * absOffset}px) rotateY(${sign * rotate}deg) scale(${scale})`
      opacity = absOffset === 1 ? 0.35 : 0
    }
  }

  return {
    transform,
    zIndex,
    opacity,
    pointerEvents: offset === 0 && !isEnteringChat.value ? 'auto' : 'none'
  }
}

watch(activeCarouselIndex, (newIdx) => {
  if (props.availableRoles[newIdx]) {
    emit('update-role', props.availableRoles[newIdx].role_type)
  }
})

watch(() => props.roleConfig.role_type, (newType) => {
  const idx = props.availableRoles.findIndex(r => r.role_type === newType)
  if (idx !== -1 && idx !== activeCarouselIndex.value) {
    activeCarouselIndex.value = idx
  }
}, { immediate: true })

const checkMobile = () => { isMobile.value = window.innerWidth <= 768 }

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => window.removeEventListener('resize', checkMobile))
</script>

<style scoped>
.selection-hall {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  perspective: 1200px; z-index: 50; user-select: none; overflow: hidden;
  background: transparent;
  touch-action: none;
}

.hall-bg-layer {
  position: absolute; inset: 0; z-index: -2; overflow: hidden;
}
.hall-bg-image {
  position: absolute; inset: 0; /* 💡 修改：归零边界，不再强行裁剪缩放，确保原始构图 */
  background-size: cover;
  background-position: center center; /* 💡 修改：强制中心对齐！ */
  opacity: 0; transition: opacity 0.8s ease-in-out;
}
.hall-bg-image.show-bg {
  opacity: 1;
}

.hall-overlay {
  position: absolute; inset: 0;
  /* 💡 修改：移除了让你觉得边缘发黑发虚的渐变圈，换成极其清透均匀的底色 */
  background: rgba(0, 0, 0, 0.1);
  z-index: -1;
  pointer-events: none;
}

/* 轮播主体 */
.carousel-3d {
  position: relative; width: 280px; height: 460px;
  transform-style: preserve-3d;
  will-change: transform;
}

.carousel-card {
  position: absolute; width: 100%; height: 100%;
  border-radius: 16px;
  background: rgba(30, 41, 59, 0.8);
  transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), opacity 0.4s ease;
  will-change: transform, opacity;
  backface-visibility: hidden;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.carousel-card.active {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.card-inner-bg {
  position: absolute; inset: 0;
  background-size: cover;
  transition: transform 0.6s ease;
  transform: translateZ(0);
  z-index: 1;
}

.card-mask {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.8) 100%);
  z-index: 2;
}

.card-glow-border {
  position: absolute; inset: 0;
  border-radius: 16px;
  pointer-events: none;
  z-index: 5;
  transition: all 0.4s ease;
}

.card-content {
  position: relative; z-index: 3;
  padding: 30px 0;
  width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}

.card-avatar {
  width: 90px; height: 90px; border-radius: 50%; margin-bottom: 20px;
  border: 3px solid rgba(255,255,255,0.8); object-fit: cover;
  transition: transform 0.6s ease;
  transform: translateZ(0);
}

.card-name {
  font-size: 30px;
  font-family: "STKaiti", "KaiTi", "serif";
  font-weight: bold; margin: 0 0 12px 0;
  letter-spacing: 2px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.8);
}

.card-desc {
  font-size: 13px; line-height: 1.5; color: #e2e8f0;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
  overflow: hidden; padding: 0 20px; margin-bottom: 10px;
}

.click-hint {
  position: absolute; bottom: 25px;
  transition: opacity 0.5s, transform 0.5s;
  opacity: 0; transform: translate3d(0, 10px, 0);
}
.click-hint.visible { opacity: 1; transform: translate3d(0, 0, 0); }

.carousel-controls {
  position: absolute; bottom: 6%; left: 50%; transform: translateX(-50%);
  display: flex; gap: 80px; z-index: 10;
  transition: opacity 0.5s ease;
}
.nav-arrow {
  background: transparent; border: none; color: white; font-size: 36px;
  cursor: pointer; opacity: 0.5; transition: opacity 0.3s, transform 0.3s;
}
.nav-arrow:hover:not(:disabled) { opacity: 1; transform: scale(1.2); }
.nav-arrow:disabled { opacity: 0.1; cursor: not-allowed; }

.top-exit-btn {
  position: absolute; top: 20px; left: 20px; z-index: 60;
  width: 44px; height: 44px; border-radius: 50%;
  background: rgba(0, 0, 0, 0.4); border: 1px solid rgba(255,255,255,0.1);
  color: white; font-size: 20px; cursor: pointer;
  transition: transform 0.3s ease, background 0.3s ease, opacity 0.5s ease;
}

.ui-fade-out {
  opacity: 0 !important;
  pointer-events: none !important;
}

.custom-inputs-center {
  position: absolute; bottom: 20%; display: flex; flex-direction: column; gap: 14px;
  width: 100%; max-width: 340px; z-index: 10;
}
:deep(.custom-name-input .el-input__inner) { text-align: center; font-weight: bold; font-size: 16px; }

.fade-hall-enter-active, .fade-hall-leave-active { transition: opacity 0.4s ease, transform 0.4s ease; }
.fade-hall-enter-from { opacity: 0; transform: scale(1.05); }
.fade-hall-leave-to { opacity: 0; transform: scale(0.95); }

/* 移动端适配 */
@media (max-width: 768px) {
  .carousel-3d { width: 210px; height: 400px; }
  .card-avatar { width: 70px; height: 70px; margin-bottom: 12px; }
  .card-name { font-size: 24px; letter-spacing: 1px;}
  .card-desc { font-size: 12px; padding: 0 14px; }
  .carousel-controls { bottom: 5%; gap: 60px; }
}
</style>
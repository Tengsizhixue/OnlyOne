<template>
  <div class="selection-hall" @touchstart.passive="handleTouchStart" @touchend.passive="handleTouchEnd" @wheel="handleWheel">

    <div class="hall-bg-layer">
      <div
        v-for="(role, index) in availableRoles"
        :key="'bg-'+role.role_type"
        class="hall-bg-image"
        :style="getBgStyle(role.role_type)"
        :class="{ 'show-bg': index === activeCarouselIndex }"
      ></div>
    </div>

    <div class="hall-overlay"></div>

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

        <!-- 边缘柔化渐变 -->
        <div class="card-edge-vignette"></div>

        <!-- 卡片闪光效果 -->
        <div class="card-shine" :class="{ 'is-shining': index === activeCarouselIndex }"></div>

        <!-- 边缘动态流光特效 -->
        <div class="streamer-wrapper" v-if="index === activeCarouselIndex">
          <div class="streamer-bg" :style="{
            '--theme-color': getCurrentRoleConfig(role.role_type).themeColor
          }"></div>
        </div>

        <!-- 静态边框 -->
        <div class="card-glow-border" :style="{
          borderColor: index === activeCarouselIndex ? 'transparent' : 'rgba(255, 255, 255, 0.15)',
          boxShadow: index === activeCarouselIndex
            ? `0 0 35px 5px ${getCurrentRoleConfig(role.role_type).glowColor}, 0 0 50px 10px rgba(255,255,255,0.1), inset 0 0 30px ${getCurrentRoleConfig(role.role_type).glowColor}`
            : 'none'
        }"></div>

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

const getBgStyle = (roleType) => {
  const config = getCurrentRoleConfig(roleType)
  if (isMobile.value) {
    return {
      backgroundImage: `url(${config.hallBgUrlMobile || config.hallBgUrl || config.bgUrl})`,
      backgroundPosition: config.hallBgPositionMobile || config.hallBgPosition || 'center center'
    }
  } else {
    return {
      backgroundImage: `url(${config.hallBgUrl || config.bgUrl})`,
      backgroundPosition: config.hallBgPosition || 'center center'
    }
  }
}

const getCardStyle = (index) => {
  const offset = index - activeCarouselIndex.value
  const absOffset = Math.abs(offset)
  const sign = Math.sign(offset)

  const xTranslate = isMobile.value ? 140 : 320
  const zTranslate = isMobile.value ? 160 : 250
  const rotate = isMobile.value ? 45 : 55
  const scale = 1 - absOffset * 0.2

  let transform = ''
  let opacity = 1
  let zIndex = 100 - absOffset

  if (isEnteringChat.value) {
    if (offset === 0) {
      transform = `translate3d(0px, 0px, 400px) scale(1.15)`
      opacity = 0
    } else {
      transform = `translate3d(${sign * (xTranslate * absOffset + 150)}px, 0, ${-zTranslate * absOffset - 100}px) rotateY(${-sign * (rotate + 20)}deg) scale(${scale - 0.2})`
      opacity = 0
    }
  } else {
    if (offset === 0) {
      transform = `translate3d(0px, 0px, 50px) rotateY(0deg) scale(1)`
      opacity = 1
    } else {
      transform = `translate3d(${sign * xTranslate * absOffset}px, 0, ${-zTranslate * absOffset}px) rotateY(${-sign * rotate}deg) scale(${scale})`
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

// 🌟 核心优化：后台静默预加载所有角色的背景和头像
const preloadAssets = () => {
  // 延迟 1 秒执行，绝对不抢占首屏 Vue 渲染和第一张图的加载带宽
  setTimeout(() => {
    props.availableRoles.forEach(role => {
      const config = getCurrentRoleConfig(role.role_type)
      if (config) {
        const bgImg = new Image()
        bgImg.src = isMobile.value ? (config.hallBgUrlMobile || config.hallBgUrl || config.bgUrl) : (config.hallBgUrl || config.bgUrl)

        const cardImg = new Image()
        cardImg.src = config.bgUrl

        const avatarImg = new Image()
        avatarImg.src = config.avatar
      }
    })
  }, 1000)
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
  preloadAssets() // 启动预加载引擎
})

onUnmounted(() => window.removeEventListener('resize', checkMobile))
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700&display=swap');

.selection-hall {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  perspective: 1200px;
  -webkit-perspective: 1200px;
  z-index: 50; user-select: none; overflow: hidden;
  background: #050505;
  touch-action: none;
}

.hall-bg-layer {
  position: absolute; inset: 0; z-index: -2; overflow: hidden;
}
.hall-bg-image {
  position: absolute; inset: 0;
  background-size: cover;
  background-position: center center;
  opacity: 0; transition: opacity 0.8s ease-in-out;
  transform: translateZ(0);
  -webkit-transform: translateZ(0);
}
.hall-bg-image.show-bg {
  opacity: 1;
}

.hall-overlay {
  position: absolute; inset: 0;
  background: rgba(0, 0, 0, 0.1);
  z-index: -1;
  pointer-events: none;
}

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
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0,0,0,0.6);
}

.carousel-card.active {
  border: none;
}

.card-inner-bg {
  position: absolute; inset: 0;
  background-size: cover;
  filter: blur(3.5px);
  transform: scale(1.08) translateZ(0);
  -webkit-transform: scale(1.08) translateZ(0);
  transition: transform 0.6s ease, filter 0.6s ease;
  z-index: 1;
}

.card-mask {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.85) 100%);
  z-index: 2;
}

.card-edge-vignette {
  position: absolute; inset: 0;
  border-radius: 16px;
  box-shadow: inset 0 0 60px rgba(0,0,0,0.9), inset 0 0 25px rgba(0,0,0,0.6);
  z-index: 3;
  pointer-events: none;
}

.card-shine {
  position: absolute; inset: 0;
  border-radius: 16px;
  z-index: 6;
  pointer-events: none;
  background: linear-gradient(
    105deg,
    transparent 20%,
    rgba(255, 255, 255, 0.05) 25%,
    rgba(255, 255, 255, 0.4) 28%,
    rgba(255, 255, 255, 0.05) 31%,
    transparent 36%
  );
  background-size: 200% 200%;
  opacity: 0;
}
.card-shine.is-shining {
  animation: shine-sweep 4s infinite cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes shine-sweep {
  0% { background-position: 200% 200%; opacity: 0; }
  10% { opacity: 1; }
  40% { background-position: -100% -100%; opacity: 0; }
  100% { background-position: -100% -100%; opacity: 0; }
}

.streamer-wrapper {
  position: absolute; inset: 0;
  border-radius: 16px;
  overflow: hidden;
  z-index: 5;
  pointer-events: none;
  padding: 2px;
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
}
.streamer-bg {
  position: absolute;
  top: 50%; left: 50%;
  width: 250%; height: 250%;
  background: conic-gradient(
    from 0deg,
    transparent 0%,
    transparent 70%,
    var(--theme-color) 90%,
    #ffffff 100%
  );
  transform: translate(-50%, -50%);
  animation: rotate-streamer 3s linear infinite;
}
@keyframes rotate-streamer {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

.card-glow-border {
  position: absolute; inset: 0;
  border-radius: 16px;
  pointer-events: none;
  z-index: 4;
  transition: all 0.4s ease;
  border: 1px solid transparent;
}

.card-content {
  position: relative; z-index: 7;
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
  font-size: 34px;
  font-family: "Kaiti SC", "STKaiti", "KaiTi", "华文楷体", "楷体", "Noto Serif SC", serif;
  font-weight: bold;
  margin: 0 0 16px 0;
  letter-spacing: 4px;
  transition: color 0.4s ease;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

.card-desc {
  font-size: 14px; line-height: 1.6; color: #e2e8f0;
  font-family: 'Noto Serif SC', 'ZCOOL XiaoWei', "STKaiti", "KaiTi", serif;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
  overflow: hidden; padding: 0 20px; margin-bottom: 10px;
  text-shadow: 0 1px 3px rgba(0,0,0,0.6);
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

@media (max-width: 768px) {
  .carousel-3d { width: 210px; height: 400px; }
  .card-avatar { width: 70px; height: 70px; margin-bottom: 12px; }
  .card-name { font-size: 26px; letter-spacing: 1px;}
  .card-desc { font-size: 13px; padding: 0 14px; }
  .carousel-controls { bottom: 5%; gap: 60px; }
}
</style>
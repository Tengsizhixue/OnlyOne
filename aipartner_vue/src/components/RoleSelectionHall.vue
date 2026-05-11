<template>
  <div class="selection-hall" @touchstart.passive="handleTouchStart" @touchend.passive="handleTouchEnd">

    <!-- 背景层 -->
    <div class="hall-bg-container">
      <div class="hall-bg" style="background-image: url('https://images.unsplash.com/photo-1534796636918-9b168a52edce?auto=format&fit=crop&w=2000&q=80');"></div>
    </div>
    <div class="hall-overlay"></div>

    <!-- 🌟 当触发进出场动画时，隐藏外围 UI -->
    <button class="top-exit-btn" :class="{ 'ui-fade-out': isEnteringChat || isAppearing }" @click="router.push('/')" title="返回首页">
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

          <div class="click-hint" :class="{ visible: index === activeCarouselIndex && !isEnteringChat && !isAppearing }">
            <span class="shimmer-text">点击进入对话</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 控制按钮 -->
    <div class="carousel-controls" :class="{ 'ui-fade-out': isEnteringChat || isAppearing }">
      <button class="nav-arrow" @click.stop="prevRole" :disabled="activeCarouselIndex === 0">
        <el-icon><ArrowLeftBold/></el-icon>
      </button>
      <button class="nav-arrow" @click.stop="nextRole" :disabled="activeCarouselIndex === availableRoles.length - 1">
        <el-icon><ArrowRightBold/></el-icon>
      </button>
    </div>

    <transition name="fade-hall">
      <div class="custom-inputs-center" v-if="roleConfig.role_type === '自定义' && !isEnteringChat && !isAppearing">
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

// 🌟 沉浸式动画状态变量
const isEnteringChat = ref(false) // 正在冲入聊天室
const isAppearing = ref(true)     // 正在从聊天室返回大厅（刚加载）

let touchStartX = 0
let isAnimating = false

const nextRole = () => {
  if (isEnteringChat.value || isAppearing.value) return // 动画中禁止滑动
  if (activeCarouselIndex.value < props.availableRoles.length - 1 && !isAnimating) {
    isAnimating = true
    activeCarouselIndex.value++
    setTimeout(() => { isAnimating = false }, 400)
  }
}

const prevRole = () => {
  if (isEnteringChat.value || isAppearing.value) return // 动画中禁止滑动
  if (activeCarouselIndex.value > 0 && !isAnimating) {
    isAnimating = true
    activeCarouselIndex.value--
    setTimeout(() => { isAnimating = false }, 400)
  }
}

const handleCardClick = (index) => {
  if (activeCarouselIndex.value === index) {
    if (props.roleConfig.role_type === '自定义' && (!props.roleConfig.name || !props.roleConfig.name.trim())) {
      ElMessage.warning('请先为自定义伙伴设定称呼！')
      return
    }

    // 🌟 触发冲向屏幕的景深动画
    isEnteringChat.value = true

    // 延迟 450ms 让卡片放大到填满视线时，再触发页面路由跳转，实现无缝衔接！
    setTimeout(() => {
      emit('enter-chat')
      // 预留重置时间，以备用户点击“新建对话”再次返回大厅时恢复原状
      setTimeout(() => { isEnteringChat.value = false }, 100)
    }, 450)

  } else {
    activeCarouselIndex.value = index
  }
}

const handleTouchStart = (e) => {
  if (isEnteringChat.value || isAppearing.value) return
  touchStartX = e.touches[0].clientX
}

const handleTouchEnd = (e) => {
  if (isEnteringChat.value || isAppearing.value) return
  const touchEndX = e.changedTouches[0].clientX
  const delta = touchStartX - touchEndX
  if (Math.abs(delta) > 30) {
    if (delta > 0) nextRole()
    else prevRole()
  }
}

// 🌟 核心景深运算：计算进退场与平时滑动时的空间位移
const getCardStyle = (index) => {
  const offset = index - activeCarouselIndex.value
  const absOffset = Math.abs(offset)
  const sign = Math.sign(offset)

  const xTranslate = isMobile.value ? 90 : 250
  const zTranslate = isMobile.value ? 120 : 200
  const rotate = isMobile.value ? 35 : 45
  const scale = 1 - absOffset * 0.1

  let transform = ''
  let opacity = 1
  let zIndex = 100 - absOffset

  if (isEnteringChat.value || isAppearing.value) {
    // 🌟 电影级过场状态：
    // 当前激活卡片冲向屏幕 (Z轴大幅拉进)，其余卡片向两端飞散并后退
    if (offset === 0) {
      transform = `translate3d(0px, 0px, 400px) scale(1.15)`
      opacity = 0
    } else {
      transform = `translate3d(${sign * (xTranslate * absOffset + 150)}px, 0, ${-zTranslate * absOffset - 100}px) rotateY(${-sign * (rotate + 20)}deg) scale(${scale - 0.2})`
      opacity = 0
    }
  } else {
    // 🌟 常规轮播状态：
    if (offset === 0) {
      transform = `translate3d(0px, 0px, 50px) rotateY(0deg) scale(1)`
    } else {
      transform = `translate3d(${sign * xTranslate * absOffset}px, 0, ${-zTranslate * absOffset}px) rotateY(${-sign * rotate}deg) scale(${scale})`
      opacity = absOffset > 2 ? 0 : 1
    }
  }

  return {
    transform,
    zIndex,
    opacity,
    pointerEvents: offset === 0 && !isEnteringChat.value && !isAppearing.value ? 'auto' : 'none'
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

  // 🌟 初次挂载时（或从聊天返回大厅时），稍微延迟 50ms 将 Appearing 状态解除
  // 让卡片从屏幕外飞回到 Coverflow 位置，形成丝滑的回退动画
  setTimeout(() => {
    isAppearing.value = false
  }, 50)
})

onUnmounted(() => window.removeEventListener('resize', checkMobile))
</script>

<style scoped>
.selection-hall {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  perspective: 1000px; z-index: 50; user-select: none; overflow: hidden;
  background-color: #050505;
}

.hall-bg-container {
  position: absolute; inset: 0; z-index: -2;
  transform: translateZ(0);
}
.hall-bg {
  position: absolute; inset: -10%;
  background-size: cover; background-position: center;
  filter: blur(20px) brightness(0.5);
  transform: translateZ(0);
}
.hall-overlay {
  position: absolute; inset: 0;
  background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.4) 100%);
  z-index: -1;
}

.carousel-3d {
  position: relative; width: 300px; height: 450px;
  transform-style: preserve-3d;
  will-change: transform;
}

.carousel-card {
  position: absolute; width: 100%; height: 100%;
  border-radius: 16px;
  background: rgba(30, 41, 59, 0.8);
  /* 🌟 动画升华：拉长动画时间到 0.6s，并加入平滑缓冲曲线，体现阻尼与重量感 */
  transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.6s ease;
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

.card-glow-layer {
  position: absolute; inset: 0;
  border-radius: 16px;
  pointer-events: none;
  z-index: 5;
  transition: opacity 0.6s ease;
  border: 2px solid rgba(255, 255, 255, 0.5);
  box-shadow:
    0 0 20px var(--glow-color),
    inset 0 0 15px var(--glow-color);
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

/* 🌟 控制按钮层：加入渐隐渐显过渡 */
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

/* 🌟 全局隐藏类：动画播放时让所有按键优雅退场 */
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
  .carousel-3d { width: 240px; height: 400px; }
  .card-avatar { width: 80px; height: 80px; }
  .card-name { font-size: 26px; }
  .carousel-controls { bottom: 4%; gap: 60px; }
}
</style>
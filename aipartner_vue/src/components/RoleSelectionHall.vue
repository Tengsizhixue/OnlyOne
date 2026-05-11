<template>
  <div class="selection-hall" @touchstart.passive="handleTouchStart" @touchend.passive="handleTouchEnd">

    <!-- 总的背景图层 -->
    <div class="hall-bg" style="background-image: url('https://images.unsplash.com/photo-1534796636918-9b168a52edce?auto=format&fit=crop&w=2000&q=80');"></div>
    <div class="hall-overlay"></div>

    <button class="top-exit-btn" @click="router.push('/')" title="返回首页">
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
        <!-- 🌟 核心清理：直接使用常量获取背景信息 -->
        <div class="card-inner-bg" :style="{
          backgroundImage: `url(${getCurrentRoleConfig(role.role_type).bgUrl})`,
          backgroundPosition: getCurrentRoleConfig(role.role_type).bgPosition
        }"></div>

        <div class="card-mask"></div>

        <!-- 🌟 动态边缘泛光：直接使用常量获取颜色 -->
        <div class="card-glow-border" :style="{
          borderColor: index === activeCarouselIndex ? 'rgba(255,255,255,0.9)' : 'rgba(255, 255, 255, 0.15)',
          boxShadow: index === activeCarouselIndex
            ? `0 0 25px 2px ${getCurrentRoleConfig(role.role_type).glowColor}, 0 0 40px 8px rgba(255,255,255,0.1), inset 0 0 20px ${getCurrentRoleConfig(role.role_type).glowColor}`
            : 'none'
        }"></div>

        <!-- 卡片内容 -->
        <div class="card-content">
          <img
            :src="getCurrentRoleConfig(role.role_type).avatar"
            class="card-avatar"
            :style="{
              borderColor: index === activeCarouselIndex ? getCurrentRoleConfig(role.role_type).themeColor : 'rgba(255,255,255,0.8)',
              boxShadow: index === activeCarouselIndex
                ? `0 0 25px ${getCurrentRoleConfig(role.role_type).glowColor}, 0 10px 20px rgba(0,0,0,0.5)`
                : '0 10px 20px rgba(0,0,0,0.5)'
            }"
          />

          <h3 class="card-name" :style="{
            color: index === activeCarouselIndex ? getCurrentRoleConfig(role.role_type).themeColor : '#f1f5f9',
            textShadow: index === activeCarouselIndex
              ? `0 0 15px ${getCurrentRoleConfig(role.role_type).glowColor}, 0 3px 6px rgba(0,0,0,0.9)`
              : `0 2px 4px rgba(0,0,0,0.9)`
          }">{{ role.name }}</h3>

          <p class="card-desc">{{ getCurrentRoleConfig(role.role_type).welcomeText }}</p>

          <div class="click-hint" :class="{ visible: index === activeCarouselIndex }">
            <span class="shimmer-text">点击进入对话</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 轮播控制按钮 -->
    <div class="carousel-controls">
      <button class="nav-arrow" @click.stop="prevRole" :disabled="activeCarouselIndex === 0">
        <el-icon><ArrowLeftBold/></el-icon>
      </button>
      <button class="nav-arrow" @click.stop="nextRole" :disabled="activeCarouselIndex === availableRoles.length - 1">
        <el-icon><ArrowRightBold/></el-icon>
      </button>
    </div>

    <!-- 自定义角色 -->
    <transition name="fade-hall">
      <div class="custom-inputs-center" v-if="roleConfig.role_type === '自定义'">
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
let touchStartX = 0

// 💡 此处已经完全移除了臃肿的 roleThemeMap 等本地字典

const nextRole = () => { if (activeCarouselIndex.value < props.availableRoles.length - 1) activeCarouselIndex.value++ }
const prevRole = () => { if (activeCarouselIndex.value > 0) activeCarouselIndex.value-- }

const handleCardClick = (index) => {
  if (activeCarouselIndex.value === index) {
    if (props.roleConfig.role_type === '自定义' && (!props.roleConfig.name || !props.roleConfig.name.trim())) {
      ElMessage.warning('请先为自定义伙伴设定称呼！')
      return
    }
    emit('enter-chat')
  } else {
    activeCarouselIndex.value = index
  }
}

const handleTouchStart = (e) => { touchStartX = e.touches[0].clientX }
const handleTouchEnd = (e) => {
  const touchEndX = e.changedTouches[0].clientX
  if (touchStartX - touchEndX > 50) nextRole()
  else if (touchEndX - touchStartX > 50) prevRole()
}

const getCardStyle = (index) => {
  const offset = index - activeCarouselIndex.value
  const absOffset = Math.abs(offset)
  const sign = Math.sign(offset)

  const xTranslate = isMobile.value ? 110 : 250
  const zTranslate = isMobile.value ? 100 : 200
  const rotate = isMobile.value ? 25 : 35
  const scaleDrop = isMobile.value ? 0.15 : 0.1

  let transform = ''
  let opacity = 1
  let zIndex = 100 - absOffset

  if (offset === 0) {
    transform = `translateX(0px) translateZ(80px) rotateY(0deg) scale(1)`
  } else {
    transform = `translateX(${sign * xTranslate * absOffset}px) translateZ(-${zTranslate * absOffset}px) rotateY(${-sign * rotate}deg) scale(${1 - absOffset * scaleDrop})`
    opacity = absOffset > 2 ? 0 : (1 - absOffset * 0.3)
  }

  return { transform, zIndex, opacity, pointerEvents: absOffset > 1 ? 'none' : 'auto' }
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
/* (样式代码保持不变，完全保留之前优化好的呼吸感 padding 和过渡效果) */
.selection-hall {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  perspective: 1200px; z-index: 50; user-select: none; overflow: hidden;
}

.hall-bg {
  position: absolute; inset: 0;
  background-size: cover; background-position: center;
  filter: blur(10px) saturate(0.8);
  transform: scale(1.1);
  z-index: -2;
}
.hall-overlay {
  position: absolute; inset: 0;
  background: radial-gradient(circle at center, rgba(15,23,42,0.3) 0%, rgba(15,23,42,0.8) 100%);
  z-index: -1;
}

.top-exit-btn {
  position: absolute; top: 30px; left: 30px; z-index: 60;
  width: 48px; height: 48px; border-radius: 50%;
  background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);
  color: white; font-size: 24px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s;
}
.top-exit-btn:hover { background: rgba(0, 0, 0, 0.6); transform: scale(1.1); }

.carousel-3d {
  position: relative; width: 340px; height: 500px;
  transform-style: preserve-3d; display: flex; justify-content: center; align-items: center;
}

.carousel-card {
  position: absolute; width: 100%; height: 100%;
  border-radius: 12px;
  text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;
  transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1); cursor: pointer;
  box-shadow: 0 15px 50px rgba(0,0,0,0.6); overflow: hidden;
}

.card-inner-bg {
  position: absolute; inset: 0;
  background-size: cover;
  transition: transform 0.6s ease;
  z-index: 1;
}
.carousel-card.active .card-inner-bg { transform: scale(1.05); }

.card-mask {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.5) 50%, rgba(0,0,0,0.9) 100%);
  z-index: 2;
}

.card-glow-border {
  position: absolute; inset: 0;
  border-radius: 12px;
  border: 2px solid transparent;
  transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
  pointer-events: none; z-index: 5;
}

.card-content {
  position: relative; z-index: 3;
  padding: 40px 0;
  width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center;
  justify-content: center;
}

.card-avatar {
  width: 110px; height: 110px; border-radius: 50%; margin-bottom: 24px;
  border: 3px solid rgba(255,255,255,0.8); object-fit: cover;
  box-shadow: 0 10px 20px rgba(0,0,0,0.5); transition: all 0.4s ease;
}

.card-name {
  font-size: 34px;
  font-family: "STKaiti", "KaiTi", "华文楷体", "楷体", serif;
  font-weight: bold;
  margin: 0 0 16px 0;
  letter-spacing: 4px;
  transition: all 0.5s ease;
}

.card-desc {
  font-size: 14px; line-height: 1.6; color: #e2e8f0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.9);
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
  padding: 0 24px;
  margin-bottom: 12px;
}

.click-hint {
  position: absolute; bottom: 30px; opacity: 0; transform: translateY(10px);
  transition: all 0.5s ease; font-size: 13px; font-weight: bold; color: rgba(255,255,255,0.9);
}
.click-hint.visible { opacity: 1; transform: translateY(0); }
.shimmer-text {
  background: linear-gradient(90deg, #fff 0%, #cbd5e1 50%, #fff 100%);
  background-size: 200% auto; color: transparent; -webkit-background-clip: text; background-clip: text;
  animation: shine 3s linear infinite; text-shadow: none;
}
@keyframes shine { to { background-position: 200% center; } }

.carousel-controls {
  position: absolute; bottom: 8%; left: 50%; transform: translateX(-50%);
  display: flex; gap: 60px; z-index: 10;
}
.nav-arrow {
  background: transparent; border: none;
  color: white; font-size: 40px; display: flex; align-items: center; justify-content: center;
  cursor: pointer; opacity: 0.6; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
}
.nav-arrow:hover:not(:disabled) {
  opacity: 1; transform: scale(1.2);
  filter: drop-shadow(0 0 10px rgba(255,255,255,0.6));
}
.nav-arrow:disabled { opacity: 0.1; cursor: not-allowed; }

.custom-inputs-center {
  position: absolute; bottom: 20%; display: flex; flex-direction: column; gap: 14px;
  width: 100%; max-width: 340px; z-index: 10;
}
:deep(.custom-name-input .el-input__inner) { text-align: center; font-weight: bold; font-size: 16px; }

.fade-hall-enter-active, .fade-hall-leave-active { transition: opacity 0.6s ease, transform 0.6s ease; }
.fade-hall-enter-from { opacity: 0; transform: scale(1.05); }
.fade-hall-leave-to { opacity: 0; transform: scale(0.95); }

@media (max-width: 768px) {
  .carousel-3d { width: 260px; height: 420px; }
  .card-avatar { width: 80px; height: 80px; margin-bottom: 16px; }
  .card-name { font-size: 28px; margin-bottom: 12px; }
  .card-desc { font-size: 13px; -webkit-line-clamp: 3; padding: 0 16px; }
  .carousel-controls { bottom: 5%; gap: 40px; }
  .nav-arrow { font-size: 32px; }
  .top-exit-btn { top: 20px; left: 20px; width: 40px; height: 40px; font-size: 20px; }
}
</style>
<template>
  <SecretLayout
    bg-image="https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=2000&q=80"
    title="⚔️ 游戏冒险的彼岸"
    title-color="#fbbf24"
    code="180818"
    @back="$emit('back')"
  >
    <div class="content-box">
      <p>这里是游戏的专属展示页面。</p>
      <p>（后续内容待设计：留给这款让你印象深刻的游戏...）</p>
    </div>
  </SecretLayout>
</template>

<script setup>
import SecretLayout from '../../components/SecretLayout.vue'

defineEmits(['back'])
</script>

<style scoped>
.content-box {
  background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 40px; border-radius: 16px; margin-bottom: 30px; width: 100%;
  flex: 1; overflow-y: auto;
  display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
  font-size: 16px; line-height: 1.8;
}
.content-box::-webkit-scrollbar { width: 8px; }
.content-box::-webkit-scrollbar-track { background: transparent; }
.content-box::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 4px; }
.content-box::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }

@media (max-width: 768px) {
  .content-box { padding: 18px; font-size: 14px; margin-bottom: 20px; border-radius: 12px; line-height: 1.8; }
}
</style>
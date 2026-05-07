<template>
  <SecretLayout
    bg-image="https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=2000&q=80"
    title="⏳ 时空与灵魂的交界处"
    title-color="#34d399"
    code="251027"
    @back="$emit('back')"
  >
    <div class="content-box">
      <p>这里是《我在七年后等着你》与《灵魂摆渡者》的专属回忆页面。</p>
      <p>（后续内容待设计：可以放游戏截图、音频、或者你对这两款游戏的感悟...）</p>
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
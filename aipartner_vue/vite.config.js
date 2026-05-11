import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
   // vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            // 只将 vue 核心库分离出来
            if (id.includes('vue/dist/vue.runtime') || id.includes('vue/dist/vue.cjs')) {
              return 'vue-vendor'
            }
            // vue-router 单独分离
            if (id.includes('vue-router')) {
              return 'vue-router-vendor'
            }
            // element-plus 单独分离
            if (id.includes('element-plus')) {
              return 'element-plus'
            }
            // element-plus icons 单独分离
            if (id.includes('@element-plus/icons-vue')) {
              return 'element-icons'
            }
          }
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
})

<template>
  <div id="app">
    <router-view />
    <Toast />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import Toast from '@/components/ui/Toast.vue'

const authStore = useAuthStore()
const themeStore = useThemeStore()

onMounted(() => {
  themeStore.initializeTheme()
  authStore.checkAuth()
})
</script>

<style lang="scss">
@import '@/assets/styles/globals.scss';

#app {
  min-height: 100vh;
  font-family: var(--font-family);
  color: var(--text-primary);
  background: var(--bg-primary);
}
</style>
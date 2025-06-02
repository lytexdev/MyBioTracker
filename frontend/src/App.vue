<template>
  <div id="app">
    <router-view />
    <Toast />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import Toast from '@/components/ui/Toast.vue'

const userStore = useUserStore()

onMounted(() => {
  userStore.initializeAuth()
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
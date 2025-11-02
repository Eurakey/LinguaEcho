<template>
  <n-message-provider>
    <AppHeader />
    <router-view />
  </n-message-provider>
</template>

<script setup>
import { NMessageProvider } from 'naive-ui'
import { onMounted } from 'vue'
import AppHeader from './components/AppHeader.vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

// Initialize auth state on app mount
onMounted(async () => {
  await authStore.initialize()
})
</script>

<style>
/* Global styles are in style.css */
</style>

<template>
  <n-message-provider>
    <router-view />
  </n-message-provider>
</template>

<script setup>
import { NMessageProvider } from 'naive-ui'
// Main app component - uses router-view to render pages
// Wrapped with NMessageProvider to enable useMessage() composable
</script>

<style>
/* Global styles are in style.css */
</style>

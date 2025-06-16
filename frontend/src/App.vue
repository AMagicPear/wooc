<script setup lang="ts">
import WoocHeader from "./components/WoocHeader.vue";
import Toast from 'primevue/toast'
</script>

<template>
  <WoocHeader />
  <main class="main-content">
    <RouterView />
  </main>
  <Toast />
</template>

<style scoped>
.main-content {
  padding-inline: 10px;
  padding-top: 60px;
  min-height: 100vh;
  height: 100vh;
  overflow: scroll;
  background-color: var(--color-background-mute);
}
</style>

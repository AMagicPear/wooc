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
  padding-inline: 20px;
  padding-top: 60px;
  padding-bottom: 20px;
}
</style>

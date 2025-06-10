<script setup lang="ts">
import WoocHeader from './components/WoocHeader.vue';
</script>

<template>
  <WoocHeader />
  <main class="main-content">
    <RouterView/>
  </main>
</template>

<style scoped>
.main-content {
  padding-top: 60px;
  min-height: 100vh;
  height: 100vh;
  background-color: var(--color-background-mute);
}

</style>

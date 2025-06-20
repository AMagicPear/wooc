<script setup lang="ts">
import getBackgroundColor from "@/util/usernameBgColor";
import Avatar from "primevue/avatar";
defineProps<{ author_name: string }>();
</script>

<template>
  <div class="user-identify">
    <Avatar
      :label="author_name.charAt(0).toUpperCase()"
      :style="{ backgroundColor: getBackgroundColor(author_name) }"
    />
    <span>{{ author_name }}</span>
  </div>
</template>

<style lang="css" scoped>
.user-identify {
  display: flex;
  align-items: center;
  padding-left: 0.5rem;
  gap: 0.5rem;
}
</style>
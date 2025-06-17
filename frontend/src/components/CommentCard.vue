<script setup lang="ts">
import Card from "primevue/card";
import Avatar from "primevue/avatar";
import Fieldset from "primevue/fieldset";

import { computed } from "vue";
const props = defineProps<{
  title: string;
  username: string;
  content: string;
}>();

const backgroundColor = computed(() => {
  let hash = 0;
  for (let i = 0; i < props.username.length; i++) {
    hash = props.username.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash % 360);
  return `hsl(${hue}, 70%, 80%)`;
});
</script>

<template>
  <Card>
    <template #title>{{ title }}</template>
    <template #content>
      <Fieldset v-for="_ in 3">
        <template #legend>
          <div class="user-identify">
            <Avatar
              :label="username.charAt(0).toUpperCase()"
              :style="{ backgroundColor }"
            />
            <span>{{ username }}</span>
          </div>
        </template>
        <p>{{ content }}</p>
      </Fieldset>
    </template>
  </Card>
</template>

<style lang="css" scoped>
.user-identify {
  display: flex;
  align-items: center;
  padding-left: 0.5rem;
  gap: 0.5rem;
  margin-bottom: 0.6rem;
}

.lengend-text {
  font-weight: bold;
  padding: 0.5rem;
}

.fieldset-content {
  margin: 0;
}
</style>

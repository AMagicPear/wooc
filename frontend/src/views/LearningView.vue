<script setup lang="ts">
import Menubar from "primevue/menubar";
import { useRoute } from "vue-router";

const route = useRoute();
const id = route.params.id as string;
const items = [
  {
    label: "公告",
    icon: "pi pi-home",
    route: "notice",
  },
  {
    label: "课件",
    icon: "pi pi-star",
    route: "courseware"
  },
  {
    label: "讨论区",
    icon: "pi pi-star",
    route: "discussion"
  }
];
</script>

<template>
  <div id="learning-container">
    <Menubar :model="items">
      <template #item="{ item, props }">
        <RouterLink v-slot="{ href, navigate }" :to="item.route" custom>
          <a :href="href" v-bind="props.action" @click="navigate">
            <span :class="item.icon" />
            <span>{{ item.label }}</span>
          </a>
        </RouterLink>
      </template>
    </Menubar>
    <RouterView/>
    <!-- <main>youce</main> -->
  </div>
</template>

<style lang="css" scoped>
#learning-container {
  padding-top: 20px;
}
</style>

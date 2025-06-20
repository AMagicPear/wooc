<script setup lang="ts">
import { useRoute } from "vue-router";

import Tabs from "primevue/tabs";
import TabList from "primevue/tablist";
import Tab from "primevue/tab";
import IconBooksStack from "@/components/icons/IconBooksStack.vue";
import IconMedia from "@/components/icons/IconMedia.vue";
import IconHat from "@/components/icons/IconHat.vue";
import IconGroup from "@/components/icons/IconGroup.vue";
import { accountState } from "@/global/account";
import IconShedule from "@/components/icons/IconShedule.vue";

const route = useRoute();
const courseId = Number(route.params.courseid);
const method = route.params.method;

const items = [
  {
    label: "公告",
    c_icon: IconHat,
    route: "notice",
  },
  {
    label: "课件",
    c_icon: IconMedia,
    route: "courseware",
  },
  {
    label: "测验",
    icon: "pi pi-pencil",
    route: "exam",
  },
  {
    label: "作业",
    c_icon: IconBooksStack,
    route: "assignments",
  },
  {
    label: "讨论区",
    c_icon: IconGroup,
    route: "discussion",
  },
];

if (method == 'manage') {
  items.push({
    label: "选课学生情况",
    c_icon: IconShedule,
    route: "student-info",
  });
}
</script>

<template>
  <div id="learning-container">
    <Tabs value="notice" class="tabs">
      <TabList>
        <Tab
          v-for="tab in items"
          :key="tab.label"
          :value="tab.route"
          @click="$router.push(`/lesson/${courseId}/${method}/${tab.route}`)"
        >
          <a class="tab-link">
            <i v-if="tab.icon" :class="tab.icon" />
            <component
              v-else-if="tab.c_icon"
              :is="tab.c_icon"
              style="max-width: 20px; max-height: 20px"
            />
            <span>{{ tab.label }}</span>
          </a>
        </Tab>
      </TabList>
    </Tabs>

    <RouterView />
  </div>
</template>

<style lang="css" scoped>
#learning-container {
  padding-top: 20px;
}
.tabs {
  border-radius: 10px;
  overflow: hidden;
}

.tab-link {
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: inherit;
}

.tab {
  background-color: aqua;
}
</style>

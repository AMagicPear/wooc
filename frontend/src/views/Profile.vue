<script setup lang="ts">
import { accountState, getEnrolled } from "@/global/account";
import { Card } from "primevue";
import { onMounted, ref } from "vue";
import Tag from "primevue/tag";
import type { Course } from "@/api/lessonApi";
import LessonCard from "@/components/LessonCard.vue";
import Divider from "primevue/divider";
import { getFile } from "@/api/baseUrl";
const myCourses = ref<Course[]>();

onMounted(async () => {
  myCourses.value = await getEnrolled();
  myCourses.value.forEach(course => course.cover_image = getFile(course.cover_image))
});
</script>

<template>
  <div style="padding-top: 20px">
    <Card>
      <template #content>
        <p class="username">{{ accountState.username }}</p>
        <div style="display: flex; gap: 16px">
          <Tag icon="pi pi-id-card" :value="`ID: ${accountState.userid}`"></Tag>
          <Tag icon="pi pi-user" :value="`身份: ${accountState.role}`"></Tag>
        </div>
      </template>
    </Card>
    <Divider type="solid"><span>我的已选课程</span></Divider>
    <LessonCard
      v-for="course in myCourses"
      v-bind="course"
    />
  </div>
</template>

<style lang="css" scoped>
.username {
  font-size: 64px;
  font-weight: bold;
}
</style>

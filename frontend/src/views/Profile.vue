<script setup lang="ts">
import { accountState, getEnrolled, getManaged } from "@/global/account";
import { Card } from "primevue";
import { onMounted, ref } from "vue";
import Tag from "primevue/tag";
import type { Course } from "@/api/lessonApi";
import LessonCard from "@/components/LessonCard.vue";
import Divider from "primevue/divider";
import { getFile } from "@/api/baseUrl";
const myCourses = ref<Course[]>();
const myManagedCourses = ref<Course[]>();

onMounted(async () => {
  myCourses.value = await getEnrolled();
  myCourses.value.forEach(
    (course) => (course.cover_image = getFile(course.cover_image))
  );
  myManagedCourses.value = await getManaged();
  myManagedCourses.value.forEach(
    (course) => (course.cover_image = getFile(course.cover_image))
  );
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
    <div v-if="accountState.role === 'teacher'">
      <Divider type="solid" itemid="my-courses">
        <div class="divider-content">
          <img src="@/assets/icon/学习档案.svg" width="20px" alt="管理的课程" />
          <p>我管理的课程</p>
        </div>
      </Divider>
      <div class="lesson-grid">
        <LessonCard v-for="course in myManagedCourses" v-bind="course" />
      </div>
    </div>
    <div>
      <Divider type="solid" itemid="my-courses">
        <div class="divider-content">
          <img src="@/assets/icon/学习档案.svg" width="20px" alt="已选课程" />
          <p>我的已选课程</p>
        </div>
      </Divider>
      <div class="lesson-grid">
        <LessonCard v-for="course in myCourses" v-bind="course" />
      </div>
    </div>
  </div>
</template>

<style lang="css" scoped>
.lesson-grid {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}
.divider-content {
  display: flex;
  align-items: center;
  gap: 8px;
}
.username {
  font-size: 64px;
  font-weight: bold;
}
</style>

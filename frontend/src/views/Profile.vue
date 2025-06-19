<script setup lang="ts">
import { accountState, getEnrolled } from "@/global/account";
import router from "@/router";
import { Card, useToast } from "primevue";
import { onBeforeMount, onMounted, ref } from "vue";
import Tag from "primevue/tag";
import type { Course } from "@/api/lessonApi";
import LessonCard from "@/components/LessonCard.vue";
import Divider from "primevue/divider";
const toast = useToast();
const myCourses = ref<Course[]>();

onBeforeMount(() => {
  if (accountState.isLoggedIn == false) {
    toast.add({
      summary: "无法查看个人信息",
      detail: "尚未登录，请首先登录",
      severity: "error",
    });
    router.push({ name: "login" });
  }
});

onMounted(async () => {
  myCourses.value = await getEnrolled();
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
      :id="course.id"
      :title="course.title"
      :teacher="course.teacher_name"
      :imgsrc="course.cover_image"
    />
  </div>
</template>

<style lang="css" scoped>
.username {
  font-size: 64px;
  font-weight: bold;
}
</style>

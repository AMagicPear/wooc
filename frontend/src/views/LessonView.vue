<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import ExampleImg from "@/assets/pic/685110093414064026.webp";
import Button from "primevue/button";
import JoinCourse from "@/components/icons/JoinCourse.vue";
import { Rating } from "primevue";
import Card from "primevue/card";
import { onMounted, ref } from "vue";
import { accountState } from "@/global/account";
import baseApiUrl, { getFile } from "@/api/baseUrl";
import type { Course } from "@/api/lessonApi";
const router = useRouter();

const lessonId = useRoute().params.id as string;

const rating = ref(4);
const courseInfo = ref<Course>()
function startLearning() {
  router.push(`/lesson/${lessonId}/learn`);
  // TODO)) 向数据库添加学习课程信息
  console.log(accountState.userid, "开始学习", lessonId);
}

onMounted(async () => {
  let res = await fetch(new URL(`/courses/${lessonId}`, baseApiUrl));
  let data: { result: boolean; course: Course } = await res.json();
  if (data.result) {
    courseInfo.value = data.course
    courseInfo.value.cover_image = getFile(data.course.cover_image)
  } else {
    console.error(`加载课程${lessonId}信息失败`);
  }
});
</script>

<template lang="pug">
.lesson-container
  .lesson-header
    img(:src="courseInfo?.cover_image")
    .lesson-title
      h3 {{ courseInfo?.title }}
      p.teacher {{ courseInfo?.teacher_name }}
      Rating(v-model="rating" readonly)
      Button(@click="startLearning" rounded)
        JoinCourse(style="width: 20px;height: 20px;")
        | 开始学习
  Card
    template(#title) 课程概述
    template(#content) {{ courseInfo?.description }}


</template>

<style lang="css" scoped>
.lesson-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.lesson-header{
  border-radius: var(--card-border-radius);
  background-color: var(--color-background);
  padding: 20px;
}

.lesson-header {
  display: flex;
  gap: 24px;
}

.lesson-header > img {
  width: 60%;
  max-width: 450px;
  border-radius: var(--card-border-radius);
  object-fit: cover;
}
.lesson-title {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.lesson-title > h3 {
  font-size: 24px;
  font-weight: bolder;
}

.lesson-title.teacher {
  font-size: 13px;
}
.lesson-title > button {
  margin-top: 30px;
}
</style>

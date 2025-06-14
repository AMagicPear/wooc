<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import ExampleImg from "@/assets/pic/685110093414064026.webp"
import Button from 'primevue/button';
import JoinCourse from '@/components/icons/JoinCourse.vue';
import { Rating } from 'primevue';
import { ref } from 'vue';
const router = useRouter();

const lessonId = useRoute().params.id as string;

const rating = ref(4);
function startLearning() {
  console.log('开始学习');
  router.push(`/lesson/${lessonId}/learn`);
}
</script>

<template lang="pug">
.lesson-container
  .lesson-header
    img(:src="ExampleImg")
    .lesson-title
      h3 课程编号： {{ lessonId }}
      p.teacher 教师名称
      Rating(v-model="rating" readonly)
      Button(@click="startLearning" rounded)
        JoinCourse(style="width: 20px;height: 20px;")
        | 开始学习
        //- JoinCourse(style="width: 20px;height: 20px;")
        //- | 开始学习
  .lesson-content
    section
      .section-title
        h3 课程概述
      p.lesson-desc 课程描述正文部分


</template>

<style lang="css" scoped>
.lesson-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.lesson-header,
.lesson-content {
  border-radius: var(--card-border-radius);
  background-color: var(--color-background);
  padding: 20px;
}

.lesson-header {
  display: flex;
  gap: 24px;
}

.lesson-header>img {
  width: 60%;
  max-width: 450px;
  border-radius: var(--card-border-radius);
  object-fit: cover;
}
.lesson-title{
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.lesson-title>h3 {
  font-size: 24px;
  font-weight: bolder;
}

.lesson-title.teacher {
  font-size: 13px;
}
.lesson-title>button{
  margin-top: 30px;
}
</style>
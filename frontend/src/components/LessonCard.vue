<script setup lang="ts">
import type { Course } from "@/api/lessonApi";
import DefaultImg from "@/assets/pic/685110093414064026.webp";
import { useRouter } from "vue-router";
const router = useRouter();

const props = withDefaults(defineProps<Course>(), {
  cover_image: DefaultImg,
  title: "课程标题不见啦",
  teacher_name: "课程教师失踪啦",
});

function onCardClick() {
  console.log("点击了课程卡片", props.id);
  router.push(`/lesson/${props.id}`);
}
</script>

<template lang="pug">
    .lesson-card(@click="onCardClick")
        img(:src="cover_image" alt="课程图片")
        .lesson-card-info
            p.title {{ title }}
            p.teacher {{ teacher_name }}
</template>

<style scoped>
.lesson-card-info {
  margin-left: 0.8rem;
}

.lesson-card-info > .title {
  font-size: 14px;
  font-weight: bolder;
}

.lesson-card-info > .teacher {
  font-size: 12px;
  color: gray;
}

.lesson-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  padding-bottom: 10px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.lesson-card:hover {
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
  transform: scale(1.02);
}

.lesson-card img {
  width: 100%;
  height: 130px;
  object-fit: cover;
}
</style>

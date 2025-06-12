<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import ExampleImg from "@/assets/pic/685110093414064026.webp"
import WoocButton from '@/components/WoocButton.vue';
const router = useRouter();

const lessonId = useRoute().params.id as string;
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
      WoocButton(@click="startLearning") 开始学习
  .lesson-content
    section
      .section-title
        h3 课程概述
      p.lesson-desc 课程描述正文部分


</template>

<style lang="css" scoped>
.lesson-container{
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.lesson-header,
.lesson-content{
    border-radius: var(--card-border-radius);
    background-color: var(--color-background);
    padding: 20px;
}

.lesson-header{
  display: flex;
  gap: 24px;
}

.lesson-header>img{
    width: 60%;
    max-width: 600px;
    /* margin: 20px; */
    border-radius: var(--card-border-radius);
    object-fit: cover;
}

.lesson-title>h3{
    margin-block: 20px;
    font-size: 24px;
    font-weight: bolder;
}

.lesson-title.teacher{
    font-size: 13px;
}

.lesson-title>button{
    margin-block: 60px;
    padding-inline: 40px;
    padding-block: 8px;
    border-radius: var(--card-border-radius);
    border-style: none;
    background-color: var(--color-tint);
    color: white;
    font-size: 16px;
    font-weight: bolder;
    cursor: pointer;
}

.lesson-title>button:hover{
  opacity: 0.8;
}

.lesson-title>button:active{
  opacity: 0.6;
}
</style>
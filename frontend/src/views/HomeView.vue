<script setup lang="ts">
import LessonCard from '@/components/LessonCard.vue';
import DefaultImg from "@/assets/pic/685110093414064026.webp"
import baseApiUrl from '@/api/baseUrl';
import { onMounted, ref } from 'vue';
import type { Course } from '@/api/lessonApi';

let courses = ref<Course[]>()

onMounted(async () => {
    let response = await fetch(new URL('/courses', baseApiUrl))
    let data: { course: Course[] } = await response.json()
    courses.value = data.course
    console.log(data.course)
})
</script>

<template lang="pug">
    h2 →🧱精品课
    .lesson-grid
      LessonCard(v-for="course in courses" :id="course.id" :title="course.title" :imgsrc="DefaultImg" :teacher="course.teacher_name")
</template>

<style lang="css" scoped>
.lesson-grid {
    margin-top: 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}
</style>
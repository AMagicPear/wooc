<script setup lang="ts">
import LessonCard from '@/components/LessonCard.vue';
import baseApiUrl, { getFile } from '@/api/baseUrl';
import { onMounted, ref } from 'vue';
import type { Course } from '@/api/lessonApi';

let courses = ref<Course[]>()

onMounted(async () => {
    let response = await fetch(new URL('/courses', baseApiUrl))
    let data: { course: Course[] } = await response.json()
    courses.value = data.course
    courses.value.forEach(course => course.cover_image = getFile(course.cover_image))
    console.log(courses.value)
})
</script>

<template lang="pug">
    .home
        h2.text-xl →🧱精品课
        .lesson-grid
            LessonCard(v-for="course in courses" v-bind="course")
</template>

<style lang="css" scoped>
.home{
    margin-block: 10px;
}

.lesson-grid {
    margin-top: 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}
</style>
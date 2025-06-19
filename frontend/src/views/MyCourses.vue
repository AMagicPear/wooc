<script setup lang="ts">
import baseApiUrl from "@/api/baseUrl";
import type { Course } from "@/api/lessonApi";
import LessonCard from "@/components/LessonCard.vue";
import { accountState } from "@/global/account";
import { onMounted, ref } from "vue";

const myCourses = ref<Course[]>();

onMounted(async () => {
  const promises = accountState.enrolled.map(async (courseId) => {
    try {
      const response = await fetch(`${baseApiUrl}/courses/${courseId}`);
      const coursesResult = await response.json();
      
      if (coursesResult.result) return coursesResult.course;
      else console.error(coursesResult.message);
    } catch (error) {
      console.error(`Failed to fetch course ${courseId}:`, error);
    }
    return null;
  });
  const results = await Promise.all(promises);
  myCourses.value = results.filter(course => course !== null) as Course[];
});
</script>

<template>
  <LessonCard
    v-for="course in myCourses"
    v-bind="course"
  />
</template>

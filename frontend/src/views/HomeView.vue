<script setup lang="ts">
import LessonCard from '@/components/LessonCard.vue';
import DefaultImg from "@/assets/pic/685110093414064026.webp"
</script>

<template lang="pug">
    h2 邮🧱精品课
    .lesson-grid
      LessonCard(v-for="_ in 10" :id="0" :title="'标题'" :imgsrc="DefaultImg" :teacher="'作者'")
</template>

<style lang="css" scoped>
.lesson-grid {
    margin-top: 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}
</style>
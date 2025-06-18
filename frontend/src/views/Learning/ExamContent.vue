<script setup lang="ts">
import baseApiUrl from "@/api/baseUrl";
import type { Question } from "@/api/lessonApi";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import Checkbox from "primevue/checkbox";

const route = useRoute();
console.log("route", route);
const examId = Number(route.params.examid);
const attemptId = Number(route.query.attempt_id);

const questions = ref<Question[]>();
const answers = ref<{ [questionId: number]: any }>({}); // 存储答案

const loadQuestions = async () => {

};

onMounted(async () => {
  let data = await (
    await fetch(new URL(`/tests/${examId}/questions`, baseApiUrl))
  ).json();
  console.log(data);
  if (data) {
    questions.value = data.questions;
  } else {
    console.error(data.result);
  }
});
</script>

<template>
  <div v-for="question in questions">
    <div v-if="question.question_type == 'multiple_choice'"></div>
  </div>
</template>

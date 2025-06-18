<script setup lang="ts">
import baseApiUrl from "@/api/baseUrl";
import type { Question } from "@/api/lessonApi";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import Checkbox from "primevue/checkbox";

const examId = Number(useRoute().params.examid);

const questions = ref<Question[]>();
const currentAnswer = ref<(string | number)[]>();

onMounted(async () => {
  let data = await (
    await fetch(new URL(`tests/${examId}/questions`, baseApiUrl))
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
    <div v-if="question.question_type == 'multiple_choice'">
      <div v-for="option in question.options">
        <div>
          <Checkbox :input-id="option" />
          <label>{{ option }}</label>
        </div>
      </div>
    </div>
  </div>
</template>

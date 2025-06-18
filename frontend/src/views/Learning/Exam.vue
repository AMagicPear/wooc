<script setup lang="ts">
import baseApiUrl from "@/api/baseUrl";
import type { Exam } from "@/api/lessonApi";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { Divider } from "primevue";
import Card from "primevue/card";

const exams = ref<Exam[]>();
let courseId = useRoute().params.courseid;

onMounted(async () => {
  let res = await fetch(new URL(`courses/${courseId}/tests`, baseApiUrl));
  let data = await res.json();
  if (data.result) {
    exams.value = data.tests as Exam[];
  } else {
    console.error(data.result);
  }
});

function enterExam(id: number) {
  console.log("enterexam", id);
}
</script>

<template>
  <div id="exam">
    <Card
      v-for="exam in exams"
      class="exam-card"
      @click="$router.push('exam/1')"
    >
      <template #title
        ><span class="title">{{ exam.title }}</span></template
      >
      <template #content>{{ exam.description }}</template>
      <template #footer
        ><span class="info"
          >测试时长：{{ exam.duration }} 问题数量：{{
            exam.question_count
          }}</span
        ></template
      >
      <Divider />
    </Card>
  </div>
</template>

<style lang="css" scoped>
#exam {
  padding-block: 20px;
}
.exam-card {
  transition: all 0.2s ease;
  cursor: pointer;
}
.title {
  font-weight: bold;
}
.exam-card:hover {
  transform: scale(1.02);
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}
.exam-card:active {
  transform: scale(1);
  background-color: rgb(244, 251, 248);
}
.info {
  color: gray;
}
</style>

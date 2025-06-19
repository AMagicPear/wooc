<script setup lang="ts">
import baseApiUrl from "@/api/baseUrl";
import type { Exam } from "@/api/lessonApi";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Divider, useToast } from "primevue";
import Card from "primevue/card";
import { accountState } from "@/global/account";

const exams = ref<Exam[]>();
let courseId = useRoute().params.courseid;
const router = useRouter();
const toast = useToast();

onMounted(async () => {
  let res = await fetch(new URL(`/courses/${courseId}/tests`, baseApiUrl));
  let data = await res.json();
  if (data.result) {
    exams.value = data.tests as Exam[];
  } else {
    console.error(data.result);
  }
});

async function enterExam(exam: Exam) {
  let startTestRes = await fetch(
    new URL(`/tests/${exam.id}/start_test`, baseApiUrl),
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        student_id: accountState.userid,
      }),
    }
  );
  let testStartInfo = await startTestRes.json();
  console.log(testStartInfo);
  if (testStartInfo.result) {
    router.push({
      name: "examcontent",
      params: { examid: exam.id },
      query: {
        attempt_id: testStartInfo.attempt_id,
        // title: exam.title,
      },
    });
  } else {
    toast.add({
      summary: "开始测试失败",
      severity: "error",
      life: 3000,
    });
  }
}
</script>

<template>
  <div id="exam">
    <Card v-for="exam in exams" class="exam-card" @click="enterExam(exam)">
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

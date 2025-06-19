<script setup lang="ts">
import baseApiUrl from "@/api/baseUrl";
import type { Exam, Question } from "@/api/lessonApi";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import Textarea from "primevue/textarea";
import Checkbox from "primevue/checkbox";
import ProgressBar from "primevue/progressbar";
import Card from "primevue/card";
import Divider from "primevue/divider";
import { Button, RadioButton, useToast } from "primevue";
import Editor from "primevue/editor";
import router from "@/router";
import { useTimer } from "vue-timer-hook";

const route = useRoute();
const toast = useToast();
console.log("route", route);
const examId = Number(route.params.examid);
const attemptId = Number(route.query.attempt_id);

const examInfo = ref<Exam>();
const questions = ref<Question[]>();
const answers = ref<{ [questionId: number]: number[] | string }>({}); // 存储答案

const progress = computed(() => {
  if (!questions.value) return 0;
  let count = Object.values(questions.value).filter((q): boolean => {
    let answer = answers.value[q.id];
    if (typeof answer == "string") {
      return answer.trim() !== "";
    } else if (Array.isArray(answer)) {
      return answer.length > 0;
    } else {
      return false;
    }
  }).length;
  return (count / questions.value.length) * 100;
});

// [ERROR] 暂无法获取信息
const loadExamInfo = async () => {
  try {
    const res = await fetch(`${baseApiUrl}/tests/${examId}`);
    const data = await res.json();
    if (data.result) {
      console.log(data.test);
      examInfo.value = data.test;
    } else {
      console.error(data.message);
    }
  } catch (e) {
    console.error(e);
  }
};

const loadQuestions = async () => {
  const res = await fetch(`${baseApiUrl}/tests/${examId}/questions`);
  const data = await res.json();
  if (data.result) {
    questions.value = data.questions as Question[];
    console.log("已获取题目数据", data.questions);
    // 初始化答案存储结构
    questions.value.forEach((q) => {
      answers.value[q.id] = q.question_type === "multiple_choice" ? [] : "";
    });
    console.log("已生成初始化答案", answers.value);
  } else {
    console.error(data.message);
  }
};

const time = new Date();
time.setSeconds(time.getSeconds() + 600); // 根据题目的时间来定
const timer = useTimer(time.getTime(), true);

onMounted(async () => {
  await loadExamInfo();
  await loadQuestions();
});

const submitExamSheet = () => {
  // 检验题目是否全部正常完成
  console.log("待提交信息", answers.value);
  if (progress.value < 100 || !questions.value || !answers.value) {
    toast.add({
      summary: "提交失败",
      detail: "尚未完成全部题目",
      severity: "warn",
      life: 3000,
    });
    return;
  }
  // 生成所有题目的提交POST
  let submits: Promise<any>[] = [];
  questions.value.forEach((q) =>
    submits.push(
      fetch(`${baseApiUrl}/tests/submit_test_answer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          attempt_id: attemptId,
          question_id: q.id,
          answer: answers.value[q.id],
        }),
      }).then((response) => {
        if (!response.ok) {
          throw new Error("HTTP error" + response.status);
        }
        return response.json();
      })
    )
  );
  // 提交答案并完成测试
  Promise.all(submits)
    .then((results) => {
      console.log("全部答案提交成功", results);
      fetch(`${baseApiUrl}/tests/complete_test`, {
        method: "POST",
        body: JSON.stringify({ attempt_id: attemptId }),
      }).then((res) => {
        res.json().then((j) => {
          toast.add({
            summary: j.message,
            severity: res.ok ? "success" : "error",
            life: 3000,
          });
          if (res.ok) router.back();
        });
      });
    })
    .catch((error) => console.error(error));
};
</script>

<template>
  <div style="margin-top: 10px">
    <ProgressBar :value="progress" />
    <Card style="margin-block: 20px">
      <!-- <template #title>{{ examInfo?.title }}</template>
      <template #subtitle>{{ examInfo?.description }}</template> -->
      <template #subtitle>
        <p>{{ examInfo?.description }}</p>
        <p style="text-align: center">
          剩余时间：{{ timer.minutes.value.toString().padStart(2, "0") }}:{{
            timer.seconds.value.toString().padStart(2, "0")
          }}
        </p>
      </template>
      <template #content>
        <div v-for="question in questions" :key="question.id" class="question">
          <Divider align="left" type="solid"
            ><span style="font-weight: bold"
              >{{ question.id }}. {{ question.question_text }}</span
            ></Divider
          >
          <div
            v-if="question.question_type == 'multiple_choice'"
            class="choice-group"
          >
            <div
              v-for="(option, index) in question.options"
              :key="index"
              class="choice"
            >
              <Checkbox v-model="answers[question.id]" :value="index" />
              <label>{{ option }}</label>
            </div>
          </div>
          <div v-else-if="question.question_type == 'short_answer'">
            <Textarea
              autoResize
              size="normal"
              rows="3"
              style="width: 100%"
              v-model="(answers[question.id] as string)"
            />
          </div>
          <div
            v-else-if="question.question_type == 'true_false'"
            class="choice-group"
          >
            <div class="choice">
              <RadioButton v-model="answers[question.id]" :value="[1]" />
              <label>正确</label>
            </div>
            <div class="choice">
              <RadioButton v-model="answers[question.id]" :value="[0]" />
              <label>错误</label>
            </div>
          </div>
          <div v-else-if="question.question_type == 'essay'">
            <Editor
              v-model="answers[question.id] as string"
              editorStyle="height: 100px"
            />
          </div>
        </div>
        <Button
          label="提交测验答案"
          style="float: right; margin-top: 10px"
          :onclick="submitExamSheet"
        />
      </template>
    </Card>
  </div>
</template>

<style lang="css" scoped>
.choice {
  display: flex;
  gap: 10px;
  align-items: center;
}

.choice-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 4px;
}
</style>

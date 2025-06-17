<script setup lang="ts">
import baseApiUrl from "@/api/baseUrl";
import type { Exam } from "@/api/lessonApi";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { Divider } from "primevue";
const exams = ref<Exam[]>();
let courseId = useRoute().params.id;

onMounted(async () => {
  let res = await fetch(new URL(`courses/${courseId}/tests`, baseApiUrl));
  let data = await res.json();
  if (data.result) {
    exams.value = data.tests as Exam[];
  } else {
    console.error(data.result);
  }
});
</script>

<template>
  <div id="exam">
    <div v-for="exam in exams">
        {{ exam }}
      <Divider />
    </div>
  </div>
</template>

<style lang="css" scoped>
#exam {
  padding-block: 20px;
}

.exam-data {
  display: flex;
  flex-direction: column;
}
</style>

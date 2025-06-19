<script setup lang="ts">
import { Card, useToast } from "primevue";
import type { Assignment } from "@/api/lessonApi";
import { ref, onMounted } from "vue";
const assignments = ref<Assignment[]>();
import baseApiUrl from "@/api/baseUrl";
import { useRoute } from "vue-router";
import Editor from "primevue/editor";
import Button from "primevue/button";
import { Form } from "@primevue/forms";
import FileUpload from "primevue/fileupload";

const toast = useToast();
let courseId = useRoute().params.courseid;

onMounted(async () => {
  let res = await fetch(
    new URL(`/courses/${courseId}/assignments`, baseApiUrl)
  );
  let data = await res.json();
  if (data.result) {
    assignments.value = data.assignments as Assignment[];
    console.log(assignments.value);
  } else {
    console.error(data.result);
  }
});

const onUpload = (event: any) => {
  console.log(event);
};

const submitAssignment = async (assignmentId: number) => {
  console.log("正在尝试提交作业", assignmentId);
};
</script>

<template>
  <div id="assignments">
    <Card v-for="assignment in assignments" :key="assignment.id">
      <template #title
        ><span class="title">{{ assignment.title }}</span>
      </template>
      <template #subtitle>
        {{ assignment.description }}
      </template>
      <template #content>
        <!-- 直接在这里写提交内容，可能有一个文本框和一个文件 -->
        <Form v-slot="$homework" @submit="submitAssignment(assignment.id)">
          <Editor name="text" editor-style="height: 120px" />
          <div style="margin-top: 10px; display: flex; justify-content: flex-end; gap: 20px;">
            <FileUpload
              mode="basic"
              choose-label="点击上传附件"
              name="assignment_file"
              url="此处需要更改为后端的API"
              @upload="onUpload($event)"
              :multiple="false"
              :auto="true"
            >
              <template #empty>
                <span>将文件拖放到此处或点击上传</span>
              </template>
            </FileUpload>
            <Button label="提交作业" type="submit" />
          </div>
        </Form>
      </template>
      <template #footer>
        <div class="info">
          <span>截止日期：{{ assignment.deadline }}</span>
          <span>总分：{{ assignment.max_score }}</span>
        </div>
      </template>
    </Card>
  </div>
</template>

<style lang="css" scoped>
#assignments {
  padding-block: 20px;
}
.info {
  color: gray;
  display: flex;
  justify-content: space-between;
}

.title {
  font-weight: bold;
}
</style>

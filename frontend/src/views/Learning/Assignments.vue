<script setup lang="ts">
import { Card, useToast } from "primevue";
import type { Assignment } from "@/api/lessonApi";
import { ref, onMounted, watch } from "vue";
import baseApiUrl from "@/api/baseUrl";
import { useRoute } from "vue-router";
import Editor from "primevue/editor";
import Button from "primevue/button";
import { Form, type FormSubmitEvent } from "@primevue/forms";
import FileUpload, { type FileUploadUploadEvent } from "primevue/fileupload";
import { accountState } from "@/global/account"; // 引入账号状态

const assignments = ref<Assignment[]>();
const toast = useToast();
let courseId = useRoute().params.courseid;
// 存储每个作业对应的文件路径，一级索引为作业ID，二级索引为本地的文件名称
const filePaths: Record<number, Record<string, string>> = {};

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

const onUpload = (event: FileUploadUploadEvent, assignmentId: number) => {
  try {
    if (event.xhr.status !== 200) throw new Error(event.xhr.response);
    const response = JSON.parse(event.xhr.response);
    console.log("文件上传响应：", response);
    if (response.result) {
      if (!filePaths[assignmentId]) {
        filePaths[assignmentId] = response.file_paths;
      } else {
        // 合并文件路径
        filePaths[assignmentId] = {
          ...filePaths[assignmentId],
          ...response.file_paths,
        };
      }
      console.log("文件路径已更新:", filePaths);
      toast.add({
        summary: "上传成功",
        detail: "文件上传成功",
        severity: "success",
        life: 3000,
      });
    } else {
      toast.add({
        summary: "上传失败",
        detail: response.message,
        severity: "error",
        life: 3000,
      });
    }
  } catch (error) {
    console.error(error);
    toast.add({
      summary: "上传失败",
      detail: "发生未知错误",
      severity: "error",
      life: 3000,
    });
  }
};

const onRemoveUploadedFile = (event: any, assignmentId: number) => {
  console.log("移除文件事件:", event, assignmentId);
  if (filePaths[assignmentId]) {
    delete filePaths[assignmentId][event.file.name];
  }
  console.log("文件路径已更新:", filePaths);
};

const submitAssignment = async (
  event: FormSubmitEvent,
  assignmentId: number
) => {
  console.log("正在尝试提交作业，初始信息：", assignmentId, event);
  let text = event.values.text as string;
  let file_paths: Record<string, string> = filePaths[assignmentId];
  if (!text && !file_paths) {
    toast.add({
      summary: "提交失败",
      detail: "请至少填写作业内容或上传文件",
      severity: "error",
      life: 3000,
    });
    return;
  }
  console.log("提交作业，作业内容：", text, "文件路径：", file_paths);
  let res = await fetch(`${baseApiUrl}/assignments/${assignmentId}/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
      file_paths,
      student_id: accountState.userid,
    }),
  });
  let data = await res.json();
  if (data.result) {
    toast.add({
      summary: "提交成功",
      detail: "作业提交成功",
      severity: "success",
      life: 3000,
    });
  } else {
    toast.add({
      summary: "提交失败",
      detail: data.message,
      severity: "error",
      life: 3000,
    });
  }
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
        <Form @submit="submitAssignment($event, assignment.id)">
          <Editor name="text" editor-style="height: 120px" />
          <div
            style="
              margin-top: 10px;
              display: flex;
              flex-direction: column;
              gap: 20px;
            "
          >
            <FileUpload
              mode="advanced"
              choose-label="添加附件"
              upload-label="上传"
              cancel-label="取消"
              name="upload_file"
              :url="`${baseApiUrl}/upload_file`"
              @upload="onUpload($event, assignment.id)"
              :multiple="true"
              @remove-uploaded-file="
                onRemoveUploadedFile($event, assignment.id)
              "
            >
              <template #empty>
                <span>点击添加或拖拽文件到此处上传</span>
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

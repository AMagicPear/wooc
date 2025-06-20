<script setup lang="ts">
import { Badge, Card, FloatLabel, InputText, useToast } from "primevue";
import type {
  Assignment,
  AssignmentSubmission,
  AssignmentSubmissionPost,
  Grade,
} from "@/api/lessonApi";
import { ref, onMounted, watch } from "vue";
import baseApiUrl from "@/api/baseUrl";
import { useRoute } from "vue-router";
import Editor from "primevue/editor";
import Button from "primevue/button";
import { Form, type FormSubmitEvent } from "@primevue/forms";
import FileUpload, { type FileUploadUploadEvent } from "primevue/fileupload";
import Dialog from "primevue/dialog";
import { accountState } from "@/global/account"; // 引入账号状态
import UserIdentity from "@/components/UserIdentity.vue";
import Fieldset from "primevue/fieldset";
import InputNumber from "primevue/inputnumber";

const assignments = ref<Assignment[]>();
const dialogVisible = ref<boolean>(false);
const toast = useToast();
let courseId = useRoute().params.courseid;
let method = useRoute().params.method;
// 存储每个作业对应的文件路径，一级索引为作业ID，二级索引为本地的文件名称
const filePaths: Record<number, Record<string, string>> = {};
// 存储每个作业的完成状态
const isComplete = ref<Record<number, boolean>>({});
const submitReadyContent = ref<AssignmentSubmissionPost>();
const submissions = ref<Record<number, AssignmentSubmission[]>>({});
const grades = ref<Record<number, Grade[]>>({});

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
  if (method == "manage") {
    assignments.value?.forEach((assignment) => {
      getSubmissionsByAssignment(assignment.id);
      getGradeOfAssignment(assignment.id);
    });
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

const submitAssignment = async () => {
  if (!submitReadyContent.value) {
    console.error("提交内容为空");
    return;
  }
  let res = await fetch(
    `${baseApiUrl}/assignments/${submitReadyContent.value.assignment_id}/submit`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: submitReadyContent.value.text,
        file_paths: submitReadyContent.value.file_paths,
        student_id: submitReadyContent.value.student_id,
      }),
    }
  );
  console.log("已提交：", submitReadyContent.value);
  console.log(submitReadyContent.value.file_paths.toString());
  let data = await res.json();
  if (data.result) {
    toast.add({
      summary: "提交成功",
      detail: "作业提交成功",
      severity: "success",
      life: 3000,
    });
    isComplete.value[submitReadyContent.value.assignment_id] = true;
  } else {
    toast.add({
      summary: "提交失败",
      detail: data.message,
      severity: "error",
      life: 3000,
    });
  }
  dialogVisible.value = false;
};

const openSubmitDialog = (event: FormSubmitEvent, assignmentId: number) => {
  console.log("正在尝试提交作业，初始信息：", assignmentId, event);
  let text = event.values.text as string;
  let filePathsC: Record<string, string> = filePaths[assignmentId];
  if (!text && !filePathsC) {
    toast.add({
      summary: "提交失败",
      detail: "请至少填写作业内容或上传文件",
      severity: "error",
      life: 3000,
    });
    return;
  }
  submitReadyContent.value = {
    assignment_id: assignmentId,
    text,
    file_paths: filePathsC,
    student_id: accountState.userid,
  };
  dialogVisible.value = true;
};

const getSubmissionsByAssignment = async (assignmentId: number) => {
  let res = await fetch(
    new URL(`/assignments/${assignmentId}/submit`, baseApiUrl)
  );
  let data = await res.json();
  let validSubmissions: AssignmentSubmission[] = [];
  if (data.result) {
    data.submissions.forEach((element: any) => {
      // element.file_path = JSON.parse(element.file_path);
      try {
        let trimmed = null;
        if (element.file_path != null) {
          trimmed = JSON.parse(element.file_path);
          if (typeof trimmed == "string") trimmed = JSON.parse(trimmed);
          // console.log(element.id, element.file_path, "反序列化后的", trimmed);
        }
        validSubmissions.push({
          ...element,
          file_path: trimmed,
        } as AssignmentSubmission);
      } catch {
        // console.error(element.id, "文件路径反序列化失败", element);
      }
    });
    console.log("有效文件的提交", validSubmissions);
    submissions.value[assignmentId] = validSubmissions;
    return validSubmissions;
  } else {
    console.error("获取作业提交失败", data.message);
    return [];
  }
};

const gradeAssignment = async (
  event: FormSubmitEvent,
  assignmentId: number
) => {
  let content = event.values.grade as string;
  let score = event.values.score as number;
  let res = await fetch(
    `${baseApiUrl}/assignments/submit/${assignmentId}/grade`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        score: score,
        feedback: content,
        grader_id: assignmentId,
      }),
    }
  );
  let data = await res.json();
  if (data.result) {
    toast.add({
      summary: "作业批改成功",
      severity: "success",
      life: 3000,
    });
  } else {
    toast.add({
      summary: "作业批改失败",
      severity: "error",
      life: 300,
      detail: data.message,
    });
  }
};

const getGradeOfAssignment = async (assignmentId: number) => {
  let res = await fetch(
    `${baseApiUrl}/assignments/submit/${assignmentId}/grade`
  );
  let data = await res.json();
  if (res.ok && data.result) {
    grades.value[assignmentId] = data.grades;
  } else {
    console.error(data.message);
  }
};
</script>

<template lang="pug">
  #assignments
    Card(v-for="assignment in assignments" :key="assignment.id")
      template(#title)
        span.title {{ assignment.title }}

      template(#subtitle) {{ assignment.description }}

      template(#content)
        .submit-content(v-if="method == 'learn'")
          Form(v-if="!isComplete[assignment.id]" @submit="openSubmitDialog($event, assignment.id)")
            Editor(name="text" editor-style="height: 120px")
            div(style="margin-top: 10px;display: flex;flex-direction: column;gap: 20px;")
              FileUpload(mode="advanced"
                choose-label="添加附件"
                upload-label="上传"
                cancel-label="取消"
                name="upload_file"
                :url="`${baseApiUrl}/upload_file`"
                @upload="onUpload($event, assignment.id)"
                :multiple="true"
                @remove-uploaded-file="onRemoveUploadedFile($event, assignment.id)")
            
                template(#empty)
                  span 点击添加或拖拽文件到此处上传

              Button(label="提交作业" type="submit")

          .complete-text(v-else)
            img(src="@/assets/icon/学习完成.svg" width="16px" alt="已完成")
            p 已完成
        
        .manage-content(v-if="method == 'manage' && submissions[assignment.id]")
          Fieldset(v-for="submission in submissions[assignment.id]")
            template(#legend)
              UserIdentity(:author_name="submission.username")
            .main-content
              div
                .submission-content
                  Badge(severity="secondary") 提交内容
                  div(v-html="submission.content")
                .submission-content(v-if="submission.file_path")
                  Badge(severity="secondary") 附件
                  div(v-for="(filePath,name) in submission.file_path")
                    Button
                      a(:href="`${baseApiUrl}/get_file/${filePath}`" :download="name" target="_blank") {{ name }}
              Button(severity="contrast" icon="pi pi-reply" rounded text)
            div()
              Form(:action="`${baseApiUrl}/`" @submit="gradeAssignment($event, assignment.id)")
                div(style="display: flex; gap: 1rem; margin-top: 1rem;")
                  FloatLabel(variant="on" style="flex-grow: 7;")
                    InputText(name="grade" autocomplete="off" fluid)
                    label(for="grade") 在此输入作业批注
                  FloatLabel(variant="on" style="flex-grow: 3;")
                    InputNumber(name="score" :min="0" :max="100" fluid showButtons)
                    label(for="score") 输入作业评分
                  Button(type="submit" label="发送" style="flex-grow: 1;")
            //- div(v-for="grade in grades[assignment.id]")
            //-   p {{ grade }}
            //- 这里后端有问题


      template(#footer)
        .info
          span 截止日期：{{ assignment.deadline }}
          span 总分：{{ assignment.max_score }}

  Dialog(v-model:visible="dialogVisible" header="确认提交作业吗？")
    template(#default)
      div
        div(v-if="submitReadyContent?.text")
          p 当前已填写正文内容：
          div(v-html="submitReadyContent?.text")

        div(v-if="submitReadyContent?.file_paths")
          p 已上传文件：
          ul: li(v-for="(path, name) in submitReadyContent.file_paths") {{ name }}

    template(#footer)
      Button(label="返回"
        text
        severity="secondary"
        @click="dialogVisible = false"
        autofocus)
      
      Button(label="提交"
        outlined
        severity="secondary"
        @click="submitAssignment()"
        autofocus)

</template>

<style lang="css" scoped>
.main-content {
  display: flex;
  justify-content: space-between;
}

.submission-content {
  display: flex;
  margin-top: 10px;
  gap: 10px;
}
.complete-text {
  display: flex;
  align-items: center;
  gap: 8px;
}
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

<script lang="ts" setup>
import Stepper from "primevue/stepper";
import StepList from "primevue/steplist";
import StepPanels from "primevue/steppanels";
import { Card, Button, FloatLabel, InputText, useToast } from "primevue";
import FileUpload, { type FileUploadUploadEvent } from "primevue/fileupload";
import Step from "primevue/step";
import StepPanel from "primevue/steppanel";
import { ref } from "vue";
import type { CoursePost } from "@/api/lessonApi";
import Editor from "primevue/editor";
import Textarea from "primevue/textarea";
import baseApiUrl from "@/api/baseUrl";
import { accountState } from "@/global/account";
import router from "@/router";

const toast = useToast();

const basicInfo = ref<CoursePost>({
  title: "",
  description: "",
  teacher_id: accountState.userid,
  cover_image: undefined,
});

const announcement = ref<string>("");

const submitOffer = async () => {
  if (!basicInfo.value.title || !basicInfo.value.cover_image) {
    toast.add({
      summary: "提交失败",
      detail: "请至少填写课程标题和封面图片",
      severity: "error",
      life: 3000,
    });
    return;
  }
  let res = await fetch(new URL("/courses", baseApiUrl), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ...basicInfo.value,
      announcement: announcement.value,
    }),
  });
  if (res.ok) {
    let data = await res.json();
    toast.add({
      summary: "提交成功",
      detail: `课程ID: ${data.course_id}`,
      severity: "success",
      life: 3000,
    });
    router.push('/');
  } else {
    toast.add({
      summary: "提交失败",
      detail: `服务器错误: ${res.status}`,
      severity: "error",
      life: 3000,
    });
  }
};

const onUpload = (event: FileUploadUploadEvent) => {
  console.log("uploaded cover img", event);
  try {
    if (event.xhr.status !== 200) throw new Error(event.xhr.response);
    const response = JSON.parse(event.xhr.response);
    if (response.result) {
      const files = Object.keys(response.file_paths);
      if (files.length < 1) {
        toast.add({
          summary: "上传失败",
          detail: "没有上传文件",
          severity: "error",
          life: 3000,
        });
      } else {
        basicInfo.value.cover_image = response.file_paths[files[0]];
        toast.add({
          summary: "上传成功",
          detail: "封面图片上传成功",
          severity: "success",
          life: 3000,
        });
      }
    } else {
      toast.add({
        summary: "上传失败",
        detail: response.message,
        severity: "error",
        life: 3000,
      });
    }
  } catch (error) {
    console.error("上传封面图片失败:", error);
    toast.add({
      summary: "上传失败",
      detail: "发生未知错误",
      severity: "error",
      life: 3000,
    });
  }
};
</script>

<template>
  <Card class="offer">
    <template #content>
      <Stepper value="1">
        <StepList>
          <Step value="1">填写基本信息</Step>
          <Step value="2">设置公告</Step>
          <Step value="3">添加课程资源</Step>
        </StepList>
        <StepPanels>
          <StepPanel v-slot="{ activateCallback }" value="1">
            <div
              class="flex flex-col gap-4 justify-center items-center font-medium"
            >
              <FloatLabel variant="on">
                <InputText v-model="basicInfo.title" />
                <label>课程标题</label>
              </FloatLabel>
              <Textarea
                v-model="basicInfo.description"
                rows="5"
                cols="30"
                placeholder="输入课程描述"
              />
            </div>
            <div class="flex pt-6 justify-end">
              <Button
                label="继续"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('2')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="2">
            <div class="flex-auto flex justify-center items-center font-medium">
              <Editor
                v-model="announcement"
                editorStyle="height: 320px"
                placeholder="请输入课程公告"
              />
            </div>
            <div class="flex pt-6 justify-between">
              <Button
                label="返回"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('1')"
              />
              <Button
                label="继续"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('3')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="3">
            <div
              class="flex-auto flex gap-4 justify-center items-center font-medium"
            >
              <span class="text-xl">上传课程封面</span>
              <FileUpload
                choose-label="选择封面图片"
                mode="basic"
                name="cover_img"
                :url="`${baseApiUrl}/upload_file`"
                accept="image/*"
                :auto="true"
                @upload="onUpload($event)"
              />
            </div>
            <div v-if="basicInfo.cover_image" class="flex gap-3 justify-center items-center">
              <img src="@/assets/icon/学习完成.svg" width="16px" alt="已完成" />
              <p class="text-lg">已成功上传</p>
            </div>

            <div class="flex pt-6 justify-between">
              <Button
                label="返回"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('2')"
              />
              <Button
                label="提交"
                icon="pi pi-cloud-upload"
                iconPos="right"
                @click="submitOffer"
              />
            </div>
          </StepPanel>
        </StepPanels>
      </Stepper>
    </template>
  </Card>
</template>

<style lang="css" scoped>
.offer {
  margin-block: 10px;
}
</style>

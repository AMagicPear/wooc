<script lang="ts" setup>
import Stepper from "primevue/stepper";
import StepList from "primevue/steplist";
import StepPanels from "primevue/steppanels";
import { Card, Button, FloatLabel, InputText } from "primevue";
import StepItem from "primevue/stepitem";
import Step from "primevue/step";
import StepPanel from "primevue/steppanel";
import { ref } from "vue";
import type { CoursePost } from "@/api/lessonApi";
import Editor from "primevue/editor";
import Textarea from "primevue/textarea";
import baseApiUrl from "@/api/baseUrl";
import { accountState } from "@/global/account";

const basicInfo = ref<CoursePost>({
  title: "",
  description: "",
  teacher_id: "",
  cover_image: "",
});
const announcement = ref<string>("");
const submitOffer = async () => {
  console.log("submit offer", basicInfo.value, announcement.value);
  let res = await fetch(new URL("/courses", baseApiUrl), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ...basicInfo.value,
      announcement: announcement.value,
      teacher_id: accountState.userid
    }),
  });
  let data = await res.json();
  console.log(data)
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
            <div class="flex flex-col h-48">
              <div
                class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium"
              >
                Content III
              </div>
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

<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import Button from "primevue/button";
import JoinCourse from "@/components/icons/JoinCourse.vue";
import { Rating, useToast } from "primevue";
import Card from "primevue/card";
import { computed, onMounted, ref } from "vue";
import { accountState } from "@/global/account";
import baseApiUrl, { getFile } from "@/api/baseUrl";
import type { Course } from "@/api/lessonApi";
const router = useRouter();
const route = useRoute();
const toast = useToast();
const lessonId = Number(useRoute().params.courseid);

const rating = ref(4);
const courseInfo = ref<Course>();
async function startLearning() {
  if (!accountState.isLoggedIn) {
    router.push({
      path: "/login",
      query: { redirect: route.fullPath },
    });
  }

  if (!isEnrolled.value) {
    let enrollResult = await (
      await fetch(new URL("/enroll", baseApiUrl), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_id: accountState.userid,
          course_id: lessonId,
        }),
      })
    ).json();
    if (enrollResult.result) {
      toast.add({
        summary: "选课成功",
        detail: enrollResult.message,
        severity: "success",
        life: 3000,
      });
      accountState.enrolled.push(lessonId);
      console.log("添加选课ID: ", enrollResult.enrollment_id);
    } else {
      toast.add({
        summary: "选课失败",
        detail: enrollResult.message,
        severity: "error",
      });
    }
  }

  router.push(`/lesson/${lessonId}/learn`);
  console.log(accountState.userid, "开始学习", lessonId);
}

onMounted(async () => {
  let res = await fetch(new URL(`/courses/${lessonId}`, baseApiUrl));
  let data: { result: boolean; course: Course } = await res.json();
  if (data.result) {
    courseInfo.value = data.course;
    courseInfo.value.cover_image = getFile(data.course.cover_image);
  } else {
    console.error(`加载课程${lessonId}信息失败`);
  }
});

const isEnrolled = computed(() =>
  accountState.enrolled.some((courseId) => courseId == lessonId)
);

const isManaged = computed(() =>
  accountState.managed.some((courseId) => courseId == lessonId)
);

const buttonText = computed(() => {
  if(accountState.role == 'teacher' && isManaged.value) {
    return '管理课程'
  }else return (isEnrolled.value ? "继续学习" : "加入课程");
});

</script>

<template lang="pug">
.lesson-container
  .lesson-header
    img(:src="courseInfo?.cover_image")
    .lesson-title
      h3 {{ courseInfo?.title }}
      p.teacher {{ courseInfo?.teacher_name }}
      Rating(v-model="rating" readonly)
      Button(@click="startLearning" rounded)
        JoinCourse(style="width: 20px;height: 20px;")
        | {{ buttonText }}
  Card
    template(#title) 课程概述
    template(#content) {{ courseInfo?.description }}


</template>

<style lang="css" scoped>
.lesson-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.lesson-header {
  border-radius: var(--card-border-radius);
  background-color: var(--color-background);
  padding: 20px;
}

.lesson-header {
  display: flex;
  gap: 24px;
}

.lesson-header > img {
  width: 60%;
  max-width: 450px;
  border-radius: var(--card-border-radius);
  object-fit: cover;
}
.lesson-title {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.lesson-title > h3 {
  font-size: 24px;
  font-weight: bolder;
}

.lesson-title.teacher {
  font-size: 13px;
}
.lesson-title > button {
  margin-top: 30px;
}
</style>

<script setup lang="ts">
import baseApiUrl from "@/api/baseUrl";
import Card from "primevue/card";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
const courseId = Number(useRoute().params.courseid);
const notice = ref<string>();

const getNotice = async () => {
  let res = await fetch(`${baseApiUrl}/courses/${courseId}`);
  let data = await res.json();
  notice.value = data.notice ?? "默认公告";
}

onMounted(() => {
  getNotice()
});
</script>

<template lang="pug">
.notice
    Card()
        template(#title) 课程公告
        template(#content)
            div(v-html="notice")
</template>

<style lang="css" scoped>
.notice {
  margin-top: 20px;
}
</style>

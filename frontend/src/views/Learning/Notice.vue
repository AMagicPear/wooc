<script setup lang="ts">
import Card from "primevue/card";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
const courseId = Number(useRoute().params.courseid);
const notice = ref("");

onMounted(async () => {
  notice.value = "公告";
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

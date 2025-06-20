<script setup lang="ts">
import { ref, onMounted } from "vue";
import DataView from "primevue/dataview";
import { Card } from "primevue";
import type { Enrollment } from "@/api/enrollment";
import baseApiUrl from "@/api/baseUrl";
import { useRoute } from "vue-router";
import UserIdentity from "@/components/UserIdentity.vue";
import Badge from "primevue/badge";

const courseId = useRoute().params.courseid;
const enrollments = ref<Enrollment[]>([]);

onMounted(async () => {
  let res = await fetch(`${baseApiUrl}/courses/${courseId}/enrollments`);
  let data = await res.json();
  if (res.ok && data.result) {
    enrollments.value = data.enrollments;
  } else {
    console.error(data.message);
  }
});
</script>

<template>
  <Card style="margin-top: 20px">
    <template #content>
      <DataView :value="enrollments" paginator :rows="5">
        <template #list="slotProps">
          <div class="flex flex-col">
            <div
              v-for="(enrollment, index) in (slotProps.items as Enrollment[])"
              :key="index"
            >
              <div
                class="enrollment-title"
                :class="{
                  'border-t border-surface-200': index !== 0,
                }"
              >
                <UserIdentity :author_name="enrollment.username" />
                <Badge severity="secondary">ID: {{ enrollment.student_id }}</Badge>
              </div>
              <div class="enrollment-info">
                <p>邮箱 | {{ enrollment.email }}</p>
                <p>选课时间 | {{ enrollment.enrolled_at }}</p>
                <p>学习进度 | {{ enrollment.progress }}</p>
              </div>
            </div>
          </div>
        </template>
      </DataView>
    </template>
  </Card>
</template>

<style lang="css" scoped>
.enrollment-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
}

.enrollment-info {
  margin-inline: 20px;
  margin-bottom: 10px;
}
</style>

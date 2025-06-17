<script setup lang="ts">
import { useRoute } from "vue-router";
import { computed, onMounted, ref, watch } from "vue";
import VideoPlayer from "@/components/VideoPlayer.vue";
import Galleria from "primevue/galleria";
import Card from "primevue/card";
import Breadcrumb from "primevue/breadcrumb";
import { PhotoService } from "@/api/PhotoService";
import baseApiUrl, { getFile } from "@/api/baseUrl";
import Listbox from "primevue/listbox";
import type { Course, CourseResourceItem } from "@/api/lessonApi";

const lessonId = useRoute().params.id as string;

const images = ref();
const courseInfo = ref<Course>();
const resources = ref<CourseResourceItem[]>();

onMounted(async () => {
  let res = await fetch(new URL(`/courses/${lessonId}`, baseApiUrl));
  let data: { result: boolean; course: Course } = await res.json();
  if (data.result) {
    courseInfo.value = data.course;
  } else {
    console.error(`加载课程${lessonId}信息失败`);
  }
  res = await fetch(new URL(`courses/${lessonId}/resources`, baseApiUrl));
  resources.value = (await res.json()).resources as CourseResourceItem[];
  if (resources.value && resources.value.length > 0) {
    selectedChapter.value = resources.value[0];
  }
  console.log(resources.value);
});

const homeItems = computed(() => [
  { label: courseInfo.value?.title },
  { label: selectedChapter.value?.title },
]);

const selectedChapter = ref<CourseResourceItem>();

watch(
  selectedChapter,
  () => {
    if (selectedChapter.value?.resource_type == "image") {
      PhotoService.getImages().then((data) => (images.value = data));
    }
  },
  { immediate: true }
);
</script>

<template>
  <div id="courseware">
    <Listbox
      v-model="selectedChapter"
      :options="resources"
      optionLabel="title"
      listStyle="max-height:100%;"
      class="listbox"
    />
    <Card class="rightcard">
      <template #title>
        {{ selectedChapter?.description }}
      </template>
      <template #subtitle>
        <Breadcrumb :home="{ icon: 'pi pi-home' }" :model="homeItems">
          <template #item="{ item }">
            <span v-if="item.icon" :class="[item.icon, 'text-color']" />
            <span>{{ item.label }}</span>
          </template>
        </Breadcrumb>
      </template>
      <template #content>
        <VideoPlayer
          :src="getFile(selectedChapter?.file_path)"
          v-if="selectedChapter?.resource_type == 'video'"
        />
        <Galleria
          :value="images"
          v-else-if="selectedChapter?.resource_type == 'image'"
        >
          <template #item="slotProps">
            <img
              :src="slotProps.item.itemImageSrc"
              :alt="slotProps.item.alt"
              style="width: 100%"
            />
          </template>
          <template #thumbnail="slotProps">
            <img
              :src="slotProps.item.thumbnailImageSrc"
              :alt="slotProps.item.alt"
            />
          </template>
        </Galleria>
        <span v-else>课程资源不见啦</span>
      </template>
      <template #footer>
        {{ selectedChapter?.created_at }}
      </template>
    </Card>
  </div>
</template>

<style lang="css" scoped>
.listbox {
  border-radius: 10px;
  flex: 2;
}

.rightcard {
  flex: 9;
}

#courseware {
  margin-top: 20px;
  display: flex;
  gap: 20px;
}
</style>

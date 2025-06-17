<script setup lang="ts">
import { useRoute } from "vue-router";
import { computed, onMounted, ref, watch } from "vue";
import VideoPlayer from "@/components/VideoPlayer.vue";
import Galleria from "primevue/galleria";
import Card from "primevue/card";
import Breadcrumb from "primevue/breadcrumb";
import { PhotoService } from "@/api/PhotoService";
import baseApiUrl from "@/api/baseUrl";
import Listbox from "primevue/listbox";
import type { Course, CourseResource } from "@/api/lessonApi";

const lessonId = useRoute().params.id as string;

const images = ref();
const courseInfo = ref<Course>();
const resources = ref<CourseResource[]>();

onMounted(async () => {
  let res = await fetch(new URL(`/courses/${lessonId}`, baseApiUrl));
  let data: { result: boolean; course: Course } = await res.json();
  if (data.result) {
    courseInfo.value = data.course;
  } else {
    console.error(`加载课程${lessonId}信息失败`);
  }
  res = await fetch(new URL(`courses/${lessonId}/resources`, baseApiUrl));
  resources.value = (await res.json()).resources as CourseResource[];
  if (resources.value && resources.value.length > 0) {
    selectedChapter.value = resources.value[0];
  }
  console.log(resources.value);
});

const homeItems = computed(() => [
  { label: courseInfo.value?.title },
  { label: selectedChapter.value?.title },
]);

const selectedChapter = ref<CourseResource>();

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
      listStyle="max-height:100%; width: 160px"
      style="border-radius: 10px"
    />
    <Card>
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
          :src="`${baseApiUrl}get_file/${selectedChapter?.file_path}`"
          v-show="selectedChapter?.resource_type == 'video'"
        />
        <Galleria
          :value="images"
          v-show="selectedChapter?.resource_type == 'image'"
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
      </template>
    </Card>
  </div>
</template>

<style lang="css" scoped>
#courseware {
  margin-top: 20px;
  display: flex;
  gap: 20px;
}
</style>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { onMounted, ref } from "vue";
import VideoPlayer from "@/components/VideoPlayer.vue";
import Galleria from "primevue/galleria";
import Card from "primevue/card";
import Breadcrumb from "primevue/breadcrumb";
import DefaultImg from "@/assets/pic/685110093414064026.webp";
import { PhotoService } from "@/api/PhotoService";
import baseApiUrl from "@/api/baseUrl";
const videoSrc = ref<string>();

const lessonId = useRoute().params.id as string;
const mediaType = ref<"img" | "video">("img");

onMounted(() => {
  PhotoService.getImages().then((data) => (images.value = data));
  videoSrc.value = new URL(
    "get_file/media/video/test_video.mp4",
    baseApiUrl
  ).toString();
});

const images = ref();

onMounted(async () => {
  images.value?.push(DefaultImg);
  mediaType.value = 'video'
});

const homeItems = ref([
  {
    label: "第一章",
    command: () => {
      console.log(homeItems.value[0].label);
    },
  },
  {
    label: "1.1 学习",
    command: () => {
      console.log("学习");
    },
  },
]);
</script>

<template>
  <div id="courseware">
    <Card>
      <template #subtitle>
        <Breadcrumb :home="{ icon: 'pi pi-home' }" :model="homeItems">
          <template #item="{ item, props }">
            <a v-bind="props.action">
              <span :class="[item.icon, 'text-color']" />
              <span class="text-surface-700 dark:text-surface-0">{{
                item.label
              }}</span>
            </a>
          </template>
        </Breadcrumb>
      </template>

      <template #content>
        <VideoPlayer :src="videoSrc" v-show="mediaType == 'video'"/>
        <Galleria :value="images" v-show="mediaType == 'img'">
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
}
</style>

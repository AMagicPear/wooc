<script setup lang="ts">
import { useRoute } from "vue-router";
import Galleria from "primevue/galleria";
import { onMounted, ref } from "vue";
import DefaultImg from "@/assets/pic/685110093414064026.webp";
import VideoPlayer from "@/components/VideoPlayer.vue";
import DefaultVideo from '@/assets/易拉罐的复仇 720p常规码率.mp4'
const lessonId = useRoute().params.id as string;
// const images = ref<string[]>();

// onMounted(async () => {
//   images.value?.push(DefaultImg);
// });
// let options = {
//   autoplay: false,
//   controls: true,
//   sources: [
//     {
//       src: DefaultVideo,
//       type: "video/mp4",
//     },
//   ],
// }
</script>

<template>
  <div id="courseware">
    <!-- <VideoPlayer v-bind="options"/> -->
     <VideoPlayer/>
    <!-- <Galleria
      :value="images"
      :numVisible="5"
      :circular="true"
      containerStyle="max-width: 640px; height: 400px"
      :showItemNavigators="true"
    >
      <template #item="slotProps">
        <img alt="alt11" :src="slotProps.item" style="width: 100%; display: block" />
      </template>
      <template #thumbnail="slotProps">
        <img alt="alt22" :src="slotProps.item" style="display: block" />
      </template>
    </Galleria> -->
  </div>
</template>

<style lang="css" scoped>
</style>

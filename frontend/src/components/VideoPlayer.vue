<template>
  <div>
    <video ref="videoPlayer" class="video-js vjs-default-skin vjs-big-play-centered"></video>
  </div>
</template>

<script setup lang="ts">
import videojs from "video.js";
import type Player from "video.js/dist/types/player";
import { onBeforeUnmount, onMounted, ref } from "vue";
const props = defineProps<VideoOptions>();

interface VideoOptions {
  autoplay: boolean;
  controls: boolean;
  sources: {
    src: string;
    type: string;
  }[];
}

let player: Player;
const videoPlayer = ref();

onMounted(() => {
  player = videojs(videoPlayer.value, props, () => {
    player.log("onPlayerReady",props);
  });
});

onBeforeUnmount(() => {
  if (player) {
    player.dispose();
  }
});
</script>

<style lang="css" scoped>
.video-js{
  width: 100%;
  max-height: 60vh;
}
</style>
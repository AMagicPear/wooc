<script lang="ts" setup>
// Import styles.
import "vidstack/player/styles/default/theme.css";
import "vidstack/player/styles/default/layouts/audio.css";
import "vidstack/player/styles/default/layouts/video.css";
// Register elements.
import "vidstack/player";
import "vidstack/player/layouts";
import "vidstack/player/ui";

import type { MediaPlayerElement } from "vidstack/elements";
import { onMounted, ref } from "vue";

defineProps<{ src?: string }>();
// import { textTracks } from './tracks';

const player = ref<MediaPlayerElement>();
// const src = ref("");

// onMounted(() => {
//   src.value = TestVideo;
// });
</script>

<template>
  <media-player
    class="player"
    title="视频标题"
    :src
    crossOrigin
    playsInline
    ref="player"
  >
    <media-provider>
      <!-- <media-poster
        class="vds-poster"
        src="https://files.vidstack.io/sprite-fight/poster.webp"
        alt="Girl walks into campfire with gnomes surrounding her friend ready for their next meal!"
      /> -->
    </media-provider>
    <!-- Layouts -->
    <media-video-layout />
  </media-player>
</template>

<style scoped>
.player {
  --brand-color: #f5f5f5;
  --focus-color: #4e9cf6;

  --audio-brand: var(--brand-color);
  --audio-focus-ring-color: var(--focus-color);
  --audio-border-radius: 2px;

  --video-brand: var(--brand-color);
  --video-focus-ring-color: var(--focus-color);
  --video-border-radius: 2px;

  /* 👉 https://vidstack.io/docs/player/components/layouts/default#css-variables for more. */
}

.player[data-view-type="video"] {
  aspect-ratio: 16 /9;
}

.src-buttons {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  margin-top: 40px;
  margin-inline: auto;
  max-width: 300px;
}
</style>

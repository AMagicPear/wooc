<script setup lang="ts">
import { useRoute } from "vue-router";
import Galleria from "primevue/galleria";
import { onMounted, ref } from "vue";
import DefaultImg from '@/assets/pic/685110093414064026.webp'
const lessonId = useRoute().params.id as string;
const images = ref<string[]>();

onMounted(async () => {
    images.value?.push(DefaultImg)
});
</script>

<template>
  Courseware
  <!-- <Galleria :value="images" :show-item-navigators="true">
    <template #item="slotProps">
      <img :src="slotProps.item" style="width: 100%" />
    </template>
    <template #thumbnail="slotProps">
      <img :src="slotProps.item"/>
    </template>
  </Galleria> -->

<Galleria :value="images"  :numVisible="5" :circular="true" containerStyle="max-width: 640px"
    :showItemNavigators="true">
    <template #item="slotProps">
        <img :src="slotProps.item.itemImageSrc" :alt="slotProps.item.alt" style="width: 100%; display: block;" />
    </template>
    <template #thumbnail="slotProps">
        <img :src="slotProps.item.thumbnailImageSrc" :alt="slotProps.item.alt" style="display: block;" />
    </template>
</Galleria>
</template>

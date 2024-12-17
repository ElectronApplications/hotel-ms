<script setup lang="ts">
import type { Gallery } from "@/types";
import { ChevronLeftIcon, ChevronRightIcon } from "@heroicons/vue/24/outline";
import { ref, toRefs, type HTMLAttributes } from "vue";
import ExpandableImage from "./ExpandableImage.vue";

const props = defineProps<{
  gallery: Gallery;
  imgClass?: HTMLAttributes["class"];
}>();

const { gallery } = toRefs(props);

const currentImage = ref(0);

function switchImage(value: number) {
  let newImage = currentImage.value + value;

  if (newImage < 0) {
    newImage = gallery.value.images.length - 1;
  } else if (newImage >= gallery.value.images.length) {
    newImage = 0;
  }

  currentImage.value = newImage;
}
</script>

<template>
  <div v-if="gallery.images.length !== 0" class="relative">
    <ExpandableImage
      :src="gallery.images[currentImage].image"
      :imgClass="imgClass"
    />
    <button
      class="absolute left-2 top-1/2 -translate-y-1/2"
      @click="switchImage(-1)"
    >
      <ChevronLeftIcon class="w-[32px] text-white drop-shadow-lg" />
    </button>
    <button
      class="absolute right-2 top-1/2 -translate-y-1/2"
      @click="switchImage(+1)"
    >
      <ChevronRightIcon class="w-[32px] text-white drop-shadow-lg" />
    </button>
  </div>
</template>

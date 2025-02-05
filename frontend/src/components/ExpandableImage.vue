<script setup lang="ts">
import { ref, toRefs, type HTMLAttributes } from "vue";

const props = defineProps<{
  src: string;
  alt?: string;
  imgClass?: HTMLAttributes["class"];
}>();

const { src, alt, imgClass } = toRefs(props);

const expanded = ref(false);
</script>

<template>
  <div>
    <button @click="expanded = true">
      <img :src="src" :alt="alt" :class="imgClass" />
    </button>
    <div v-if="expanded"
      class="fixed inset-0 z-10 flex h-full w-full cursor-pointer items-center justify-center bg-black bg-opacity-50"
      @click="expanded = false">
      <img class="h-fit w-fit" :src="src" :alt="alt" />
    </div>
  </div>
</template>

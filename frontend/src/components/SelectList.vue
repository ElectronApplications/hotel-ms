<script setup lang="ts">
import { toRefs, watch } from "vue";

const props = defineProps<{
  options: readonly string[];
  defaultOption?: number;
}>();

const { options, defaultOption } = toRefs(props);

const model = defineModel<number>();

watch(
  defaultOption,
  (value) => {
    model.value = value;
  },
  {
    immediate: true,
  },
);
</script>

<template>
  <select
    class="rounded-md border-0 bg-surface-light p-2 py-2 shadow-sm ring-1 ring-secondary-light hover:cursor-pointer sm:text-sm/6 dark:bg-surface-dark dark:ring-secondary-active-dark"
    v-model="model"
  >
    <option
      v-for="[index, option] in options.entries()"
      v-bind:key="index"
      :value="index"
    >
      {{ option }}
    </option>
  </select>
</template>

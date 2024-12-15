<script setup lang="ts" generic="Blank extends boolean = false">
import { toRefs, watch } from "vue";

export type SelectModel<T extends boolean> = T extends false
  ? number
  : number | undefined;

const props = defineProps<{
  options: readonly string[];
  defaultOption?: number;
  blankOption?: Blank;
}>();

const { options, defaultOption, blankOption } = toRefs(props);

const model = defineModel<SelectModel<Blank>>();

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
    <option v-if="blankOption" :value="undefined" />
    <option
      v-for="[index, option] in options.entries()"
      v-bind:key="index"
      :value="index"
    >
      {{ option }}
    </option>
  </select>
</template>

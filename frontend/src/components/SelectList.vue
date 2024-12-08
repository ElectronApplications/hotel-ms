<script setup lang="ts">
import { nextTick, ref, toRefs, watch } from "vue";

const props = defineProps<{
  options: readonly string[];
  selected: number;
}>();

const { options, selected } = toRefs(props);

const emit = defineEmits<{
  updateSelection: [id: number];
}>();

const selectedOption = ref(0);

watch(
  selected,
  (value) => {
    selectedOption.value = value;
  },
  {
    immediate: true,
  },
);

function updateSelection() {
  emit("updateSelection", selectedOption.value);
  nextTick(() => {
    selectedOption.value = selected.value;
  });
}
</script>

<template>
  <select
    class="rounded-md border-0 bg-surface-light p-2 py-2 shadow-sm ring-1 ring-secondary-light hover:cursor-pointer sm:text-sm/6 dark:bg-surface-dark dark:ring-secondary-active-dark"
    @change.prevent="updateSelection"
    v-model="selectedOption"
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

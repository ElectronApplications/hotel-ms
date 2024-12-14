<script setup lang="ts">
import { nextTick, ref, toRefs, watch } from "vue";
import SelectList from "@/components/SelectList.vue";

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
    nextTick(() => {
      selectedOption.value = value;
    });
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
  <SelectList
    @change="updateSelection"
    v-model="selectedOption"
    :options="options"
  />
</template>

<script setup lang="ts" generic="Blank extends boolean = false">
import { nextTick, ref, toRefs, watch } from "vue";
import SelectList, { type SelectModel } from "@/components/SelectList.vue";

const props = defineProps<{
  options: readonly string[];
  selected: number;
  blankOption?: Blank;
}>();

const { options, selected, blankOption } = toRefs(props);

const emit = defineEmits<{
  updateSelection: [id: SelectModel<Blank>];
}>();

const selectedOption = ref<SelectModel<Blank>>(0);

watch(
  selected,
  (value) => {
    nextTick(() => {
      selectedOption.value = value;
    });
  },
  {
    immediate: true,
  }
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
    :blankOption="blankOption"
  />
</template>
